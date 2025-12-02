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

### 1. Clinical Hardening of Existing Benchmarks

Review ALL 46 benchmarks in `benchmarks/a-component/*.yaml` from a **prehospital medical SME perspective**. For each rubric category, assess:

| Rubric | Benchmarks | Focus |
|--------|------------|-------|
| **A-NEG** | A-NEG1, A-NEG2, A-NEG3, A-NEG4 | Are negation patterns clinically comprehensive for EMS dictation? |
| **A-FCT** | A-FCT1, A-FCT4 | Are extraction failure modes comprehensive? Missing vital types? |
| **A-TMP** | A-TMP1, A-TMP2, A-TMP3, A-TMP4 | Are temporal failure modes realistic for EMS workflows? |
| **A-EVD** | A-EVD1, A-EVD3 | Are evidence attribution criteria clinically meaningful? |
| **A-CMP** | A-CMP1-6, A-ALL1 | Are completeness checks aligned with documentation standards? |
| **A-SFT** | A-SFT1, A-SFT2, A-SFT4 | Are safety-critical thresholds (1.0) appropriate? |
| **A-PRT** | A-PRT1, A-PRT2 | Are protocol elements comprehensive for RSI and STEMI? |
| **A-PED** | A-PED1, A-PED2 | Are pediatric failure modes realistic? |
| **A-CAR** | A-CAR1, A-CAR2 | Are cardiac arrest documentation elements complete? |
| **A-REF** | A-REF1, A-REF2, A-REF3 | Are refusal documentation requirements complete per Denver 0032? |
| **A-STR** | A-STR1, A-STR2 | Are stroke documentation elements aligned with time-sensitive protocols? |
| **A-TRM** | A-TRM1, A-TRM2, A-TRM3 | Are trauma documentation elements complete? |
| **A-OBS** | A-OBS1, A-OBS2 | Are obstetric/neonatal elements complete? |
| **A-BHV** | A-BHV1, A-BHV2 | Are behavioral/restraint documentation requirements aligned with CMS? |
| **A-UNC** | A-UNC1, A-UNC2 | Are uncertainty handling criteria appropriate? |
| **A-FMT** | A-FMT1, A-FMT2 | Are format validation checks sufficient? |

For each rubric, answer:
1. **Concept clarity**: Is the failure mode clearly defined and unambiguous?
2. **Examples quality**: Are examples realistic EMS scenarios?
3. **Threshold appropriateness**: Is the threshold clinically justified?
4. **Missing patterns**: What EMS-specific patterns are NOT covered?

### 2. Denver Protocol Cross-Reference (Deep Dive)

Systematically review these Denver protocols against current benchmarks:

| Protocol | Section | Documentation Requirements to Verify |
|----------|---------|-------------------------------------|
| **0032** | Refusal | Informed refusal elements, capacity assessment, risk explanation, base contact |
| **0050** | Field Pronouncement | Obvious death criteria, pronouncement time, physician contact |
| **0051** | TOR | Termination criteria, ROSC attempts, family notification |
| **1000** | RSI/Intubation | Pre-oxygenation, medications, **attempts count**, tube confirmation |
| **3000** | Cardiac Arrest | Initial rhythm, ROSC time, defibrillation count, drug timing |
| **3010** | STEMI | 12-lead interpretation, aspirin, NTG, cath lab activation |
| **4030** | Stroke | Last known well, stroke scale score, alert activation |
| **6000-6020** | Behavioral | Restraint justification, **reassessment intervals**, capacity documentation |
| **7000-7010** | OB/Neonatal | APGAR timing, delivery complications, neonatal assessment |
| **8000-8110** | Trauma | Mechanism documentation, GCS components, intervention timing |

**Specific items to investigate**:
- **Intubation attempts**: Protocol 1000 requires documentation of attempts. Is this covered by A-PRT1?
- **Restraint reassessment**: Protocol 6010 requires q15 monitoring. Is this covered by A-BHV1/A-SFT4?
- **Trauma alert criteria**: Is trauma alert activation covered by A-TRM3?

### 3. Identify Enhancement Opportunities

Based on your protocol review and clinical expertise, identify:

1. **Benchmark gaps**: Documentation elements NOT currently tested
2. **Threshold adjustments**: Benchmarks that should be stricter or more lenient
3. **Example improvements**: Benchmarks with weak or unrealistic examples
4. **Inclusion/exclusion refinements**: Criteria that need clinical clarification
5. **New benchmark proposals**: High-value failure modes not currently covered

Prioritize by clinical impact:
- **Critical**: Could affect patient safety or medicolegal risk
- **High**: Common documentation failure with downstream impact
- **Medium**: Useful but less frequent or lower impact
- **Low**: Edge cases or minor improvements

---

## Deliverable Format

Produce a structured markdown document for paired programming execution. Use this format:

