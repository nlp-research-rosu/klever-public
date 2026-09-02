import ast
import json
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
K_COMMIT = "ff15baac9e66426612ec45ff912af7f14965b64a"
K_IMAGE = (
    "runtimeverificationinc/kframework-k:ubuntu-jammy-7.1.293@"
    "sha256:f3f64ab72bd7b560082d50e4c6c23e107025cf217ca62ab73700104fc45de09a"
)
LEAN = "leanprover/lean4:v4.22.0"


def copied_tool_modules(dockerfile: Path) -> set[str]:
    source = dockerfile.read_text().replace("\\\n", " ")
    copied: set[str] = set()
    for line in source.splitlines():
        if not line.startswith("COPY "):
            continue
        tokens = shlex.split(line)
        for item in tokens[1:-1]:
            path = Path(item)
            if path.parent == Path("tools") and path.suffix == ".py":
                copied.add(path.stem)
    return copied


def direct_local_tool_imports(module: Path) -> set[str]:
    imported: set[str] = set()
    for node in ast.parse(module.read_text()).body:
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module == "tools":
            imported.update(alias.name for alias in node.names)
        elif node.module is not None and node.module.startswith("tools."):
            imported.add(node.module.split(".", 1)[1])
    return imported


def local_tool_import_closure(module: str) -> set[str]:
    pending = [module]
    visited: set[str] = set()
    while pending:
        current = pending.pop()
        if current in visited:
            continue
        visited.add(current)
        pending.extend(
            direct_local_tool_imports(
                REPO / "tools" / f"{current}.py"
            )
            - visited
        )
    visited.remove(module)
    return visited


