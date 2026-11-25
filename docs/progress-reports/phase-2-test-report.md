# Phase 2 Test Report — Characterization Test Results

## 1. Test Environment & Framework
- **Framework:** `pytest` (`9.2.0`) with `unittest.TestCase` and `approvaltests` (`21.1.0`)
- **Python Version:** Python `3.15.0` on Windows (`win32`)
- **Working Directory:** `python/`
- **Command Executed:** `pytest -v`

## 2. Test Suites Executed
| Test File | Test Count | Purpose |
| --- | --- | --- |
| `python/tests/test_supermarket.py` | 12 | Existing approval tests for checkout and special offers |
| `python/tests/test_receipt_printer.py` | 6 | Existing approval tests for 40-column receipt formatting |
| `python/tests/test_characterization.py` | 10 | New Phase 2 characterization tests for edge cases and boundaries |
| **Total** | **28** | **All 28 tests passed (`28 passed in 0.60s`)** |

## 3. Characterization Cases Added (`test_characterization.py`)
1. `test_three_for_two_below_threshold_gives_no_discount` — verifies 2 items under `THREE_FOR_TWO` receive no discount.
2. `test_three_for_two_for_six_items_applies_twice` — verifies 6 items receive 2 free items (`-1.98`).
3. `test_two_for_amount_below_threshold_gives_no_discount` — verifies 1 item under `TWO_FOR_AMOUNT` receives no discount.
4. `test_two_for_amount_with_three_items_preserves_existing_calculation` — locks down current `offer.argument * (3 / 2) + unit_price` behavior.
5. `test_percent_discount_on_loose_weight_product` — verifies `20.0% off` on `2.5` kg `KILO` product.
6. `test_multiple_add_item_calls_aggregate_for_offer_but_keep_receipt_lines` — verifies separate cart additions aggregate for offer calculation while preserving separate receipt lines.
7. `test_teller_product_with_name_found_and_missing` — verifies `Teller.product_with_name` returns `Product` or `None`.
8. `test_receipt_returns_defensive_copies` — verifies `Receipt.items` and `Receipt.discounts` return shallow copies and `total_price()` sums items + negative discounts.
9. `test_receipt_printer_custom_columns_and_each_quantity_formatting` — verifies `ReceiptPrinter(columns=30)` line width and `EACH` quantity formatting.
10. `test_base_supermarket_catalog_raises_exception` — verifies `SupermarketCatalog` base methods raise `Exception`.

## 4. Observations
- Zero application source files were modified.
- All 28 tests pass with no skipped or relaxed assertions.