```markdown
# Medical SME Review: Clinical Hardening & Enhancement

## Executive Summary
[3-4 sentences: Overall assessment of benchmark quality, key gaps found, priority recommendations]

---

## Rubric-by-Rubric Clinical Review

### A-NEG (Negation Handling)
**Assessment**: [Sound / Needs Refinement / Critical Gap]
**Strengths**:
- [What's working well]
**Issues Found**:
- [Specific issue with benchmark or example]
**Recommended Changes**:
- [ ] [Actionable item with specific benchmark reference]

### A-SFT (Safety Flags)
[Same structure — focus on safety-critical benchmarks]

### A-PRT (Protocol Tracking)
[Same structure — focus on RSI and STEMI completeness]

[Continue for all 16 rubrics]

---

## Denver Protocol Gap Analysis

| Protocol | Requirement | Current Coverage | Gap | Priority | Action |
|----------|-------------|------------------|-----|----------|--------|
| 1000 RSI | Intubation attempts | A-PRT1 | Yes | High | Add to A-PRT1 inclusion criteria |
| 6010 Restraint | Q15 reassessment | A-SFT4 | Partial | Medium | Expand A-SFT4 examples |
| [Continue...] |

---

## Enhancement Backlog

### Critical Priority
| Enhancement | Benchmark | Rationale |
|-------------|-----------|-----------|
| [Specific enhancement] | [A-XXX] | [Why this matters clinically] |

### High Priority
| Enhancement | Benchmark | Rationale |
|-------------|-----------|-----------|
| [Specific enhancement] | [A-XXX] | [Why this matters] |

### Medium Priority
[Same structure]

### Low Priority / Future Consideration
[Same structure]

---

## Threshold Review

| Benchmark | Current | Recommended | Justification |
|-----------|---------|-------------|---------------|
| [A-XXX] | 0.XX | 0.XX | [Clinical rationale] |

---

## Example Quality Assessment

| Benchmark | Issue | Current Example | Suggested Replacement |
|-----------|-------|-----------------|----------------------|
| [A-XXX] | [Unrealistic/vague/etc.] | "[Current]" | "[Better example]" |

---

## Summary Statistics

- **Benchmarks Reviewed**: 46
- **Sound (no changes)**: XX
- **Minor refinements**: XX
- **Significant changes needed**: XX
- **New benchmarks proposed**: XX
```

---

## Key Files to Reference

### All Benchmarks (review all 46)
- `benchmarks/a-component/*.yaml` — All benchmark definitions
- `rubrics/*.yaml` — All rubric definitions (16 rubrics)

### Key Benchmarks to Scrutinize
- **Safety-critical**: A-SFT1, A-SFT2, A-SFT4, A-UNC1 (all have threshold 1.0)
- **Protocol-specific**: A-PRT1 (RSI), A-PRT2 (STEMI), A-CAR1/2 (Arrest)
- **Specialty scenarios**: A-PED1/2, A-OBS1/2, A-BHV1/2, A-REF1/2/3

### Schema and Scope
- `README.md` — Scope boundary principle (critical to understand)
- `benchmarks/FIELD_SPECS.md` — Benchmark field specifications
- `rubrics/FIELD_SPECS.md` — Rubric field specifications
- `WORKING.md` — Current backlog and future enhancements

### Documentation Templates (for clinical context)
- `asr/v3.0/full-draatt/full-draatt-template.v3.0.md` — Complete DRAATT structure
- `asr/v3.0/doa/doa-template.v3.0.md` — DOA documentation requirements
- `asr/v3.0/rsi-overlay/rsi-overlay-template.v3.0.md` — RSI documentation requirements

### External Reference (Primary Source)
- [Denver Metro EMS Protocols July 2025](https://www.dmemsmd.org/sites/default/files/DMEMSMD%20Protocols%20July%202025%20FINAL%202025-07-14.pdf) — Authoritative clinical reference

---

## Constraints

- **Be hyper-critical** — assume a medicolegal reviewer will scrutinize these benchmarks
- **Ground in Denver protocols** — every recommendation should cite specific protocol sections
- Focus on **extraction accuracy and documentation completeness**, not clinical correctness
- **Prioritize by clinical impact** — patient safety > medicolegal risk > billing accuracy
- Provide **specific, actionable recommendations** — not vague suggestions
- **Do NOT recommend** embedding clinical formulas or dose ranges into benchmarks
- Respect the **scope boundary** — eval harness tests extraction fidelity, not clinical judgment

---

## Research Agent Instructions

1. **Read `README.md` scope boundary** — understand what the eval harness does and doesn't do
2. **Review ALL 46 benchmarks** systematically by rubric
3. **Cross-reference Denver protocols** for each clinical scenario type
4. **Identify gaps** — what documentation requirements are NOT tested?
5. **Assess examples** — are they realistic EMS scenarios?
6. **Evaluate thresholds** — are hard gates (1.0) appropriately assigned?
7. **Propose enhancements** — prioritize by clinical impact
8. **Be specific** — cite benchmark codes, protocol sections, and line numbers

---

## Current State

The evaluation framework has been through multiple iterations and is considered mature:
- **16 rubrics** covering all major documentation categories
- **46 benchmarks** testing specific failure modes
- **32 LLM prompts** for subjective evaluation
- **Consistency validated** — no structural issues

Your task is **clinical hardening** — ensuring the benchmarks are comprehensive, accurate, and clinically meaningful before final human SME review and developer handoff.

---

*This prompt is for a final clinical review before production. Output should identify specific improvements, not create new structures from scratch.*