class PipelineContainerTests(unittest.TestCase):
    def test_klean_audit_tool_bundle_lock_matches_sources(self) -> None:
        checker = REPO / "docker/klean-audit/check_tool_bundle.py"
        lock = REPO / "data/klean-audit-tools.lock.json"
        self.assertTrue(checker.is_file())
        self.assertTrue(lock.is_file())
        result = subprocess.run(
            [
                sys.executable,
                str(checker),
                "--root",
                str(REPO),
                "--lock",
                str(lock),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_klean_audit_tool_bundle_rejects_stale_dependency(self) -> None:
        checker = REPO / "docker/klean-audit/check_tool_bundle.py"
        lock = REPO / "data/klean-audit-tools.lock.json"
        self.assertTrue(checker.is_file())
        self.assertTrue(lock.is_file())
        document = json.loads(lock.read_text())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for relative in document["files"]:
                destination = root / relative
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(REPO / relative, destination)
            stale = root / "tools/lemma_discovery_contract.py"
            stale.write_text(stale.read_text() + "\n# stale copy\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--root",
                    str(root),
                    "--lock",
                    str(lock),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("lemma_discovery_contract.py", result.stdout)
        self.assertIn("SHA-256 mismatch", result.stdout)

    def test_klean_audit_tool_bundle_requires_schema_v2(self) -> None:
        checker = REPO / "docker/klean-audit/check_tool_bundle.py"
        lock = REPO / "data/klean-audit-tools.lock.json"
        self.assertTrue(checker.is_file())
        with tempfile.TemporaryDirectory() as temporary:
            manifest = Path(temporary) / "manifest.json"
            manifest.write_text(json.dumps({"schema_version": 1}) + "\n")
            result = subprocess.run(
                [
                    sys.executable,
                    str(checker),
                    "--root",
                    str(REPO),
                    "--lock",
                    str(lock),
                    "--discovery-manifest",
                    str(manifest),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("schema_version must be 2", result.stdout)

    def test_toolchain_lock_and_both_images_use_exact_pins(self) -> None:
        lock = json.loads(
            (REPO / "data/klean-toolchain.lock.json").read_text()
        )
        self.assertEqual(lock["codex_cli_version"], "0.144.6")
        self.assertEqual(lock["k_base_image"], K_IMAGE)
        self.assertEqual(lock["k_version"], "7.1.293")
        self.assertEqual(lock["runtimeverification_k_commit"], K_COMMIT)
        self.assertEqual(lock["pyk_version"], "7.1.293")
        self.assertEqual(lock["lean_toolchain"], LEAN)
        for relative in (
            "docker/codex/Dockerfile",
            "docker/klean/Dockerfile",
        ):
            source = (REPO / relative).read_text()
            self.assertIn(f"K_COMMIT={K_COMMIT}", source, relative)
            self.assertIn(f"LEAN_TOOLCHAIN={LEAN}", source, relative)
            self.assertIn(f"FROM {K_IMAGE}", source, relative)
            self.assertIn(
                "/opt/runtimeverification-k/pyk/.venv/bin", source, relative
            )
            self.assertIn("/opt/elan/bin", source, relative)
            self.assertIn(
                'elan toolchain install "$LEAN_TOOLCHAIN"', source, relative
            )
            self.assertIn("ENV ELAN_HOME=/opt/elan", source, relative)
            self.assertIn(
                "/usr/local/bin/assert-frozen-toolchain", source, relative
            )
            self.assertNotIn('PATH="/root/', source, relative)

    def test_agent_and_generator_images_have_separate_capabilities(self) -> None:
        agent = (REPO / "docker/codex/Dockerfile").read_text()
        generator = (REPO / "docker/klean/Dockerfile").read_text()
        self.assertIn("@openai/codex@0.144.6", agent)
        self.assertIn("tools/klean.py", agent)
        self.assertNotIn("@openai/codex", generator)
        self.assertNotIn("auth.json", generator)
        self.assertNotIn("CODEX_HOME", generator)
        for source in (agent, generator):
            self.assertIn("tools/klean_export.py", source)
            self.assertIn("tools/klean_preflight.py", source)

    def test_generator_pins_python_hash_seed(self) -> None:
        generator = (REPO / "docker/klean/Dockerfile").read_text()
        self.assertIn("ENV PYTHONHASHSEED=0", generator)

    def test_stage_entrypoints_assert_the_frozen_toolchain_first(self) -> None:
        expected = {
            "docker/codex/entrypoint.sh": "agent",
            "docker/audit/entrypoint.sh": "agent",
            "docker/klean/entrypoint.sh": "klean",
        }
        for relative, mode in expected.items():
            source = (REPO / relative).read_text()
            self.assertIn(
                "/usr/local/bin/assert-frozen-toolchain", source, relative
            )
            assertion = f'"$FROZEN_TOOLCHAIN_CHECK" {mode}'
            self.assertIn(assertion, source, relative)
            self.assertLess(
                source.index(assertion),
                source.index(": \"${")
                if ": \"${" in source
                else source.index("WORKSPACE="),
                relative,
            )

    def test_runtime_images_copy_exact_command_module_closures(
        self,
    ) -> None:
        agent = copied_tool_modules(REPO / "docker/codex/Dockerfile")
        generator = copied_tool_modules(
            REPO / "docker/klean/Dockerfile"
        )
        self.assertEqual(
            agent,
            {
                "klean",
                "klean_export",
                "klean_preflight",
                "klean_final_gate",
                "k_rule_inventory",
                "lemma_discovery_contract",
                "pipeline_contract",
                "stage5_mechanical_check",
                "stage6_resolution_contract",
            },
        )
        self.assertEqual(
            generator,
            {
                "klean",
                "klean_export",
                "klean_preflight",
                "k_rule_inventory",
                "lemma_discovery_contract",
            },
        )

    def test_final_gate_direct_local_imports_are_in_agent_image(
        self,
    ) -> None:
        copied = copied_tool_modules(
            REPO / "docker/codex/Dockerfile"
        )
        imported = direct_local_tool_imports(
            REPO / "tools/klean_final_gate.py"
        )
        self.assertEqual(
            imported,
            {
                "klean_export",
                "klean_preflight",
                "pipeline_contract",
                "stage6_resolution_contract",
            },
        )
        self.assertLessEqual(imported, copied)
        self.assertEqual(
            local_tool_import_closure("klean_final_gate"),
            copied
            - {"klean", "klean_final_gate", "stage5_mechanical_check"},
        )
        self.assertEqual(
            direct_local_tool_imports(
                REPO / "tools/stage5_mechanical_check.py"
            ),
            {"klean_final_gate"},
        )
        self.assertEqual(
            direct_local_tool_imports(
                REPO / "tools/stage6_resolution_contract.py"
            ),
            set(),
        )

    def test_agent_image_tool_copy_imports_final_gate_in_isolation(
        self,
    ) -> None:
        copied = copied_tool_modules(
            REPO / "docker/codex/Dockerfile"
        )
        with tempfile.TemporaryDirectory() as temporary:
            tools = Path(temporary) / "opt/humaneval/tools"
            tools.mkdir(parents=True)
            for module in copied:
                shutil.copy2(
                    REPO / "tools" / f"{module}.py",
                    tools / f"{module}.py",
                )
            result = subprocess.run(
                [
                    sys.executable,
                    "-I",
                    str(tools / "klean_final_gate.py"),
                    "--help",
                ],
                cwd=temporary,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_generator_image_tool_copy_imports_commands_in_isolation(
        self,
    ) -> None:
        copied = copied_tool_modules(
            REPO / "docker/klean/Dockerfile"
        )
        with tempfile.TemporaryDirectory() as temporary:
            tools = Path(temporary) / "opt/humaneval/tools"
            tools.mkdir(parents=True)
            for module in copied:
                shutil.copy2(
                    REPO / "tools" / f"{module}.py",
                    tools / f"{module}.py",
                )
            for command in ("klean_export.py", "klean_preflight.py"):
                with self.subTest(command=command):
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-I",
                            str(tools / command),
                            "--help",
                        ],
                        cwd=temporary,
                        text=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                    )
                    self.assertEqual(
                        result.returncode, 0, result.stdout
                    )

    def test_no_runtime_launcher_downloads_dependencies(self) -> None:
        for relative in (
            "docker/codex/entrypoint.sh",
            "docker/codex/run_task.sh",
            "docker/codex/resume_lemma_discovery_task.sh",
            "docker/codex/resume_lean_task.sh",
            "docker/codex/resume_klean_task.sh",
            "docker/klean/entrypoint.sh",
            "docker/klean/generate_task.sh",
            "docker/klean/check_task.sh",
            "docker/klean-audit/entrypoint.sh",
            "docker/klean-audit/run_task.sh",
        ):
            source = (REPO / relative).read_text()
            for forbidden in (
                "apt-get install",
                "npm install",
                "uv sync",
                "elan toolchain install",
                "lake update",
                "docker pull",
            ):
                self.assertNotIn(forbidden, source, relative)

    def test_compose_and_audit_mounts_match_stage_boundaries(self) -> None:
        base = (REPO / "docker/codex/docker-compose.yml").read_text()
        discovery = (
            REPO
            / "docker/codex/docker-compose.lemma-discovery.yml"
        ).read_text()
        lean = (REPO / "docker/codex/docker-compose.klean.yml").read_text()
        audit = (REPO / "docker/klean-audit/run_task.sh").read_text()
        self.assertIn("context: ../..", base)
        self.assertIn("dockerfile: docker/codex/Dockerfile", base)
        self.assertIn(":/workspace:rw", base)
        self.assertIn(":/invocation-output:rw", base)
        self.assertIn(":/codex-home:rw", base)
        self.assertNotIn("/reference/", base)
        self.assertNotIn("K_REFERENCE_DIR", base)
        self.assertNotIn("RULE_INVENTORY_PATH", base)
        self.assertNotIn("LEMMA_DISCOVERY", base)
        self.assertEqual(discovery.count(":ro"), 2)
        self.assertNotIn(":rw", discovery)
        self.assertIn(":/reference/k-proof:ro", discovery)
        self.assertIn(
            ":/reference/rule-inventory.json:ro", discovery
        )
        self.assertIn('LEMMA_DISCOVERY: "1"', discovery)
        self.assertIn("/reference/k-proof:ro", lean)
        self.assertIn("/reference/trust-boundary.json:ro", lean)
        self.assertIn("/workspace/Base:ro", lean)
        self.assertIn("/workspace/lakefile.lean:ro", lean)
        self.assertIn("/workspace/lean-toolchain:ro", lean)
        self.assertNotIn("02-k-audit", lean)
        self.assertNotIn(
            "/home/yuqing/Documents/Code/kit",
            (REPO / "docker/audit/run_task.sh").read_text(),
        )
        for target in (
            "/reference/k-proof,readonly",
            "/reference/k-audit,readonly",
            "/reference/klean-generation,readonly",
            "/candidate,readonly",
        ):
            self.assertIn(target, audit)

    def test_stage6_launcher_fail_fast_checks_bundle_and_schema(self) -> None:
        source = (REPO / "docker/klean-audit/run_task.sh").read_text()
        for fragment in (
            "check_tool_bundle.py",
            "/reference/check-tool-bundle.py",
            "--discovery-manifest",
        ):
            self.assertIn(fragment, source)
        prepare = source.index("klean_audit_contract.py\" prepare")
        host_check = source.index("check_tool_bundle.py")
        image_check = source.index("/reference/check-tool-bundle.py")
        schema_check = source.index("--discovery-manifest")
        self.assertLess(host_check, prepare)
        self.assertLess(image_check, prepare)
        self.assertLess(schema_check, prepare)
        self.assertIn("mechanical_checker_lock_sha256", source)
        self.assertGreaterEqual(source.count('\"$IMAGE_ID\"'), 3)

    def test_layout_creator_builds_all_six_stage_roots(self) -> None:
        contract = (REPO / "tools/pipeline_contract.py").read_text()
        for stage in (
            "01-k-proof",
            "02-k-audit",
            "03-lemma-discovery",
            "04-klean-generation",
            "05-lean-proof",
            "06-lean-audit",
        ):
            self.assertIn(f'"{stage}"', contract)

    def test_existing_offline_smoke_checks_codex_lean_and_klean(self) -> None:
        smoke = (REPO / "tests/smoke-containers.sh").read_text()
        self.assertIn("CODEX_PIPELINE_CHECKS", smoke)
        self.assertIn(
            "/usr/local/bin/assert-frozen-toolchain agent", smoke
        )
        self.assertIn("command -v lean", smoke)
        self.assertIn("command -v lake", smoke)
        self.assertIn("import pyk.klean", smoke)
        self.assertIn(
            "python3 /opt/humaneval/tools/klean_final_gate.py "
            "--help >/dev/null",
            smoke,
        )

    def test_offline_smoke_runs_both_six_stage_contract_modes(self) -> None:
        smoke = (REPO / "tests/smoke-containers.sh").read_text()
        for fragment in (
            "SIX_STAGE_CONTRACT_TEST",
            "test_resolves_proof_bearing_and_no_obligation_modes",
            "CLASSIFICATION_AND_PROOF",
            "KLEAN_NO_OBLIGATIONS",
            "CLASSIFICATION_ONLY",
            "06-lean-audit",
        ):
            with self.subTest(fragment=fragment):
                self.assertIn(fragment, smoke)


if __name__ == "__main__":
    unittest.main()
