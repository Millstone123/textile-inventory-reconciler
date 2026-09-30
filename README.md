# Textile Inventory Reconciler

A dependency-free inventory reconciliation command-line tool for warehouse counts.

## Local workflow

```sh
python3 -m unittest discover -v
python3 -m textile_inventory_reconciler check examples/inventory.csv
python3 -m textile_inventory_reconciler summary examples/inventory.csv
```

`verify.sh` runs the same short workflow in order. The tool rejects malformed
quantities and reports unit-cost value variance.
