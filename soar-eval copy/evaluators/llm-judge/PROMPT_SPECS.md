# LLM-as-a-Judge Prompt Specifications

This folder contains prompts for LLM-based evaluation. For human labeling guidance, see `docs/labeling_guide.md`.

Prompt files live in this directory. See `AGENTS.md` for the current inventory.

For the full research basis and Pydantic Evals integration patterns, see `docs/lag-boolean-prompt-spec.md`.

---

## Scope Boundary (applies to all LLM-as-a-judge prompts)

LLM judges evaluate **Medic Copilot's output against ground truth labels**. They do NOT:
- Compute clinical correctness (dose appropriateness, protocol compliance)
- Embed clinical knowledge (dose ranges, contraindication rules)
- Make clinical judgments (those belong in S-component SME review)

LLM judges answer: **"Did Medic Copilot's output match what ground truth expected?"**

**Example**:
- Correct: "Ground truth marks this as a negation error; does output show the error?"
- Wrong: "Is this dose clinically appropriate?" (clinical judgment belongs in Medic Copilot)

For system logic benchmarks (A-SFT, A-PRT, A-PED), LLM judges check whether Medic Copilot's inference-time logic fired correctly on known test cases—they don't evaluate clinical correctness themselves.

---

## Core Design Principles

1. **Single behavior per judge** — Each judge answers exactly one yes/no question. If multiple aspects need evaluation, define separate judges.

2. **Binary verdict** — The canonical outcome is a boolean `pass`. A numeric `score` (1.0 if pass, 0.0 if fail) is optional for reporting.

3. **Rubric-first, criteria as numbered list** — Write a short behavior description followed by numbered pass conditions. The list uses strict AND logic: all conditions must be satisfied to pass.

4. **Explicit pass/fail logic** — Always state how criteria map to the final boolean:
   - "Set `pass = true` only if all conditions 1–N hold."
   - "Otherwise set `pass = false`."

5. **Explicit edge cases** — Capture "automatic fail" triggers and "acceptable variations" in separate sections to avoid clutter in pass conditions.

6. **Grounded evaluation only** — Judges base decisions solely on supplied ground truth, source narrative, and candidate output. No external knowledge to fill gaps.

7. **Reason-before-verdict** — Judges identify evidence and reasons before finalizing the verdict. Captured in a short `reason` field.

8. **Strict structured output** — Return a small, fixed JSON object. No extra text, headings, or markdown.

9. **Deterministic inference** — Use temperature=0 and fixed system prompt to minimize variance.

10. **Alignment by example** — For difficult behaviors, add 1-2 few-shot examples (clear pass, clear fail) in the prompt.

---

## Canonical Prompt Structure

Each prompt file follows this structure:

```markdown
SYSTEM: You are a neutral medical documentation evaluator.
You evaluate one behavior at a time.
Your job is to decide whether a single evaluation behavior is satisfied, using the rubric provided.
Be strict and literal about the rubric.
If you cannot tell from the evidence whether all conditions are met, treat the behavior as NOT satisfied.

Use only the information in the provided inputs.
Do not invent clinical details or use outside knowledge to fill gaps.

Respond only with a single JSON object. Do not include any text before or after the JSON.

---

BEHAVIOR: {behavior_id}

DESCRIPTION:
{One-sentence description of what is being evaluated}

EVALUATION SCOPE:
Include:
- {What to examine}
- {Relevant data elements}
Ignore:
- {What to exclude from evaluation}
- {Formatting-only differences}

RUBRIC

Automatic fail if any of the following are true:
- {Failure trigger 1}
- {Failure trigger 2}

Pass conditions (all must be satisfied):
1. {Condition 1}
2. {Condition 2}
3. {Condition 3}

Acceptable variations (still treated as pass):
- {Acceptable deviation 1}
- {Acceptable deviation 2}

Uncertainty policy:
If the information is ambiguous or incomplete, set pass = false and explain that the case is uncertain in the reason.

---

INPUTS

GROUND_TRUTH:
{Rendered ground truth for this case}

SOURCE_NARRATIVE:
{Rendered clinical note or transcript}

CANDIDATE_OUTPUT:
{Rendered Medic Copilot output for this case}
```

---

## Output Schema

All prompts return compact JSON with these fields:

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `pass` | boolean | `true` if behavior is satisfied under the rubric; `false` otherwise (including "cannot determine" cases) |
| `reason` | string | 50-200 characters referencing key evidence for the decision |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `score` | number | Default: 1.0 if pass, 0.0 if fail. Can extend to discrete scale if needed. |
| `confidence` | string | One of `"high"`, `"medium"`, `"low"`. Use `"low"` when judge cannot decide cleanly. |
| `uncertain` | boolean | `true` if case is ambiguous. Still implies `pass = false` but can route to human review. |

### Example Output

```json
{"pass": true, "reason": "All ground-truth meds present with correct dose/route; no extra meds.", "score": 1.0}
```

### Behavior-Specific Keys

For legacy compatibility or dashboard clarity, behavior-specific keys (e.g., `medications_extracted_correct`) can map from `pass` at the aggregation/logging layer:

```python
result.medications_extracted_correct = judge_output.pass
```

---

## Rubric Section Reference

### Automatic Fail

Lists conditions that immediately fail the evaluation regardless of other factors.

**Format**: Bullet list of failure triggers using OR logic ("any of the following").

**Critical: AND vs OR Logic**

The header "any of the following are true" means bullets use **OR logic** — any single bullet triggers failure. When the original behavior requires multiple conditions to ALL be true (AND logic), express them as a **single bullet with explicit AND**:

```markdown
# WRONG - OR logic (any single condition fails independently)
Automatic fail if any of the following are true:
- Field is blank/null in the output.
- Narrative does not contain this information.
- Output provides no acknowledgment of the gap.

# CORRECT - AND logic (all three must be true together to fail)
Automatic fail if any of the following are true:
- Field is blank/null AND narrative lacks information AND output provides no acknowledgment.
```

Use `tools/flag_compound_logic.py` to identify prompts that may have incorrectly split AND conditions.

**Example** (independent failure modes, OR is correct):
```
Automatic fail if any of the following are true:
- Any administered medication in the ground truth is missing from the AI output.
- A medication in the AI output has a clearly incorrect dose (wrong magnitude or units).
- The AI output adds a medication that does not appear in either the ground truth or narrative.
```

### Pass Conditions

Lists criteria that must ALL be satisfied for the behavior to pass. Uses strict AND logic.

**Format**: Numbered list (1. 2. 3.)

**Example**:
```
Pass conditions (all must be satisfied):
1. Every administered medication in the ground truth appears in the AI output.
2. For each medication, name, dose, and route match ground truth, allowing minor spelling differences.
3. No extra medications are present beyond those supported by ground truth or narrative.
```

### Acceptable Variations

Lists deviations that should NOT be penalized. Keeps pass conditions focused on substance.

**Format**: Bullet list.

**Example**:
```
Acceptable variations (still treated as pass):
- Brand vs generic names for the same active ingredient.
- Abbreviations such as ASA/aspirin, NTG/nitroglycerin, NS/normal saline.
- Differences in ordering or formatting.
```

### Uncertainty Policy

Standard language for handling ambiguous cases.

**Format**: Prose statement.

**Standard text**:
```
Uncertainty policy:
If the information is ambiguous or incomplete, set pass = false and explain that the case is uncertain in the reason.
```

---

## Naming Convention

Prompt files follow the pattern `{concept}_prompt.md` and map to benchmarks via the `llm_prompt_file` field in each benchmark YAML.

---

## Creating New Prompts

When adding a prompt for a new benchmark:

1. **Name the file** descriptively: `{concept}_prompt.md`
2. **Follow the canonical structure** above exactly
3. **Single behavior only** — one prompt evaluates one thing
4. **Include all rubric sections** — Automatic fail, Pass conditions, Acceptable variations, Uncertainty policy
5. **Define evaluation scope** — Explicit Include/Ignore lists
6. **Update the benchmark** — add `llm_prompt_file` field pointing to the new prompt
7. **Test with examples** — verify pass/fail cases before committing

---

## Relationship to Benchmarks

Benchmarks with `evaluator_type: llm_judge` or `hybrid` include an `llm_prompt_file` field:

```yaml
# In benchmarks/a-component/A-NEG1.yaml
evaluator_type: hybrid
llm_prompt_file: "evaluators/llm-judge/negation_simple_prompt.md"
```

The prompt is invoked by Pydantic Evals' `LLMJudge` evaluator with the trace as context.

### Mapping Benchmark Fields to Prompt Sections

| Benchmark YAML Field | Prompt Section |
|---------------------|----------------|
| `concept` | DESCRIPTION |
| `inclusion_criteria` ("Flag if...") | Automatic fail + Pass conditions |
| `exclusion_criteria` | Acceptable variations |
| `examples` | Few-shot examples (if needed) |

---

## Pydantic Evals Integration

When using Pydantic Evals, the `LLMJudge` `rubric` string contains the behavior-specific sections (everything except SYSTEM and INPUTS).

```python
from pydantic_evals.evaluators import LLMJudge

MEDS_EXTRACTED_RUBRIC = """
Behavior: medications_extracted_correct

Goal:
Check whether the AI output correctly extracts all active medications
administered during the encounter.

Automatic fail if:
- Any administered medication in the ground truth is missing from the AI output.
- A medication in the AI output has a clearly incorrect dose.
- The AI output adds a medication not in ground truth or narrative.

Pass conditions (all must hold):
1. Every administered medication in ground truth appears in AI output.
2. For each medication, name, dose, and route match ground truth.
3. No extra medications beyond those in ground truth or narrative.

Acceptable variations:
- Brand vs generic names for the same active ingredient.
- Common abbreviations (ASA for aspirin, NTG for nitroglycerin).
- Formatting differences such as order or line breaks.

Uncertainty policy:
If you cannot determine whether all conditions are met, set pass = false
and explain briefly why the case is uncertain.
"""

meds_judge = LLMJudge(
    rubric=MEDS_EXTRACTED_RUBRIC,
    include_input=True,
    include_expected_output=True,
    assertion={"evaluation_name": "medications_extracted_correct"},
)
```

---

## Migration Note

Some existing prompts in this directory may not follow the full canonical structure. When updating prompts:

1. Add missing sections (Automatic fail, Acceptable variations, Uncertainty policy)
2. Convert "Focus on:" bullets to formal "EVALUATION SCOPE: Include/Ignore"
3. Convert "(Note:...)" clauses to "Acceptable variations" section
4. Ensure output uses `pass`/`reason` schema (or document mapping to behavior-specific keys)

---

## Related Documentation

- **Full research basis**: `docs/lag-boolean-prompt-spec.md`
- **Human labeling guide**: `docs/labeling_guide.md`
- **Benchmark field specs**: `benchmarks/FIELD_SPECS.md`
- **Evaluator type definitions**: `benchmarks/FIELD_SPECS.md` → Evaluator Types table
