# Claude Agent Skills - Engineering Blog Insights

> **Source**: Anthropic Engineering Blog - https://www.anthropic.com/engineering/agent-skills
> **Purpose**: Key insights that informed repository best practices (emphatic language, progressive disclosure)
> **Last Synced**: October 2025

## Motivation

From Anthropic's engineering blog post...

Real work requires procedural knowledge and organizational context.

(Especially true for knowledge work)

This led us to create Agent Skills: organized folders of instructions, scripts, and resources that agents can discover and load dynamically to perform better at specific tasks. Skills extend Claude’s capabilities by packaging your expertise into composable resources for Claude, transforming general-purpose agents into specialized agents that fit your needs.

The key here is the "load dynamically" part. More on that later. Let's first breakdown what a skill actually is.

Skill Anatomy
Skills are just a folder with an instruction file SKILL.md and optional additional context. So at a minimum you need a SKILL.md file that has the skill's specialized instructions, similar to a slash command.

- my-skill/
	- SKILL.md
	- scripts/
		- validate.py
	- additional_context.md
	- data.csv
But you can have any additional files in the skills folder that is relevant context.

SKILL.md :

The SKILL.md file just has the instructions for how the skill is employed. The file is required to have a YAML front matter section with, at minimum, a name and description field as in the example below.

---
name: Your Skill Name
description: Brief description of what this Skill does and when to use it
---

# Your Skill Name

## Instructions
Provide clear, step-by-step guidance for Claude.

If you want to do X, then you *MUST* also read:
`/path/to/additional_context.md`

## Examples
Show concrete examples of using this Skill.
Progressive disclosure - Only skill names and descriptions are loaded into Claude's system prompt. When it decides to use a skill, it will fully read the SKILL.md file. Any additional context that is referenced in the SKILL.md is then read as needed (see example above). You can imagine this potentially going on forever where Claude can continue to read additional context sources as they're pointed to from each file.

The progressive disclosure design pattern is the core of the Agent Skill's value. Minimal context loading to start and only critical context loaded as necessary. In theory, this not only makes it very token efficient, but also allows Claude to maintain a higher "quality" context window where only necessary tokens are loaded.

Skills vs Claude Projects, MCPs, Subagents, and Slash Commands
Projects
Projects are isolated or silos of work. You don't use a ton of context between different projects, except for common tools or MCP servers.

Skills can be used by Claude across any and many projects. The context of the skills are relevant to the skills themselves, and not project specific. It therefore makes sense to package all of the context together with the skill so it can be used by any agent, no matter what project or environment it's working in.

Slash Commands
Slash commands are similar in that you have pre-defined or templated prompts (SKILL.md) that are optimized for a specific goal.

They key difference with skills is that agents decide when to use skills whereas the user decides when to use a slash command. Imagine that instead of you using a slash command with additional input args, the agent chooses when to use the slash command, but also what input args to use. Slash commands are also fixed, linear workflows. Skills are more like tools that can be used whenever necessary, giving the agent more degrees of freedom in using them.

Here's a concrete example.

I previously had a slash command to create a new thumbnail using Nanobanana. I first had to gather all of the relevant context to use the slash command, like the new video title, video description, reference images if I wanted to use a style transfer, or logos, or my own headshots for that particular thumbnail. The slash command prompt itself did a ton of the heavy lifting such as ensuring the thumbnail prompt for NanoBanana met all of the design requirements for a high-converting thumbnail, as well as followed all of the best prompting practices for Nanobanana.

