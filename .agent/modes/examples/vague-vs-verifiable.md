# Vague vs. Verifiable Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Fix the authentication system."

Wrong pattern:

```text
I will review authentication, identify issues, make improvements, and test the changes.
```

Better pattern:

```text
Define the specific failure first. If the issue is "users stay logged in after password change," the plan is:
1. Write test: change password -> old session rejected.
2. Implement session invalidation on password change.
3. Verify the new test and existing auth tests pass.
```
