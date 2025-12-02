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

### 1. Clinical Accuracy of Current Benchmarks

Review each benchmark in `benchmarks/a-component/*.yaml` and assess:

- **A-NEG (Negation Handling)**: Are the negation patterns clinically comprehensive? What EMS-specific negation phrases are missing? (e.g., "pt AOx4 but confused" — is "but" a negation risk?)

- **A-FCT (Fact Extraction)**: Are the extraction failure modes comprehensive? What categories of stated facts commonly get misinterpreted (e.g., vital trends, medication timing)? **Do NOT embed clinical ranges** — test extraction accuracy only.

- **A-SFT (Safety Flags)** [System Logic]: These benchmarks test whether Medic Copilot's safety detection logic fires on known-unsafe test cases. Are there additional safety-relevant documentation patterns that Medic Copilot should flag but we're not testing? (e.g., missing allergy acknowledgment when contraindicated med given)

- **A-PRT (Protocol Tracking)** [System Logic]: These benchmarks test whether Medic Copilot's protocol-awareness logic captures stated steps and flags gaps. Are there protocol-documentation elements from Denver protocols that we should test Medic Copilot's handling of?

- **A-CMP (Completeness)** [Extraction]: Are the DOA pronouncement fields (`A-CMP5`) and airport transfer fields (`A-CMP6-airport`) clinically complete per jurisdictional expectations? Cross-reference with Denver protocol 0050 and template requirements.

- **A-PED (Pediatric)** [System Logic]: A-PED1 tests whether Medic Copilot correctly calculates weight-based doses (ground truth provides expected calculation result). Are there other pediatric documentation elements where Medic Copilot's logic should be tested?

- **A-CAR (Cardiac Arrest)** [System Logic]: A-CAR1/A-CAR2 test Medic Copilot's arrest documentation logic. Does this align with documentation expectations in Denver protocol 0051? Are there extraction failure modes for arrest documentation that we're missing?

### 2. Coverage Gaps — Missing Failure Modes

What clinically significant documentation elements could Medic Copilot fail to extract that are NOT covered by the current benchmarks?

Consider reviewing the Denver protocols for documentation-heavy sections:
- **Refusal documentation** (0032) — Informed refusal elements, competency assessment, risk explanation
- **Behavioral/restraint documentation** (6000-6020, 1130) — Restraint justification, reassessment intervals
- **Trauma mechanism documentation** (8000-8110) — MOI details, GCS trending, intervention timing
- **Obstetric documentation** (7000-7010) — APGAR scores, delivery complications, neonatal assessment
- **Stroke documentation** (4030) — Last known well time, stroke scale scores, alert activation

**Output Format**: For each gap identified, specify:
1. The documentation element at risk
2. The extraction failure mode (how Medic Copilot might misinterpret it)
3. Proposed benchmark code and concept (following existing A-XXX pattern)

### 3. Threshold and Weight Validation

Review the `threshold` and `weight` values in benchmark YAMLs:

- Are safety-critical benchmarks (A-SFT*) appropriately weighted?
- Are the 0.85-0.95 thresholds clinically justified for **extraction accuracy**?
- Should any benchmark be a "hard gate" (100% pass required for binary elements like allergy presence)?

**Note**: Thresholds should reflect extraction accuracy expectations, not clinical severity. A benchmark for "extracted pronouncement time" might be 0.95 (some ambiguity acceptable), while "extracted allergy mention" might be 1.0 (binary presence).

### 4. LLM Prompt Medical Accuracy

Review the LLM-as-a-judge prompts in `evaluators/llm-judge/*.md`:

- Do they capture the clinical nuance needed for **extraction evaluation**?
- Are the inclusion/exclusion criteria medically precise?
- Do they avoid embedding clinical judgment that belongs in Medic Copilot's inference?

**Specific Review**: Check that prompts like `impression_mismatch_prompt.md` test whether the stated impression was extracted correctly, not whether the impression itself was clinically appropriate.

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
- [Specific clinical observation about extraction accuracy]
- [Specific clinical observation]
**Recommended Changes**:
- [ ] [Actionable item focused on extraction failure modes]

### A-FCT: Fact Extraction
[Same structure]

### A-SFT: Safety Flags
[Same structure]

[Continue for all rubrics including A-PED, A-CAR, A-REF, A-STR, A-TRM, A-OBS, A-BHV]

## Missing Failure Modes (Proposed New Benchmarks)

