# Advanced Topics

Research integration, iteration patterns, multi-model testing, and customization options.

## Claude A/B Iteration Pattern

The most effective skill development involves two roles:

- **Claude A** (this instance): The skill author helper that refines instructions
- **Claude B** (fresh instance with skill loaded): Tests the skill on real tasks

**Why this works**: Claude A understands agent needs, you provide domain expertise, Claude B reveals gaps through real usage.

### Creating a New Skill with A/B Pattern

1. **Complete a task without a skill** (with Claude A): Work through a problem using normal prompting. Notice what context you repeatedly provide.

2. **Identify the reusable pattern**: After completing the task, determine what context would be useful for similar future tasks.

3. **Ask Claude A to create the skill**: "Create a skill that captures the pattern we just used. Include [specific context, rules, workflows]."

4. **Review for conciseness**: Check that Claude A hasn't added unnecessary explanations. Ask: "Remove explanations Claude already knows."

5. **Test with Claude B**: Use the skill with a fresh Claude instance on related tasks. Observe whether Claude B finds the right information.

6. **Iterate based on observation**: If Claude B struggles, return to Claude A with specifics: "When Claude used this skill, it forgot to [X]. Should we add a section about [Y]?"

### Iterating on Existing Skills

1. **Use the skill in real workflows**: Give Claude B actual tasks, not test scenarios
2. **Observe Claude B's behavior**: Note struggles, successes, unexpected choices
3. **Return to Claude A for improvements**: Share SKILL.md and describe observations
4. **Apply and test changes**: Update the skill, test again with Claude B
5. **Repeat**: Continue observe-refine-test cycle

### What to Watch For

- **Unexpected exploration paths**: Does Claude read files in unexpected order?
- **Missed connections**: Does Claude fail to follow references?
- **Overreliance on sections**: If Claude repeatedly reads the same file, move content to SKILL.md
- **Ignored content**: If Claude never accesses a file, it might be unnecessary

---

## Multi-Model Testing

Skills behave differently across Claude models. Test with all models you plan to use.

### Testing Considerations by Model

| Model | Characteristic | What to Test |
|-------|---------------|--------------|
| **Claude Haiku** | Fast, economical | Does skill provide enough explicit guidance? |
| **Claude Sonnet** | Balanced | Is skill clear and efficient? |
| **Claude Opus** | Powerful reasoning | Does skill avoid over-explaining? |

### Model-Specific Patterns

**What works for Opus might need more detail for Haiku**:
- Opus can infer from context; Haiku benefits from explicit steps
- Opus handles ambiguous instructions; Haiku needs clearer decision points
- Opus reads between the lines; Haiku follows instructions literally

### Testing Workflow

1. **Pick 3 representative tasks** that exercise the skill
2. **Run each task** on Haiku, Sonnet, and Opus
3. **Compare outputs**: Does quality vary significantly?
4. **Adjust if needed**: Add detail for Haiku or remove redundancy for Opus
5. **Document model expectations** if skill is model-specific

---

## Research Integration

The factory can invoke the `background-research` skill for time-sensitive topics.

### When Research is Auto-Invoked

**Invoke for**:
- Frameworks or methodologies (copywriting patterns, analysis workflows)
- Tools or technologies (libraries, platforms, APIs)
- Best practices that evolve (SEO/AEO, social media)
- Industry standards or conventions

**Skip for**:
- Evergreen tasks (meeting notes to action items)
- Fixed specifications (file format schemas)
- User-provided complete specifications

### Research Parameters

```
Topic: [skill domain from user request]
Current Date: [YYYY-MM-DD]
Focus Areas: [frameworks/tools/templates/methodologies]
Research Depth: standard (2-3 searches) or comprehensive (5+ searches)
```

### Using Research Findings

- **Core Principles**: Incorporate evidence-based rules
- **references/**: Include current frameworks and templates
- **Keywords**: Add contemporary terminology
- **Description**: Add temporal context ("as of October 2025")
- **Citations**: Preserve source citations for statistics

### Citation Format

**Required for**: Specific statistics, timeframes, performance metrics

Format: "[claim] (Source: [Publication], [Year])"

Example:
```
"57% of searches show AI Overviews as of October 2025 (Source: CXL, BrightEdge, Ahrefs 2025)"
```

### Research Archiving

Archive filename: `research-archive/YYYY-MM-DD-HHMM-topic-kebab.md`

Include in generated skill: `references/research-findings.md`

---

## User-Controllable Variables

Customize skill generation by specifying:

### 1. Business/Domain Type
**Default**: General business/productivity

Examples: Financial services, Healthcare, E-commerce, Software development, Marketing, Legal, Manufacturing, Education

### 2. Use Cases
**Default**: General-purpose skills

Examples:
- "Analyze quarterly sales reports and identify trends"
- "Generate customer support response templates"
- "Create technical specifications from user stories"

### 3. Number of Skills
**Default**: 1 skill per request

Range: 1-10 skills

### 4. Overlap Preference
**Default**: Mutually exclusive

Options:
- `mutually exclusive` - Distinct, non-overlapping functionality
- `overlapping` - Complementary or overlapping capabilities
- `workflow-chained` - Skills designed to work together in sequence

### 5. Complexity Level
**Default**: Intermediate

Options:
- `beginner` - Simple workflows, minimal scripts
- `intermediate` - Moderate complexity, some scripts
- `advanced` - Complex workflows, multiple scripts, edge case handling

### 6. Script Preference
**Default**: Only when necessary

Options:
- `only when necessary` - Scripts only for fragile operations
- `prefer scripts` - Include scripts when they add reliability
- `minimal scripts` - Text instructions preferred

### 7. Research Depth
**Default**: Auto-detect

Options:
- `auto` - Factory determines based on skill type
- `skip` - No web research (fast, for evergreen skills)
- `standard` - 2-3 targeted searches
- `comprehensive` - 5+ searches for thorough investigation

---

## Example Requests

### Simple Request
```
Generate a skill for analyzing customer feedback from CSV files
```

### Detailed Request
```
Generate 3 intermediate skills for financial services:
- Quarterly report analysis with trend identification
- Risk assessment summaries from audit data
- Regulatory compliance documentation generator

Complexity: intermediate
Script preference: only when necessary
```

### Domain-Specific Request
```
Domain: E-commerce/retail
Generate 2 skills:
1. Customer purchase pattern analysis from CSV exports
2. Product description templates with SEO optimization

Overlap: mutually exclusive
```

### Quick Request
```
Create a beginner skill for converting meeting notes to action items
```

