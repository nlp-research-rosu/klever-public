#!/usr/bin/env python3
"""Populate runs/<config>/ task folders from data/selection.json.

Usage: python3 tools/populate_runs.py <config> [<config> ...]

Each task folder gets prompt.py + py2mpy.py; semantics conditions additionally
get a self-contained reference-semantics/ copy. Existing task folders are
validated before they are skipped.
"""
from dataclasses import dataclass
import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Condition:
    name: str
    kit: bool
    semantics: bool
    prompt_file: str


CONDITIONS = (
    Condition("kit-semantics", True, True, "kit-semantics.md"),
    Condition("semantics", False, True, "with-semantics.md"),
    Condition("kit", True, False, "kit-bare.md"),
    Condition("bare", False, False, "bare.md"),
)


class SeedContractError(RuntimeError):
    pass


def validate_safe_component(
    value: object, label: str, *, allow_hidden: bool
) -> None:
    if not isinstance(value, str):
        raise ValueError(
            f"{label} must be one "
            f"{'safe' if allow_hidden else 'nonhidden safe'} path component: "
            f"{value!r}"
        )
    path = Path(value)
    if (
        not value
        or value in {".", ".."}
        or (not allow_hidden and value.startswith("."))
        or path.is_absolute()
        or len(path.parts) != 1
        or "/" in value
        or "\\" in value
        or any(ord(character) < 32 or ord(character) == 127 for character in value)
    ):
        raise ValueError(
            f"{label} must be one "
            f"{'safe' if allow_hidden else 'nonhidden safe'} path component: "
            f"{value!r}"
        )


def validate_config_name(config: str) -> None:
    validate_safe_component(config, "config", allow_hidden=True)


def validate_problem_id(problem_id: object) -> None:
    validate_safe_component(problem_id, "problem ID", allow_hidden=False)


def parse_condition(config: str) -> Condition:
    validate_config_name(config)
    for condition in CONDITIONS:
        if config.endswith(f"-{condition.name}"):
            return condition
    names = ", ".join(condition.name for condition in CONDITIONS)
    raise ValueError(f"config must end in one of: {names}: {config}")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        relative = path.relative_to(root).as_posix().encode()
        digest.update(len(relative).to_bytes(4, "big"))
        digest.update(relative)
        content = path.read_bytes()
        digest.update(len(content).to_bytes(8, "big"))
        digest.update(content)
    return digest.hexdigest()


def tree_entry_types(root: Path) -> dict[Path, str]:
    if root.is_symlink() or not root.is_dir():
        raise SeedContractError(f"{root}: tree root must be a real directory")
    entries: dict[Path, str] = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if path.is_symlink():
            raise SeedContractError(f"{path}: tree symlinks are forbidden")
        if path.is_dir():
            entries[relative] = "directory"
        elif path.is_file():
            entries[relative] = "file"
        else:
            raise SeedContractError(f"{path}: unsupported tree entry type")
    return entries


def validate_task_seed(repo: Path, config: str, problem_id: str, task: Path) -> None:
    validate_problem_id(problem_id)
    condition = parse_condition(config)
    if task.is_symlink() or not task.is_dir():
        raise SeedContractError(f"{task}: task directory must be a real directory")
    forbidden = next(task.rglob("canonical.py"), None)
    if forbidden is not None:
        raise SeedContractError(f"{forbidden}: canonical.py is forbidden")
    expected_prompt = repo / "data/questions" / problem_id / "prompt.py"
    expected_translator = repo / "tools/py2mpy.py"
    for actual, expected in (
        (task / "prompt.py", expected_prompt),
        (task / "py2mpy.py", expected_translator),
    ):
        if actual.is_symlink():
            raise SeedContractError(f"{actual}: seed file symlinks are forbidden")
        if not actual.is_file() or actual.read_bytes() != expected.read_bytes():
            raise SeedContractError(f"{actual}: missing or stale seed file")
    semantics = task / "reference-semantics"
    if condition.semantics:
        source = repo / "data/reference/src"
        expected_entries = tree_entry_types(source)
        actual_entries = tree_entry_types(semantics)
        if actual_entries != expected_entries:
            raise SeedContractError(
                f"{semantics}: missing, unexpected, or mistyped semantics entry"
            )
        for relative, entry_type in expected_entries.items():
            if entry_type != "file":
                continue
            expected = source / relative
            actual = semantics / relative
            if actual.read_bytes() != expected.read_bytes():
                raise SeedContractError(f"{actual}: missing or stale semantics file")
    elif semantics.is_symlink() or semantics.exists():
        raise SeedContractError(f"{semantics}: forbidden for {condition.name}")
    manifest = task / "run-input.json"
    expected_manifest = render_manifest(build_manifest(repo, config, problem_id))
    try:
        manifest_mode = manifest.lstat().st_mode
    except OSError as error:
        raise SeedContractError(
            f"{manifest}: manifest must be a real regular file"
        ) from error
    if not stat.S_ISREG(manifest_mode):
        raise SeedContractError(f"{manifest}: manifest must be a real regular file")
    try:
        actual_manifest = manifest.read_bytes()
    except OSError as error:
        raise SeedContractError(
            f"{manifest}: missing, malformed, or stale manifest"
        ) from error
    if actual_manifest != expected_manifest.encode():
        raise SeedContractError(f"{manifest}: missing, malformed, or stale manifest")


