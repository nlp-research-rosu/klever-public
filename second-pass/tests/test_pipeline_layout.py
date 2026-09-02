import json
import os
import stat
import tempfile
import unittest
from pathlib import Path

from tools import pipeline_contract


class PipelineLayoutFixture(unittest.TestCase):
    PROBLEM = "8-sum-product"

    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.repo = Path(self.temporary_directory.name)
        self.make_problem(self.PROBLEM)
        (self.repo / "tools").mkdir(exist_ok=True)
        (self.repo / "tools/py2mpy.py").write_text("# translator\n")
        (self.repo / "prompts").mkdir()
        for name in (
            "bare.md",
            "with-semantics.md",
            "kit-bare.md",
            "kit-semantics.md",
        ):
            (self.repo / "prompts" / name).write_text(f"# {name}\n")
        (self.repo / "prompts/timeout-resume.md").write_text(
            "Continue the same session after the resource timeout.\n"
        )
        (self.repo / "prompts/oom-resume.md").write_text(
            "Continue the same session after the memory limit.\n"
        )
        (self.repo / "prompts/terminal-resume.md").write_text(
            "Continue the same session after terminal interruption.\n"
        )
        (self.repo / "prompts/infrastructure-resume.md").write_text(
            "Continue the same session after runner infrastructure repair.\n"
        )
        semantics = self.repo / "data/reference/src"
        semantics.mkdir(parents=True)
        (semantics / "semantics.k").write_text("module SEMANTICS endmodule\n")
        (semantics / "empty-dir").mkdir()
        (self.repo / "data/reference-semantics-versions.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "versions": {
                        pipeline_contract.sha256_tree(semantics): {
                            "path": "data/reference/src",
                            "label": "fixture semantics",
                        }
                    },
                }
            )
            + "\n"
        )
        (self.repo / "data/kit-skills.lock.json").write_text(
            json.dumps(
                {
                    "commit": "kit-commit",
                    "skills_tree": "kit-tree",
                }
            )
            + "\n"
        )
        (self.repo / "data/klean-toolchain.lock.json").write_text(
            json.dumps(pipeline_contract.FROZEN_TOOLCHAIN_LOCK)
            + "\n"
        )
        (self.repo / "runs").mkdir()

    def make_problem(self, problem: str) -> Path:
        question = self.repo / "data/questions" / problem
        question.mkdir(parents=True)
        (question / "prompt.py").write_text("def sum_product(numbers):\n    pass\n")
        (question / "canonical.py").write_text(
            "def sum_product(numbers):\n    return sum(numbers), 1\n"
        )
        return question


