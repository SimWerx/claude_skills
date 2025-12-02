# Skill Ideas

This directory contains seed ideas for skills that can be generated using the Skills Factory Generator.

## How to Use

### 1. Load the Skills Factory Generator

In Claude Code or Cursor IDE:
```
Drag SKILLS_FACTORY_GENERATOR_PROMPT.md into your conversation
```

Claude will respond:
> "I am now ready to generate production-quality Claude skills..."

### 2. Reference Any Idea File

Simply tell Claude which idea to implement:
```
Generate the skill described in skill-ideas/video_script_generator.md
```

Or describe your own:
```
Generate a skill for analyzing customer feedback CSV files
```

### 3. Factory Creates Everything Automatically

Claude will generate:
- ✅ `SKILL.md` with complete content (not templates)
- ✅ `sample_prompt.md` with casual "Hey Claude!" test prompts
- ✅ `references/*.md` files with detailed templates
- ✅ `assets/*` files with realistic sample data
- ✅ `zips/skill-name.zip` ready for deployment

### 4. Deploy to Your Platform

**Claude.ai**: Upload the ZIP via Settings → Skills

**Claude Code Personal**:
```bash
unzip zips/skill-name.zip -d ~/.claude/skills/
```

**Claude Code Project** (team-shared):
```bash
unzip zips/skill-name.zip -d .claude/skills/
git add .claude/skills/skill-name/
git commit -m "Add skill-name skill"
```

---

## File Format

Each file contains a natural language skill request with:
- **Skill Purpose** - What it does
- **When to Use** - Specific triggers
- **Required Inputs** - What to ask users for
- **Output Format** - How results should be structured
- **Best Practices** - Key frameworks and guidelines

The Skills Factory Generator transforms these descriptions into production-ready skills.

---

## Implemented Skills

✅ **hook-creator** (from `hook_creator.md`)
- Status: Generated and production-ready
- Location: Available in repository as reference
- Purpose: Generate attention-grabbing headlines using 10 copywriting frameworks

---

## Available Skill Ideas (Ready to Generate)

| Skill Idea | Use Case | Complexity |
|------------|----------|------------|
| `video_script_generator.md` | TikTok, Reels, YouTube scripts | Medium |
| `brand_voice_guide.md` | Brand voice documentation | Medium |
| `email_sequence_builder.md` | Multi-email campaigns | Medium |
| `competitor_content_gap_analyzer.md` | Content strategy research | High |
| `AI_engine_optimization.md` | AEO for AI search engines | High |
| `landing_pg_optimizer.md` | Landing page optimization | Medium |
| `social_media_content.md` | Social media content creation | Medium |
| `mini_problem_solver.md` | Quick problem solving | Low |
| `pdcast_show_notes_promotion.md` | Podcast content workflow | Medium |

---

## Creating Your Own Skill Ideas

Want to add your own? Follow the existing file format:

```markdown
Use Case: [One-line description]

Prompt:

Help me create a Skill called "[skill-name]" that [does what].

## Skill Purpose
[What it accomplishes]

## When to Use This Skill
Invoke this skill whenever I need to:
- [Use case 1]
- [Use case 2]

## Required Inputs
When I invoke this skill, ask me for:
1. [Input 1] - [description]
2. [Input 2] - [description]

## Output Format
[How results should be structured]

## [Other relevant sections]
```

Then use the Skills Factory Generator to build it!

---

## Tips for Best Results

1. **Be specific about triggers** - "When analyzing CSV files with customer feedback columns"
2. **Provide frameworks** - If you have 10 copywriting patterns, list them
3. **Include templates** - Show exact output structure you want
4. **Add examples** - Realistic sample data helps
5. **Define principles** - 3-5 key rules the skill should follow

The more specific your seed idea, the better the generated skill.
