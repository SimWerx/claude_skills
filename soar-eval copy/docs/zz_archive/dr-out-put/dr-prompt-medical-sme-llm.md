# Deep Research Prompt: Medical SME Review of SOAR Evaluation Framework

## Context for the Research Agent

You have access to the full `synthetic-data-gen` repository. Focus your analysis on `zy_experimental/soar-pydantic-eval/`, which defines evaluation criteria for **Medic Copilot** — an AI system that converts messy EMS speech-to-text transcriptions into structured clinical documentation (DRAATT format).

### What is Medic Copilot?

Medic Copilot is a **retrospective documentation AI** for Emergency Medical Services (EMS). It:
- Receives raw ASR (Automatic Speech Recognition) output from paramedic dictation
- Extracts structured clinical data into DRAATT JSON format
- Supports QA review, billing, and hospital handoff

**Critical distinction**: This is NOT real-time clinical decision support. It documents what already happened. Errors impact downstream care continuity, billing accuracy, and medicolegal records.

### What is DRAATT?

DRAATT is the structured documentation format:
- **D**ispatch — Chief complaint, response type, scene info
- **R**esponse — Unit response, crew, delays
- **A**rrival — Scene findings, patient presentation
- **A**ssessment — Physical exam, vitals, clinical impression
- **T**reatment — Interventions, medications, procedures
- **T**ransport — Destination, handoff, condition on arrival

### The Evaluation Framework

The `soar-pydantic-eval/` folder contains:
- **Rubrics** (`rubrics/*.yaml`) — Evaluation categories (Negation, Fact Extraction, Safety, etc.)
- **Benchmarks** (`benchmarks/a-component/*.yaml`) — Specific failure modes to detect
- **LLM Prompts** (`evaluators/llm-judge/*.md`) — For subjective evaluations

See `docs/corpus-validator-mapping.md` for how these map to existing corpus validators.

---

## Research Questions

### 1. Clinical Accuracy of Current Benchmarks

Review each benchmark in `benchmarks/a-component/*.yaml` and assess:

- **A-NEG (Negation Handling)**: Are the negation patterns clinically comprehensive? What EMS-specific negation phrases are missing? (e.g., "pt AOx4 but confused" — is "but" a negation risk?)

- **A-FCT (Fact Extraction)**: Are the vital sign ranges and medication extraction criteria clinically appropriate for EMS? What about pediatric vs adult distinctions?

- **A-SFT (Safety Flags)**: Are the contraindication and dose safety rules medically sound? What common EMS medication errors are NOT covered?

- **A-PRT (Protocol Tracking)**: Do RSI and STEMI protocol checks align with current NAEMSP/AHA guidelines? What protocol-critical steps are missing?

- **A-CMP (Completeness)**: Are the DOA pronouncement fields (`A-CMP5`) and airport transfer fields (`A-CMP6-airport`) clinically complete per jurisdictional standards?

### 2. Coverage Gaps — Missing Failure Modes

What clinically significant documentation errors could Medic Copilot make that are NOT covered by the current benchmarks?

- **Refusal documentation** — Informed refusal elements, competency assessment

### 3. Threshold and Weight Validation

Review the `threshold` and `weight` values in benchmark YAMLs:

- Are safety-critical benchmarks (A-SFT*) appropriately weighted?
- Are the 0.85-0.95 thresholds clinically justified?
- Should any benchmark be a "never event" (100% pass required)?

### 4. LLM Prompt Medical Accuracy

Review the LLM-as-a-judge prompts in `evaluators/llm-judge/*.md`:

- Do they capture the clinical nuance needed?
- Are the inclusion/exclusion criteria medically precise?
- What clinical edge cases might they miss?

---

## Deliverable Format

Produce a structured markdown document that I can import into my IDE for paired programming execution. Use this format:

```markdown
# Medical SME Review: SOAR Benchmark Validation

## Executive Summary
[2-3 sentences on overall clinical soundness and priority gaps]

## Benchmark-by-Benchmark Clinical Review

### A-NEG: Negation Handling
**Clinical Assessment**: [Sound / Needs Revision / Critical Gap]
**Findings**:
- [Specific clinical observation]
- [Specific clinical observation]
**Recommended Changes**:
- [ ] [Actionable item with clinical justification]

### A-FCT: Fact Extraction
[Same structure]

### A-SFT: Safety Flags
[Same structure]

[Continue for all 8 rubrics]

## Missing Failure Modes (Proposed New Benchmarks)

### Proposed: A-PED (Pediatric-Specific)
**Clinical Rationale**: [Why this matters for EMS documentation]
**Suggested Benchmarks**:
- A-PED1: [Specific failure mode]
- A-PED2: [Specific failure mode]

### Proposed: [Additional rubric]
[Same structure]

## Threshold and Weight Recommendations

| Benchmark | Current Threshold | Recommended | Clinical Justification |
|-----------|------------------|-------------|------------------------|
| A-SFT1 | 0.95 | 1.0 (never event) | [Reason] |

## LLM Prompt Improvements

### negation_simple_prompt.md
**Issue**: [Clinical gap]
**Suggested Addition**: [Specific text to add]

## Priority Action Items (for paired programmer)

1. **[High]** [Specific task]
2. **[High]** [Specific task]
3. **[Medium]** [Specific task]
```

---

## Key Files to Reference

- `benchmarks/a-component/*.yaml` — All 20 benchmark definitions
- `rubrics/*.yaml` — All 8 rubric definitions
- `evaluators/llm-judge/*.md` — LLM prompt files
- `docs/corpus-validator-mapping.md` — How benchmarks map to corpus validators
- `WORKING.md` — Current active tasks
- `AGENTS.md` — Project conventions and vocabulary

## Constraints

- Focus on **medical accuracy**, not framework architecture (that's validated)
- Cite clinical guidelines where applicable (NAEMSP, AHA, ACEP, local protocols)
- Be specific — "add pediatric considerations" is not actionable; "add A-PED1 for weight-based dosing errors" is
- Assume the reader is a paired programmer who needs exact specifications

---

*This prompt is designed for a research LLM with internet access and full repository context. The output should be immediately actionable for an AI-paired programming session.*

