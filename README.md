# Codex DSH

Two small Codex plugins for keeping the human in the loop while work is underway:

- **codex-dsh** — adds decision checkpoints during implementation, debugging, review, and verification. It asks focused questions when direction is genuinely ambiguous, instead of limiting interaction to plan mode.
- **codex-dsh-tts** — the same behavior plus an optional local Windows reminder. If a blocking question remains unanswered for 60 seconds, `scripts/nudge.py` uses the built-in `System.Speech` voice once; a response cancels it.

## Install from this repository

The repository includes a repo-local marketplace at `.agents/plugins/marketplace.json`. From a cloned checkout, install the marketplace with:

```text
codex plugin marketplace add .
```

Then install either `codex-dsh` or `codex-dsh-tts` from the Codex plugin UI/CLI.

## TTS notes

TTS is intentionally local and Windows-first. It does not send text to a service or require credentials. The helper prints a reminder id when started; cancel it as soon as the user answers:

```powershell
python .\plugins\codex-dsh-tts\scripts\nudge.py start --message "Codex is waiting for your direction." --delay-seconds 60
python .\plugins\codex-dsh-tts\scripts\nudge.py cancel --id <id>
```

If speech synthesis is unavailable, the normal text checkpoint still works.

## License

MIT. See [LICENSE](LICENSE).
