import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import List

from .model import InventoryRecord, ReconciliationError, ReconciliationReport

FIELDS = ("sku", "expected", "counted", "unit_cost", "reference_uri")


def _integer(raw: str, field: str, row_number: int) -> int:
    try:
        value = int(raw)
    except ValueError as exc:
        raise ReconciliationError(f"row {row_number}: invalid {field}") from exc
    if value < 0:
        raise ReconciliationError(f"row {row_number}: negative {field}")
    return value


def _cost(raw: str, row_number: int) -> Decimal:
    try:
        value = Decimal(raw)
    except InvalidOperation as exc:
        raise ReconciliationError(f"row {row_number}: invalid unit_cost") from exc
    if not value.is_finite() or value < 0:
        raise ReconciliationError(f"row {row_number}: invalid unit_cost")
    return value.quantize(Decimal("0.01"))


def reconcile_file(path: Path) -> ReconciliationReport:
    records: List[InventoryRecord] = []
    seen = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ReconciliationError("unexpected inventory columns")
        for row_number, row in enumerate(reader, start=2):
            sku = (row["sku"] or "").strip()
            if not sku:
                raise ReconciliationError(f"row {row_number}: missing sku")
            if sku in seen:
                raise ReconciliationError(f"row {row_number}: duplicate sku")
            reference_uri = (row["reference_uri"] or "").strip()
            if not reference_uri:
                raise ReconciliationError(f"row {row_number}: missing reference_uri")
            seen.add(sku)
            records.append(
                InventoryRecord(
                    sku=sku,
                    expected=_integer(row["expected"], "expected", row_number),
                    counted=_integer(row["counted"], "counted", row_number),
                    unit_cost=_cost(row["unit_cost"], row_number),
                    reference_uri=reference_uri,
                )
            )
    if not records:
        raise ReconciliationError("inventory contains no records")
    return ReconciliationReport(tuple(records))
