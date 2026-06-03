# Test-First Verification Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Sorting breaks when there are duplicate scores."

Wrong pattern:

```python3
def sort_scores(scores):
    return sorted(scores, key=lambda item: -item['score'])
```

Better pattern:

```python3
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
