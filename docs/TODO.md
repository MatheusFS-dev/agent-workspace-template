## New features to add



## Problems and bugs to fix

- When the user asks to add a memory to memories.md, the agent usually adds it to the default provider memory location, like .codex. It should be added to the memories.md in the project file instead. This can be fixed by making the prompt more specific, like "Add this memory to the memories.md file in the project directory" instead of just "Add this memory to your memories". But, is there a better way to do this? 