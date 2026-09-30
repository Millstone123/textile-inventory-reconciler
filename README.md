# Textile Inventory Reconciler

A dependency-free inventory reconciliation command-line tool for warehouse counts.

## Local workflow

```sh
sh verify.sh
```

`verify.sh` is the supported smoke workflow: it checks the source layout, runs
the ordinary tests, validates the example inventory, prints reconciliation
totals, and performs a desktop spot-check on macOS.

The tool rejects malformed quantities and reports unit-cost value variance.
