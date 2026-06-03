![header](https://capsule-render.vercel.app/api?height=190&type=blur&color=4ea7f7&section=header&text=Agent%20Workspace%20Template&fontColor=f8f8f2&fontSize=40)

<p align="center">
<a href="https://github.com/DenverCoder1/readme-typing-svg"><img src="https://readme-typing-svg.herokuapp.com?font=Time+New+Roman&color=%234ea7f7&size=25&center=true&vCenter=true&width=600&height=30&lines=👋+Welcome!"></a>
</p>

<p align="center">
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template"><img src="https://img.shields.io/github/license/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="License"/></a>
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template/stargazers"><img src="https://img.shields.io/github/stars/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="Stars"/></a>
  <a href="https://github.com/MatheusFS-dev/agent-workspace-template/network/members"><img src="https://img.shields.io/github/forks/MatheusFS-dev/agent-workspace-template?style=flat-square" alt="Forks"/></a>
  <a href="https://visitor-badge.laobi.icu/badge?page_id=MatheusFS-dev/agent-workspace-template"><img src="https://visitor-badge.laobi.icu/badge?page_id=MatheusFS-dev/agent-workspace-template" alt="Visitors"/></a>
</p>

This template adds a reusable `.agent` workspace to your project.

It helps an AI coding agent understand how to work in your project without loading too much unnecessary context.

## Table of Contents

- [📦 What to Copy Into Your Project](#what-to-copy-into-your-project)
- [🧭 What Each File Does](#what-each-file-does)
- [🚀 First Use in a Project](#first-use-in-a-project)
- [🔄 Updating the Project Map Later](#updating-the-project-map-later)
- [💬 Using the Agent Day to Day](#using-the-agent-day-to-day)
- [🧠 Memories](#memories)
- [⏳ Long Tasks](#long-tasks)
- [🛠️ Skills Included](#skills-included)
- [🚫 What Not to Copy](#what-not-to-copy)
- [🤝 Contributing](#contributing)
- [📜 License](#license)

## 📦 What to Copy Into Your Project

Copy these items into the root folder of your project:

### Copy List

```text
.agent/
AGENTS.md
CLAUDE.md
GEMINI.md
```

### Example Final Structure

```text
your-project/
  .agent/
  AGENTS.md
  CLAUDE.md
  GEMINI.md
  src/
  tests/
  README.md
```

`CLAUDE.md` and `GEMINI.md` are optional, but useful if you use Claude Code or Gemini-based agents.

## 🧭 What Each File Does

### AGENTS.md

Main instruction file for the AI agent.

The agent reads this first.

### .agent/

Internal workspace used by the agent.

It contains:

- routing rules,
- compact task instructions,
- risk-specific coding example cards,
- project memory,
- paper-writing support,
- plotting support,
- helper scripts.

You usually do not need to edit files inside `.agent` manually.

### CLAUDE.md

Small compatibility file for Claude Code.

It points Claude to `AGENTS.md`.

### GEMINI.md

Small compatibility file for Gemini agents.

It points Gemini to `AGENTS.md`.

## 🚀 First Use in a Project

After copying the template into your project, ask the AI:

```text
Update the project map for this repository.
```

The AI will inspect the project and update:

```text
.agent/context/project-map.md
```

You do not need to run any scripts yourself.

## 🔄 Updating the Project Map Later

When your project structure changes, ask:

```text
Update the project map.
```

The AI will handle the internal command.

## 💬 Using the Agent Day to Day

Ask normally. For example:

```text
fix this bug.
```

```text
refactor this file without changing behavior.
```

```text
create a publication-quality plot.
```

```text
rewrite this paragraph.
```

The agent will decide which `.agent` files are relevant.

## 🧠 Memories

The file below stores compact long-term project context:

```text
.agent/context/memories.md
```

Use it for durable decisions only.

Good examples:

- preferred model architecture,
- accepted experiment protocol,
- naming convention,
- important project constraint.

Bad examples:

- temporary task notes,
- one-time debugging output,
- copied logs,
- large explanations.

To update memories, ask:

```text
Update the project memories with this decision: ...
```

The AI should keep the memory file short and remove outdated context.

## ⏳ Long Tasks

For long tasks, ask the AI to create task state:

```text
Create a task state file for this refactor and keep it updated.
```

The AI will create a local state file only for that task.

Do not use task state for small edits.

## 🛠️ Skills Included

This template keeps only two automatic skills.

### Scientific plot maker

Used when you ask for plots, figures, charts, histograms, scatter plots, or publication-quality visualizations.

Example:

```text
Create a publication-quality histogram for these results.
```

### Scribe

Used when you ask for academic writing, paper editing, reviewer responses, abstracts, introductions, conclusions, or manuscript text.

Example:

```text
Rewrite this paragraph for an IEEE-style paper.
```

## 🚫 What Not to Copy

Do not copy prompt libraries or unused skills into `.agent`.

Avoid folders like:

```text
.agent/prompts/
.agent/skills/some-other-skill/
```

Keeping unused files inside `.agent` can make agents read too much context.

Save it outside `.agent`.

## 🤝 Contributing

> [!IMPORTANT]
> First read the `CONTRIBUTING.md` file if your project provides one.

Contributions are what make the open-source community amazing. To contribute:

1. Fork the project.
2. Create a feature branch.
3. Commit your changes.
4. Push to the branch.
5. Open a Pull Request.

## 📜 License

This project is licensed under the **[Apache License 2.0](LICENSE)**.
