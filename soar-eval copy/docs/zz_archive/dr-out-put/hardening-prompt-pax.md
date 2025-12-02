# Clinical Hardening Prompt Pack

> **Purpose**: Delegate implementation of `hardening-action-list.md` to AI coding agents.
> Each prompt covers one priority tier. Execute in sequence.
>
> **Last updated**: 2025-11-29 — Aligned with current action list state.

---

## Specification Documents (Reference for All Prompts)

These documents define HOW to structure changes. The action list defines WHAT to change.

| Artifact Type | Specification | Key Rules |
|---------------|---------------|-----------|
| Benchmarks | `benchmarks/AGENTS.md`, `benchmarks/FIELD_SPECS.md` | `inclusion_criteria` format: "Apply when [TRIGGER]. Flag if [FAILURE]." |
| Rubrics | `rubrics/AGENTS.md`, `rubrics/FIELD_SPECS.md` | evaluation_guidelines structure, aggregation methods |
| LLM Prompts | `evaluators/llm-judge/AGENTS.md`, `evaluators/llm-judge/PROMPT_SPECS.md` | Canonical prompt structure, AND/OR logic in Automatic fail |

**Precedence model**: The nearest `AGENTS.md` to the file you're editing takes precedence.

---

## Prompt 1 — Critical Priority: Capacity Documentation

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

Before making any changes, read these specification documents:
1. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md` — Required fields and `inclusion_criteria` format
2. `zy_experimental/soar-pydantic-eval/benchmarks/AGENTS.md` — Benchmark-specific guidance
3. `zy_experimental/soar-pydantic-eval/evaluators/llm-judge/PROMPT_SPECS.md` — If editing any prompts

### Baseline Validation

Run before starting to confirm current state is clean:
```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement the remaining **Critical Priority** item:

- **Enforce explicit capacity documentation in refusals**
  - Tighten `A-REF1` to treat absence of a capacity statement (when narrative supports it) as a failure
  - Ensure `A-UNC2` marks capacity as a critical field that must be flagged `unknown` if truly unavailable
  - Files: `benchmarks/a-component/A-REF1.yaml`, `benchmarks/a-component/A-UNC2.yaml`

### Implementation Guidelines

- The **action list** tells you WHAT to implement
- The **FIELD_SPECS.md** tells you HOW to structure it
- When in doubt, match the style of existing compliant benchmarks (e.g., `A-FCT2.yaml`, `A-TMP5.yaml`)

### Constraints

- Do NOT introduce new clinical rules or external protocol logic
- Do NOT modify `AGENTS.md` files or repo structure
- Preserve existing `inclusion_criteria` two-part format: "Apply when... Flag if..."

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   python3 tools/validate_benchmark_criteria.py  # Verify criteria format
   ```
2. Mark the item as `[x]` in `hardening-action-list.md`
3. Summarize what you changed and any non-obvious decisions

---

## Prompt 2 — High Priority

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

Before making any changes, read these specification documents:
1. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md` — Required fields and formats
2. `zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md` — Rubric structure
3. `zy_experimental/soar-pydantic-eval/evaluators/llm-judge/PROMPT_SPECS.md` — Prompt structure (critical for AND/OR logic)

### Baseline Validation

```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement **all unchecked High Priority items**:

1. **Restraint/sedation documentation details (RASS + de-escalation)**
   - Update `A-BHV1` to explicitly mention capturing RASS and de-escalation efforts if present in narrative
   - Update associated LLM prompt if needed
   - Files: `benchmarks/a-component/A-BHV1.yaml`, `evaluators/llm-judge/restraint_sedation_prompt.md`

2. **Twin / multi-newborn delivery handling**
   - Confirm `A-OBS1` examples and criteria explicitly require separate documentation for each baby
   - Files: `benchmarks/a-component/A-OBS1.yaml`

3. **Medication contraindication override rationale**
   - Refine `A-SFT2` acceptable-deviation criteria to permit contraindicated administration if override rationale is present
   - Files: `benchmarks/a-component/A-SFT2.yaml`, associated prompt

### Implementation Guidelines

- The **action list** tells you WHAT to implement
- The **FIELD_SPECS.md** files tell you HOW to structure it
- For prompts: Follow the canonical structure in `PROMPT_SPECS.md`, especially the AND/OR logic rules in "Automatic fail" sections

### Constraints

- Do NOT add new clinical rules or protocol steps
- Do NOT modify `AGENTS.md` files
- When editing prompts, ensure "Automatic fail" conditions use correct AND vs OR logic per `PROMPT_SPECS.md`

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   python3 tools/validate_benchmark_criteria.py  # if you edited benchmarks
   python3 tools/validate_prompt_structure.py    # if you edited prompts
   ```
2. Mark each item as `[x]` in `hardening-action-list.md`
3. Summarize which items you completed and note any unresolved questions

---

## Prompt 3 — Medium Priority

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

Before making any changes, read these specification documents:
1. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md`
2. `zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md`

### Baseline Validation

```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement **all unchecked Medium Priority items**:

1. **Pediatric documentation clarifications (A-PED / A-OBS interplay)**
   - Clarify division of responsibility between pediatric and OB rubrics
   - Add Broselow tape example to `A-PED2`
   - Files: `rubrics/A-PED.yaml`, `benchmarks/a-component/A-PED2.yaml`, `benchmarks/a-component/A-OBS1.yaml`

