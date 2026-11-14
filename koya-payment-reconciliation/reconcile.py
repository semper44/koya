#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

latest_attempts = {}

with open("payments.jsonl", encoding="utf-8", errors="replace") as payments:
    for line in payments:
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        if not isinstance(event, dict) or not event.get("txn_id"):
            continue

        timestamp = datetime.fromisoformat(event["ts"].replace("Z", "+00:00"))
        txn_id = event["txn_id"]
        previous = latest_attempts.get(txn_id)
        if previous is None or timestamp >= previous[0]:
            latest_attempts[txn_id] = (timestamp, event)

count = 0
total = Decimal("0")
for _, event in latest_attempts.values():
    if event["status"] == "success":
        count += 1
        total += Decimal(str(event["amount"]).replace(",", ""))

with open("expected.txt", encoding="utf-8") as expected_file:
    expected = int(expected_file.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    rounded_total = total.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{rounded_total}")
