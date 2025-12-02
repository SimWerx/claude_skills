# Claude Skills Factory Generator

> **This prompt has been restructured into a modular skill following progressive disclosure best practices.**

## New Location

The Skills Factory is now a proper skill at: **[skill-factory/](skill-factory/)**

## How to Use

### Option 1: Load the Skill Directory (Recommended)

Tell Claude to read the skill:

```
Load the skill-factory skill and help me create a new skill for [your use case].
```

Claude will read:
1. `skill-factory/SKILL.md` - Core instructions and overview
2. `skill-factory/references/generation-workflow.md` - Detailed generation steps (when needed)
3. `skill-factory/references/patterns.md` - Templates and patterns (when needed)
4. `skill-factory/references/quality-checklist.md` - Validation criteria (when needed)
5. `skill-factory/references/advanced.md` - Research, testing, customization (when needed)

### Option 2: Direct File Reference

Point Claude directly to the SKILL.md:

```
Read skill-factory/SKILL.md and use it to create a skill for [your use case].
```

## Why This Change?

The original monolithic prompt was ~1,300 lines. This made it:
- Hard to maintain
- Expensive in tokens
- Difficult for agents to process effectively

The new modular structure:
- **SKILL.md**: ~80 lines - Core instructions and navigation
- **references/**: ~600 lines total - Detailed content loaded only when needed

This follows the same progressive disclosure pattern the factory teaches:
1. Metadata always loaded (name + description)
2. SKILL.md loaded when skill triggers
3. References loaded only as needed

## Quick Reference

| File | Purpose | Lines |
|------|---------|-------|
| `skill-factory/SKILL.md` | Core instructions | ~80 |
| `skill-factory/references/generation-workflow.md` | Step-by-step process | ~180 |
| `skill-factory/references/patterns.md` | Templates, style | ~220 |
| `skill-factory/references/quality-checklist.md` | Validation criteria | ~130 |
| `skill-factory/references/advanced.md` | Research, testing | ~200 |
| `skill-factory/sample_prompt.md` | Test prompts | ~40 |

## Migration Notes

If you have workflows that reference this file directly, update them to use `skill-factory/SKILL.md` instead.

The functionality is identical; only the organization has changed.
