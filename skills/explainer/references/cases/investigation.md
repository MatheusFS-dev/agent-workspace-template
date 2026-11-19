# Case: Issue investigation

Cover these in order. Each item is a short paragraph unless marked.

1. Open with the cause and how sure you are: confirmed, likely, or unknown.
   Then describe the symptom the user sees and when it happens.
2. The chain from root cause to symptom, with a diagram.

   ```mermaid
   flowchart LR
     A[Root cause] --> B[Effect] --> C[Visible symptom]
   ```

3. Evidence (list): what was checked and what it showed, such as a log line,
   a reproduction, or a measurement.
4. Other suspected causes and why each was ruled out, in one or two sentences
   each.
5. The fix or the next check. If the cause is not confirmed, say what would
   confirm it.

Saved report headings: "Evidence" and "Next step".
