# Action Policies: Extending SOAR with Correction Loops

**Status**: Draft for CTO Review  
**Date**: 2025-11-28

---

## Executive Summary

The current SOAR evaluation framework detects documentation failures but does not define what happens after detection. This proposal extends the framework with **action policies** that enable:

1. **Agent self-correction** — Medic Copilot re-reads the source ASR and attempts to fix the error
2. **User escalation** — When agent cannot resolve, prompt the Medic for clarification

The key insight: **the agent always has access to the original ASR transcript**. Self-correction is re-extraction with feedback, not guessing.

---

## Problem Statement

Currently, when the evaluation harness detects an error (e.g., hallucinated value, negation misinterpretation), the system only logs the failure. There is no mechanism for:

- Medic Copilot to attempt self-correction
- The Medic to be prompted for clarification

This limits the framework to **measurement** without enabling **improvement**.

---

## Proposed Solution

### The Correction Loop

```
┌──────────────┐
│  ASR Source  │ ←────────────────────────────┐
└──────┬───────┘                              │
       ↓                                      │
┌──────────────┐                              │
│ Medic Copilot│                              │
│  (Extract)   │                              │
└──────┬───────┘                              │
       ↓                                      │
┌──────────────┐                              │
│ Eval Harness │                              │
│ (Benchmarks) │                              │
└──────┬───────┘                              │
       ↓                                      │
   ┌───┴───┐                                  │
   │Error? │──── No ──→ Output approved       │
   └───┬───┘                                  │
       │ Yes                                  │
       ↓                                      │
┌──────────────────────────────────┐          │
│         ACTION ROUTER            │          │
│                                  │          │
│  1. Send feedback to Agent       │──────────┘
│     "Re-read source, verify X"   │   (Re-extract)
│                                  │
│  2. If agent fails again:        │
│     → Escalate to User           │
│     → "Please clarify X"         │
└──────────────────────────────────┘
```

### Two Primary Actors

| Actor | Role | When Engaged |
|-------|------|--------------|
| **Agent** (Medic Copilot) | Re-read source, attempt correction | First response to any error |
| **User** (Medic) | Clarify ambiguous input | When agent cannot resolve |

*System logging and metrics are assumed via the broader SOAR/DII framework.*

### Action Policy by Failure Type

| Failure Type | Agent Re-extraction | Escalate to User When |
|--------------|--------------------|-----------------------|
| Hallucination | Re-read source, verify value exists | Agent keeps producing same invalid value |
| Negation | Re-read with focus on negation phrase | Source is genuinely ambiguous |
| Completeness | Re-scan source for missing data | Data truly not present in source |
| Format | Mechanical fix (JSON structure) | Almost never |
| Safety | Re-verify dose/route extraction | Source is ambiguous or agent uncertain |
| Contradiction | Re-read both conflicting statements | Both are clearly stated (human decides) |

---

## Key Design Principles

### 1. Agent Self-Correction is Re-Extraction, Not Invention

The agent always has access to the original ASR transcript. When flagged for hallucination, the agent doesn't "guess" — it re-reads the source with specific feedback about what was wrong.

**Example**:
- Error: `weight: 80` flagged as hallucination (not in source)
- Feedback: "Re-read source. Verify patient weight appears in transcript."
- Agent re-reads, finds no weight mentioned, returns `weight: null`

### 2. Escalation is Not Failure

When the agent escalates to the user, it means the source material is genuinely ambiguous. This is valuable signal, not system failure.

**Example**:
- Source: "Patient denies chest pain but appears uncomfortable"
- Agent uncertain: Is this chest pain present or absent?
- Escalation: "Clarify: Does patient have chest pain?"

---

## Escalation Triggers

Agent escalates to User when:

1. **Max iterations reached** — Agent tried N times, still failing
2. **Agent reports uncertainty** — "Source ambiguous, cannot determine"
3. **Source genuinely missing** — "Value not found in transcript"
4. **Conflicting evidence** — "Found contradictory statements, cannot resolve"

---

## Schema Extension (Conceptual)

Each benchmark would include an `action_policy` field:

```yaml
action_policy:
  agent_correction:
    enabled: true
    max_attempts: 2
    feedback_template: "Re-read source. Verify '{{field}}' value."
    
  user_escalation:
    trigger: agent_exhausted | agent_uncertainty
    prompt_id: negation-double-negative  # Links to user-prompts/
```

---

## User Escalation Prompts

