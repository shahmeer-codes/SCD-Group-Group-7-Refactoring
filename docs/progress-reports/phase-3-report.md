# Phase 3 Progress Report — Four-Member Refactoring, Feature Branches & Pull Requests

## 1. Implementation Summary
All four distinct refactorings were implemented on separate feature branches created from `develop` (`a651612`), merged into `develop` via Pull Requests `#1`, `#2`, `#3`, and `#4`, and verified together on `develop` (`98ec2b7`). Exact external behavior is preserved across all characterization, approval, and unit tests. No unrelated language implementations were modified, and `main` remains untouched.

> **GitHub & Attribution Transparency:** Because `gh` CLI was not installed in this environment and collaborator accounts (`Ahmad-naqvi`, `mughal-codes`, `shahnawz-tech`) cannot be impersonated, the feature branch commits were created under `shahmeer-codes` and merged via GitHub Pull Requests `#1`–`#4`.

---

## 2. Feature Branches, Commits & Merged PR Status

| Member | Branch | Feature Commits | Merge Commit | Merged PR | Integrated Test Results |
| --- | --- | --- | --- | --- | --- |
| `shahmeer-codes` (Owner) | `refactor/teller-catalog-contract` | `c827f23`, `df98093` | `98ec2b7` | [PR #1](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/1) | `31 passed` on branch; **`42 passed in 1.19s`** integrated on `develop` |
| `Ahmad-naqvi` (prepared by `shahmeer-codes`) | `refactor/decompose-offer-calculation` | `a493feb`, `e0135a3` | `be08bdb` | [PR #2](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/2) | `32 passed` on branch; **`42 passed in 1.19s`** integrated on `develop` |
| `mughal-codes` (prepared by `shahmeer-codes`) | `refactor/receipt-printer-cleanup` | `cf9882b`, `a7b99a1` | `f689779` | [PR #3](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/3) | `32 passed` on branch; **`42 passed in 1.19s`** integrated on `develop` |
| `shahnawz-tech` (prepared by `shahmeer-codes`) | `refactor/receipt-and-domain-models` | `f0b9fb1`, `a0a23cc` | `5e566a8` | [PR #4](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/4) | `31 passed` on branch; **`42 passed in 1.19s`** integrated on `develop` |

---

## 3. Ready-to-Use Pull Request Descriptions (Target: `develop`)

### PR 1: `refactor: move product_with_name contract to SupermarketCatalog and extract Teller helper` (`refactor/teller-catalog-contract` -> `develop`)
- **Problem:** `Teller.product_with_name` accessed `self.catalog.products` directly, which was missing from `SupermarketCatalog`, and `Teller.checks_out_articles_from` mixed item pricing with checkout orchestration.
- **Refactoring technique:** Move Method (`product_with_name` into `SupermarketCatalog` / `FakeCatalog`) and Extract Method (`_add_cart_items_to_receipt`).
- **Implementation:** Added `product_with_name` to `python/catalog.py` and `python/tests/fake_catalog.py`, delegated `Teller.product_with_name` to `self.catalog.product_with_name`, extracted `_add_cart_items_to_receipt` in `python/teller.py`, and added `python/tests/test_teller_catalog.py`.
- **Behavior preservation:** All 28 baseline/characterization tests remain unmodified and passing; lookup and checkout outputs are identical.
- **Testing:** `cd python && pytest -v`
- **Test results:** `31 passed in 0.63s`
- **Review:** Focused strictly on `catalog.py`, `teller.py`, `tests/fake_catalog.py`, and `tests/test_teller_catalog.py`.

### PR 2: `refactor: replace offer conditionals with OfferStrategy hierarchy` (`refactor/decompose-offer-calculation` -> `develop`)
- **Problem:** `ShoppingCart.handle_offers` was a 39-line method with tangled `if`/`elif` and sequential `if` branches over `SpecialOfferType`, duplicated multi-buy math, magic numbers, and cryptic variable names.
- **Refactoring technique:** Replace Conditional with Polymorphism (`OfferStrategy`), Decompose Conditional, Extract Method, Replace Magic Number with Symbolic Constant, Rename Variable.
- **Implementation:** Added `python/offer_strategies.py` (`OfferStrategy`, `ThreeForTwoStrategy`, `PercentDiscountStrategy`, `BundleForAmountStrategy`, `OFFER_STRATEGIES`), refactored `ShoppingCart.handle_offers` in `python/shopping_cart.py`, and added `python/tests/test_offer_strategies.py`.
- **Behavior preservation:** Preserved exact legacy behavior including `TWO_FOR_AMOUNT` division (`floor_bundle_count=False`).
- **Testing:** `cd python && pytest -v`
- **Test results:** `32 passed in 0.67s`
- **Review:** Focused strictly on `offer_strategies.py`, `shopping_cart.py`, and `tests/test_offer_strategies.py`.

### PR 3: `refactor: extract ReceiptFormatter and replace magic numbers in ReceiptPrinter` (`refactor/receipt-printer-cleanup` -> `develop`)
- **Problem:** `ReceiptPrinter` coupled value formatting with 40-column plain-text layout, used magic numbers (`40`, `1`), and built whitespace padding via a character loop.
- **Refactoring technique:** Extract Class (`ReceiptFormatter`), Replace Magic Number with Symbolic Constant (`DEFAULT_COLUMNS`, `SINGLE_ITEM_QUANTITY`), Replace Loop with Expression.
- **Implementation:** Extracted `ReceiptFormatter` in `python/receipt_printer.py`, replaced loops with `" " * whitespace_size` and `"".join(lines)`, and added `python/tests/test_receipt_formatter.py`.
- **Behavior preservation:** All public `ReceiptPrinter` methods and 40-column output formatting are unchanged.
- **Testing:** `cd python && pytest -v`
- **Test results:** `32 passed in 0.62s`
- **Review:** Focused strictly on `receipt_printer.py` and `tests/test_receipt_formatter.py`.

### PR 4: `refactor: extract Receipt total pipelines and clarify domain models` (`refactor/receipt-and-domain-models` -> `develop`)
- **Problem:** `Receipt.total_price` used imperative accumulation loops, and domain models lacked docstrings and `__repr__` representations.
- **Refactoring technique:** Replace Loop with Pipeline (`sum`), Extract Method (`items_total`, `discounts_total`), Encapsulate / Clarify Domain Models.
- **Implementation:** Updated `python/receipt.py` and `python/model_objects.py`, and added `python/tests/test_receipt_and_models.py`.
- **Behavior preservation:** `Receipt.total_price()`, `items`, `discounts`, and object identity semantics remain identical.
- **Testing:** `cd python && pytest -v`
- **Test results:** `31 passed in 0.64s`
- **Review:** Focused strictly on `receipt.py`, `model_objects.py`, and `tests/test_receipt_and_models.py`.

---

## 4. Phase 3 Verification Checklist
- [x] **At least four distinct refactorings:** 4 completed across non-overlapping scopes.
- [x] **Each on its own feature branch:** All 4 `refactor/*` branches created from `develop` and pushed to `origin`.
- [x] **Each has a PR targeting `develop` & `develop` contains approved changes:** All 4 PRs merged into `develop` (`#1` `98ec2b7`, `#2` `be08bdb`, `#3` `f689779`, `#4` `5e566a8`).
- [x] **At least 12 meaningful commits across the group:** 4 commits on `develop` (Phase 2) + 8 commits across the 4 feature branches + 4 PR merge commits + Phase 3 documentation commits = **18+ commits**.
- [x] **Complete Python test suite passes on integrated `develop`:** `cd python && pytest -v` -> **`42 passed in 1.19s`** (12 `test_supermarket.py`, 6 `test_receipt_printer.py`, 10 `test_characterization.py`, 3 `test_teller_catalog.py`, 4 `test_offer_strategies.py`, 4 `test_receipt_formatter.py`, 3 `test_receipt_and_models.py`).
- [x] **`main` not prematurely modified:** `origin/main` remains untouched.
- [x] **No unrelated language implementation changed:** Only `python/` and `docs/` were modified.
- [x] **UML & documentation updated:** [design-model.puml](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/design-model.puml), [design-model.png](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/design-model.png), [refactoring-log.md](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/refactoring-log.md), and `member-1` through `member-4` reports created.
