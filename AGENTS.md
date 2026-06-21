# AGENTS Instructions for unit-x

## MUST READ

Before participating in unit-x team work, read:
- `docs/team-protocol.md`
- `.claude/skills/sc-git-worktree/SKILL.md`

The messaging protocol in that document is mandatory for all team
communications.

All implementation work must be done in a git worktree created via
`.claude/skills/sc-git-worktree/SKILL.md`. Do not do development work
directly on the `develop` branch.

## Quick Rule

Always follow this sequence for every team message:
1. Immediate acknowledgement
2. Do the work
3. Completion summary
4. Immediate completion acknowledgement by receiver

No silent processing.

## Rust Guidance

For Rust design and review work, also read:
- `.claude/skills/rust-best-practices/SKILL.md`

Use it as the baseline for state machines, newtypes, sealed traits, structured
error design, and crate-boundary review.
