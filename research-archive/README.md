# Research Archive

This directory contains archived research from the `background-research` skill. Each file represents a research session that informed skill generation, providing audit trails for fact-checking, temporal tracking, and knowledge reuse.

## Purpose

- **Auditability**: Track what evidence informed skill decisions and verify source citations
- **Reusability**: Research can inform multiple related skills (batch generation efficiency)
- **Fact-Checking**: Source citations available for verification and credibility assessment
- **Currency Tracking**: Know when research was conducted to assess if skills need updating
- **Temporal Knowledge**: Compare research over time to see how domain knowledge evolved
- **Team Transparency**: Shared understanding of WHY skills were generated with specific recommendations

## Why Research is Version Controlled

Research archives are **committed to git** (unlike `generated-skills/` which are gitignored) because:

- **Research = INPUT**: Documents reasoning and evidence that informed decisions
- **Skills = OUTPUT**: Generated code that can be regenerated from research
- **Different purposes**: Research explains WHY, skills are derivative WHAT
- **Team value**: Everyone sees research rationale, enabling reproducible decisions
- **Temporal record**: Captures what was known at the time skill was created

## File Naming Convention

**Pattern**: `YYYY-MM-DD-HHMM-topic-kebab.md`

**Components**:
- **Date**: YYYY-MM-DD (sortable, chronological)
- **Time**: HHMM (24-hour format, prevents same-day collisions)
- **Topic**: kebab-case topic slug (max 50 chars)

**Examples**:
- `2025-10-25-1430-ai-engine-optimization.md`
- `2025-10-26-0915-copywriting-hook-frameworks.md`
- `2025-10-26-1420-python-csv-libraries.md`

**Collision handling**: If same topic researched twice in same minute (rare), append sequence: `2025-10-25-1430-topic-02.md`

## File Structure

Each research archive contains:

### YAML Frontmatter (Structured Metadata)

```yaml
---
research_date: 2025-10-25
topic: AI Engine Optimization (AEO) for conversational search platforms
generated_for_skill: ai-engine-optimization
confidence_level: High
sources: CXL, BrightEdge, Ahrefs, SurferSEO, Passionfruits
focus_areas: Frameworks, optimization techniques, content structure, E-E-A-T
---
```

**Fields**:
- `research_date`: When research was conducted (YYYY-MM-DD)
- `topic`: Full descriptive research topic
- `generated_for_skill`: Skill name this research informed
- `confidence_level`: Quality assessment (High/Medium/Low)
- `sources`: Comma-separated source names
- `focus_areas`: What was investigated

### Content Sections

1. **Research Summary**: Date, topic, focus areas
2. **Key Findings**: 3-5 actionable insights with source citations
3. **Recommended Frameworks/Tools**: Current best practices as of research date
4. **Temporal Context**: What changed, current standards, deprecated approaches
5. **Confidence Level**: Quality assessment with rationale

## Usage

### Referencing Research in Skills

Skills generated with research include pointers in SKILL.md:

```html
<!--
Generated with research on 2025-10-25 14:30.
Research archive: research-archive/2025-10-25-1430-ai-engine-optimization.md
Progressive disclosure: See references/research-findings.md for full research context.
-->
```

### Dual Storage: Archive + ZIP Inclusion

Research is stored in **two locations**:

1. **research-archive/** (this directory)
   - Source of truth for local development
   - Version controlled in git
   - Enables fact-checking and temporal comparison

2. **references/research-findings.md** (in generated skill)
   - Copy of research included in skill ZIP
   - Uploaded to Claude.ai with skill
   - Available as progressive disclosure context
   - Users can say "review your research findings" after skill upload

This dual approach provides both **local auditability** and **portable context**.

### Fact-Checking Sources

To verify claims in generated skills:

1. Open research archive file (filename in SKILL.md HTML comment)
2. Check "Key Findings" section for source citations
3. Verify sources are recent (2024-2025 preferred) and authoritative
4. Review "Confidence Level" rationale
5. Cross-reference specific statistics (e.g., "57% of searches") with sources listed

### Updating Skills with New Research

When updating an existing skill:

1. Run `background-research` skill with same topic
2. Compare new archive file to old one (same topic, different dates)
3. Identify what changed (new frameworks, updated statistics, deprecated approaches)
4. Update skill if findings changed significantly
5. Note update in skill HTML comment with new archive filename

### Temporal Comparison

Compare how domain knowledge evolved:

```bash
# Find all research on specific topic
ls research-archive/*ai-engine-optimization*

# Output:
# 2025-10-25-1430-ai-engine-optimization.md
# 2026-03-15-1045-ai-engine-optimization.md

# Compare what changed in 5 months
diff research-archive/2025-10-25-*-ai-engine-optimization.md \
     research-archive/2026-03-15-*-ai-engine-optimization.md
```

### Batch Research Reuse

When generating multiple related skills:

```markdown
Research once with comprehensive depth:
- Topic: Financial services frameworks
- Focus: Risk assessment, compliance, portfolio analysis, reporting

Then reference same archive from multiple skills:
- risk-assessment-analyzer/SKILL.md → points to same archive
- compliance-documentation/SKILL.md → points to same archive
- portfolio-analysis/SKILL.md → points to same archive
```

Benefits: Research once, reuse for multiple skills. More efficient than separate research sessions.

## Maintenance

### Cleanup Recommendations

**When to archive old research**:
- Research older than 12-18 months (domains evolve)
- Deprecated frameworks or tools no longer relevant
- Skills that were regenerated with updated research

**How to archive**:
```bash
# Create archive subdirectory for old research
mkdir research-archive/archived-2024

# Move old research
mv research-archive/2024-*.md research-archive/archived-2024/
```

### Re-Research Triggers

Consider re-researching when:
- Skill recommendations seem outdated (18+ months old)
- Major industry changes (new platforms, frameworks, regulations)
- User reports statistics or sources are stale
- Confidence level was Medium/Low and better sources now available

### Organization at Scale

**Current**: Flat structure (works well for <100 files)

**If archive grows large** (100+ files), consider:
- Monthly subdirectories: `research-archive/2025-10/`, `research-archive/2025-11/`
- Annual subdirectories: `research-archive/2025/`, `research-archive/2026/`
- Topic-based subdirectories: `research-archive/seo/`, `research-archive/data-analysis/`

Reorganize only when needed (YAGNI principle).

## Future Enhancements

### Research Reuse Detection (Planned)

Before conducting new research, check for recent related research:

```bash
# Look for research on same topic from last 30 days
find research-archive/ -name "*${topic_slug}*" -mtime -30
```

If recent research found:
- Option 1: Reuse findings (saves tokens/time)
- Option 2: Ask user: "Research from 2025-10-15 exists. Reuse or refresh?"
- Option 3: Always refresh (default for currency)

### Auto-Generated Index (Planned)

Generate `research-archive/index.md` with metadata table:

| Date | Topic | Skill | Confidence | Sources |
|------|-------|-------|------------|---------|
| 2025-10-25 | AEO | ai-engine-optimization | High | CXL, BrightEdge, Ahrefs |
| 2025-10-26 | Hooks | copywriting-hooks | High | HubSpot, CMI, Copyblogger |

Enables quick discovery of existing research without scanning filenames.

## Example Research Archive

**Filename**: `2025-10-25-1430-ai-engine-optimization.md`

```markdown
---
research_date: 2025-10-25
topic: AI Engine Optimization (AEO) for conversational search platforms
generated_for_skill: ai-engine-optimization
confidence_level: High
sources: CXL, BrightEdge, Ahrefs, SurferSEO, Passionfruits, AirOps
focus_areas: Frameworks, optimization techniques, content structure, E-E-A-T, platform-specific strategies
---

# Research: AI Engine Optimization (AEO)

**Generated**: 2025-10-25 14:30
**For Skill**: ai-engine-optimization

---

## Research Summary
**Date**: 2025-10-25
**Topic**: AI Engine Optimization (AEO) for conversational search platforms
**Focus**: Frameworks, optimization techniques, content structure requirements, E-E-A-T principles, platform-specific strategies for ChatGPT/Perplexity/Claude/Gemini

## Key Findings
1. AEO focuses on zero-click citations with 57% of SERPs featuring AI Overviews as of June 2025 - Source: CXL, BrightEdge, Ahrefs 2025
2. Content freshness creates peak citation opportunity within 2-3 days (2% of citations) - Source: Startup GTM, Geneo 2025
[... rest of findings ...]

## Recommended Frameworks/Tools
- **Question-Answer (Q&A) Format**: Direct question-based headers with concise answers. Highest AI citation rates as of October 2025.
- **Schema.org JSON-LD Markup**: Required for competitive visibility (58% higher snippet appearance). Apply to all content types.
[... rest of frameworks ...]

## Temporal Context
- Notable changes since 2024: Featured snippet visibility declined 35% as AI Overviews replaced traditional snippets
- Current industry standards: Dual optimization for AI citations and featured snippets required
- Deprecated approaches: Keyword stuffing, optimizing only for Google
[... rest of context ...]

## Confidence Level
High - Based on 5 authoritative sources from 2024-2025 showing strong consensus on techniques

**Rationale**: Multiple industry-leading sources published within 12 months with consistent frameworks; cross-validated by platform guidelines; supported by measurable metrics from Ahrefs and McKinsey.
```

## Questions?

For questions about research archiving, see:
- [CLAUDE.md](../CLAUDE.md) - Repository conventions and architecture
- [SKILLS_FACTORY_GENERATOR_PROMPT.md](../SKILLS_FACTORY_GENERATOR_PROMPT.md) - How research is automatically archived
- [background-research skill](../generated-skills/background-research/) - Research methodology and output format
