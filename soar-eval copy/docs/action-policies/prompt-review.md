# User Prompt Review (Medical SME)

**Status**: Draft for Review  
**Purpose**: Evaluate prompt tone and wording for field Medic appropriateness

---

## Review Criteria

1. **Clarity** — Is the question unambiguous?
2. **Brevity** — Can it be answered quickly in the field?
3. **Clinical relevance** — Does it ask for information the Medic actually knows?
4. **Tone** — Professional but not condescending?

---

## Prompt-by-Prompt Review

### 01-negation: Double Negative

**Current**:
> "You used '{phrase}'. Confirm: {symptom} present or absent?"

**Assessment**: Good. Direct, binary choice, easy to answer.

**Response type**: `select_one` [present, absent]

**Recommendation**: Keep as-is.

---

### 02-units: EtCO2 Percent

**Current**:
> "EtCO₂ recorded as %. Confirm mmHg value?"

**Assessment**: Good. Medics know EtCO₂ is in mmHg, not percent.

**Response type**: `numeric_value`

**Recommendation**: Keep as-is.

---

### 02-units: Dose Missing Unit

**Current**:
> "'Fentanyl 125' noted without unit. Confirm unit and route?"

**Assessment**: Appropriate. Common ASR artifact where unit gets dropped.

**Response type**: `select_one` [125 mcg IV, 125 mcg IN, other]

**Recommendation**: Consider expanding options based on common doses. Example options should be dynamically generated based on medication.

**Enhancement**: Template should support `{medication}` and `{value}` placeholders.

---

### 03-time: Ambiguous HH:MM

**Current**:
> "Nitro at 9:00 — confirm 09:00 or 21:00?"

**Assessment**: Good. Common 12/24 hour ambiguity.

**Response type**: `time_hhmm`

**Enhancement**: Template should support `{medication}` and `{time}` placeholders.

---

### 04-structure: Timeline Mismatch

**Current**:
> "Timeline mismatch. Currently: dispatch {dispatch}, on scene {on_scene}, last known well {lkw}. Confirm/correct order."

**Assessment**: May be too verbose. Consider splitting into specific clarifications.

**Response type**: `text_short`

**Recommendation**: Consider breaking into specific time clarifications rather than presenting all times at once.

---

### 05-contradictions: Laterality

**Current**:
> "Left vs right documented. Which side is correct?"

**Assessment**: Good. Clear, direct, critical for procedures.

**Response type**: `select_one` [left, right, bilateral]

**Recommendation**: Keep as-is.

---

### 06-data-gaps: Second Vitals

**Current**:
> "Second vitals set missing or unclear. Were repeat vitals obtained?"

**Assessment**: Good. Simple confirmation without requiring justification for omission.

**Response type**: `text_short`

**Recommendation**: Keep as-is. Avoid "if not, state why" pattern — creates documentation noise.

---

### 06-data-gaps: Dose/Route Incomplete

**Current**:
> "Dose/route/time incomplete. Confirm dose, route, and time for relevant meds."

**Assessment**: Too vague. Should specify which medication.

**Response type**: `text_short`

**Enhancement**: Template should support `{medication}` placeholder.

**Proposed**:
> "{medication} — dose, route, or time unclear. Please confirm."

---

### 07-acronyms: Clarify

**Current**:
> "Acronym may be ambiguous. Expand the acronym(s) as intended."

**Assessment**: Too vague. Should specify which acronym.

**Response type**: `text_short`

**Enhancement**: Template should support `{acronym}` placeholder.

**Proposed**:
> "'{acronym}' — please confirm full term."

---

### 08-med-names: Brand/Generic

**Current**:
> "Medication naming. Confirm brand vs generic or provide both."

**Assessment**: Low priority. Most EMS systems normalize medication names.

**Response type**: `text_short`

**Recommendation**: May be unnecessary if Medic Copilot normalizes internally.

---

### 10-numeric-style: Spoken Number

**Current**:
> "You spoke a number ('two oh three'). Confirm numeric value?"

**Assessment**: Good for ASR artifacts where numbers are spelled out.

**Response type**: `numeric_value`

**Enhancement**: Template should support `{spoken}` placeholder.

---

### 11-rsi: Core Details

**Current**:
> "RSI noted. Confirm sedative, paralytic, ETT size/depth, and confirmation method."

**Assessment**: Appropriate for RSI documentation, which has specific required fields.

**Response type**: `text_short`

**Recommendation**: Consider structured response with specific fields rather than free text.

**Enhancement**: Could be `multi_field` response type:
- Sedative: ___
- Paralytic: ___
- ETT size: ___
- Depth: ___
- Confirmation: [waveform, auscultation, colorimetric]

---

### 12-disposition: Conflict

**Current**:
> "Refusal noted but transport documented. Which final disposition applies?"

**Assessment**: Critical clarification. Disposition drives billing and QA.

**Response type**: `select_one` [refusal, transported, cancelled]

**Recommendation**: Keep as-is.

---

### 13-source: Attribution

**Current**:
> "Patient vs bystander accounts conflict. Which source is primary for this detail?"

**Assessment**: Useful for history clarification.

**Response type**: `select_one` [patient, bystander, provider]

**Enhancement**: Should specify which detail is in conflict.

---

### 14-arrest: Sequence Consistency

**Current**:
> "Defib/rhythm sequence seems inconsistent. Confirm rhythm immediately before and after shock?"

**Assessment**: Critical for cardiac arrest QA.

**Response type**: `text_short`

**Recommendation**: Consider structured response:
- Pre-shock rhythm: [VF, VT, asystole, PEA]
- Post-shock rhythm: [VF, VT, asystole, PEA, ROSC]

---

## Summary of Enhancements

| Category | Enhancement |
|----------|-------------|
| **Placeholders** | Add `{medication}`, `{time}`, `{acronym}`, `{spoken}` to templates |
| **Response types** | Consider `multi_field` for RSI and arrest details |
| **Specificity** | Vague prompts should specify what needs clarification |
| **Priority review** | `08-med-names` may be unnecessary |

---

## Tone Guidance

All prompts should:
- Be **direct** — Medics are busy
- Avoid **condescension** — They know their job
- Provide **context** — Why is this being asked?
- Allow **explanation** — Sometimes omissions are intentional

---

*This review is from Medical SME perspective. Implementation details TBD.*

