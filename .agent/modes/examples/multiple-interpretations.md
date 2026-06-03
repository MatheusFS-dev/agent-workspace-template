# Multiple Interpretations Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Make the search faster."

Wrong pattern:

```python
# Adds caching, async execution, and indexes without knowing whether latency,
# throughput, or perceived UI speed is the actual problem.
```

Better pattern:

```text
"Faster" could mean lower response latency, higher throughput, lower memory, or faster perceived UI. Each leads to a different implementation and verification check. Ask which target matters.
```