def _selected_problem_ids(
    repo: Path, *, require_exact_count: bool = True
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    selection_path = repo / "data/selection.json"
    try:
        document = json.loads(selection_path.read_text())
        selected = document["selected"]
        if not isinstance(selected, list):
            raise TypeError("selected must be a list")
    except (OSError, ValueError, KeyError, TypeError) as error:
        return [], [f"{selection_path}: invalid selection: {error}"]

    problem_ids: list[str] = []
    for index, entry in enumerate(selected):
        try:
            problem_id = entry["id"]
        except (KeyError, TypeError) as error:
            errors.append(f"{selection_path}: selected[{index}] has no valid id: {error}")
            continue
        try:
            validate_problem_id(problem_id)
        except ValueError as error:
            errors.append(f"{selection_path}: selected[{index}]: {error}")
        if isinstance(problem_id, str):
            problem_ids.append(problem_id)

    if require_exact_count and (
        len(selected) != 24
        or len(problem_ids) != 24
        or len(set(problem_ids)) != 24
    ):
        errors.append(
            f"{selection_path}: selection must contain exactly 24 distinct problem IDs"
        )
    return problem_ids, errors


def _entry_mode(
    entry: os.DirEntry[str], context: str, errors: list[str]
) -> int | None:
    try:
        return entry.stat(follow_symlinks=False).st_mode
    except OSError as error:
        errors.append(f"{context}: cannot inspect entry without following it: {error}")
        return None


def audit_active_runs(repo: Path, runs_root: Path | None = None) -> list[str]:
    """Return every active-run contract error without following unknown entries."""
    root = repo / "runs" if runs_root is None else Path(runs_root)
    errors: list[str] = []
    try:
        root_mode = root.lstat().st_mode
    except OSError as error:
        return [f"{root}: runs root must be a real directory: {error}"]
    if not stat.S_ISDIR(root_mode):
        return [f"{root}: runs root must be a real directory"]

    problem_ids, selection_errors = _selected_problem_ids(repo)
    errors.extend(selection_errors)
    selected = set(problem_ids)

    try:
        with os.scandir(root) as iterator:
            config_entries = sorted(iterator, key=lambda entry: entry.name)
    except OSError as error:
        return errors + [f"{root}: cannot scan runs root: {error}"]

    for config_entry in config_entries:
        config_name = config_entry.name
        config_path = root / config_name
        context = f"{config_path}: config entry"
        config_mode = _entry_mode(config_entry, context, errors)

        if config_name == "archive":
            if config_mode is not None and not stat.S_ISDIR(config_mode):
                errors.append(f"{config_path}: archive must be a real directory")
            continue

        hidden = config_name.startswith(".")
        if hidden:
            errors.append(f"{config_path}: hidden config entries are forbidden")
        if config_mode is not None and not stat.S_ISDIR(config_mode):
            errors.append(f"{config_path}: config entry must be a real directory")
        if hidden or config_mode is None or not stat.S_ISDIR(config_mode):
            continue

        try:
            with os.scandir(config_path) as iterator:
                task_entries = sorted(iterator, key=lambda entry: entry.name)
        except OSError as error:
            errors.append(f"{config_path}: cannot scan config directory: {error}")
            continue

        task_names = {entry.name for entry in task_entries}
        pipeline_required = {"run.json", "task-list.txt", "tasks"}
        pipeline_allowed = pipeline_required | {"usage-summary.json"}
        if pipeline_required.issubset(task_names) and task_names <= pipeline_allowed:
            stage_entries = {entry.name: entry for entry in task_entries}
            run_mode = _entry_mode(
                stage_entries["run.json"],
                f"{config_path / 'run.json'}: pipeline run manifest",
                errors,
            )
            list_mode = _entry_mode(
                stage_entries["task-list.txt"],
                f"{config_path / 'task-list.txt'}: pipeline task list",
                errors,
            )
            tasks_mode = _entry_mode(
                stage_entries["tasks"],
                f"{config_path / 'tasks'}: pipeline tasks root",
                errors,
            )
            summary_mode = None
            if "usage-summary.json" in stage_entries:
                summary_mode = _entry_mode(
                    stage_entries["usage-summary.json"],
                    f"{config_path / 'usage-summary.json'}: pipeline usage summary",
                    errors,
                )
            if (
                run_mode is not None
                and stat.S_ISREG(run_mode)
                and list_mode is not None
                and stat.S_ISREG(list_mode)
                and tasks_mode is not None
                and stat.S_ISDIR(tasks_mode)
                and (
                    "usage-summary.json" not in stage_entries
                    or (
                        summary_mode is not None
                        and stat.S_ISREG(summary_mode)
                    )
                )
            ):
                # The stage-oriented resumable pipeline owns this distinct
                # layout. Its contract validator, not the legacy seed auditor,
                # is responsible for the run and task subtree.
                continue
        if task_names != selected:
            missing = sorted(selected - task_names)
            unexpected = sorted(task_names - selected)
            errors.append(
                f"{config_path}: task set differs from selection; "
                f"missing={missing}; unexpected={unexpected}"
            )

        valid_tasks: dict[str, Path] = {}
        for task_entry in task_entries:
            problem_id = task_entry.name
            task_path = config_path / problem_id
            context = f"{task_path}: task entry"
            task_mode = _entry_mode(task_entry, context, errors)
            hidden = problem_id.startswith(".")
            if hidden:
                errors.append(f"{task_path}: hidden task entries are forbidden")
            if task_mode is not None and not stat.S_ISDIR(task_mode):
                errors.append(f"{task_path}: task entry must be a real directory")
            if hidden or task_mode is None or not stat.S_ISDIR(task_mode):
                continue
            valid_tasks[problem_id] = task_path

        for problem_id in problem_ids:
            task_path = valid_tasks.get(problem_id)
            if task_path is None:
                continue
            try:
                validate_task_seed(repo, config_name, problem_id, task_path)
            except (
                SeedContractError,
                ValueError,
                OSError,
                KeyError,
                TypeError,
            ) as error:
                errors.append(f"{config_name}/{problem_id}: {error}")

    return errors


def build_manifest(repo: Path, config: str, problem_id: str) -> dict[str, object]:
    validate_problem_id(problem_id)
    condition = parse_condition(config)
    prompt = repo / "data/questions" / problem_id / "prompt.py"
    instruction = repo / "prompts" / condition.prompt_file
    manifest: dict[str, object] = {
        "schema_version": 1,
        "config": config,
        "problem_id": problem_id,
        "condition": {
            "name": condition.name,
            "kit": condition.kit,
            "semantics": condition.semantics,
        },
        "inputs": {
            "problem_prompt_sha256": sha256_file(prompt),
            "instruction_prompt": condition.prompt_file,
            "instruction_prompt_sha256": sha256_file(instruction),
            "translator_sha256": sha256_file(repo / "tools/py2mpy.py"),
        },
    }
    if condition.semantics:
        manifest["inputs"]["reference_semantics_sha256"] = sha256_tree(
            repo / "data/reference/src"
        )
    if condition.kit:
        lock = json.loads((repo / "data/kit-skills.lock.json").read_text())
        manifest["kit"] = {
            "commit": lock["commit"],
            "skills_tree": lock["skills_tree"],
        }
    return manifest


def render_manifest(manifest: dict[str, object]) -> str:
    return json.dumps(manifest, indent=2, sort_keys=True) + "\n"


def populate(
    config: str, repo: Path = REPO, runs_root: Path | None = None
) -> tuple[int, int]:
    condition = parse_condition(config)
    problem_ids, selection_errors = _selected_problem_ids(
        repo, require_exact_count=False
    )
    if selection_errors:
        raise ValueError("selection validation failed: " + "; ".join(selection_errors))
    root = (repo / "runs" if runs_root is None else runs_root).resolve()
    unresolved_cfg_dir = root / config
    cfg_dir = unresolved_cfg_dir.resolve()
    archive = (repo / "runs/archive").resolve()
    if (
        unresolved_cfg_dir.is_symlink()
        or cfg_dir.parent != root
        or cfg_dir == archive
        or archive in cfg_dir.parents
    ):
        raise ValueError(f"config must resolve safely below runs root: {config!r}")
    created, skipped = 0, 0
    for pid in problem_ids:
        task = cfg_dir / pid
        manifest = build_manifest(repo, config, pid)
        if task.is_symlink() or task.exists():
            validate_task_seed(repo, config, pid, task)
            skipped += 1
            continue
        cfg_dir.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=f".{pid}.", dir=cfg_dir))
        try:
            staging.chmod(cfg_dir.stat().st_mode & 0o777)
            shutil.copy2(
                repo / "data/questions" / pid / "prompt.py", staging / "prompt.py"
            )
            shutil.copy2(repo / "tools/py2mpy.py", staging / "py2mpy.py")
            if condition.semantics:
                shutil.copytree(
                    repo / "data/reference/src", staging / "reference-semantics"
                )
            (staging / "run-input.json").write_text(render_manifest(manifest))
            validate_task_seed(repo, config, pid, staging)
            staging.rename(task)
        finally:
            if staging.exists():
                shutil.rmtree(staging)
        created += 1
    print(f"{config}: created {created}, skipped {skipped} existing")
    return created, skipped


def validate_task_cli(args: list[str]) -> int:
    if len(args) != 3:
        print(
            "usage: populate_runs.py --validate-task "
            "<config> <problem-id> <task-path>",
            file=sys.stderr,
        )
        return 2
    config, problem_id, task_path = args
    try:
        validate_task_seed(REPO, config, problem_id, Path(task_path))
    except (SeedContractError, ValueError, OSError, KeyError) as error:
        print(f"task seed validation failed: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if sys.argv[1] == "--validate-task":
        sys.exit(validate_task_cli(sys.argv[2:]))
    for cfg in sys.argv[1:]:
        populate(cfg)
