# Corpus Validator Mapping

**Purpose**: Bridge between the synthetic ASR corpus validators/schemas and the SOAR evaluation benchmarks for Medic Copilot.

**Key Insight**: The corpus validators are a first-generation "A-component" for transcript authorship quality. The SOAR benchmarks apply the same detection patterns to Medic Copilot's outputs.

---

## Corpus Integration: Why This Project Lives Here

The `soar-pydantic-eval/` folder is intentionally nested within the larger `synthetic-data-gen/` repository because:

1. **Ground Truth Proximity**: The synthetic ASR corpus (`asr/v3.0/`) provides ground truth for evaluation. YAML frontmatter defines what Medic Copilot should extract.

2. **Pattern Reuse**: Corpus validators (`tools/validate_*.py`) contain battle-tested regex detectors, section keyword logic, and consistency checks that directly inform benchmark implementations.

3. **Shared Vocabulary**: Terms like "DRAATT", "required_coverage", "artifact tags", and section names are defined once in the corpus schemas.

4. **Single Context Window**: AI-paired programming agents can see both corpus structure AND evaluation framework in one workspace.

### The Relationship

```
Synthetic ASR Corpus                    Medic Copilot Evaluation
─────────────────────                   ────────────────────────
asr/v3.0/*.md                    →      Input to Medic Copilot
  └─ YAML frontmatter            →      Ground truth for comparison
  └─ ASR body                    →      What Medic Copilot processes

tools/validate_*.py              →      Detection patterns to reuse
schemas/*.yaml                   →      Taxonomies (sections, acronyms, keywords)

Validates transcript authorship  →      Validates Medic Copilot extraction
```

---

## Rubric Glossary (A-Component)

Each rubric groups related benchmarks. Current definitions are in `rubrics/*.yaml`.

| Rubric | Label | Description | Benchmarks |
|--------|-------|-------------|------------|
| A-NEG | Negation Handling | Correct interpretation of negated findings | [`A-NEG1`](../benchmarks/a-component/A-NEG1.yaml), [`A-NEG2`](../benchmarks/a-component/A-NEG2.yaml), [`A-NEG3`](../benchmarks/a-component/A-NEG3.yaml), [`A-NEG4`](../benchmarks/a-component/A-NEG4.yaml) |
| A-FCT | Fact Extraction | Accuracy of clinical fact extraction (vitals, meds, demographics) | [`A-FCT1`](../benchmarks/a-component/A-FCT1.yaml), [`A-FCT4`](../benchmarks/a-component/A-FCT4.yaml) |
| A-TMP | Temporal Ordering | Event sequence and trend accuracy | [`A-TMP1`](../benchmarks/a-component/A-TMP1.yaml), [`A-TMP2`](../benchmarks/a-component/A-TMP2.yaml) |
| A-EVD | Evidence Attribution | Facts supported by narrative spans | [`A-EVD1`](../benchmarks/a-component/A-EVD1.yaml) |
| A-CMP | Completeness | DRAATT section coverage | [`A-CMP1`](../benchmarks/a-component/A-CMP1.yaml), [`A-CMP5`](../benchmarks/a-component/A-CMP5.yaml), [`A-CMP6`](../benchmarks/a-component/A-CMP6.yaml), [`A-CMP6-airport`](../benchmarks/a-component/A-CMP6-airport.yaml) |
| A-SFT | Safety Flags | Dose safety, contraindications, reassessment | [`A-SFT1`](../benchmarks/a-component/A-SFT1.yaml), [`A-SFT2`](../benchmarks/a-component/A-SFT2.yaml), [`A-SFT4`](../benchmarks/a-component/A-SFT4.yaml) |
| A-PRT | Protocol Tracking | Protocol step detection (RSI, STEMI) | [`A-PRT1`](../benchmarks/a-component/A-PRT1.yaml), [`A-PRT2`](../benchmarks/a-component/A-PRT2.yaml) |
| A-FMT | Format Validity | JSON structure, required fields | [`A-FMT1`](../benchmarks/a-component/A-FMT1.yaml) |

---

## Evaluator Types

| Type | Value | Description | When to Use |
|------|-------|-------------|-------------|
| Code-based | `code` | Deterministic Python checks | Schema validation, regex matching, coverage |
| LLM-as-Judge | `llm_judge` | Rubric-based LLM evaluation | Fuzzy behaviors, clinical judgment |
| Hybrid | `hybrid` | Code prefilter + LLM verification | Complex checks with judgment component |
| Manual SME | `manual_sme` | Human expert review | Safety-critical, novel failures |

**Design principle**: Evaluators should be atomic ("sniper shots"). Composite aggregation happens at the rubric level, not inside individual checks.

---

## Validator → Benchmark Mapping

### Schema / Format Correctness → A-FMT

| Corpus Tool | Pattern | Benchmark | Notes |
|-------------|---------|-----------|-------|
| `validate_frontmatter.py` | YAML schema validation | A-FMT1 | Same pattern for `draatt_json` |
| `schemas/frontmatter.v1.json` | Required fields, enums | A-FMT1 | Field compliance |

