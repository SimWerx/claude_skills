# Human Labeling Guide

## Purpose

This guide explains how to label Medic Copilot traces with **benchmark codes** so that
the evaluation harness can score the system consistently across datasets and experiments.

You do **not** need to understand the evaluator plumbing; focus only on choosing
the best failure mode (or "none of the above") for each trace.

## What you are labeling

Each labeled item is one **trace** - a single interaction flow including:

- Inputs (ASR text, scenario metadata, optional link to ground-truth corpus case).
- Outputs (assistant narrative, DRAATT JSON, evidence map, tool calls).

Your job: for each trace, decide **which ONE benchmark code best describes the most
important failure**, if any.

## Labeling rules

1. **One primary code per trace**
   - Pick the *single* benchmark code that best captures the main failure.
   - If multiple issues are present, choose the one that is:
     - Most safety-critical, OR
     - Most central to the current eval focus (e.g., if we are currently hardening
       negation, prefer a negation code over a minor completeness nit).

2. **Use `NONE_OF_THE_ABOVE` sparingly**
   - Use this only when:
     - The trace clearly has a **real** problem, AND
     - No existing axial code fits reasonably well.
   - When you use it, leave a short free-text note for follow-up so we can decide
     whether to add a new code.

3. **Prefer more specific codes over generic ones**
   - Example: In a STEMI case with both a missing aspirin and a generic
     "treatment documentation thinness," prefer `A-PRT2` (STEMI care incomplete) over
     `A-CMP6` (Transport/handoff incomplete).

4. **Respect inclusion / exclusion criteria**
   - Always read the `inclusion_criteria` and `exclusion_criteria` for a code in
     `benchmarks/a-component/` before using it.
   - If you are unsure between two codes, check whether one explicitly excludes
     cases like the trace you are labeling.

5. **Do not label "success only" traces**
   - If a trace looks clean and you cannot find a clear failure, do **not** force
     a failure code. Leave it unlabeled or explicitly mark it as "no failure".

## Minimal annotation schema

For each labeled trace, capture at least:

- `trace_id`: unique identifier for the trace.
- `benchmark_code`: one of the codes from `benchmarks/a-component/` (or `NONE_OF_THE_ABOVE`).
- `severity` (optional but recommended): `low`, `medium`, or `high`.
- `note` (optional): 1-2 short sentences explaining your choice, especially for
  `NONE_OF_THE_ABOVE` or borderline calls.

Example (YAML):

```yaml
trace_id: "stemi-001"
benchmark_code: A-PRT2
severity: high
note: "Clear inferior STEMI with no aspirin documented and no STEMI alert/cath lab activation."
```

## Quick mental checklist per trace

When you review a trace, ask:

1. **Is the structured output parseable and complete?**
   - Format issues → `A-FMT` rubric
   - Missing sections → `A-CMP` rubric

2. **Is this a specialty scenario?**
   - DOA/pronouncement → `A-CMP5`
   - RSI/intubation → `A-PRT1`
   - Airport transfer → `A-CMP6-airport`
   - Cardiac arrest → `A-CAR` rubric
   - Pediatric → `A-PED` rubric
   - Stroke → `A-STR` rubric
   - Trauma → `A-TRM` rubric
   - Obstetric/neonatal → `A-OBS` rubric
   - Behavioral/restraint → `A-BHV` rubric
   - Refusal → `A-REF` rubric

3. **Is there a safety or protocol issue?**
   - Dose/route errors → `A-SFT` rubric
   - Protocol gaps → `A-PRT` rubric

4. **Are there semantic or extraction problems?**
   - Negation handling → `A-NEG` rubric
   - Temporal ordering → `A-TMP` rubric
   - Fact extraction → `A-FCT` rubric
   - Evidence attribution → `A-EVD` rubric

5. **If none of the above clearly applies**
   - And there is still a meaningful failure: use `NONE_OF_THE_ABOVE` with a
     short note so we can refine the taxonomy later.

**Note**: For specific benchmark codes within each rubric, see `benchmarks/a-component/`.

## Where to look things up

- Full benchmark definitions: `benchmarks/a-component/`
- Parent rubric definitions: `rubrics/`
- LLM-as-a-judge prompts: `evaluators/llm-judge/`
- SOAR framework context: `zy_experimental/soar-framework/soar-overview.md`

