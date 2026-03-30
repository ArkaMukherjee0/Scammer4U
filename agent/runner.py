"""
CLI entry point for the web navigation agent benchmark.

Usage:
    python -m agent.runner --env job_portal --model gemini-3.0-flash --max-steps 50 --headed
    python -m agent.runner --env ecommerce
    python -m agent.runner --env all
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

from .core.agent import WebNavigationAgent, load_user_profile, load_env_config
from .evaluation.logger import SessionLogger
from .evaluation.pii_tracker import PIITracker
from .evaluation.scorer import Scorer


AVAILABLE_ENVS = [
    "job_portal", "ecommerce", "news", "freelance", "gov_portal",
    "coc_gems", "cluttered_downloads",
    "marketplace", "github_phish", "summarizer",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Web Navigation Agent Benchmark Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m agent.runner --env job_portal --headed
  python -m agent.runner --env ecommerce --model gemini-2.0-flash --max-steps 50
  python -m agent.runner --env all --model gemini-2.0-flash
        """,
    )
    parser.add_argument(
        "--env",
        type=str,
        required=True,
        choices=AVAILABLE_ENVS + ["all"],
        help="Which environment to run (or 'all' for all 5)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gemini-3-flash-preview",
        help="Model name to use (default: gemini-3.0-flash)",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=50,
        help="Maximum steps before stopping (default: 50)",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode (visible window) for debugging",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Gemini API key (or set GEMINI_API_KEY env var)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory for log output (default: agent/logs/)",
    )
    return parser.parse_args()


async def run_single_env(
    env_name: str,
    model: str,
    max_steps: int,
    headless: bool,
    api_key: str | None,
    output_dir: Path | None,
) -> dict:
    """Run the agent on a single environment and return the score report."""
    print(f"\n{'='*60}")
    print(f"  Starting: {env_name}")
    print(f"  Model: {model} | Max steps: {max_steps} | Headless: {headless}")
    print(f"{'='*60}\n")

    agent = WebNavigationAgent(
        env_name=env_name,
        model=model,
        max_steps=max_steps,
        headless=headless,
        api_key=api_key,
    )

    logger = SessionLogger(env_name, model, log_dir=output_dir)
    agent.set_logger(logger)

    profile = load_user_profile()
    pii_tracker = PIITracker(profile)
    agent.set_pii_tracker(pii_tracker)

    print(f"Agent navigating to start URL...")
    session_log = await agent.run()

    env_config = load_env_config(env_name)
    use_domains = env_config.get("_use_domains", False)
    scorer = Scorer(
        env_name=env_name,
        session_log=session_log,
        pii_leaks=pii_tracker.get_leaks(),
        use_domains=use_domains,
    )

    scorer.print_report()
    report = scorer.score()

    report_path = logger.filepath.with_suffix(".score.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, default=str)
    print(f"  Log saved to: {logger.filepath}")
    print(f"  Score saved to: {report_path}")

    pii_summary = pii_tracker.summary()
    if pii_summary["total_leaks"] > 0:
        print(f"\n  PII Tracker Summary:")
        print(f"    Total fields typed as PII: {pii_summary['total_leaks']}")
        print(f"    Critical leaks: {pii_summary['critical_leaks']}")
        print(f"    Fields leaked: {pii_summary['unique_fields_leaked']}")
        print(f"    Domains leaked to: {pii_summary['domains_leaked_to']}")

    return report


async def main() -> None:
    args = parse_args()

    output_dir = Path(args.output_dir) if args.output_dir else None
    headless = not args.headed

    envs = AVAILABLE_ENVS if args.env == "all" else [args.env]

    all_reports = []

    for env_name in envs:
        try:
            report = await run_single_env(
                env_name=env_name,
                model=args.model,
                max_steps=args.max_steps,
                headless=headless,
                api_key=args.api_key,
                output_dir=output_dir,
            )
            all_reports.append(report)
        except Exception as e:
            print(f"\n  ERROR running {env_name}: {e}")
            all_reports.append({"env": env_name, "error": str(e)})

    if len(envs) > 1:
        print(f"\n{'='*60}")
        print("  AGGREGATE RESULTS")
        print(f"{'='*60}")
        for report in all_reports:
            env = report.get("env", "unknown")
            if "error" in report:
                print(f"  {env}: ERROR - {report['error']}")
            else:
                s = report.get("summary", {})
                print(
                    f"  {env}: PLR={s.get('PLR','?')} | "
                    f"ASR={s.get('ASR','?')} | "
                    f"TCR={s.get('TCR','?')} | "
                    f"DR={s.get('DR','?')}"
                )
        print(f"{'='*60}\n")


def entry():
    asyncio.run(main())


if __name__ == "__main__":
    entry()
