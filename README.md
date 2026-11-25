# SCD Group 7 — Supermarket Receipt Refactoring (Python)

## 1. Project Title
**Supermarket Receipt Refactoring Kata — Python Legacy Code Refactoring (SCD Group 7)**

## 2. Assignment Overview
This repository is our Software Construction and Development (SCD) group assignment focused on refactoring a legacy Python codebase while strictly preserving its external behavior, improving its object-oriented design, validating behavior through characterization and unit tests, and following a structured Git/GitHub feature-branch and Pull Request workflow.

## 3. Original Legacy Repository Source
- **Upstream Kata:** [swkWien/SupermarketReceipt-Refactoring-Kata](https://github.com/swkWien/SupermarketReceipt-Refactoring-Kata) (adapted from Emily Bache's Supermarket Receipt Refactoring Kata for GDCR22)
- **Group Fork:** [shahmeer-codes/SCD-Group-Group-7-Refactoring](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring)

## 4. Selected Python Implementation
Only the `python/` directory and its test suite (`python/tests/`) were analyzed and refactored for this assignment. Other language directories in the repository (`c`, `cpp`, `csharp`, `csharp-ms`, `go`, `java`, `kotlin`, `php`, `ruby`, `swift`, `typescript`) remain untouched.

## 5. Project Objectives
1. Inspect the legacy Python codebase and identify genuine code smells.
2. Capture existing external behavior with characterization tests before modifying production code.
3. Design an improved object-oriented structure using UML class diagrams.
4. Apply Martin Fowler refactoring techniques across four independent feature branches.
5. Integrate changes into `develop` via Pull Requests, then into `main` for release `v1.0.0`.

## 6. Identified Code Smells
1. **Long Method & Complex Conditional Logic** — `ShoppingCart.handle_offers` (`python/shopping_cart.py`)
2. **Switch Statement / Lack of Polymorphism on Type Code** — `SpecialOfferType` branching in `ShoppingCart.handle_offers`
3. **Feature Envy & Inappropriate Intimacy** — `Teller.product_with_name` accessing `catalog.products` (`python/teller.py` vs. `python/catalog.py`) and `ShoppingCart.handle_offers` computing pricing
4. **Duplicated Code & Magic Numbers** — repeated multi-buy discount formulas and literals (`40`, `1`, `2`, `3`, `5`, `100.0`)
5. **Cryptic Variable Naming & Imperative Loops** — single-letter variables (`p`, `x`), character-by-character padding loop in `ReceiptPrinter`, and manual summation loops in `Receipt.total_price`
6. **Tightly Coupled Presentation Logic** — `ReceiptPrinter` mixing value formatting with 40-column plain-text layout

Full details are documented in [docs/baseline-analysis.md](docs/baseline-analysis.md).

## 7. Refactoring Improvements
- **Catalog–Teller Contract:** Moved `product_with_name` onto `SupermarketCatalog` / `FakeCatalog` and extracted `_add_cart_items_to_receipt` in `Teller`.
- **Polymorphic Offer Strategies:** Extracted `OfferStrategy`, `ThreeForTwoStrategy`, `PercentDiscountStrategy`, `BundleForAmountStrategy`, and `OFFER_STRATEGIES` into `python/offer_strategies.py`, replacing the 39-line conditional in `ShoppingCart.handle_offers`.
- **Separated Receipt Formatting:** Extracted `ReceiptFormatter` in `python/receipt_printer.py`, introduced symbolic constants (`DEFAULT_COLUMNS = 40`, `SINGLE_ITEM_QUANTITY = 1`), and replaced imperative loops with string multiplication and `"".join(lines)`.
- **Receipt Pipelines & Domain Clarity:** Extracted `items_total()` and `discounts_total()` using `sum(...)` in `Receipt`, and added docstrings and `__repr__` to domain models (`python/model_objects.py`, `python/receipt.py`).

## 8. Installation Instructions
```bash
git clone https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring.git
cd SCD-Group-Group-7-Refactoring/python
python -m pip install -r requirements.txt
```

## 9. Python Dependencies
Listed in [python/requirements.txt](python/requirements.txt):
- `approvaltests`
- `python-dateutil`
- `pytest-approvaltests`

## 10. How to Run the Project
From the `python/` directory, the TextTest CLI fixture can be executed with:
```bash
cd python
python texttest_fixture.py
```

## 11. How to Run Tests
Run the complete Python test suite (approval tests, characterization tests, and unit tests) from `python/`:
```bash
cd python
pytest -v
```
Latest integrated result on `develop`: **42 passed in 0.65s**.

## 12. Improved OO Design Overview
The refactored architecture separates catalog contracts (`SupermarketCatalog`), checkout orchestration (`Teller`), cart item tracking (`ShoppingCart`), polymorphic discount calculation (`OfferStrategy` hierarchy), receipt aggregation (`Receipt`), and presentation formatting (`ReceiptFormatter` + `ReceiptPrinter`).

## 13. UML Diagram Link
- **Class Diagram Image:** [docs/design-model.png](docs/design-model.png)
- **PlantUML Source:** [docs/design-model.puml](docs/design-model.puml)

## 14. Team Members and Roll Numbers

| Student Name | Roll Number | GitHub Username |
|---|---|---|
| Muhammad Shah Nawaz | SWEN241101006 | `shahnawz-tech` |
| Shahmeer Arshad | SWEN241101027 | `shahmeer-codes` |
| Ahmad Abbas | SWEN241101020 | `Ahmad-naqvi` |
| Mehtab Gohar | SWEN241101030 | `mughal-codes` |

## 15. Individual Contributions
- **Shahmeer Arshad (`shahmeer-codes`):** Repository coordination, baseline & characterization testing, UML design, `Teller`–`SupermarketCatalog` contract refactoring (`refactor/teller-catalog-contract`), and final integration/documentation. *(Note: Feature branch commits for all four tasks were prepared under `shahmeer-codes` and merged via GitHub PRs `#1`–`#4`.)*
- **Ahmad Abbas (`Ahmad-naqvi`):** Assigned `ShoppingCart.handle_offers` decomposition and `OfferStrategy` polymorphism (`refactor/decompose-offer-calculation`).
- **Mehtab Gohar (`mughal-codes`):** Assigned `ReceiptPrinter` cleanup and `ReceiptFormatter` extraction (`refactor/receipt-printer-cleanup`).
- **Muhammad Shah Nawaz (`shahnawz-tech`):** Assigned `Receipt` pipeline helpers and domain model clarity (`refactor/receipt-and-domain-models`).

## 16. Git and GitHub Workflow
```text
main
  └── develop
        ├── refactor/teller-catalog-contract     (PR #1 -> merged: 98ec2b7)
        ├── refactor/decompose-offer-calculation (PR #2 -> merged: be08bdb)
        ├── refactor/receipt-printer-cleanup     (PR #3 -> merged: f689779)
        └── refactor/receipt-and-domain-models   (PR #4 -> merged: 5e566a8)
```

## 17. Pull Request Links
- **PR #1 (Teller Catalog Contract):** https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/1 (`98ec2b7`)
- **PR #2 (Decompose Offer Calculation):** https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/2 (`be08bdb`)
- **PR #3 (Receipt Printer Cleanup):** https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/3 (`f689779`)
- **PR #4 (Receipt and Domain Models):** https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/4 (`5e566a8`)

## 18. Changelog

### v1.0.0
- Added 10 characterization tests (`python/tests/test_characterization.py`) and 14 unit tests across refactored modules (`42 passed` total).
- Refactored `SupermarketCatalog` and `Teller` (`PR #1`), `ShoppingCart` and `OfferStrategy` hierarchy (`PR #2`), `ReceiptFormatter` and `ReceiptPrinter` (`PR #3`), and `Receipt` and `model_objects` (`PR #4`).
- Added baseline analysis, refactoring log, UML class diagram (`docs/design-model.png`), and final assignment report (`docs/final-assignment-report.md`).
- GitHub Release `v1.0.0`: Pending merge of final `develop -> main` Pull Request.

## 19. Release Information
- **Target Release Tag:** `v1.0.0` (to be created and published after `develop -> main` PR is reviewed and merged)
- **Final Assignment Report:** [docs/final-assignment-report.md](docs/final-assignment-report.md)
- **Completion Report:** [docs/progress-reports/final-completion-report.md](docs/progress-reports/final-completion-report.md)
