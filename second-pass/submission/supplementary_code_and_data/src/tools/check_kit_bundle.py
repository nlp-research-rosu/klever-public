#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LOCK_PATH = REPO / "data/kit-skills.lock.json"
BUNDLE = REPO / "data/skills"
FROZEN_KIT = {
    "commit": "46af96a89de7b297e9dd4e9cfc2bf248e6d4698f",
    "skills_tree": "ac515c9de2c87ac2366c9ea3d55c78cad172897b",
    "plugin_version": "0.2.12",
}


class BundleError(ValueError):
    pass


def entry_manifest(root: Path) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}

    def visit(path: Path, relative: str) -> None:
        try:
            metadata = path.lstat()
        except OSError as error:
            raise BundleError(f"cannot inspect entry {relative}: {error}") from error
        mode = f"{stat.S_IMODE(metadata.st_mode):04o}"
        if stat.S_ISLNK(metadata.st_mode):
            raise BundleError(f"symlink entries are not allowed: {relative}")
        if stat.S_ISDIR(metadata.st_mode):
            entries[relative] = {"type": "directory", "mode": mode}
            try:
                names = sorted(entry.name for entry in os.scandir(path))
            except OSError as error:
                raise BundleError(f"cannot scan directory {relative}: {error}") from error
            for name in names:
                child = name if relative == "." else f"{relative}/{name}"
                visit(path / name, child)
            return
        if stat.S_ISREG(metadata.st_mode):
            entries[relative] = {"type": "file", "mode": mode}
            return
        raise BundleError(f"special entries are not allowed: {relative}")

    visit(root, ".")
    return entries


def hash_file(path: Path, expected_mode: str) -> str:
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise BundleError(f"cannot open regular file {path}: {error}") from error
    try:
        metadata = os.fstat(descriptor)
        mode = f"{stat.S_IMODE(metadata.st_mode):04o}"
        if not stat.S_ISREG(metadata.st_mode) or mode != expected_mode:
            raise BundleError(f"entry changed while hashing: {path}")
        digest = hashlib.sha256()
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    finally:
        os.close(descriptor)


def snapshot(root: Path) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    entries = entry_manifest(root)
    files = {
        relative: hash_file(root / relative, entry["mode"])
        for relative, entry in entries.items()
        if entry["type"] == "file"
    }
    return entries, files


def hash_files(root: Path) -> dict[str, str]:
    return snapshot(root)[1]