When agent correction fails or reports uncertainty, the Action Router selects a user prompt from the prompt library.

### Prompt Library Structure

```
action-policies/
├── user-prompts/           # 13 YAML prompt packs
│   ├── 01-negation.yaml    # Negation clarification
│   ├── 02-units.yaml       # Unit/dose clarification
│   ├── 03-time.yaml        # Time ambiguity
│   └── ...
├── benchmark-to-prompt-map.json  # Which benchmarks use which prompts
└── prompt-review.md        # Medical SME review of prompt wording
```

### Example: Benchmark to Prompt Flow

```yaml
# In A-NEG1.yaml benchmark
action_policy:
  agent_correction:
    enabled: true
    max_attempts: 2
    feedback_template: "Re-read source. Focus on negation phrase: '{{phrase}}'."
    
  user_escalation:
    trigger: agent_exhausted
    prompt_id: negation-double-negative
```

```yaml
# In user-prompts/01-negation.yaml (simplified SME schema)
prompts:
  - id: negation-double-negative
    prompt_neutral: "You used '{phrase}'. Confirm: {symptom} present or absent?"
    prompt_medic_copilot: "Medic Copilot detected '{phrase}'. Confirm: {symptom} present or absent?"
    response_type: select_one
    options: [present, absent]
    severity: warn
    examples:
      - "denies no chest pain"
```

### Prompt Tone Selection

| Context | Tone | Example |
|---------|------|---------|
| Medic review of own dictation | `neutral` | "You used 'denies no pain'. Confirm: pain present or absent?" |
| QA review or audit | `medic_copilot` | "Medic Copilot detected 'denies no pain'. Confirm: pain present or absent?" |

### Response Types

| Type | Description | Example |
|------|-------------|---------|
| `select_one` | Single choice from options | [present, absent] |
| `text_short` | Free-text clarification | "Confirm dose, route, time" |
| `numeric_value` | Numeric input | EtCO2 in mmHg |
| `time_hhmm` | Time in 24-hour format | 09:00 or 21:00 |

---

## Out of Scope (for this proposal)

- **Blocking output** — This is retrospective documentation; output must always be produced
- **Clinical decision support** — Actions do not make clinical judgments
- **Automatic approval** — All corrections require either agent success or user confirmation

---

## Next Steps (Pending Approval)

1. Define `action_policy` schema in `benchmarks/FIELD_SPECS.md`
2. Add default action policies to existing benchmarks
3. Define feedback templates for each benchmark category

---

## Open Question for CTO

Should action policies be defined at the **benchmark** level or **rubric** level?

- **Benchmark level**: More granular control (e.g., A-NEG1 and A-NEG2 could have different escalation triggers)
- **Rubric level**: Simpler to manage, consistent behavior within a category

---

## Architecture Alignment (Per CTO Discussion)

The following context from CTO aligns with and extends this proposal:

### Benchmarks as Modular Tools

Each benchmark functions as a discrete "tool" that can be:
- **Enabled/disabled** per agency
- **Configured** with agency-specific thresholds or action policies
- **Extended** by adding new benchmarks for agency-specific requirements

**Example**: A pediatric specialty agency enables stricter A-PED thresholds and additional pediatric benchmarks, while a general transport agency may disable them entirely.

### Event Bus Integration

Benchmark evaluations publish events to the event bus:

```
┌─────────────────┐        ┌─────────────────┐        ┌─────────────────┐
│   Benchmark     │───────▶│    Event Bus    │───────▶│  Action Router  │
│   (Tool fires)  │ event  │                 │ subscribe│                 │
└─────────────────┘        └─────────────────┘        └─────────────────┘
```

This decouples evaluation from action handling:
- Benchmarks are responsible for **detection** (publishing events)
- Action Router is responsible for **response** (subscribing and routing)
- Agencies can customize both which tools are active AND how responses are routed

### Agency-Specific Configuration

| Configuration Level | What Gets Customized | Example |
|---------------------|---------------------|---------|
| **Benchmark enablement** | Which tools are active | Pediatric agency enables A-PED benchmarks |
| **Threshold override** | How strict the tool is | Stricter negation handling for high-acuity agencies |
| **Action policy** | How the system responds | High-profile cases escalate immediately to User |

This architecture supports the action policy proposal: each benchmark (tool) carries its own `action_policy` configuration, and the event bus routes these to the appropriate handler.

---

*This document represents the Medical SME perspective on action policies. Implementation details to be defined by engineering after approval.*
