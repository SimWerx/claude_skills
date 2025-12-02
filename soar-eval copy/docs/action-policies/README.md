# Action Policies

**Status**: Draft for CTO Review  
**Purpose**: Extend SOAR evaluation framework with correction loops and user escalation

---

## Contents

| File/Folder | Description |
|-------------|-------------|
| `action-policies.md` | Main proposal — correction loops, action routing, event bus integration |
| `PLACEHOLDER_SCHEMA.md` | Placeholder taxonomy for prompt templates |
| `user-prompts/` | Pre-written Medic clarification prompts (13 YAMLs) |
| `benchmark-to-prompt-map.json` | Maps benchmark codes to user escalation prompts |
| `prompt-review.md` | Detailed SME assessment of each prompt *(reference material)* |

---

## How It Works

When a benchmark detects an error that Medic Copilot cannot self-correct, the system asks the Medic for clarification. The `user-prompts/` folder contains **pre-written clarification prompts** for each type of error.

**Flow**:
1. Benchmark fires (e.g., A-NEG1 detects negation ambiguity)
2. Agent attempts self-correction (re-reads ASR source)
3. If agent fails → lookup prompt via `benchmark-to-prompt-map.json`
4. Surface prompt to Medic (using appropriate tone)
5. Medic responds → correction applied to output

---

## Quick Links

- **Proposal**: [action-policies.md](action-policies.md) — Start here
- **Prompt Review**: [prompt-review.md](prompt-review.md) — SME assessment of each prompt
- **Benchmark Mapping**: [benchmark-to-prompt-map.json](benchmark-to-prompt-map.json) — Which benchmarks use which prompts

---

## User Prompt Schema (SME-Focused)

Each prompt in `user-prompts/` uses a simplified schema focused on SME deliverables:

```yaml
prompts:
  - id: negation-double-negative
    
    # Prompt wording (both tones)
    prompt_neutral: "You used '{phrase}'. Confirm: {symptom} present or absent?"
    prompt_medic_copilot: "Medic Copilot detected '{phrase}'. Confirm: {symptom} present or absent?"
    
    # Response structure
    response_type: select_one
    options: [present, absent]
    
    # Clinical context
    severity: warn
    examples:
      - "denies no chest pain"
      - "patient states no history of no diabetes"
```

### SME-Defined Fields

| Field | Purpose |
|-------|---------|
| `id` | Unique identifier (referenced by benchmark map) |
| `prompt_neutral` | Medic-facing wording (reviewing own dictation) |
| `prompt_medic_copilot` | System-detected wording (QA/audit context) |
| `response_type` | What kind of answer: `select_one`, `text_short`, `numeric_value`, `time_hhmm` |
| `options` | Valid responses (for `select_one` type) |
| `severity` | Clinical importance: `warn` or `info` |
| `examples` | Clinical scenarios that trigger this prompt |

### Dev Team Adds (Implementation Layer)

The development team will add engineering concerns in their implementation:
- Priority ordering, cooldown, deduplication (UX behavior)
- Template routing, trigger mapping
- Data model (where responses are stored)
- Versioning and localization

---

## Response Types

| Type | Description | Example Use |
|------|-------------|-------------|
| `select_one` | Single choice from predefined options | Present/absent, left/right/bilateral |
| `text_short` | Free-text clarification | Dose/route/time confirmation |
| `numeric_value` | Numeric input | EtCO2 in mmHg, weight in kg |
| `time_hhmm` | Time in 24-hour format | Clarify 9:00 as 09:00 or 21:00 |

---

## Prompt Tone Selection

| Context | Tone Key | Example |
|---------|----------|---------|
| Medic reviewing own dictation | `prompt_neutral` | "You used 'denies no pain'. Confirm: pain present or absent?" |
| QA review or audit | `prompt_medic_copilot` | "Medic Copilot detected 'denies no pain'. Confirm: pain present or absent?" |

---

## Pending CTO Decision

**Open Question**: Should action policies be defined at the **benchmark** level or **rubric** level?

See [action-policies.md](action-policies.md#open-question-for-cto) for details.

---

*See `action-policies.md` for the full proposal.*
