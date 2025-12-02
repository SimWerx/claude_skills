# Agent Instructions — evaluators/llm-judge/

## Read First

1. Read `PROMPT_SPECS.md` — canonical prompt structure, output schema, AND/OR logic patterns.
2. Reference existing `*_prompt.md` files as templates.

## Validation

Run after creating or editing prompts:

```bash
python3 tools/validate_prompt_structure.py                    # Required: check sections
python3 tools/flag_compound_logic.py                          # Recommended: AND/OR review
```

## Allowed Without Asking

- Read/list files, create/edit prompts following PROMPT_SPECS.md, run validation tools

## Require Approval First

- Delete prompts, modify PROMPT_SPECS.md structure, rename files (breaks benchmark refs)