class CreateRunTests(PipelineLayoutFixture):
    def test_creates_stage_oriented_bare_task_and_external_state(self) -> None:
        result = pipeline_contract.create_run(
            self.repo,
            run_id="run-001",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[self.PROBLEM],
        )

        run = self.repo / "runs/run-001"
        task = run / "tasks" / self.PROBLEM
        workspace = task / "01-k-proof/workspace"
        state = self.repo / "runner-state/run-001" / self.PROBLEM
        self.assertEqual(result, run.resolve())
        self.assertTrue((run / "run.json").is_file())
        self.assertEqual((run / "task-list.txt").read_text(), f"{self.PROBLEM}\n")
        self.assertTrue((task / "task.json").is_file())
        self.assertEqual(
            pipeline_contract.STAGE_NAMES,
            (
                "01-k-proof",
                "02-k-audit",
                "03-lemma-discovery",
                "04-klean-generation",
                "05-lean-proof",
                "06-lean-audit",
            ),
        )
        for stage in pipeline_contract.STAGE_NAMES:
            self.assertTrue((task / stage).is_dir(), stage)
        for relative in (
            "03-lemma-discovery/workspace",
            "03-lemma-discovery/invocations",
            "04-klean-generation/generations",
            "05-lean-proof/workspace",
            "05-lean-proof/invocations",
            "06-lean-audit/executions",
        ):
            self.assertTrue((task / relative).is_dir(), relative)
        self.assertEqual(
            (workspace / "prompt.py").read_bytes(),
            (self.repo / f"data/questions/{self.PROBLEM}/prompt.py").read_bytes(),
        )
        self.assertEqual(
            (workspace / "py2mpy.py").read_bytes(),
            (self.repo / "tools/py2mpy.py").read_bytes(),
        )
        self.assertFalse((workspace / "reference-semantics").exists())
        self.assertEqual(list(task.rglob("canonical.py")), [])
        self.assertTrue((state / "codex-home").is_dir())
        self.assertEqual(stat.S_IMODE(state.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((state / "codex-home").stat().st_mode), 0o700)

        run_manifest = json.loads((run / "run.json").read_text())
        self.assertEqual(run_manifest["run_id"], "run-001")
        self.assertEqual(
            run_manifest["config"], "codex-gpt-5.6-sol-xhigh-bare"
        )
        self.assertEqual(run_manifest["condition"]["name"], "bare")
        self.assertEqual(run_manifest["model"], "gpt-5.6-sol")
        self.assertEqual(run_manifest["effort"], "xhigh")
        self.assertEqual(
            run_manifest["timeouts"],
            {
                "k_initial_s": 3600,
                "k_total_s": 7200,
                "lemma_initial_s": 1200,
                "lemma_total_s": 1200,
                "lean_initial_s": 3600,
                "lean_total_s": 7200,
            },
        )
        self.assertRegex(
            run_manifest["runtime"]["klean_toolchain_lock_sha256"],
            r"^[0-9a-f]{64}$",
        )
        self.assertEqual(
            run_manifest["runtime"],
            {
                "codex_cli_version": "0.144.6",
                "k_version": "7.1.293",
                "runtimeverification_k_commit": (
                    "ff15baac9e66426612ec45ff912af7f14965b64a"
                ),
                "pyk_version": "7.1.293",
                "lean_toolchain": "leanprover/lean4:v4.22.0",
                "klean_toolchain_lock_sha256": (
                    run_manifest["runtime"][
                        "klean_toolchain_lock_sha256"
                    ]
                ),
            },
        )

    def test_rejects_a_modified_frozen_toolchain_lock(self) -> None:
        lock = self.repo / "data/klean-toolchain.lock.json"
        document = json.loads(lock.read_text())
        document["k_version"] = "7.1.337"
        lock.write_text(json.dumps(document) + "\n")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "frozen toolchain lock differs",
        ):
            pipeline_contract.create_run(
                self.repo,
                run_id="mixed-toolchain",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM],
            )
        self.assertFalse((self.repo / "runs/mixed-toolchain").exists())

    def test_rejects_resuming_a_run_with_a_different_toolchain(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="mixed-resume",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/mixed-resume/run.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["runtime"]["codex_cli_version"] = "0.145.0"
        manifest_path.write_text(json.dumps(manifest) + "\n")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "run toolchain differs from the frozen",
        ):
            pipeline_contract._resolve_task_state(
                self.repo, "mixed-resume", self.PROBLEM
            )

    def test_rejects_any_changed_recorded_runtime_field(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="mixed-runtime",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/mixed-runtime/run.json"
        for field, changed in (
            ("k_version", "7.1.337"),
            ("runtimeverification_k_commit", "different"),
            ("pyk_version", "7.1.337"),
            ("lean_toolchain", "leanprover/lean4:v4.23.0"),
        ):
            with self.subTest(field=field):
                manifest = json.loads(manifest_path.read_text())
                original = manifest["runtime"][field]
                manifest["runtime"][field] = changed
                manifest_path.write_text(json.dumps(manifest) + "\n")
                with self.assertRaisesRegex(
                    pipeline_contract.PipelineContractError,
                    "run toolchain differs from the frozen",
                ):
                    pipeline_contract._resolve_task_state(
                        self.repo, "mixed-runtime", self.PROBLEM
                    )
                manifest["runtime"][field] = original
                manifest_path.write_text(json.dumps(manifest) + "\n")

    def test_resolves_historical_kit_provenance_without_current_lock(
        self,
    ) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="mixed-kit",
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/mixed-kit/run.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["kit"]["commit"] = "historical-commit"
        manifest["kit"]["skills_tree"] = "historical-tree"
        manifest_path.write_text(json.dumps(manifest) + "\n")

        _task, _state, resolved = pipeline_contract._resolve_task_state(
            self.repo, "mixed-kit", self.PROBLEM
        )
        self.assertEqual(
            resolved["kit"],
            {
                "commit": "historical-commit",
                "skills_tree": "historical-tree",
            },
        )

    def test_new_model_work_rejects_noncurrent_kit_provenance(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="mixed-kit-launch",
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/mixed-kit-launch/run.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["kit"]["commit"] = "historical-commit"
        manifest_path.write_text(json.dumps(manifest) + "\n")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "run Kit provenance differs",
        ):
            pipeline_contract._resolve_task_state(
                self.repo,
                "mixed-kit-launch",
                self.PROBLEM,
                require_current_kit=True,
            )
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "run Kit provenance differs",
        ):
            pipeline_contract.prepare_invocation(
                self.repo, "mixed-kit-launch", self.PROBLEM, "01-k-proof"
            )

    def test_task_kit_override_takes_precedence_for_model_work(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="override-kit",
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/override-kit/run.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["kit"]["commit"] = "historical-commit"
        manifest["kit"]["skills_tree"] = "historical-tree"
        manifest_path.write_text(json.dumps(manifest) + "\n")
        task_path = (
            self.repo / "runs/override-kit/tasks" / self.PROBLEM / "task.json"
        )

        # A task promoted from a current-Kit replacement generation may
        # launch new model work even though the run-level Kit is historical.
        task_manifest = json.loads(task_path.read_text())
        task_manifest["kit"] = {
            "commit": "kit-commit",
            "skills_tree": "kit-tree",
        }
        task_path.write_text(json.dumps(task_manifest) + "\n")
        pipeline_contract._resolve_task_state(
            self.repo,
            "override-kit",
            self.PROBLEM,
            require_current_kit=True,
        )

        # An override older than the current bundle blocks new model work
        # but still resolves for status, audits, and selection.
        task_manifest["kit"] = {
            "commit": "older-commit",
            "skills_tree": "older-tree",
        }
        task_path.write_text(json.dumps(task_manifest) + "\n")
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "run Kit provenance differs",
        ):
            pipeline_contract._resolve_task_state(
                self.repo,
                "override-kit",
                self.PROBLEM,
                require_current_kit=True,
            )
        pipeline_contract._resolve_task_state(
            self.repo, "override-kit", self.PROBLEM
        )

    def test_rejects_malformed_kit_provenance(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="broken-kit",
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/broken-kit/run.json"
        for kit in (None, "kit", {}, {"commit": "only"}, {"commit": "",
                    "skills_tree": "tree"}):
            with self.subTest(kit=kit):
                manifest = json.loads(manifest_path.read_text())
                manifest["kit"] = kit
                manifest_path.write_text(json.dumps(manifest) + "\n")
                with self.assertRaisesRegex(
                    pipeline_contract.PipelineContractError,
                    "Kit provenance is malformed",
                ):
                    pipeline_contract._resolve_task_state(
                        self.repo, "broken-kit", self.PROBLEM
                    )
        task_path = (
            self.repo / "runs/broken-kit/tasks" / self.PROBLEM / "task.json"
        )
        manifest = json.loads(manifest_path.read_text())
        manifest["kit"] = {"commit": "kit-commit", "skills_tree": "kit-tree"}
        manifest_path.write_text(json.dumps(manifest) + "\n")
        task_manifest = json.loads(task_path.read_text())
        task_manifest["kit"] = {"commit": "task-only"}
        task_path.write_text(json.dumps(task_manifest) + "\n")
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "Kit provenance is malformed",
        ):
            pipeline_contract._resolve_task_state(
                self.repo, "broken-kit", self.PROBLEM
            )

    def test_rejects_a_nonlegacy_run_without_toolchain_provenance(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="missing-runtime",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[self.PROBLEM],
        )
        manifest_path = self.repo / "runs/missing-runtime/run.json"
        manifest = json.loads(manifest_path.read_text())
        manifest.pop("runtime")
        manifest_path.write_text(json.dumps(manifest) + "\n")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError,
            "missing frozen toolchain provenance",
        ):
            pipeline_contract._resolve_task_state(
                self.repo, "missing-runtime", self.PROBLEM
            )

    def test_semantics_task_contains_exact_reference_tree_and_kit_lock(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="run-kit-semantics",
            config="codex-gpt-5.6-sol-xhigh-kit-semantics",
            problem_ids=[self.PROBLEM],
        )

        run = self.repo / "runs/run-kit-semantics"
        workspace = run / f"tasks/{self.PROBLEM}/01-k-proof/workspace"
        self.assertEqual(
            pipeline_contract.sha256_tree(workspace / "reference-semantics"),
            pipeline_contract.sha256_tree(self.repo / "data/reference/src"),
        )
        manifest = json.loads((run / "run.json").read_text())
        self.assertEqual(manifest["condition"]["name"], "kit-semantics")
        self.assertEqual(
            manifest["kit"],
            {"commit": "kit-commit", "skills_tree": "kit-tree"},
        )

    def test_prevalidates_every_problem_before_creating_run(self) -> None:
        missing = "999-missing"

        with self.assertRaises(pipeline_contract.PipelineContractError):
            pipeline_contract.create_run(
                self.repo,
                run_id="atomic-run",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM, missing],
            )

        self.assertFalse((self.repo / "runs/atomic-run").exists())
        self.assertFalse((self.repo / "runner-state/atomic-run").exists())

    def test_existing_compatible_run_is_not_silently_reused(self) -> None:
        pipeline_contract.create_run(
            self.repo,
            run_id="once-only",
            config="codex-gpt-5.6-sol-xhigh-bare",
            problem_ids=[self.PROBLEM],
        )

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "already exists"
        ):
            pipeline_contract.create_run(
                self.repo,
                run_id="once-only",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM],
            )

    def test_rejects_unsafe_components_before_creating_paths(self) -> None:
        unsafe = (
            "",
            ".",
            "..",
            ".hidden",
            "../escape",
            "a/b",
            "a\\b",
            "/tmp/x",
            "bad\nname",
        )
        for value in unsafe:
            with self.subTest(run_id=value):
                with self.assertRaises(pipeline_contract.PipelineContractError):
                    pipeline_contract.create_run(
                        self.repo,
                        run_id=value,
                        config="codex-gpt-5.6-sol-xhigh-bare",
                        problem_ids=[self.PROBLEM],
                    )
            with self.subTest(problem=value):
                with self.assertRaises(pipeline_contract.PipelineContractError):
                    pipeline_contract.create_run(
                        self.repo,
                        run_id="safe-run",
                        config="codex-gpt-5.6-sol-xhigh-bare",
                        problem_ids=[value],
                    )
                self.assertFalse((self.repo / "runs/safe-run").exists())

    def test_rejects_linked_runs_and_state_roots(self) -> None:
        outside = self.repo / "outside"
        outside.mkdir()
        (self.repo / "runs").rmdir()
        os.symlink(outside, self.repo / "runs")

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "runs root"
        ):
            pipeline_contract.create_run(
                self.repo,
                run_id="linked-root",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM],
            )

        (self.repo / "runs").unlink()
        (self.repo / "runs").mkdir()
        os.symlink(outside, self.repo / "runner-state")
        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "runner-state root"
        ):
            pipeline_contract.create_run(
                self.repo,
                run_id="linked-state",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM],
            )

    @unittest.skipUnless(hasattr(os, "mkfifo"), "mkfifo unavailable")
    def test_rejects_nonregular_trusted_seed_without_reading_it(self) -> None:
        prompt = self.repo / f"data/questions/{self.PROBLEM}/prompt.py"
        prompt.unlink()
        os.mkfifo(prompt)

        with self.assertRaisesRegex(
            pipeline_contract.PipelineContractError, "prompt"
        ):
            pipeline_contract.create_run(
                self.repo,
                run_id="fifo-seed",
                config="codex-gpt-5.6-sol-xhigh-bare",
                problem_ids=[self.PROBLEM],
            )


if __name__ == "__main__":
    unittest.main()
