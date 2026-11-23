import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "calculator"))
sys.path.insert(0, os.path.join(ROOT, "agreement"))

import fill  # noqa: E402
import margin  # noqa: E402

AGREEMENT = os.path.join(ROOT, "agreement", "white-label-voice-ai-agreement.md")

BASE = {
    "sub_accounts_live": 12,
    "sub_accounts_included": 10,
    "platform_fee": 500,
    "extra_sub_account_fee": 25,
    "platform_cost": 300,
    "minutes_per_month": 1000,
    "cost_per_minute": 0.10,
    "price_per_minute": 0.25,
    "phone_numbers": 10,
    "number_cost": 1,
    "number_price": 3,
    "sms_segments": 1000,
    "sms_cost_per_segment": 0.01,
    "sms_price_per_segment": 0.03,
    "monthly_growth_pct": 0,
}


def close(a, b):
    return abs(a - b) < 1e-9


def test_month_one_numbers():
    r = margin.calculate(BASE)
    # platform 500 + 2 extra * 25 = 550; usage 250 + 30 + 30 = 310
    assert close(r["revenue_platform"], 550)
    assert close(r["revenue_usage"], 310)
    assert close(r["revenue"], 860)
    # cost 300 + 100 + 10 + 10 = 420
    assert close(r["cost"], 420)
    assert close(r["margin"], 440)
    assert close(r["markup_multiple"], 860 / 420)


def test_no_extra_subaccounts_when_under_included():
    cfg = dict(BASE, sub_accounts_live=4)
    assert close(margin.calculate(cfg)["revenue_platform"], 500)


def test_zero_cost_does_not_divide_by_zero():
    cfg = dict(BASE, platform_cost=0, cost_per_minute=0, number_cost=0, sms_cost_per_segment=0)
    r = margin.calculate(cfg)
    assert r["markup_multiple"] == 0.0
    assert close(r["margin"], r["revenue"])


def test_projection_flat_with_no_growth():
    r = margin.calculate(BASE)
    assert len(r["projection"]) == 12
    assert all(close(row["margin"], 440) for row in r["projection"])
    assert close(r["year_margin"], 440 * 12)
    assert close(r["projection"][-1]["cumulative_margin"], r["year_margin"])


def test_projection_grows():
    r = margin.calculate(dict(BASE, monthly_growth_pct=10))
    assert r["projection"][11]["margin"] > r["projection"][0]["margin"]
    assert r["projection"][11]["sub_accounts"] > 12


def test_defaults_fill_missing_keys():
    assert margin.calculate({})["revenue"] > 0


def test_fill_replaces_and_reports_missing():
    text, missing, unused = fill.fill("Hi {{a}} and {{ b }} and {{c}}", {"a": "1", "b": 2, "z": 3})
    assert text == "Hi 1 and 2 and {{c}}"
    assert missing == ["c"]
    assert unused == ["z"]


def test_example_deal_fills_whole_agreement():
    with open(AGREEMENT, encoding="utf-8") as f:
        template = f.read()
    with open(os.path.join(ROOT, "examples", "deal.example.json"), encoding="utf-8") as f:
        deal = json.load(f)
    text, missing, unused = fill.fill(template, deal)
    assert missing == []
    assert unused == []
    assert "{{" not in text


def test_fill_cli_fails_on_missing():
    empty = os.path.join(ROOT, "tests", "_empty.json")
    with open(empty, "w", encoding="utf-8") as f:
        f.write("{}")
    try:
        p = subprocess.run(
            [sys.executable, os.path.join(ROOT, "agreement", "fill.py"), AGREEMENT, empty],
            capture_output=True,
            text=True,
        )
    finally:
        os.remove(empty)
    assert p.returncode == 1
    assert "missing values" in p.stderr


def test_margin_cli_runs_on_example():
    p = subprocess.run(
        [
            sys.executable,
            os.path.join(ROOT, "calculator", "margin.py"),
            os.path.join(ROOT, "examples", "margin.example.json"),
        ],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0
    assert "12 month projection" in p.stdout


if __name__ == "__main__":
    failed = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print("PASS " + name)
            except AssertionError:
                failed += 1
                print("FAIL " + name)
    print("ALL PASSED" if not failed else str(failed) + " FAILED")
    sys.exit(1 if failed else 0)
