#!/usr/bin/env python3
"""Upload a local tree to Google My Drive using the official `gws` CLI.

Prerequisites:
  1. Install Google Workspace CLI: https://github.com/googleworkspace/cli
  2. Authenticate (browser):  gws auth login -s drive

Default safety: skips `.git`, `secret_keys`, `__pycache__`, `.venv`, `node_modules`.

Usage:
  python3 scripts/upload_to_google_drive.py
  python3 scripts/upload_to_google_drive.py --local-root /path/to/book --remote-name my-backup
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


DEFAULT_EXCLUDE_DIRS = frozenset(
    {
        ".git",
        "secret_keys",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
    }
)


def skip_file_name(filename: str) -> bool:
    """Skip junk / alternate-data-stream artifacts often seen under WSL."""
    if filename.startswith(".DS_Store"):
        return True
    if ":Zone.Identifier" in filename or filename.endswith(":Zone.Identifier"):
        return True
    if ":RVContext" in filename:
        return True
    return False


def run_json(cmd: list[str]) -> dict:
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(
            f"Command failed ({p.returncode}): {' '.join(cmd)}\n"
            f"{p.stderr.strip() or p.stdout.strip()}"
        )
    return json.loads(p.stdout)


def check_gws_auth() -> None:
    p = subprocess.run(
        ["gws", "drive", "files", "list", "--params", '{"pageSize":1}'],
        capture_output=True,
        text=True,
    )
    if p.returncode == 2:
        sys.stderr.write(
            "Google Drive 인증이 없습니다. 먼저 터미널에서 다음을 실행하세요:\n"
            "  gws auth login -s drive\n"
        )
        sys.exit(2)
    if p.returncode != 0:
        sys.stderr.write(p.stderr or p.stdout)
        sys.exit(p.returncode or 1)


def create_remote_folder(name: str, parent_id: str | None) -> str:
    body: dict = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
    if parent_id:
        body["parents"] = [parent_id]
    out = run_json(
        ["gws", "drive", "files", "create", "--json", json.dumps(body)]
    )
    if "id" not in out:
        raise RuntimeError(f"Unexpected files.create response: {out!r}")
    return str(out["id"])


def upload_file(local: Path, parent_id: str, remote_name: str) -> str:
    cmd = [
        "gws",
        "drive",
        "+upload",
        str(local),
        "--parent",
        parent_id,
        "--name",
        remote_name,
    ]
    out = run_json(cmd)
    if "id" not in out:
        raise RuntimeError(f"Unexpected +upload response: {out!r}")
    return str(out["id"])


def collect_dirs_and_files(
    root: Path, exclude_dirs: frozenset[str]
) -> tuple[list[str], list[tuple[str, str]]]:
    """Returns (relative_dir_paths using '/', relative file paths as posix)."""
    dir_set: set[str] = {""}

    rel_files: list[tuple[str, str]] = []
    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        dirnames[:] = sorted(d for d in dirnames if d not in exclude_dirs)
        rel_dir = os.path.relpath(dirpath, root)
        if rel_dir == ".":
            rel_dir_key = ""
        else:
            rel_dir_key = Path(rel_dir).as_posix()
            dir_set.add(rel_dir_key)
        for fn in sorted(filenames):
            if skip_file_name(fn):
                continue
            p = Path(dirpath) / fn
            if p.is_file():
                rel_file = Path(rel_dir_key) / fn if rel_dir_key else Path(fn)
                rel_files.append((rel_dir_key, rel_file.as_posix()))

    def depth(s: str) -> int:
        return 0 if not s else s.count("/") + 1

    ordered_dirs = sorted(dir_set, key=lambda s: (depth(s), s))
    return ordered_dirs, rel_files


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--local-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Local directory to upload (default: repo root)",
    )
    ap.add_argument(
        "--remote-name",
        default="harness-engineering-book",
        help="Top-level folder name on My Drive",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="List folders/files only; no API calls",
    )
    args = ap.parse_args()

    local_root: Path = args.local_root.resolve()
    if not local_root.is_dir():
        sys.stderr.write(f"Not a directory: {local_root}\n")
        sys.exit(3)

    ordered_dirs, rel_files = collect_dirs_and_files(local_root, DEFAULT_EXCLUDE_DIRS)

    if args.dry_run:
        print(f"[dry-run] local_root={local_root}")
        print(f"[dry-run] remote folder name={args.remote_name!r}")
        print(f"[dry-run] dirs (relative, {len(ordered_dirs)}):")
        for d in ordered_dirs:
            print(f"  {d or '.'}")
        print(f"[dry-run] files ({len(rel_files)}):")
        for _, rf in rel_files[:50]:
            print(f"  {rf}")
        if len(rel_files) > 50:
            print(f"  ... +{len(rel_files) - 50} more")
        return

    check_gws_auth()

    print(f"Creating top folder {args.remote_name!r} on My Drive...")
    root_id = create_remote_folder(args.remote_name, parent_id=None)
    path_ids: dict[str, str] = {"": root_id}

    for rel in ordered_dirs:
        if rel == "":
            continue
        parent_rel, name = rel.rsplit("/", 1) if "/" in rel else ("", rel)
        parent_id = path_ids[parent_rel]
        print(f"  mkdir Drive:{rel!r}")
        path_ids[rel] = create_remote_folder(name, parent_id)

    print(f"Uploading {len(rel_files)} files...")
    for i, (parent_rel, rel_file) in enumerate(rel_files, 1):
        parent_id = path_ids[parent_rel]
        local_path = local_root / rel_file
        name = Path(rel_file).name
        print(f"  [{i}/{len(rel_files)}] {rel_file}")
        upload_file(local_path, parent_id, name)

    print("Done.")
    print(f"Root folder id: {root_id}")
    print(f"Open: https://drive.google.com/drive/folders/{root_id}")


if __name__ == "__main__":
    main()
