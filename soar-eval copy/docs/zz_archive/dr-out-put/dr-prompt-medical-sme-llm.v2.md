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

### Medic Copilot's Clinical Knowledge Base

Medic Copilot has access to the **Denver Metropolitan Prehospital Protocols (July 2025)** as its authoritative clinical reference:

> **Protocol Source**: [DMEMSMD Protocols July 2025](https://www.dmemsmd.org/sites/default/files/DMEMSMD%20Protocols%20July%202025%20FINAL%202025-07-14.pdf)

Key protocol sections relevant to documentation:
- **0050 Field Pronouncement** — Obvious death criteria and pronouncement procedures
- **0051 Termination of Resuscitation** — Cardiac arrest termination criteria
- **0032 Patient Non-Transport or Refusal** — Refusal documentation requirements
- **3000-3090 Cardiac Protocols** — STEMI, arrest, and arrhythmia documentation
- **8000-8110 Trauma Protocols** — Mechanism documentation, GCS, injury assessment
- **1000 Intubation: Oral** — RSI documentation requirements
- **6000-6020 Behavioral Protocols** — Restraint and capacity documentation

**Research Task**: Review the Denver protocols to understand what documentation elements are clinically expected, then assess whether the current eval harness adequately tests for extraction of those elements.

### The Evaluation Framework

The `soar-pydantic-eval/` folder contains:
- **Rubrics** (`rubrics/*.yaml`) — Evaluation categories (Negation, Fact Extraction, Safety, etc.)
- **Benchmarks** (`benchmarks/a-component/*.yaml`) — Specific failure modes to detect
- **LLM Prompts** (`evaluators/llm-judge/*.md`) — For subjective evaluations
- **Field Specs** (`*/FIELD_SPECS.md`) — Schema and scope boundary documentation

**Important**: Review `README.md` and `benchmarks/FIELD_SPECS.md` for the **scope boundary principle** before analyzing benchmarks.

---

## Scope Boundary: What the Evaluation Harness Does NOT Do

**CRITICAL**: The SOAR evaluation harness tests **semantic preservation fidelity**, NOT clinical correctness.

| Eval Harness Tests | Eval Harness Does NOT Test |
|--------------------|---------------------------|
| Did Medic Copilot extract the stated dose correctly? | Is that dose clinically appropriate? |
| Did it preserve the negation semantics? | Is the clinical finding itself accurate? |
| Did it capture all stated vitals? | Are those vitals within normal ranges? |
| Did it document the stated protocol steps? | Were the correct protocol steps followed? |
| Did it extract the pronouncement time? | Was the pronouncement time appropriate? |

**Why this matters**: Clinical validation (dose checking, protocol compliance, contraindication alerts) happens at **Medic Copilot inference time** using its knowledge base. The evaluation harness tests whether the AI correctly **extracted and preserved** what was dictated.

**Research Focus**: Identify **failure mode categories** (types of errors), not clinical rules to embed. The eval harness should be:
- **Protocol-agnostic** — Works regardless of which EMS protocol set is used
- **Jurisdiction-portable** — Not hardcoded to Denver Metro specifics
- **Ground-truth driven** — Test cases carry known-correct answers; eval checks Medic Copilot's behavior

### Three Benchmark Categories

| Category | Benchmarks | What We Test | Ground Truth Contains |
|----------|------------|--------------|----------------------|
| **Extraction** | A-FCT, A-NEG, A-TMP, A-CMP, A-EVD, A-FMT | Did AI extract stated information correctly? | Expected extraction values |
| **System Logic** | A-SFT, A-PRT, A-PED, A-CAR, A-STR, etc. | Does Medic Copilot's inference-time logic work? | What Medic Copilot should detect/flag |
| **Clinical Judgment** | S-component (not in scope) | Is output clinically appropriate? | SME labels (human review) |

**Key distinction for research**:
- For **extraction benchmarks**: Look for patterns Medic Copilot might misparse (negations, complex structures)
- For **system logic benchmarks**: Look for documentation elements Medic Copilot should flag/calculate (safety issues, protocol gaps, pediatric doses)

---

## Documentation Templates (Additional Context)

The repository contains DRAATT templates that define expected documentation structure. These may inform what extraction failure modes to look for:

### Template Files to Review

| Template | Path | Documentation Focus |
|----------|------|---------------------|
| **Full DRAATT** | `asr/v3.0/full-draatt/full-draatt-template.v3.0.md` | Complete call documentation with 20 assessment systems |
| **DOA/Obvious Death** | `asr/v3.0/doa/doa-template.v3.0.md` | Field pronouncement, obvious death signs, scene preservation |
| **Airport Transfer** | `asr/v3.0/airport-transfer/airport-transfer-template.v3.0.md` | Aeromedical handoff, transfer of care, flight crew coordination |
| **RSI Overlay** | `asr/v3.0/rsi-overlay/rsi-overlay-template.v3.0.md` | Rapid sequence intubation procedure documentation |

**Research Task**: Cross-reference these templates with the Denver protocols to identify documentation elements that:
1. Are protocol-required but not currently covered by benchmarks
2. Have high extraction error potential (complex structures, conditional fields)
3. Represent common EMS documentation gaps

---

## Research Questions

### 1. Define Placeholder Benchmarks

Seven benchmarks were referenced in rubrics but lack definitions. For each, provide:

| Benchmark | Parent Rubric | Your Task |
|-----------|---------------|-----------|
| **A-CMP2** | A-CMP (Completeness) | Define a completeness check — perhaps Response section fields |
| **A-CMP3** | A-CMP (Completeness) | Define a completeness check — perhaps Arrival section fields |
| **A-CMP4** | A-CMP (Completeness) | Define a completeness check — perhaps Assessment section fields |
| **A-EVD3** | A-EVD (Evidence Attribution) | Define an evidence attribution check beyond A-EVD1 |
| **A-FMT2** | A-FMT (Format Validity) | Define a format check — perhaps field type compliance or enum validity |
| **A-TMP3** | A-TMP (Temporal Ordering) | Define a temporal check beyond ordering and trends |
| **A-TMP4** | A-TMP (Temporal Ordering) | Define another temporal check |

For each benchmark, answer:
1. **Concept**: What specific failure mode does this catch? (1-2 sentences)
2. **Inclusion Criteria**: When should this benchmark be applied?
3. **Exclusion Criteria**: When should this NOT flag an error?
4. **Examples**: 2-3 concrete examples of failures this would catch
5. **Threshold**: Suggested threshold (0.80-1.0) and whether `hard_gate` or `threshold_gate`
6. **Evaluator Type**: `code` (deterministic), `hybrid` (code + LLM), or `llm_judge` (subjective)

**Guidance**:
- A-CMP2/3/4 should cover DRAATT section completeness not already handled by A-CMP1 (core sections), A-CMP5 (DOA), or A-CMP6 (transport)
- A-EVD3 should address evidence attribution gaps beyond "span unsupported" (A-EVD1)
- A-FMT2 should address format issues beyond JSON validity (A-FMT1)
- A-TMP3/4 should address temporal issues beyond ordering (A-TMP1) and trends (A-TMP2)

### 2. Evaluate A-UNC (Uncertainty Handling) Rubric

A proposed new rubric addresses AI behavior when data is **absent** (distinct from wrong):

| Proposed Benchmark | Concept |
|--------------------|---------|
| A-UNC1 | Hallucination on missing data — AI fills in a value not stated in transcript |
| A-UNC2 | Silent omission — required field left blank without clarification |

**Questions**:
1. Is this a valid failure category distinct from A-EVD (evidence) and A-CMP (completeness)?
2. Should it be a standalone rubric or folded into existing rubrics?
3. If standalone, what threshold and weight would you assign?
4. What examples from EMS documentation would trigger these benchmarks?

### 3. Cross-Reference Denver Protocols for Coverage Gaps

Using the Denver Metro protocols linked above, identify any **documentation requirements** not currently covered by benchmarks. Focus on:

- **0032 Patient Non-Transport/Refusal** — Are refusal documentation elements covered by A-REF?
- **0050/0051 Field Pronouncement/TOR** — Are pronouncement fields covered by A-CMP5 and A-CAR?
- **1000 RSI/Intubation** — Are RSI documentation elements covered by A-PRT1?
- **6000-6020 Behavioral** — Are restraint/capacity elements covered by A-BHV?

For any gaps found, propose which placeholder benchmark (A-CMP2-4, A-EVD3, A-FMT2, A-TMP3-4) could address it, or recommend a new benchmark code.

---

## Deliverable Format

Produce a structured markdown document that I can import into my IDE for paired programming execution. Use this format:

```markdown
# Medical SME Review: Placeholder Benchmark Definitions

## Executive Summary
[2-3 sentences on approach and key decisions]

---

## Placeholder Benchmark Definitions

### A-CMP2: [Your Label]

**Concept**:
> [1-2 sentence description of the failure mode]

**Inclusion Criteria**:
> [When to apply this benchmark]

**Exclusion Criteria**:
> [When NOT to flag an error]

**Examples**:
- "[Concrete example 1]"
- "[Concrete example 2]"

**Threshold**: [0.XX] | **Criticality**: [hard_gate / threshold_gate]
**Evaluator Type**: [code / hybrid / llm_judge]

---

### A-CMP3: [Your Label]
[Same structure as above]

### A-CMP4: [Your Label]
[Same structure]

### A-EVD3: [Your Label]
[Same structure]

### A-FMT2: [Your Label]
[Same structure]

### A-TMP3: [Your Label]
[Same structure]

### A-TMP4: [Your Label]
[Same structure]

---

## A-UNC Rubric Assessment

**Recommendation**: [Create standalone rubric / Fold into existing / Do not create]

**Rationale**:
> [Why this is or isn't a distinct failure category]

**If creating A-UNC**:
- **A-UNC1 Concept**: [Refined definition]
- **A-UNC2 Concept**: [Refined definition]
- **Threshold**: [0.XX]
- **Weight**: [0.XXX]

---

## Denver Protocol Coverage Analysis

| Protocol | Documentation Requirement | Current Coverage | Gap/Action |
|----------|--------------------------|------------------|------------|
| 0032 Refusal | [Requirement] | A-REF1, A-REF2 | [Gap or OK] |
| 0050 Pronouncement | [Requirement] | A-CMP5 | [Gap or OK] |
| 1000 RSI | [Requirement] | A-PRT1 | [Gap or OK] |
| 6000 Behavioral | [Requirement] | A-BHV1, A-BHV2 | [Gap or OK] |

---

## Summary Table

| Benchmark | Label | Evaluator | Threshold | Criticality |
|-----------|-------|-----------|-----------|-------------|
| A-CMP2 | [Label] | [Type] | [0.XX] | [Gate] |
| A-CMP3 | [Label] | [Type] | [0.XX] | [Gate] |
| A-CMP4 | [Label] | [Type] | [0.XX] | [Gate] |
| A-EVD3 | [Label] | [Type] | [0.XX] | [Gate] |
| A-FMT2 | [Label] | [Type] | [0.XX] | [Gate] |
| A-TMP3 | [Label] | [Type] | [0.XX] | [Gate] |
| A-TMP4 | [Label] | [Type] | [0.XX] | [Gate] |
```

---

## Key Files to Reference

### Placeholder Benchmarks (your task is to define these)
- `benchmarks/a-component/A-CMP2.yaml` — Placeholder
- `benchmarks/a-component/A-CMP3.yaml` — Placeholder
- `benchmarks/a-component/A-CMP4.yaml` — Placeholder
- `benchmarks/a-component/A-EVD3.yaml` — Placeholder
- `benchmarks/a-component/A-FMT2.yaml` — Placeholder
- `benchmarks/a-component/A-TMP3.yaml` — Placeholder
- `benchmarks/a-component/A-TMP4.yaml` — Placeholder

### Existing Benchmarks (for context on what's already covered)
- `benchmarks/a-component/A-CMP1.yaml` — Core section presence
- `benchmarks/a-component/A-CMP5.yaml` — DOA pronouncement fields
- `benchmarks/a-component/A-CMP6.yaml` — Transport/handoff completeness
- `benchmarks/a-component/A-EVD1.yaml` — Evidence span unsupported
- `benchmarks/a-component/A-FMT1.yaml` — JSON format validity
- `benchmarks/a-component/A-TMP1.yaml` — Temporal ordering
- `benchmarks/a-component/A-TMP2.yaml` — Pre/post trends

### Schema and Scope
- `README.md` — Scope boundary principle
- `benchmarks/FIELD_SPECS.md` — Benchmark schema and field definitions
- `WORKING.md` — Backlog showing placeholder status

### Documentation Templates (for DRAATT section structure)
- `asr/v3.0/full-draatt/full-draatt-template.v3.0.md` — Complete DRAATT structure

### External Reference
- [Denver Metro EMS Protocols July 2025](https://www.dmemsmd.org/sites/default/files/DMEMSMD%20Protocols%20July%202025%20FINAL%202025-07-14.pdf) — Documentation requirements by protocol

---

## Constraints

- **Define extraction failure modes**, not clinical rules
- Each benchmark should catch a **distinct** failure type not covered by existing benchmarks
- Benchmarks should be **testable** — evaluator must be able to determine pass/fail
- Focus on **documentation completeness and accuracy**, not clinical appropriateness
- Provide **concrete examples** from realistic EMS scenarios
- Thresholds should reflect **extraction accuracy expectations** (not clinical severity)
- Be specific — "[TBD]" is not a definition; provide actionable content

---

## Research Agent Instructions

1. **Read existing benchmarks** in the same rubric to understand what's already covered
2. **Review `benchmarks/FIELD_SPECS.md`** for required fields and enum values
3. **Review Denver protocols** for documentation requirements that map to each rubric
4. **Define each placeholder** with concept, criteria, examples, threshold, and evaluator type
5. **Ensure no overlap** — each benchmark should catch failures the others miss
6. **Assess A-UNC** — decide if uncertainty handling is a distinct category or folded in
7. **Produce YAML-ready definitions** — output should be directly pasteable into placeholder files

---

*This prompt targets the 7 placeholder benchmarks identified by the consistency validator. Output should be immediately usable to populate the YAML files.*

