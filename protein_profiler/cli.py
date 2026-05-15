"""
cli.py
Docs: https://docs.python.org/3/library/argparse.html
"""

import argparse
import logging
from protein_profiler import __version__
from protein_profiler import pipeline, display, visualize


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="protein_profiler",
        description="Compile a biochemical profile for a protein from its UniProt ID.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py P41145
  python main.py P41145 --no-display
  python main.py P41145 --headless --email you@example.com
  python main.py P41145 --limit 250
        """,
    )

    parser.add_argument(
        "uniprot_id",
        type=str,
        nargs="?",
        default=None,
        help="UniProt accession number (e.g. P41145). If omitted, you will be prompted.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Suppress terminal output and write logs to logs/ instead",
    )
    parser.add_argument(
        "--no-display",
        action="store_true",
        default=False,
        help="Skip popup windows — saves plots to temp files only",
    )
    parser.add_argument(
        "--email",
        type=str,
        default="",
        help="Email for NCBI Entrez API identification",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Max number of ChEMBL ligands to fetch (default: 100)",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # if no uniprot_id provided, prompt for it
    if not args.uniprot_id:
        args.uniprot_id = input("Enter UniProt ID: ").strip()

    if not args.headless:
        logging.disable(logging.CRITICAL)

    profile = pipeline.run(
        uniprot_id=args.uniprot_id,
        headless=args.headless,
        no_display=args.no_display,
        email=args.email,
        limit=args.limit,
    )

    if not args.headless:
        display.show_profile(profile)

    if not args.no_display and not args.headless:
        visualize.plot_activity_distribution(profile)
        visualize.plot_chemical_space(profile)
        visualize.draw_top_ligands(profile)