2. **Sepsis/shock protocol documentation**
   - Decide whether to extend existing rubrics or introduce focused benchmark
   - Only implement if synthetic scenarios include sepsis/shock cases
   - Files: Candidate new benchmark if warranted

3. **Trauma assessment thoroughness**
   - Add LLM-judge guidance under `A-TRM1` to check all named injuries are reflected
   - Files: `benchmarks/a-component/A-TRM1.yaml`, associated prompt

4. **Refusal high-risk scenario coverage**
   - Add or adapt an `A-REF` test case for post-intervention refusal (post-naloxone, post-hypoglycemia)
   - Files: `benchmarks/a-component/A-REF1.yaml`–`A-REF3.yaml`

### Implementation Guidelines

- The **action list** tells you WHAT to implement
- The **FIELD_SPECS.md** files tell you HOW to structure it
- Match existing benchmark style and formatting

### Constraints

- Do NOT introduce new clinical rules or web-sourced protocol content
- Do NOT modify `AGENTS.md` files
- Keep edits within files explicitly named in the action list

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   python3 tools/validate_benchmark_criteria.py  # Verify criteria format
   ```
2. Mark each item as `[x]` in `hardening-action-list.md`
3. Summarize key changes made

---

## Prompt 4 — Low Priority + Future Work

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

1. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md`

### Baseline Validation

```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement **all unchecked Low Priority items**:

1. **NKDA and allergy niceties**
   - Clarify in `A-ALL1` acceptable deviations how NKDA should be represented
   - Consider soft LLM-judge note rather than hard failure
   - Files: `benchmarks/a-component/A-ALL1.yaml`

2. **Other future enhancements**
   - Record candidate future checks in `WORKING.md` (do not build new systems)
   - Items to record: OCR robustness, spelling/abbreviation consistency, timeline plausibility, demographic mismatch flags

### Constraints

- For Low Priority: Document ideas, don't build systems
- Do NOT introduce new clinical rules
- Keep edits minimal and documentation-focused

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   ```
2. Mark each item as `[x]` in `hardening-action-list.md`
3. Brief summary of what was documented

---

## Prompt 5 — Threshold Adjustments

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

1. `zy_experimental/soar-pydantic-eval/rubrics/FIELD_SPECS.md` — Understand `passing_threshold` field
2. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md` — Understand `threshold` field

### Baseline Validation

```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement the **Threshold adjustments** item:

| File | Field | Current | Target |
|------|-------|---------|--------|
| `rubrics/A-NEG.yaml` | `passing_threshold` | 0.85 | 0.90 |
| `benchmarks/a-component/A-REF2.yaml` | `threshold` | 0.85 | 0.95 |
| `benchmarks/a-component/A-SFT4.yaml` | `threshold` | 0.90 | 1.0 |
| `rubrics/A-CMP.yaml` | `passing_threshold` | 0.80 | 0.85 |

### Constraints

- Make minimal edits — only change the numeric threshold values
- Preserve all existing comments and structure
- Do NOT change benchmark semantics beyond the threshold

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   ```
2. Mark "Threshold adjustments" as `[x]` in `hardening-action-list.md`
3. List which thresholds you changed

---

## Prompt 6 — Example-Quality Clarifications

You are an AI coding agent working in the `synthetic-data-gen` repo.

### Read First

Before making any changes, read these specification documents:
1. `zy_experimental/soar-pydantic-eval/benchmarks/FIELD_SPECS.md` — Example format requirements
2. Review at least 2 existing compliant benchmarks (e.g., `A-FCT2.yaml`, `A-NEG1.yaml`) for style reference

### Baseline Validation

```bash
cd zy_experimental/soar-pydantic-eval && python3 tools/validate_consistency.py
```

### Your Task

Open `docs/backlog/hardening-action-list.md` and implement the **Example-quality and criteria clarifications** item.

Add or refine examples in these benchmarks (guidance in action list):

| Category | Benchmarks | Key Additions |
|----------|------------|---------------|
| Negation, evidence & impressions | A-NEG3, A-EVD1, A-EVD3, A-FCT4 | Partial denial, contradictory evidence spans |
| Temporal, completeness & arrest | A-TMP1, A-CMP1, A-CMP5, A-CAR1 | Protocol ordering, DOA nuances, ROSC/termination time |
| Refusal & stroke | A-REF1, A-REF3, A-STR1, A-STR2 | Risk+capacity joint examples, LKW unknown handling |
| Trauma & OB | A-TRM2, A-TRM3, A-OBS1, A-OBS2 | Pelvic binder, cricothyrotomy, twin deliveries, EBL |
| Behavioral & uncertainty | A-BHV1, A-BHV2, A-UNC2 | RASS/de-escalation, implied consent, positive "unknown" example |

### Implementation Guidelines

- Derive examples from patterns already present in the benchmark OR from suggested text in the action list
- Do NOT invent new clinical scenarios beyond what the action list implies
- Maintain YAML formatting conventions (see existing `examples:` blocks)

### Constraints

- Keep all logic consistent with existing rubrics/benchmarks
- Do NOT add new protocol rules or categories
- Do NOT modify benchmark semantics — only enhance examples

### Validation & Completion

1. Run validation:
   ```bash
   python3 tools/validate_consistency.py
   python3 tools/validate_benchmark_criteria.py  # Verify criteria format preserved
   ```
2. Mark "Example-quality and criteria clarifications" as `[x]` in `hardening-action-list.md`
3. Provide rubric-by-rubric summary of which benchmarks had examples updated
