# Pricing guide

How to price a white label voice AI business so you earn on the license and on usage. Not legal or tax advice.

## You have two revenue lines

1. **White label fee.** A flat monthly fee for access under your brand, with a set number of sub-accounts included and a fee for each extra one.
2. **Usage markup.** Your customers spend credits on minutes, texts and phone numbers. You buy that usage at your cost and sell it at your price. The gap is your margin.

Most agencies price the first line and forget the second. The second one grows with your customers' success, and it is usually the bigger number after a few months. Put both in your agreement and your rate card.

## How to set a markup

- **2x to 3x your cost is common.** If a voice minute costs you $0.09, a price of $0.18 to $0.27 is normal.
- Start near 2.5x. You can lower a price later. Raising one on live customers is harder.
- Price per minute, not per call. It is easier to explain and it tracks your cost.
- Round to clean numbers. $0.20 per minute reads better than $0.1937.
- Check the whole account, not one line. Run `python calculator/margin.py` with your real costs and look at the margin percentage and the 12 month total.
- Re-check when your vendor changes its rates. Your agreement should let you pass increases through (see section 3 of the template).

## Why prepaid wallets beat billing in arrears

Billing for usage after the fact means you fund your customers' calls and hope they pay. A bad month can cost you more than the fee you collected.

A prepaid wallet fixes that:

- You collect before the cost happens.
- Auto-reload keeps agents running without a conversation about money every month.
- At zero balance the features pause, so a runaway agent or a stolen account cannot rack up a bill you carry.
- Chargebacks drop, because the customer chose the amount.

Set a minimum load that covers a few weeks of normal use, and an auto-reload floor high enough that a busy weekend does not drain it.

## What to put in the rate card

- One-time launch fee and what it covers
- Monthly platform fee, with the number of included sub-accounts
- Price per extra sub-account
- Voice price per minute
- Phone number price per month
- SMS price per segment (long texts are more than one segment)
- Email price per 1,000 sends
- Minimum wallet load and the auto-reload amount and floor
- Reactivation fee, early exit fee and number transfer fee
- Which rates can change, and how much notice you give

Use real numbers in brackets while drafting, then remove the brackets when you send it.

## Red flags in agreements

Read these in any white label agreement you are offered, and check your own for them too.

- **Blank brackets.** Fees, dates or terms left as [____] mean the deal is not finished. Do not sign it.
- **A "cost basis" column.** If a rate card shows what the provider pays its vendors, someone expects you to price off that number, or to argue about it later. Your rates should be the price you pay, not a cost-plus formula you have to defend.
- **Billing usage after the fact.** Usage charged in arrears means you carry the risk and the invoice can be a surprise.
- **No non-circumvention clause.** If you are the provider, this is how you stop a customer from going straight to your vendors after you built the account. If you are the client, read the length and the damages, because 12 months of fees is common and more than that deserves a question.
- **Vague exit terms.** Look for a minimum term, an exit fee, a data export window, and whether you can take your numbers with you.
- **One-sided liability.** A cap that only protects one party is a warning sign.
- **Rates that can change with no notice.** A short notice period is normal. No notice is not.

Have a lawyer in your state review any agreement before you use it. The template in this repo is a starting point.
