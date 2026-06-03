# Drive-by Refactoring Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Fix the bug where empty emails crash the validator."

Wrong pattern:

```diff
- if '@' not in user_data['email']:
+ email = user_data.get('email', '').strip()
+ if '@' not in email or '.' not in email.split('@')[1]:
      raise ValueError('Invalid email')
+ username = user_data.get('username', '').strip()
+ if len(username) < 3:
+     raise ValueError('Username too short')
```

Problems:

- Changes email validation semantics beyond the crash.
- Adds username validation nobody requested.
- Mixes bug fix with unrelated behavior changes.

Better pattern:

```diff
- if not user_data.get('email'):
+ email = user_data.get('email', '')
+ if not email or not email.strip():
      raise ValueError('Email required')

- if '@' not in user_data['email']:
+ if '@' not in email:
      raise ValueError('Invalid email')
```

Only change the specific empty-email path.
