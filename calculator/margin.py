#!/usr/bin/env python3
"""White label voice AI margin calculator.

Usage: python calculator/margin.py examples/margin.example.json

Same math as calculator/margin.html. Prices are in dollars per month.
"""
import json
import math
import sys

DEFAULTS = {
    "sub_accounts_live": 12,
    "sub_accounts_included": 10,
    "platform_fee": 497,
    "extra_sub_account_fee": 30,
    "platform_cost": 297,
    "minutes_per_month": 6000,
    "cost_per_minute": 0.09,
    "price_per_minute": 0.20,
    "phone_numbers": 12,
    "number_cost": 1.15,
    "number_price": 3.00,
    "sms_segments": 8000,
    "sms_cost_per_segment": 0.008,
    "sms_price_per_segment": 0.02,
    "monthly_growth_pct": 5,
}


def _round_half_up(x):
    return math.floor(x + 0.5)


def month_numbers(cfg, scale=1.0):
    """Revenue, cost and margin for one month. scale grows subs and usage."""
    subs = _round_half_up(cfg["sub_accounts_live"] * scale)
    extra = max(0, subs - cfg["sub_accounts_included"])
    minutes = cfg["minutes_per_month"] * scale
    numbers = cfg["phone_numbers"] * scale
    sms = cfg["sms_segments"] * scale

    revenue_platform = cfg["platform_fee"] + extra * cfg["extra_sub_account_fee"]
    revenue_usage = (
        minutes * cfg["price_per_minute"]
        + numbers * cfg["number_price"]
        + sms * cfg["sms_price_per_segment"]
    )
    cost_usage = (
        minutes * cfg["cost_per_minute"]
        + numbers * cfg["number_cost"]
        + sms * cfg["sms_cost_per_segment"]
    )
    revenue = revenue_platform + revenue_usage
    cost = cfg["platform_cost"] + cost_usage
    margin = revenue - cost
    return {
        "sub_accounts": subs,
        "revenue_platform": revenue_platform,
        "revenue_usage": revenue_usage,
        "revenue": revenue,
        "cost": cost,
        "margin": margin,
        "margin_pct": (margin / revenue * 100) if revenue else 0.0,
        "usage_markup": (revenue_usage / cost_usage) if cost_usage else 0.0,
        "markup_multiple": (revenue / cost) if cost else 0.0,
    }


def calculate(cfg):
    """Return month-one numbers plus a 12 month projection."""
    full = dict(DEFAULTS)
    full.update(cfg)
    growth = full["monthly_growth_pct"] / 100.0
    result = month_numbers(full)
    projection = []
    cumulative = 0.0
    for m in range(1, 13):
        row = month_numbers(full, (1 + growth) ** (m - 1))
        cumulative += row["margin"]
        projection.append(
            {
                "month": m,
                "sub_accounts": row["sub_accounts"],
                "revenue": row["revenue"],
                "cost": row["cost"],
                "margin": row["margin"],
                "cumulative_margin": cumulative,
            }
        )
    result["projection"] = projection
    result["year_revenue"] = sum(r["revenue"] for r in projection)
    result["year_cost"] = sum(r["cost"] for r in projection)
    result["year_margin"] = cumulative
    return result


def money(x):
    return f"${x:,.2f}"


def report(res):
    lines = [
        "Month one",
        f"  Sub-accounts live    {res['sub_accounts']}",
        f"  Revenue              {money(res['revenue'])}"
        f"  (platform {money(res['revenue_platform'])}, usage {money(res['revenue_usage'])})",
        f"  Cost                 {money(res['cost'])}",
        f"  Margin               {money(res['margin'])}  ({res['margin_pct']:.1f}%)",
        f"  Markup multiple      {res['markup_multiple']:.2f}x revenue over cost",
        f"  Usage markup         {res['usage_markup']:.2f}x price over cost",
        "",
        "12 month projection",
        "  Month  Subs   Revenue       Cost        Margin   Cumulative",
    ]
    for r in res["projection"]:
        lines.append(
            f"  {r['month']:>5}  {r['sub_accounts']:>4}  {r['revenue']:>10,.2f}  "
            f"{r['cost']:>10,.2f}  {r['margin']:>10,.2f}  {r['cumulative_margin']:>11,.2f}"
        )
    lines.append(
        f"  Year   revenue {money(res['year_revenue'])}, cost {money(res['year_cost'])}, "
        f"margin {money(res['year_margin'])}"
    )
    return "\n".join(lines)


def main(argv):
    if len(argv) != 2:
        print("usage: margin.py config.json", file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        cfg = json.load(f)
    unknown = [k for k in cfg if k not in DEFAULTS and not k.startswith("_")]
    if unknown:
        print("error: unknown keys: " + ", ".join(unknown), file=sys.stderr)
        return 1
    print(report(calculate(cfg)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
