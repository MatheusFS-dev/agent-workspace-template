# Multi-Step Verification Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Add rate limiting to the API."

Wrong pattern:

```text
Implement Redis, middleware, endpoint-specific config, monitoring, and tests in one large change.
```

Better pattern:

```text
1. Add basic in-memory limiting for one endpoint -> verify: 11th request returns 429.
2. Extract to middleware -> verify: limits apply to selected endpoints.
3. Add Redis backend only if multi-instance deployment is required -> verify: counter is shared.
4. Add per-endpoint configuration only if requirements require multiple limits -> verify: config parsing test passes.
```
