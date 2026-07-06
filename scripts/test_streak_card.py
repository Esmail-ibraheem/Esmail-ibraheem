"""Tests for streak computation. Run: python scripts/test_streak_card.py"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from streak_card import compute_streaks, derive_today


def test(name, days, today, current, longest, current_range=None, longest_range=None):
    r = compute_streaks(days, today)
    assert r["current"] == current, f"{name}: current {r['current']} != {current}"
    assert r["longest"] == longest, f"{name}: longest {r['longest']} != {longest}"
    if current_range is not None:
        assert r["current_range"] == current_range, f"{name}: current_range {r['current_range']} != {current_range}"
    if longest_range is not None:
        assert r["longest_range"] == longest_range, f"{name}: longest_range {r['longest_range']} != {longest_range}"
    print(f"  ok: {name}")


test("empty calendar", {}, "2026-07-06", 0, 0, None, None)

test("streak ending today",
     {"2026-07-03": 0, "2026-07-04": 1, "2026-07-05": 2, "2026-07-06": 3},
     "2026-07-06", 3, 3, ("2026-07-04", "2026-07-06"), ("2026-07-04", "2026-07-06"))

test("today zero keeps streak alive",
     {"2026-07-02": 0, "2026-07-03": 1, "2026-07-04": 1, "2026-07-05": 2, "2026-07-06": 0},
     "2026-07-06", 3, 3, ("2026-07-03", "2026-07-05"))

test("today and yesterday zero ends streak",
     {"2026-07-03": 1, "2026-07-04": 1, "2026-07-05": 0, "2026-07-06": 0},
     "2026-07-06", 0, 2, None, ("2026-07-03", "2026-07-04"))

test("longest streak in the past beats current",
     {"2026-06-01": 1, "2026-06-02": 1, "2026-06-03": 4, "2026-06-04": 1, "2026-06-05": 2,
      "2026-06-06": 0, "2026-07-05": 1, "2026-07-06": 1},
     "2026-07-06", 2, 5, ("2026-07-05", "2026-07-06"), ("2026-06-01", "2026-06-05"))

test("single active day", {"2026-07-06": 5}, "2026-07-06", 1, 1,
     ("2026-07-06", "2026-07-06"), ("2026-07-06", "2026-07-06"))

test("missing dates count as gaps",
     {"2026-07-01": 1, "2026-07-03": 1, "2026-07-06": 1},
     "2026-07-06", 1, 1, ("2026-07-06", "2026-07-06"))

assert derive_today({}, "2026-07-06") == "2026-07-06"
assert derive_today({"2026-07-05": 1, "2026-07-06": 8}, "2026-07-06") == "2026-07-06"
assert derive_today({"2026-07-06": 8, "2026-12-31": 0}, "2026-07-06") == "2026-07-06", \
    "future zero-count days from the API must not shift 'today'"
assert derive_today({"2026-07-04": 2, "2026-07-05": 1}, "2026-07-06") == "2026-07-05", \
    "calendar lagging behind real today uses the last calendar day"
print("  ok: derive_today clamps to now")

print("ALL TESTS PASS")
