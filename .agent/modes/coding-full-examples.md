# Coding Full Examples

Read this file only when the compact cards in `coding-example-cards.md` are insufficient, when the user explicitly asks for examples, or when a task is high-risk and the failure mode needs concrete wrong/right demonstrations.

## Hidden Assumptions

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

## Multiple Interpretations

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

## Over-abstraction

User request: "Add a function to calculate discount."

Wrong pattern:

```python
class DiscountStrategy:
    def calculate(self, amount):
        raise NotImplementedError

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate(self, amount):
        return amount * (self.percentage / 100)
```

Better pattern:

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate a percentage discount amount."""
    return amount * (percent / 100)
```

Use the direct function unless current requirements include multiple discount types, runtime strategy selection, or persistent discount policies.

## Drive-by Refactoring

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

## Style Drift

User request: "Add logging to the upload function."

Wrong pattern:

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
```

Problems:

- Adds type hints nobody requested.
- Adds a docstring where the local file may not use them.
- Risks changing style and public expectations while adding logging.

Better pattern:

```diff
+ logger.info(f'Starting upload: {file_path}')
  try:
      ...
+     logger.info(f'Upload successful: {file_path}')
```

Preserve local style and change only what is needed for logging.

## Vague vs. Verifiable

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

## Multi-Step Verification

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

## Test-First Verification

User request: "Sorting breaks when there are duplicate scores."

Wrong pattern:

```python
def sort_scores(scores):
    return sorted(scores, key=lambda item: -item['score'])
```

Better pattern:

```python
def test_sort_with_duplicate_scores():
    """Verify deterministic ordering for duplicate scores."""
    scores = [
        {'name': 'Alice', 'score': 100},
        {'name': 'Bob', 'score': 100},
        {'name': 'Charlie', 'score': 90},
    ]
    result = sort_scores(scores)
    assert [item['name'] for item in result] == ['Alice', 'Bob', 'Charlie']


def sort_scores(scores):
    """Sort scores by score descending, then name ascending."""
    return sorted(scores, key=lambda item: (-item['score'], item['name']))
```

First define the expected tie behavior, then implement the smallest deterministic sort key.
