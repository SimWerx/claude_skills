Use Case: Conduct targeted web research to gather current best practices, frameworks, and evidence for grounding skills in contemporary context.

Prompt:

Help me create a Skill called "background-research" that conducts targeted web research to ensure generated skills are grounded in current best practices and evidence.

## Skill Purpose
Research current information before generating skills or updating existing skills. Ensures skills reference up-to-date frameworks, tools, and methodologies with temporal grounding. This skill should be invoked automatically by the Skills Factory Generator for time-sensitive topics.

## When to Use This Skill
Invoke this skill automatically when:
- Generating skills about frameworks or methodologies (e.g., copywriting, SEO/AEO, data analysis patterns, workflow optimization)
- Generating skills about tools or technologies (libraries, platforms, APIs, software standards)
- User explicitly requests current best practices or latest information
- Skill domain involves time-sensitive information that evolves (social media, AI tools, marketing)

Skip research for:
- Evergreen skills with timeless workflows (e.g., "convert meeting notes to action items")
- Skills based on fixed specifications (file format schemas like OOXML, PDF structure)
- User has provided complete, current specification with all necessary details

## Required Inputs
When invoking this skill, provide:
1. **Topic/Domain** - What to research (e.g., "copywriting hook frameworks", "CSV data analysis best practices", "executive memo templates")
2. **Current Date** - For temporal grounding (auto-populate with today's date)
3. **Focus Areas** - Specific aspects to investigate (frameworks, tools, templates, metrics, methodologies)
4. **Research Depth** - `standard` (2-3 searches) or `comprehensive` (5+ searches across multiple sources)

## Output Format
Return structured findings in this EXACT format for easy parsing:

---
### Research Summary
**Date**: [current date in YYYY-MM-DD format]
**Topic**: [topic researched]
**Focus**: [focus areas specified]

### Key Findings
1. [Finding with evidence citation - source name and year]
2. [Finding with evidence citation - source name and year]
3. [Finding with evidence citation - source name and year]
4. [Additional finding if comprehensive depth]
5. [Additional finding if comprehensive depth]

### Recommended Frameworks/Tools
- **[Framework/Tool Name]**: [Why relevant, when to use, current status]
- **[Framework/Tool Name]**: [Why relevant, when to use, current status]
- **[Framework/Tool Name]**: [Why relevant, when to use, current status]

### Temporal Context
- Notable changes since [previous year]: [What's new or different]
- Current industry standards as of [current date]: [What's considered best practice now]
- Deprecated approaches to avoid: [What's outdated or no longer recommended]

### Confidence Level
[High/Medium/Low] - Based on source authority, recency, and consensus across sources

**Rationale**: [Brief explanation of confidence assessment]
---

## Research Methodology
Follow this workflow:

1. **Generate Targeted Search Queries**
   - Include current date or year in queries (e.g., "copywriting hook frameworks 2025")
   - Be specific, not generic (e.g., "AEO optimization techniques October 2025" not just "SEO tips")
   - Use 2-3 queries for standard depth, 5+ for comprehensive

2. **Execute Web Searches**
   - Prioritize authoritative sources from 2024-2025
   - Look for: Industry blogs, official documentation, recent case studies, expert analyses
   - Cross-reference multiple sources for validation

3. **Synthesize Findings**
   - Extract actionable insights, not copy-paste excerpts
   - Identify patterns and consensus across sources
   - Note contradictions or areas of uncertainty
   - Focus on practical, implementable recommendations

4. **Structure Output**
   - Use exact format specified above
   - Include source citations for credibility
   - Provide temporal context (what's new, what's changed)
   - Assess confidence based on source quality

5. **Quality Check**
   - Findings are specific and actionable (not generic advice)
   - Sources are recent (2024-2025 preferred)
   - Output answers the original focus areas
   - Temporal context is clear

## Core Principles
1. **Temporal grounding** - Always include current date in search queries and output
2. **Source quality** - Prioritize authority, recency, and relevance over volume
3. **Actionable synthesis** - Distill to 3-5 key insights, avoid information overload
4. **Evidence-based** - Include citations for all claims and recommendations
5. **Scope discipline** - Stay focused on specified topic and focus areas, avoid research rabbit holes
6. **Uncertainty acknowledgment** - Note when sources disagree or evidence is limited

## Additional Guidelines
- For tools/libraries: Include version numbers and current status (active/maintained/deprecated)
- For frameworks: Explain when to use and when to avoid
- For best practices: Note if they're consensus or emerging/controversial
- For temporal changes: Highlight what's different from previous years
- Always assess confidence level - helps downstream skill generation make informed decisions

## Integration with Skills Factory
This skill is designed to be invoked by the Skills Factory Generator. The structured output format allows the factory to:
- Extract key findings for "Core Principles" section
- Identify current frameworks for "references/" files
- Update terminology and keywords with contemporary terms
- Add temporal context to skill descriptions
- Include evidence citations for authority

Create this skill now and save it for use by the Skills Factory Generator and standalone research tasks.

---

## Bootstrap Notes

This seed file solves the bootstrap problem: How do you create a research skill without research?

**To regenerate/update this skill**:
1. Load SKILLS_FACTORY_GENERATOR_PROMPT.md in Claude Code
2. Request: `"Generate the skill described in skill-ideas/background_research.md"`
3. First generation: Skip research (use this complete specification as-is)
4. Future updates: Use the generated background-research skill to research best practices:
   ```
   Use background-research skill to research:
   Topic: Research methodology best practices
   Focus: Query formulation strategies, source evaluation criteria, synthesis techniques, confidence assessment frameworks
   Current Date: [Year]
   Depth: comprehensive
   ```
5. Apply findings to regenerate an improved version of the skill

**Self-improvement cycle**: The skill researches research methodology best practices, then uses those findings to improve itself. Each iteration incorporates latest advances in information synthesis, source evaluation, and evidence assessment.

**Maintenance cadence**: Annual review recommended to capture methodology evolution and emerging research best practices.

**Why this works**: Research skills improve through practicing research. The background-research skill is uniquely positioned to keep itself current by investigating its own domain.