**Reuse**: The frontmatter schema validation pattern becomes DRAATT JSON validation.

### Coverage / Completeness → A-CMP

| Corpus Tool | Pattern | Benchmark | Notes |
|-------------|---------|-----------|-------|
| `validate_template.py` | `required_coverage` flags | A-CMP1 | Section-level presence |
| `schemas/section_keywords.v1.yaml` | Keyword detection | A-CMP1, A-CMP5, A-CMP6 | What triggers section detection |
| Template validators | DOA pronouncement fields | A-CMP5 | Template-specific completeness |
| Template validators | Airport transfer fields | A-CMP6-airport | Template-specific completeness |

**Reuse**: `_validate_coverage_consistency()` logic → `draatt_has_[section]` checks.

### YAML ↔ Body Consistency → A-FCT, A-EVD

| Corpus Tool | Pattern | Benchmark | Notes |
|-------------|---------|-----------|-------|
| `validate_consistency.py` | Regex detectors for vitals | A-FCT1 | `vitals_f1` extraction accuracy |
| `validate_consistency.py` | Med/dose matching | A-FCT1 | Medication extraction |
| `validate_consistency.py` | Span-finding logic | A-EVD1 | Evidence attribution |

**Reuse**: Ground-truth YAML vs Medic Copilot extraction alignment.

### Safety / Negation / Temporal → A-SFT, A-NEG, A-TMP

| Corpus Tool | Pattern | Benchmark | Notes |
|-------------|---------|-----------|-------|
| `detect_artifacts.py` | `negation_risk` detection | A-NEG1, A-NEG2, A-NEG3, A-NEG4 | Negation patterns |
| `detect_artifacts.py` | `contradiction_notes` | A-NEG4 | Internal contradictions |
| `validate_template.py` | RSI meds with dose/route | A-SFT1 | Dose safety |
| `validate_template.py` | RSI ETT/EtCO₂ requirements | A-PRT1 | Protocol completeness |
| Template validators | Repeat vitals after intervention | A-SFT4 | Reassessment checks |

**Reuse**: Artifact detection logic → benchmark prefilters or LLM prompt context.

### Shared Taxonomies → Cross-Cutting Utilities

| Corpus Resource | Used By Benchmarks | Pattern |
|-----------------|-------------------|---------|
| `schemas/section_keywords.v1.yaml` | A-CMP*, A-PRT* | Section presence detection |
| `schemas/medical_acronyms.v1.yaml` | A-FCT*, A-FMT* | Acronym normalization |
| `tools/detect_artifacts.py` | A-NEG*, A-SFT*, A-TMP* | Risk pattern detection |

---

## Implementation Mapping

When implementing benchmarks as Pydantic Evals evaluators:

| Benchmark | Evaluator Type | Source Pattern | Implementation Notes |
|-----------|---------------|----------------|---------------------|
| A-FMT1 | `code` | `validate_frontmatter` | `draatt_json_is_valid()` |
| A-CMP1 | `code` | `validate_template` + `section_keywords` | `draatt_has_core_sections()` |
| A-CMP5 | `code` | DOA template rules | `doa_pronouncement_complete()` |
| A-CMP6-airport | `code` | Airport transfer rules | `airport_fields_complete()` |
| A-FCT1 | `hybrid` | `validate_consistency` regexes | `vitals_extraction_correct()` + LLM |
| A-NEG1 | `hybrid` | `detect_artifacts` negation | Code prefilter + `negation_simple_prompt.md` |
| A-NEG4 | `llm_judge` | `contradiction_notes` pattern | `contradiction_prompt.md` |
| A-SFT1 | `code` | RSI dose rules | `dose_within_safe_range()` |
| A-SFT2 | `code` | Allergy/contraindication logic | `contraindication_check()` |
| A-PRT1 | `code` | RSI template requirements | `rsi_critical_fields_present()` |
| A-EVD1 | `hybrid` | Span-finding in `validate_consistency` | `evidence_spans_valid()` + LLM |

---

## Related Resources

### Corpus (Ground Truth)
- `asr/v3.0/` — Synthetic ASR transcripts with YAML frontmatter
- `schemas/frontmatter.v1.json` — Authoritative YAML schema
- `schemas/section_keywords.v1.yaml` — Section detection keywords
- `schemas/medical_acronyms.v1.yaml` — Medical acronym registry

### Validators (Detection Patterns)
- `tools/validate_frontmatter.py` — Schema compliance
- `tools/validate_consistency.py` — YAML ↔ body alignment (regex detectors)
- `tools/validate_template.py` — Template-specific rules
- `tools/detect_artifacts.py` — Artifact pattern detection

### SOAR Benchmarks
- `rubrics/*.yaml` — Rubric definitions (8 files)
- `benchmarks/a-component/*.yaml` — Benchmark definitions (20 files)
- `evaluators/llm-judge/*.md` — LLM-as-a-judge prompts (10 files)

### Documentation
- `benchmarks/FIELD_SPECS.md` — Benchmark field specifications
- `rubrics/FIELD_SPECS.md` — Rubric field specifications
- `evaluators/llm-judge/PROMPT_SPECS.md` — Prompt structure specifications
