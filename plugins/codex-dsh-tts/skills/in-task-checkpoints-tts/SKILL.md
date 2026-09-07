---
name: in-task-checkpoints-tts
description: Ask focused decision questions during execution and optionally play a local Windows TTS reminder after 60 seconds without a response.
---

# In-task checkpoints with TTS

Apply the checkpoint behavior below throughout implementation, debugging, review, and verification—not only in plan mode.

## Checkpoint behavior

1. Ask only when an unanswered choice can materially change scope, behavior, safety, or rework.
2. State the recommended default and the consequence of the alternatives. Ask one concise question.
3. If the user answers, cancel the reminder immediately and continue using that answer.
4. If the user does not answer, leave the work paused at the decision boundary and let the reminder play once. Do not guess a preference.

## Starting a reminder

After asking a question that genuinely blocks progress, start the helper in the background from this plugin's `scripts` directory:

```powershell
python .\nudge.py start --message "Codex is waiting for your direction." --delay-seconds 60
```

The command prints a reminder id. Keep that id in the current task context. On any user response, cancel it:

```powershell
python .\nudge.py cancel --id <reminder-id>
```

The helper is Windows-first and uses the built-in `System.Speech` voice, so it needs no cloud service or API key. It is optional: if Python, PowerShell, or speech synthesis is unavailable, continue with the normal text checkpoint and mention the limitation once.

## Safety and etiquette

- Never use TTS for routine updates or more than once for the same unanswered question.
- Keep spoken text short, neutral, and non-sensitive; do not read source code, secrets, or private content aloud.
- Do not claim that audio proves the user heard the reminder.
- If the user asks to stop reminders, cancel all active ids and do not start new ones for the rest of the task.
