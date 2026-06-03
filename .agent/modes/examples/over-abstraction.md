# Over-abstraction Full Example

Read this file only when the compact card is insufficient, when the user explicitly asks for a full example for this risk, or when this exact failure mode remains ambiguous.

User request: "Add a function to calculate discount."

Wrong pattern:

```python3
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

```python3
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate a percentage discount amount."""
    return amount * (percent / 100)
```

Use the direct function unless current requirements include multiple discount types, runtime strategy selection, or persistent discount policies.
