# Phase 1 Progress Report — Repository Inspection, Code Smells & Task Distribution

## 1. Repository Inspected
- **Repository:** `SCD-Group-Group-7-Refactoring` (`https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring.git`)
- **Group Number:** Group 7
- **Current Local Branch:** `with_tests` (tracking `origin/with_tests`; `origin/main` also present)
- **Python Folder Identified:** `python/`
- **Selected Legacy Code:** *The Supermarket Receipt Refactoring Kata* (Python implementation)

## 2. Files Inspected (No Source Code Modified)
- `README.md` (kata description and new feature context)
- `python/README.md`, `python/requirements.txt`
- `python/catalog.py`, `python/model_objects.py`, `python/receipt.py`, `python/receipt_printer.py`, `python/shopping_cart.py`, `python/teller.py`, `python/texttest_fixture.py`
- `python/tests/fake_catalog.py`, `python/tests/test_receipt_printer.py`, `python/tests/test_supermarket.py`

## 3. Identified Code Smells Summary
1. **Long Method & Complex Conditional Logic** — `ShoppingCart.handle_offers` (`python/shopping_cart.py`)
2. **Switch Statement / Lack of Polymorphism** — `SpecialOfferType` branching in `ShoppingCart.handle_offers` (`python/shopping_cart.py`, `python/model_objects.py`)
3. **Feature Envy & Inappropriate Intimacy** — `ShoppingCart.handle_offers` (`python/shopping_cart.py`) and `Teller.product_with_name` (`python/teller.py` vs. `python/catalog.py`)
4. **Duplicated Code & Magic Numbers** — Repeated discount formulas and literal constants (`python/shopping_cart.py`, `python/receipt_printer.py`)
5. **Cryptic Variable Naming & Imperative Loops** — `p`, `x`, `discount_n` (`python/shopping_cart.py`), character-by-character padding loop (`python/receipt_printer.py`), manual total loops (`python/receipt.py`)
6. **Tightly Coupled Presentation Logic** — `ReceiptPrinter` mixing traversal with 40-column ASCII formatting (`python/receipt_printer.py`)

Full details, snippets, and Martin Fowler refactoring techniques are documented in [baseline-analysis.md](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/baseline-analysis.md).

## 4. Team Responsibilities & Proposed Feature Branches
- **Me (`shahmeer-codes`):** Coordination, `develop` baseline integration, and refactoring `Teller`/`SupermarketCatalog` contract (`python/teller.py`, `python/catalog.py`, `python/tests/fake_catalog.py`) — Branch: `refactor/teller-catalog-contract`
- **`Ahmad-naqvi`:** Refactoring `ShoppingCart.handle_offers` (`python/shopping_cart.py`) — Branch: `refactor/decompose-offer-calculation`
- **`mughal-codes`:** Refactoring `ReceiptPrinter` (`python/receipt_printer.py`) — Branch: `refactor/receipt-printer-cleanup`
- **`shahnawz-tech`:** Refactoring `Receipt` and domain models (`python/receipt.py`, `python/model_objects.py`) — Branch: `refactor/receipt-and-domain-models`

## 5. Testing Observations
- Executed `pytest -v` in `python/`: **18 passed in 1.02s** (12 in `test_supermarket.py`, 6 in `test_receipt_printer.py`).
- Existing tests use `approvaltests` for golden-master characterization.
- Gaps identified: edge cases for `TWO_FOR_AMOUNT` (quantities 1 and 3), `THREE_FOR_TWO` below threshold, `TEN_PERCENT_DISCOUNT` on `KILO` items and non-10% rates, `Teller.product_with_name`, and direct unit tests on `Receipt`.

## 6. Remaining Work for Phase 2
1. Confirm GitHub collaborator access and branch-protection rules on `main` and `develop`.
2. Create the `develop` branch from the verified baseline.
3. Add missing characterization/unit tests before refactoring to lock down edge-case behavior.
4. Create the four `refactor/*` feature branches from `develop` and execute each refactoring task independently.
5. Open Pull Requests from each feature branch into `develop`, verify `pytest` passes on each, and merge `develop` into `main` via PR.
