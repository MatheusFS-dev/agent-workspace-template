---
name: readmaker
description: Use when creating, rewriting, refreshing, or editing Markdown README.md files in repositories, including root and nested READMEs.
---

# Readmaker

Create accurate, project-specific Markdown READMEs in the style family shown by
[the canonical template](template/README.md). Read that template completely
before writing. It is an illustrative style reference, not boilerplate: never
copy its example project facts, commands, sections, people, or placeholders.

## Ground the README in verified sources

Before writing, determine the Git worktree root with
`git rev-parse --show-toplevel`, then inspect all of these sources:

- repository remotes,
- the target README and other existing documentation,
- package, dependency, build, and test configuration,
- `CONTRIBUTING.md`,
- `LICENSE` or other license files,
- GitHub repository metadata and, when contributors are needed, GitHub
  contributor and user metadata.

Use source files and executable configuration as evidence. Do not infer a
command merely because a conventional directory such as `tests/` exists. For a
GitHub remote, verify the canonical owner, repository name, default branch,
description, and license through GitHub metadata rather than parsing the remote
alone.

If information required for the requested README is absent, inaccessible, or
conflicting, stop before modifying the README and ask the user a targeted
question. This includes unavailable canonical GitHub identity, license,
project-specific contribution prerequisites, or facts needed for requested
installation and usage instructions. Do not draft a partial document while
waiting for the answer. Generated READMEs must contain no invented facts,
unresolved placeholders, guessed commands, or links to files that do not exist.

## Choose the editing mode

A root README is exactly `README.md` at the Git worktree root.

| Request and target | Required behavior |
| --- | --- |
| Create a root README or explicitly rewrite, refresh, or modernize it | Use the complete root contract below. |
| Make a narrow edit to a nonconforming root README | Keep the edit narrow. Ask for confirmation before migrating the rest of the document to the readmaker style. |
| Edit a conforming root README | Preserve every mandatory root element while making the requested change. |
| Create or edit a nested README | Use the nested README guidance below. |

Do not treat a narrow correction, link update, or command replacement as
permission to rewrite the entire root README.

## Root README contract

Root README creation and explicit rewrite or refresh must include all of the
following, adapted to verified project data:

1. A capsule-render header whose text and colors suit the actual project.
2. A `<div align="center">` containing a fenced text block with an ASCII banner
   for the actual project name.
3. A centered typing welcome that names or meaningfully describes the project.
4. A centered badge row with valid license, stars, forks, and visitor badges.
5. A concise project description.
6. A table of contents containing only headings that appear in the document,
   with working GitHub Markdown anchors.
7. A project-adapted Contributing section with an `[!IMPORTANT]` admonition and
   the fork, branch, commit, push, and pull-request workflow.
8. A License section naming the detected license and linking to the repository's
   license file.
9. A collaborators table built from verified GitHub contributor and user data.

For a repository identified as `OWNER/REPO`, use badge targets shaped like
these, substituting verified values and URL-encoding path and query components
where required:

```text
https://img.shields.io/github/license/OWNER/REPO?style=flat-square
https://img.shields.io/github/stars/OWNER/REPO?style=flat-square
https://img.shields.io/github/forks/OWNER/REPO?style=flat-square
https://visitor-badge.laobi.icu/badge?page_id=OWNER.REPO
```

Link the badges to the canonical repository, license file, stargazers, forks,
or visitor endpoint as appropriate. Do not leave angle-bracket tokens or sample
owner/repository names in any URL.

Adapt the Contributing admonition to verified repository policy. Link to
`CONTRIBUTING.md` when it exists. If no source establishes the important
prerequisite contributors should follow, ask the user instead of inventing one.
Keep the five-step contribution workflow consistent with verified branch and
contribution conventions. Include literal branch names, commit messages, remote
names, or command examples only when repository sources verify them. The five
steps may use accurate prose when literal values are not documented; if the
user requires command-ready instructions, ask for the missing values instead
of inventing examples.

Use the license's verified name, such as `Apache License 2.0`, and link the
actual license file. Never assume the template's GPL example applies.

### Build the collaborators table

Use the GitHub repository contributors API to obtain contributors, then use the
GitHub user API for each login represented in the table. Build each entry from
verified `login`, `name`, `html_url`, `avatar_url`, `type`, and stable identity
data.

- Keep one entry per stable GitHub user identity; otherwise deduplicate logins
  case-insensitively.
- Exclude accounts whose user metadata identifies them as bots, including
  `type: Bot` and bot-form logins such as names ending in `[bot]`.
- Exclude anonymous entries that cannot be verified through a GitHub user
  record.
- Use the display name when available and the login otherwise.
- Preserve the contributors API order unless the repository documents another
  ordering rule.

Do not duplicate contributors, substitute repository members for contributors,
or fabricate names, profile links, or avatar URLs.

## Nested READMEs

Nested READMEs document their directory, component, example, or workflow. Omit
root-only decoration: the capsule header, project-name ASCII banner, typing
welcome, repository badge row, and project-wide collaborators table.

Select sections and template techniques according to the nested content. Use
GitHub admonitions when they convey a meaningful note, prerequisite, warning,
or risk. Use expandable sections, lists, tables, Mermaid diagrams, hover text,
or GeoJSON only when they make the specific documentation easier to understand.
If one of these elements might help but its applicability is uncertain, propose
the concrete idea and ask before adding it.

## When writing commands

You may explain what each command does, then add the command. But, at the end of a command
block section, provide a full script for easy copy paste (nothing complicated, simple stuff.
No need for .sh or other scripts). However, only use these for blocks/sections with more than
3 commands.

## Secondary job

Also update, when present, CITATION.cff and LICENSE.txt to follow project correct info, replacing
placeholders with the correct information.

## Verify before returning

Review the finished README against the evidence and the applicable contract:

- Every factual claim, command, version, path, link, and person is verified.
- No sample content, invented data, or unresolved placeholder remains.
- A root README has every mandatory root element, adapted rather than copied.
- Its table of contents matches the headings actually present.
- Its license name and link match the detected license.
- Its collaborators are unique, verified, and non-bot.
- A nested README contains no root-only decoration.
- A narrow edit did not silently become a full migration.

If any check fails because evidence is missing, pause and ask the user rather
than weakening or omitting the requirement.
