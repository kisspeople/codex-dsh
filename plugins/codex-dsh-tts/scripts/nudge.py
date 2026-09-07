#!/usr/bin/env python3
"""Local, one-shot Windows TTS nudge for Codex DSH checkpoints."""

from __future__ import annotations

import argparse
import os
import secrets
import subprocess
import sys
import tempfile
import time
from pathlib import Path


STATE_DIR = Path(tempfile.gettempdir()) / "codex-dsh-tts"


def state_paths(reminder_id: str) -> tuple[Path, Path]:
    return STATE_DIR / f"{reminder_id}.pending", STATE_DIR / f"{reminder_id}.cancel"


def worker(reminder_id: str, message: str, delay: int) -> int:
    pending, cancel = state_paths(reminder_id)
    for _ in range(max(0, delay)):
        if cancel.exists():
            pending.unlink(missing_ok=True)
            cancel.unlink(missing_ok=True)
            return 0
        time.sleep(1)
    if cancel.exists():
        pending.unlink(missing_ok=True)
        cancel.unlink(missing_ok=True)
        return 0
    if os.name != "nt":
        print("TTS nudge is only supported on Windows.", file=sys.stderr)
        pending.unlink(missing_ok=True)
        return 2
    env = os.environ.copy()
    env["CODEX_DSH_TTS_MESSAGE"] = message
    command = (
        "$m=[Environment]::GetEnvironmentVariable('CODEX_DSH_TTS_MESSAGE');"
        "Add-Type -AssemblyName System.Speech;"
        "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer;"
        "$s.Speak($m);$s.Dispose()"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
        env=env,
        check=False,
    )
    pending.unlink(missing_ok=True)
    cancel.unlink(missing_ok=True)
    return result.returncode


def start(message: str, delay: int) -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    reminder_id = secrets.token_hex(8)
    pending, _ = state_paths(reminder_id)
    pending.touch()
    flags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0) | getattr(
        subprocess, "DETACHED_PROCESS", 0
    )
    subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "worker", reminder_id, message, str(delay)],
        creationflags=flags,
        close_fds=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print(reminder_id)
    return 0


def cancel(reminder_id: str) -> int:
    pending, cancel_path = state_paths(reminder_id)
    if not pending.exists() and not cancel_path.exists():
        print(f"No active reminder: {reminder_id}", file=sys.stderr)
        return 1
    cancel_path.parent.mkdir(parents=True, exist_ok=True)
    cancel_path.touch()
    print(f"cancelled {reminder_id}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    start_parser = sub.add_parser("start")
    start_parser.add_argument("--message", required=True)
    start_parser.add_argument("--delay-seconds", type=int, default=60)
    cancel_parser = sub.add_parser("cancel")
    cancel_parser.add_argument("--id", required=True)
    worker_parser = sub.add_parser("worker")
    worker_parser.add_argument("id")
    worker_parser.add_argument("message")
    worker_parser.add_argument("delay", type=int)
    args = parser.parse_args()
    if args.action == "start":
        return start(args.message, args.delay_seconds)
    if args.action == "cancel":
        return cancel(args.id)
    return worker(args.id, args.message, args.delay)


if __name__ == "__main__":
    raise SystemExit(main())