def git(source: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def git_bytes(source: Path, *args: str) -> bytes:
    return subprocess.run(
        ["git", "-C", str(source), *args],
        check=True,
        capture_output=True,
    ).stdout


def parse_tree_record(record: bytes) -> tuple[str, str, str, str]:
    try:
        header, raw_path = record.split(b"\t", 1)
        mode, kind, object_id = header.decode("ascii").split()
        path = os.fsdecode(raw_path)
    except (UnicodeError, ValueError) as error:
        raise BundleError("cannot parse Git tree entry") from error
    return mode, kind, object_id, path


def committed_skills(
    source_repo: Path, commit: str
) -> tuple[dict[str, dict[str, str]], dict[str, str]]:
    output = git_bytes(
        source_repo,
        "ls-tree",
        "-rtz",
        "--full-tree",
        commit,
        "--",
        "skills",
    )
    entries: dict[str, dict[str, str]] = {}
    files: dict[str, str] = {}
    for record in output.split(b"\0"):
        if not record:
            continue
        mode, kind, object_id, path = parse_tree_record(record)
        if path == "skills":
            relative = "."
        elif path.startswith("skills/"):
            relative = path.removeprefix("skills/")
        else:
            raise BundleError(f"unexpected Git tree path: {path}")
        if mode == "040000" and kind == "tree":
            entries[relative] = {"type": "directory", "mode": "0755"}
        elif mode in {"100644", "100755"} and kind == "blob":
            permission = "0644" if mode == "100644" else "0755"
            entries[relative] = {"type": "file", "mode": permission}
            files[relative] = hashlib.sha256(
                git_bytes(source_repo, "cat-file", "blob", object_id)
            ).hexdigest()
        else:
            raise BundleError(f"unsupported committed entry {mode} {kind}: {path}")
    if entries.get(".", {}).get("type") != "directory":
        raise BundleError("HEAD does not contain a skills tree")
    return entries, files


def committed_plugin_manifest(source_repo: Path, commit: str) -> tuple[bytes, str]:
    output = git_bytes(
        source_repo,
        "ls-tree",
        "-z",
        "--full-tree",
        commit,
        "--",
        ".codex-plugin/plugin.json",
    )
    records = [record for record in output.split(b"\0") if record]
    if len(records) != 1:
        raise BundleError("HEAD must contain .codex-plugin/plugin.json")
    mode, kind, object_id, path = parse_tree_record(records[0])
    if path != ".codex-plugin/plugin.json" or kind != "blob":
        raise BundleError("HEAD has an invalid plugin manifest entry")
    if mode not in {"100644", "100755"}:
        raise BundleError("HEAD plugin manifest is not a regular file")
    permission = "0644" if mode == "100644" else "0755"
    return git_bytes(source_repo, "cat-file", "blob", object_id), permission


def read_source_manifest(path: Path, expected_mode: str) -> bytes:
    try:
        metadata = path.lstat()
    except OSError as error:
        raise BundleError(f"cannot inspect source plugin manifest: {error}") from error
    mode = f"{stat.S_IMODE(metadata.st_mode):04o}"
    if not stat.S_ISREG(metadata.st_mode) or mode != expected_mode:
        raise BundleError("source plugin manifest does not match HEAD")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as error:
        raise BundleError(f"cannot open source plugin manifest: {error}") from error
    try:
        opened = os.fstat(descriptor)
        opened_mode = f"{stat.S_IMODE(opened.st_mode):04o}"
        if not stat.S_ISREG(opened.st_mode) or opened_mode != expected_mode:
            raise BundleError("source plugin manifest changed while reading")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            return stream.read()
    finally:
        os.close(descriptor)


def require_clean_source(
    source_repo: Path, commit: str
) -> tuple[dict[str, dict[str, str]], dict[str, str], bytes]:
    changes = git(
        source_repo,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignored=matching",
        "--",
        "skills",
        ".codex-plugin/plugin.json",
    )
    if changes:
        raise BundleError(f"source inputs do not match HEAD:\n{changes}")

    expected_entries, expected_files = committed_skills(source_repo, commit)
    actual_entries, actual_files = snapshot(source_repo / "skills")
    if actual_entries != expected_entries or actual_files != expected_files:
        raise BundleError("source skills worktree does not match HEAD")

    manifest, manifest_mode = committed_plugin_manifest(source_repo, commit)
    actual_manifest = read_source_manifest(
        source_repo / ".codex-plugin/plugin.json", manifest_mode
    )
    if actual_manifest != manifest:
        raise BundleError("source plugin manifest does not match HEAD")
    if git(source_repo, "rev-parse", "HEAD") != commit:
        raise BundleError("source HEAD changed while building the lock")
    return expected_entries, expected_files, manifest


def build_lock(source_repo: Path) -> dict[str, object]:
    commit = git(source_repo, "rev-parse", "HEAD")
    entries, files, manifest_bytes = require_clean_source(source_repo, commit)
    manifest = json.loads(manifest_bytes)
    return {
        "schema_version": 2,
        "source_repository": str(source_repo.resolve()),
        "commit": commit,
        "skills_tree": git(source_repo, "rev-parse", f"{commit}:skills"),
        "plugin_version": manifest["version"],
        "files": files,
        "entries": entries,
    }


def validate_bundle(root: Path, lock: dict[str, object]) -> None:
    if lock.get("schema_version") != 2:
        raise BundleError("unsupported Kit bundle lock schema")
    entries, files = snapshot(root)
    if files != lock.get("files") or entries != lock.get("entries"):
        raise BundleError(f"{root} does not match its Kit bundle lock")


def validate_frozen_kit(lock: dict[str, object]) -> None:
    actual = {name: lock.get(name) for name in FROZEN_KIT}
    if actual != FROZEN_KIT:
        raise BundleError(
            "Kit bundle differs from frozen Kit 0.2.11 commit "
            "46af96a89de7b297e9dd4e9cfc2bf248e6d4698f"
        )


def write_lock_atomically(lock: dict[str, object]) -> None:
    contents = (json.dumps(lock, indent=2, sort_keys=True) + "\n").encode()
    descriptor, temporary = tempfile.mkstemp(
        prefix=f".{LOCK_PATH.name}.", suffix=".tmp", dir=LOCK_PATH.parent
    )
    try:
        os.fchmod(descriptor, 0o644)
        stream = os.fdopen(descriptor, "wb")
        descriptor = -1
        with stream:
            stream.write(contents)
            stream.flush()
            os.fsync(stream.fileno())
    except BaseException:
        if descriptor >= 0:
            try:
                os.close(descriptor)
            except OSError:
                pass
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise
    try:
        os.replace(temporary, LOCK_PATH)
    except BaseException:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--write-lock", action="store_true")
    parser.add_argument("--require-frozen", action="store_true")
    parser.add_argument(
        "--bundle",
        type=Path,
        default=BUNDLE,
        help="vendored skills bundle to validate (default: data/skills)",
    )
    parser.add_argument(
        "--lock",
        type=Path,
        default=LOCK_PATH,
        help=(
            "bundle lock to validate against "
            "(default: data/kit-skills.lock.json)"
        ),
    )
    args = parser.parse_args()
    try:
        if args.write_lock:
            if args.source is None:
                parser.error("--write-lock requires --source")
            source = args.source.resolve()
            lock = build_lock(source)
            validate_bundle(BUNDLE, lock)
            if build_lock(source) != lock:
                raise BundleError("source changed while finalizing the bundle lock")
            write_lock_atomically(lock)
            return
        lock = json.loads(args.lock.read_text())
        validate_bundle(args.bundle, lock)
        if args.require_frozen:
            validate_frozen_kit(lock)
        if args.source is not None and build_lock(args.source.resolve()) != lock:
            raise SystemExit("bundle lock does not match the source Kit repository")
    except BundleError as error:
        raise SystemExit(str(error)) from error


if __name__ == "__main__":
    main()
