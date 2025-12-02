# User Prompt Placeholder Schema

**Status**: Draft for CTO Review  
**Purpose**: Define placeholder taxonomy for user escalation prompts

---

## Overview

User prompts use `{placeholder}` syntax where the system must inject context-specific values at runtime. This schema defines the standard placeholders and their usage.

---

## Placeholder Categories

### 1. User Speech (Quoted)

Values extracted from what the Medic actually said. Always wrapped in quotes in the prompt.

| Placeholder | Description | Example Prompt |
|-------------|-------------|----------------|
| `{phrase}` | Exact text that triggered the error | "You used '{phrase}'. Confirm..." |
| `{spoken}` | Spoken number or word | "You spoke '{spoken}'. Confirm numeric value?" |

### 2. Clinical Entities

Clinical concepts the prompt is asking about.

| Placeholder | Description | Example Prompt |
|-------------|-------------|----------------|
| `{medication}` | Drug name | "'{medication}' — confirm dose and route?" |
| `{vital}` | Vital sign type (BP, HR, SpO2, EtCO2) | "'{vital}' recorded as {wrong_unit}. Confirm?" |
| `{procedure}` | Procedure or intervention | "Laterality conflict for {procedure}. Which side?" |
| `{symptom}` | Symptom or clinical finding | "Confirm: {symptom} present or absent?" |
| `{acronym}` | Ambiguous acronym | "'{acronym}' may be ambiguous. Please expand." |

### 3. Data Values

Specific values that need clarification.

| Placeholder | Description | Example Prompt |
|-------------|-------------|----------------|
| `{value}` | Numeric or text value | "'{medication} {value}' noted without unit." |
| `{time}` | Time value (HH:MM format) | "'{event}' at {time} — confirm AM or PM?" |
| `{wrong_unit}` | Incorrectly recorded unit | "'{vital}' recorded as {wrong_unit}. Confirm?" |

### 4. Contextual Detail

System-provided context about what triggered the prompt.

| Placeholder | Description | Example Prompt |
|-------------|-------------|----------------|
| `{detail}` | Specific detail in conflict | "Conflicting sources for '{detail}'. Which is primary?" |
| `{field}` | DRAATT field name | "'{field}' missing. Please provide." |

### 5. Timeline (Structure Prompts)

For timeline/sequence clarification prompts.

| Placeholder | Description | Example Prompt |
|-------------|-------------|----------------|
| `{dispatch}` | Dispatch time | "Dispatch: {dispatch}, On scene: {on_scene}..." |
| `{on_scene}` | On-scene time | (same as above) |
| `{event}` | Event description | "'{event}' at {time} — confirm?" |

---

## Design Principles

### Principle 1: Simple Confirmation Over Justification

Prompts should ask for **confirmation**, not **justification**.

**Avoid**: "Confirm if obtained; if not, state why."  
**Prefer**: "Were repeat vitals obtained?"

Asking "why" for every omission creates:
- Documentation noise in final reports
- Burden on Medics
- Defensive documentation habits

**Exception**: High-stakes safety scenarios (e.g., missing vitals after sedation) may warrant explanation prompts via dedicated safety benchmarks (A-SFT4).

---

## Usage Rules

### Rule 1: Quote User Speech

When showing what the user said, wrap the placeholder in quotes:

```yaml
# CORRECT
prompt_neutral: "You used '{phrase}'. Confirm..."

# INCORRECT
prompt_neutral: "You used {phrase}. Confirm..."
```

### Rule 2: Don't Quote System Context

When the system is describing something (not quoting the user), no quotes:

```yaml
# CORRECT
prompt_neutral: "Laterality conflict for {procedure}. Which side?"

# INCORRECT  
prompt_neutral: "Laterality conflict for '{procedure}'. Which side?"
```

### Rule 3: Static Prompts Are Valid

Some prompts don't need placeholders — they're always the same:

```yaml
# VALID - RSI prompt is always identical
prompt_neutral: "RSI noted. Confirm sedative, paralytic, ETT size/depth, and confirmation method."
```

---

## Complete Placeholder List

| Placeholder | Category | Quoted? | Used In |
|-------------|----------|---------|---------|
| `{phrase}` | User Speech | Yes | 01-negation |
| `{spoken}` | User Speech | Yes | 10-numeric-style |
| `{medication}` | Clinical Entity | Yes | 02-units, 06-data-gaps, 08-med-names |
| `{vital}` | Clinical Entity | Yes | 02-units |
| `{procedure}` | Clinical Entity | No | 05-contradictions |
| `{symptom}` | Clinical Entity | No | 01-negation |
| `{acronym}` | Clinical Entity | Yes | 07-acronyms |
| `{value}` | Data Value | No | 02-units |
| `{time}` | Data Value | No | 03-time |
| `{wrong_unit}` | Data Value | No | 02-units |
| `{detail}` | Context | Yes | 13-source |
| `{dispatch}` | Timeline | No | 04-structure |
| `{on_scene}` | Timeline | No | 04-structure |
| `{event}` | Timeline | Yes | 03-time, 04-structure |

---

## Dev Team Implementation Notes

The development team will:
1. Extract placeholder values from the benchmark failure context
2. Inject values into prompt templates at runtime
3. Handle missing placeholder values gracefully (omit or use "unknown")

---

*This schema defines the SME-approved placeholder taxonomy. Implementation details TBD by engineering.*

