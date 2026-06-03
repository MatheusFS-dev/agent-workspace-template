# Hidden Assumptions Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Add a feature to export user data."

Wrong pattern:

```python
def export_users(format='json'):
    """Export all users to a file."""
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as file_obj:
            json.dump([user.to_dict() for user in users], file_obj)
    return f"Exported {len(users)} users"
```

Problems:

- Assumes all users should be exported.
- Assumes local file output.
- Assumes fields and privacy policy.
- Assumes format and path.

Better pattern:

```text
Before implementing, clarify scope, output mechanism, fields, and expected volume. The smallest safe approach may be a paginated JSON endpoint, but file export needs more requirements.
```
