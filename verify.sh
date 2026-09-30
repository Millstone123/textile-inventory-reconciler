#!/bin/sh
set -eu
printf "%s\n" "textile inventory reconciler verification"
printf "%s\n" "phase=summary"
python3 -m textile_inventory_reconciler summary examples/inventory.csv
printf "%s\n" "phase=unit-tests"
python3 -m unittest discover -v
printf "%s\n" "phase=validation"
python3 -m textile_inventory_reconciler check examples/inventory.csv
printf "%s\n" "verification-complete"
