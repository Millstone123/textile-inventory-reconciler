import tempfile
import unittest
from pathlib import Path

from textile_inventory_reconciler.model import ReconciliationError
from textile_inventory_reconciler.reconcile import reconcile_file

VALID = """sku,expected,counted,unit_cost
LIN-1,10,8,2.50
CTN-2,4,5,3.00
"""


class TextileInventoryReconcilerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)

    def write(self, text: str) -> Path:
        path = Path(self.directory.name) / "inventory.csv"
        path.write_text(text, encoding="utf-8")
        return path

    def test_reconciles_units_and_value_variance(self) -> None:
        report = reconcile_file(self.write(VALID))
        self.assertEqual(report.unit_variance, -1)
        self.assertEqual(report.value_variance, -2)
        self.assertEqual(report.render().splitlines()[0], "skus=2")

    def test_rejects_duplicate_sku(self) -> None:
        invalid = VALID.replace("CTN-2", "LIN-1")
        with self.assertRaises(ReconciliationError):
            reconcile_file(self.write(invalid))

    def test_rejects_negative_count(self) -> None:
        invalid = VALID.replace("10,8,2.50", "10,-8,2.50")
        with self.assertRaises(ReconciliationError):
            reconcile_file(self.write(invalid))


if __name__ == "__main__":
    unittest.main()