### Proposed: [Rubric Code] ([Description])
**Category**: [Extraction / System Logic]
**Documentation Element at Risk**: [What protocol/template requires this]
**Failure Mode**: [How Medic Copilot might err]
**Ground Truth Structure**: [What test cases need to contain]
**Suggested Benchmarks**:
- [Code]: [Specific failure mode]

Example ground truth for **extraction** benchmark:
```yaml
input: "narrative with ambiguous structure"
expected_extraction: { field: "correct_value" }
```

Example ground truth for **system logic** benchmark:
```yaml
input: "narrative with safety issue"
expected_flag: "allergy_contraindication"
expected_calculation: 0.2  # mg based on stated weight
```

## Threshold and Weight Recommendations

| Benchmark | Current Threshold | Recommended | Justification (extraction accuracy basis) |
|-----------|------------------|-------------|-------------------------------------------|
| A-SFT1 | 0.95 | 1.0 (hard gate) | Allergy mention is binary — if stated, must appear |

## LLM Prompt Improvements

### [prompt_file.md]
**Issue**: [Extraction accuracy gap, not clinical judgment]
**Suggested Addition**: [Specific text to add]

## Denver Protocol Cross-Reference

| Protocol Section | Documentation Requirement | Current Benchmark Coverage | Gap? |
|------------------|--------------------------|---------------------------|------|
| 0050 Field Pronouncement | Pronouncement time, method, physician | A-CMP5 | [Y/N] |
| 3000 Medical Pulseless Arrest | ROSC time, rhythm, interventions | A-CAR1, A-CAR2 | [Y/N] |
| [Continue for key protocols] |

## Priority Action Items (for medical SME)

1. **[High]** [Specific task focused on extraction failure modes]
2. **[High]** [Specific task]
3. **[Medium]** [Specific task]
```

---

## Key Files to Reference

### Evaluation Framework
- `README.md` — Scope boundary principle (critical to understand first)
- `benchmarks/FIELD_SPECS.md` — Benchmark schema and three-category framework
- `benchmarks/a-component/*.yaml` — All benchmark definitions
- `rubrics/*.yaml` — All rubric definitions
- `evaluators/llm-judge/*.md` — LLM prompt files
- `WORKING.md` — Current active tasks
- `AGENTS.md` — Project conventions and vocabulary

### Documentation Templates
- `asr/v3.0/full-draatt/full-draatt-template.v3.0.md` — Complete DRAATT structure
- `asr/v3.0/doa/doa-template.v3.0.md` — Obvious death documentation
- `asr/v3.0/airport-transfer/airport-transfer-template.v3.0.md` — Aeromedical transfer
- `asr/v3.0/rsi-overlay/rsi-overlay-template.v3.0.md` — RSI procedure overlay

### External Reference
- [Denver Metro EMS Protocols July 2025](https://www.dmemsmd.org/sites/default/files/DMEMSMD%20Protocols%20July%202025%20FINAL%202025-07-14.pdf) — Medic Copilot's clinical knowledge base

---

## Constraints

- **Categorize each finding** as extraction (pattern parsing) or system logic (inference-time rules) per the three-category framework
- Focus on **semantic preservation**, not clinical correctness (that's Medic Copilot's job)
- **Do NOT recommend** embedding clinical formulas, dose ranges, or protocol decision trees into the eval harness
- Reference Denver protocols to understand **documentation expectations**, then translate findings into **failure mode categories**
- For **system logic benchmarks**: Describe what Medic Copilot should flag/calculate, not the clinical rule itself
- Cite clinical guidelines where applicable (NAEMSP, AHA, ACEP) for documentation standards, not treatment decisions
- Be specific — "add pediatric considerations" is not actionable; "add A-PED1 for weight-based dose extraction errors" is
- **Propose ground truth structures** for new benchmarks so developers know how to construct test cases
- Assume the reader is a medical SME who will hand this off to a developer for implementation

---

## Research Agent Instructions

1. **Read `README.md` and `benchmarks/FIELD_SPECS.md`** first — understand the scope boundary and three-category framework before analyzing benchmarks
2. **Review the Denver Metro protocols** linked above, focusing on documentation requirements (not treatment algorithms)
3. **Cross-reference with existing benchmarks** to identify coverage gaps
4. **Review the DRAATT templates** to understand expected documentation structure
5. **Categorize findings** as extraction (pattern parsing) vs system logic (inference-time rules)
6. **Propose ground truth structures** for new benchmarks, not just concepts
7. **Produce actionable recommendations** focused on what Medic Copilot might misinterpret, not what clinicians might do wrong

---

*This prompt is designed for a research LLM with internet access and full repository context. The output should be immediately actionable for medical SME review before developer handoff.*

