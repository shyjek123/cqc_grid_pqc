#!/usr/bin/env python3
"""Run the extracted secure-grid circuits on Aer, qBraid simulators, and a QPU."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from qbraid_demo.workflow import run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-only", action="store_true", help="Aer only; do not call qBraid")
    parser.add_argument("--max-credits", type=float, default=None, help="QPU quote ceiling (default 100)")
    parser.add_argument("--no-hardware", action="store_true", help="Quote QPUs but do not submit them")
    parser.add_argument("--wait-seconds", type=float, default=None, help="How long to poll jobs (default 300)")
    args = parser.parse_args()
    run(
        local_only=args.local_only,
        max_credits=args.max_credits,
        run_hardware=False if args.no_hardware else None,
        wait_s=args.wait_seconds,
    )


if __name__ == "__main__":
    main()