Now, I gave my personal assistant agent the same skill to create the thumbnail (I'll show you the exact skill below), essentially just using my slash command prompt. The difference is, my personal assistant agent actually understands my youtube project, sees what my next video is, has MCPs to analyze my youtube analytics and forms its own version of all the context it needs to provide for a complete prompt. It is now my agent's goal to create an optimized thumbnail prompt and then call the Nanobanana MCP to generate the thumbnail. This effectively removes me out of the picture, which is what I wanted!

MCPs
MCPs are closer to skills in that the tools, prompts, data/context (aka resources), are all packaged together: in this case on the MCP server. And MCPs can essentially do everything, as far as I can think of, that skills can.

There are a few key differences still.

Skills are designed to be self-contained and run locally, in the same process as the agent. A skill is just a prepared prompt with additional context and potentially additional "tools" that the agent can run. So in addition to the normal tools that we can prompt the agent to use in the skill, we could also give it additional python scripts, bash commands, etc. to run. The agent can only leverage a skill if it has the required context and tools to do so. In contrast, MCPs run externally to the agent. They can access external data/APIs and can of course be setup as a server.
Complexity - implementing a skill is much more straightforward because it doesn't involve standing up MCP server/infrastructure. It's just some markdown files and potentially scripts. To me, there's now a motivation to prefer Agent Skills over MCPs. They're simpler to implement, maintain, monitor, and debug.
Progressive disclosure - Claude initially only sees each skill's name and description, so the context load is minimal. Claude will load additional context from a skill as needed. MCPs have complete tool, prompt, and resource schemas injected into system prompt.

I'm actually not entirely sure why this is the case. Technically we don't have to do this. We could for example only tell Claude in the system prompt which MCPs are available and for what use cases and then have it get additional docs or list resources when needed to use the tools. I've done that in the past with custom agents.
MCPs still absolutely have their place and utility. You can't shove the entire Github MCP into a skill. Even if you did, it's not a good idea. Remote MCP servers especially, still have all of the benefits they had when they first came out which is that there's only one maintainer, the rest of us just get to use them with little integration effort.

Subagents
Subagents for Claude are very much like tools. Claude actually invokes subagents by calling the Task tool which takes an input prompt. In the input prompt, Claude details the specific task the subagent should carry out. The subagent will work until it completes the task and return the result to Claude as a tool response. The subagent can be given access to a subset or the complete set of tools and MCP servers that the main Claude agent has. But either way it will get all of the tool schemas loaded into the system prompt, so it suffers from the same issue of front-loading MCP server and tool schemas.

Subagents also aren't the main agent, so you can't interact with them directly and therefore can't steer them. So yes, you could achieve the same functionality in a subagent as you can in a skill, but you won't have the same level of control as if you're working directly with a main agent carrying out the same task. There's no human-in-the-loop with subagents. Sure, you can ask the main Claude agent to prompt the subagent differently, but again this is not the same control.

Finally, there is a benefit to using a skill in the main agent where you may have a lot of relevant context that you wouldn't have in the subagent. Subagents have separate context. The main agent is already going to have the full context of all the work done in the conversation up to that point. You would need to ensure all of the relevant context is passed down to the Subagent which is an additional optimization and more to manage. In general, my rule of thumb is that if I can solve it with one agent, then I'll lean towards that. I only use subagents or multi-agents where it absolutely makes sense, like in deep research.

Benefits of Skills
Why would you want to use skills?



Example of progressive disclosure

Reduced Context Load - Only skill metadata (name, description) is initially loaded. Everything else is "progressively disclosed". You can potentially fit WAY more tools and functionality into an agent for the same context size, or reduce the same number of tools/functionality into a smaller context size.
Compounding Abilities - Skills can leverage other skills (with every little additional effort I might add!), opening up the opportunity to compound the agent's capabilities. E.g. I have a financial-modeling skill that leverages the lower level excel skill. All while not overloading the context because of "progressive disclosure".
Simplicity - In Claude, the harness takes care of the infrastructure around skill usage. This greatly simplifies our ability to implement skills. At a minimum you just need a SKILL.md that has the skill instructions. This is a much more natural and low barrier way to give Claude and agents additional capabilities.
Custom Skills
Today, you can create your own custom skills and use them with the web app (Claude.ai) or with Claude Code. See the Skills announcement for how to use with Claude.ai.

To use with Claude Code, see the docs.



You can use Claude's built-in skill skill-creator to generate new skills (very meta), just make sure to enable it in the options for the web or desktop app.

Thumbnail-generator Example
Here's an example of a real skill that I created so that my personal assistant (built with Claude Agent SDK) can create thumbnails for my youtube videos. Some files and text are omitted.

- youtube-thumbnail/
	- SKILL.md
	- Design Requirements.md
	- Prompting Guidelines.md
	...
SKILL.md:

---
name: youtube-thumbnail
description: "Skill for creating and editing Youtube thumbnails that are optimized for conversion. Use when the user asks to create a thumbnail from scratch or edit an existing thumbnail."
---
# YouTube Thumbnail

## File Structure

`.claude/skills/youtube-thumbnail/Design Requirements.md` design requirements for YouTube thumbnails.

`.claude/skills/youtube-thumbnail/Prompting Guidelines.md` prompting guidelines for generating YouTube thumbnails with the Nanobanana model.

`.claude/skills/youtube-thumbnail/Thumbnail Templates.md` list of valid thumbnail templates that can be used, including detailed visual descriptions and use cases.

`/Users/kennethliao/Movies/YT/thumbnails/templates` thumbnail template image files that can be used as a starting point for generating thumbnails.

`/Users/kennethliao/Movies/YT/kenny_headshots` headshots of Kenny that can be used in thumbnails.

`/Users/kennethliao/Movies/YT/icons` icons and logos that can be used in thumbnails.

## 🚨 REQUIRED READING 🚨

The following documents are **MANDATORY READING**. It's **ABSOLUTELY CRITICAL** you follow both the design requirements and prompting guidelines in order to generate high converting thumbnails. Failure to do so will result in a failed task.

Carefully read both the design requirements and prompting guidelines before proceeding.

### Design Requirements

All thumbnails **MUST** follow these design requirements:
`.claude/skills/youtube-thumbnail/Design Requirements.md`

The design requirements are what enable you to generate high click-through-rate thumbnails through proven strategies.

### Prompting Guidelines

Thumbnails are generated using NanoBanana, an image generation large language model. You **MUST** carefully review the best prompting practices for NanoBanana here: `.claude/skills/youtube-thumbnail/Prompting Guidelines.md`.

The prompting guidelines will enable you to get more predictable and consistent results from NanoBanana.

### Additional Notes

With both generating and editing thumbnails, you can include reference images such as headshots, icons, logos, or images for style transfer.

If using icons and logos, use actual images by passing the absolute path to the image files instead of simply describing them. This is because Nanobanana is not very good at guessing what common company logos look like. Commonly used icons and logos are stored in `/Users/kennethliao/Movies/YT/icons`.

## Generating a Thumbnail

There are two options for generating a thumbnail: generating a new thumbnail from scratch or editing an existing thumbnail template. In each case, you must strictly adhere to the design requirements and prompting guidelines above.

### Option A: Generate a New Thumbnail

...
Definitely check out Anthropic's official skills repo below to see more skills as well as the "Awesome Claude Skills" Repo which is a curated list of community-developed skills to get more ideas of what you can do with Agent Skills!

Optimizing Custom Skills
Whether you create a skill from scratch on your own or with Claude's skill-creator skill, you might run into errors or failures when the agent actually uses the skill.

You can improve the skill over time just like you would anything else "vibe-coded". What's worked well for me is telling my agent (Claude Code, Cursor, custom agent, etc.) that usage of the skill failed because X, showing it the failure mode if possible, having it review the full skill and identify the failure point, and then suggesting to me how to improve the skill.

Sources: https://share.note.sx/8k50udm8#ME3MD6walWogaQZxAVIdsAMaYPFQvw694zbFb622c0Y
Skills News Announcement - General announcement and additional resources
Skills Engineering Blog Post - Technical deep dive into skills
Anthropic Skills Repo - All of the default skills that come with Claude
Developer Docs - Agent Skills - General skills documentation
Claude Code - Agent Skills - Using skills with Claude Code
Github Skills Cookbook - Get real code examples of building custom skills
Anthropic Support - What are skills? - FAQ
Anthropic Support - Using Skills in Claude - FAQ
Simon Willison - Claude Skills - Great breakdown and opinion on Claude Skills
Awesome Claude Skills - Directory of community-developed skills.