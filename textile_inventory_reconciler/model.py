from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


class ReconciliationError(ValueError):
    """Raised when inventory data cannot be reconciled."""


@dataclass(frozen=True)
class InventoryRecord:
    sku: str
    expected: int
    counted: int
    unit_cost: Decimal
    reference_uri: str

    @property
    def variance(self) -> int:
        return self.counted - self.expected

    @property
    def value_variance(self) -> Decimal:
        return self.unit_cost * self.variance


@dataclass(frozen=True)
class ReconciliationReport:
    records: Tuple[InventoryRecord, ...]

    @property
    def unit_variance(self) -> int:
        return sum(record.variance for record in self.records)

    @property
    def value_variance(self) -> Decimal:
        return sum((record.value_variance for record in self.records), Decimal("0.00"))

    def render(self) -> str:
        return "\n".join(
            [
                f"skus={len(self.records)}",
                f"unit_variance={self.unit_variance}",
                f"value_variance={self.value_variance:.2f}",
            ]
        )
