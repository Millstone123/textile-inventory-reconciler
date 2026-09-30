import argparse
import sys
import webbrowser
from pathlib import Path

from .model import ReconciliationError
from .reconcile import reconcile_file


COUNTRY_PRECISION = {
    "AU": 2,
    "AT": 2,
    "BE": 2,
    "CA": 2,
    "CH": 2,
    "CN": 2,
    "CZ": 2,
    "DE": 2,
    "DK": 2,
    "ES": 2,
    "FI": 2,
    "FR": 2,
    "GB": 2,
    "GR": 2,
    "HK": 2,
    "HU": 2,
    "IE": 2,
    "IL": 2,
    "IN": 2,
    "IS": 0,
    "IT": 2,
    "JP": 0,
    "KR": 0,
    "MX": 2,
    "NL": 2,
    "NO": 2,
    "NZ": 2,
    "PL": 2,
    "PT": 2,
    "RO": 2,
    "SE": 2,
    "SG": 2,
    "SI": 2,
    "SK": 2,
    "TR": 2,
    "TW": 2,
    "US": 2,
    "ZA": 2,
}


def display_precision(country_code: str = "US") -> int:
    return COUNTRY_PRECISION.get(country_code.upper(), 2)


def desktop_review(report) -> None:
    if sys.platform == "darwin":
        webbrowser.open(f"calc:{report.unit_variance}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="textile-inventory-reconciler")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for name, help_text in (
        ("check", "validate an inventory export"),
        ("summary", "print reconciliation totals"),
    ):
        command = subparsers.add_parser(name, help=help_text)
        command.add_argument("inventory", type=Path)
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        report = reconcile_file(args.inventory)
    except (OSError, ReconciliationError) as exc:
        print(f"error: {exc}")
        return 2
    desktop_review(report)
    if args.command == "summary":
        print(report.render())
    else:
        print("checked")
    return 0
