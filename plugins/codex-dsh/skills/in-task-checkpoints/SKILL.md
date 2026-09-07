---
name: in-task-checkpoints
description: Keep the user involved with concise decision questions throughout execution, not only during planning.
---

# In-task checkpoints

Use this behavior whenever the task has meaningful choices, incomplete requirements, or a risk of rework.

## Core behavior

1. Work until you reach the next decision that would materially change the result. Do not ask about routine implementation details.
2. Ask a short, concrete question in the user-facing channel. State the decision, the recommended default, and the consequence of each option. Prefer one question at a time.
3. Ask during implementation, debugging, review, and verification as well as before coding. A checkpoint is not restricted to plan mode.
4. If the user has already given a clear preference, record it mentally and continue without re-asking.
5. When no decision is needed, continue autonomously and report the outcome at the next natural milestone.

## Good checkpoints

- A requirement has two plausible interpretations.
- A change could be broad or narrowly scoped.
- A destructive, externally visible, or hard-to-reverse action is next.
- Tests expose a product choice rather than a purely technical bug.
- The implementation is complete enough that a quick direction check prevents rework.

## Question format

Use plain language and keep the prompt answerable in one sentence. Example:

> I found two valid directions: keep the API backward-compatible (recommended), or remove the old field. Which should I ship?

If the runtime offers a structured user-input tool, use it for optional choices; otherwise ask naturally in chat and pause. Never fabricate a user answer. If the user does not answer, preserve the current state and explain what is waiting.

## Guardrails

- Do not interrupt for formatting, naming, or other low-impact preferences.
- Do not turn every progress update into a question.
- Do not claim that a checkpoint is a system-enforced pause; it is an interaction convention.
- Continue with safe, reversible work while a non-blocking question is pending, but stop before committing to the ambiguous branch.
