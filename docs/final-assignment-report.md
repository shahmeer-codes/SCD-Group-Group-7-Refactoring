# Software Construction and Development — Final Assignment Report

**Group:** Group 7  
**Repository:** [SCD-Group-Group-7-Refactoring](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring)  
**Legacy Project:** Supermarket Receipt Refactoring Kata (Python Implementation)  
**Upstream Source:** [swkWien/SupermarketReceipt-Refactoring-Kata](https://github.com/swkWien/SupermarketReceipt-Refactoring-Kata)  

---

## 1. Introduction

Legacy software systems often accumulate structural decay over time—long conditional methods, duplicated business rules, tightly coupled presentation logic, and incomplete abstractions—making new feature development risky and error-prone. Refactoring addresses this decay by improving internal object-oriented design without altering observable external behavior.

For this Software Construction and Development (SCD) group assignment, Group 7 selected the Python implementation (`python/`) of the **Supermarket Receipt Refactoring Kata**. The system models a supermarket point-of-sale checkout workflow: products (`Product`, `ProductUnit`) are stored in a catalog (`SupermarketCatalog`), added to a `ShoppingCart`, evaluated by a `Teller` against promotional `Offer`s (`SpecialOfferType`), recorded onto a `Receipt`, and formatted into a fixed-width ticket by `ReceiptPrinter`. All other language implementations in the repository were left untouched.

The objectives of this assignment were to:
1. Identify genuine code smells in the legacy Python codebase.
2. Establish a safety net of characterization tests before modifying production code.
3. Design a cleaner object-oriented architecture modeled in UML.
4. Execute at least four distinct Martin Fowler refactorings across independent feature branches.
5. Demonstrate disciplined Git and GitHub collaboration using `develop`, feature branches, Pull Requests, and release management.

---

## 2. Team Members and Contributions

| Student Name | Roll Number | GitHub Username | Assigned Scope & Contributions |
|---|---|---|---|
| Shahmeer Arshad | `SWEN241101027` | `shahmeer-codes` | Repository coordination, `develop` baseline setup, characterization tests, UML design, `Teller`–`SupermarketCatalog` contract refactoring (`refactor/teller-catalog-contract`), and final documentation/integration. |
| Ahmad Abbas | `SWEN241101020` | `Ahmad-naqvi` | Assigned `ShoppingCart.handle_offers` decomposition and `OfferStrategy` polymorphism (`refactor/decompose-offer-calculation`). |
| Mehtab Gohar | `SWEN241101030` | `mughal-codes` | Assigned `ReceiptPrinter` presentation decoupling, `ReceiptFormatter` extraction, and symbolic constants (`refactor/receipt-printer-cleanup`). |
| Muhammad Shah Nawaz | `SWEN241101006` | `shahnawz-tech` | Assigned `Receipt` summation pipeline helpers and domain model clarity (`refactor/receipt-and-domain-models`). |

> **Commit Attribution Note:** Because `gh` CLI was unavailable in the local execution environment and collaborator accounts cannot be impersonated, the feature-branch commits (`c827f23`, `df98093`, `a493feb`, `e0135a3`, `cf9882b`, `a7b99a1`, `f0b9fb1`, `a0a23cc`) were prepared under `shahmeer-codes` and integrated into `develop` via GitHub Pull Requests `#1`–`#4`.

---

## 3. Baseline Code Smell Analysis

Inspection of the legacy `python/` codebase (documented in [docs/baseline-analysis.md](baseline-analysis.md)) revealed six genuine code smells:

| Code Smell | Original Location | Fowler Technique | Responsible Member |
|---|---|---|---|
| Long Method & Complex Conditional Logic (39-line `if`/`elif` + sequential `if` blocks) | `python/shopping_cart.py` (`ShoppingCart.handle_offers`) | Decompose Conditional, Extract Method | Ahmad Abbas (`Ahmad-naqvi`) |
| Switch Statement / Lack of Polymorphism on `SpecialOfferType` | `python/shopping_cart.py` (`handle_offers`), `python/model_objects.py` | Replace Conditional with Polymorphism | Ahmad Abbas (`Ahmad-naqvi`) |
| Feature Envy & Incomplete Abstraction (`Teller` accessing `catalog.products` absent from `SupermarketCatalog`) | `python/teller.py` (`Teller.product_with_name`), `python/catalog.py` | Move Method, Extract Method | Shahmeer Arshad (`shahmeer-codes`) |
| Duplicated Multi-Buy Formulas & Magic Numbers (`40`, `1`, `2`, `3`, `5`, `100.0`) | `python/shopping_cart.py`, `python/receipt_printer.py` | Replace Magic Number with Symbolic Constant, Extract Method | Ahmad Abbas & Mehtab Gohar |
| Cryptic Naming (`p`, `x`, `discount_n`) & Imperative Loops (character padding loop, manual total loops) | `python/shopping_cart.py`, `python/receipt_printer.py`, `python/receipt.py` | Rename Variable, Replace Loop with Pipeline (`sum`) | Ahmad Abbas, Mehtab Gohar & Muhammad Shah Nawaz |
| Tightly Coupled Presentation Logic (value formatting mixed with 40-column ASCII layout) | `python/receipt_printer.py` (`ReceiptPrinter`) | Extract Class (`ReceiptFormatter`) | Mehtab Gohar (`mughal-codes`) |

---

## 4. Refactoring Implementation

Each refactoring was implemented on an isolated feature branch created from `develop` and merged back into `develop` via its own Pull Request:

| Refactoring | Feature Branch | Pull Request | Commit Hash |
|---|---|---|---|
| Teller–Catalog Contract & Checkout Helper | `refactor/teller-catalog-contract` | [PR #1](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/1) | `98ec2b7` (merge), `c827f23`, `df98093` |
| OfferStrategy Polymorphism & `handle_offers` Decomposition | `refactor/decompose-offer-calculation` | [PR #2](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/2) | `be08bdb` (merge), `a493feb`, `e0135a3` |
| `ReceiptFormatter` Extraction & Symbolic Constants | `refactor/receipt-printer-cleanup` | [PR #3](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/3) | `f689779` (merge), `cf9882b`, `a7b99a1` |
| `Receipt` Summation Pipelines & Domain Model Clarity | `refactor/receipt-and-domain-models` | [PR #4](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/4) | `5e566a8` (merge), `f0b9fb1`, `a0a23cc` |

Detailed before/after comparisons for every refactoring are recorded in [docs/refactoring-log.md](refactoring-log.md).

---

## 5. Before and After UML Design

### Original Design Problems
In the baseline codebase, no formal UML diagram existed, and responsibilities were blurred across classes:
- `ShoppingCart` acted as both a container for `ProductQuantity` items and a monolithic promotional pricing engine.
- `Teller.product_with_name` bypassed `SupermarketCatalog`'s public interface by reading `catalog.products` directly, which only existed on `FakeCatalog`.
- `ReceiptPrinter` combined value formatting (`%.2f`, `%.3f`, discount labels) with fixed-width 40-column whitespace padding, making future formats (such as the planned HTML receipt) require duplicated traversal and formatting logic.

### Improved Object-Oriented Design
The target UML class diagram is available at [docs/design-model.png](design-model.png) (PlantUML source: [docs/design-model.puml](design-model.puml)).

Key structural improvements include:
1. **`SupermarketCatalog` Contract Alignment:** `product_with_name(name)` is defined on `SupermarketCatalog` and implemented by `FakeCatalog`, so `Teller` depends only on the catalog abstraction.
2. **Polymorphic `OfferStrategy` Hierarchy (`python/offer_strategies.py`):** `OfferStrategy` defines `calculate_discount(product, quantity, unit_price, argument)`. Concrete strategies—`ThreeForTwoStrategy`, `PercentDiscountStrategy`, and parameterized `BundleForAmountStrategy`—eliminate the 39-line conditional in `ShoppingCart.handle_offers` and remove duplicated multi-buy formulas.
3. **Separated `ReceiptFormatter` (`python/receipt_printer.py`):** `ReceiptFormatter` encapsulates `format_price`, `format_quantity`, and `format_discount_label`, while `ReceiptPrinter` focuses on 40-column text layout using `DEFAULT_COLUMNS = 40` and `SINGLE_ITEM_QUANTITY = 1`.
4. **`Receipt` Aggregation Pipelines (`python/receipt.py`):** `items_total()` and `discounts_total()` use `sum(...)` pipelines while preserving defensive copies of `items` and `discounts`.

---

## 6. Testing and Behavior Preservation

### Characterization and Unit Test Suites
- **Existing Approval Tests (`18` tests):** `python/tests/test_supermarket.py` (`12`) and `python/tests/test_receipt_printer.py` (`6`) use `approvaltests` golden files to lock down receipt text output.
- **Phase 2 Characterization Tests (`10` tests):** `python/tests/test_characterization.py` was added before any refactoring to capture edge cases: below-threshold `THREE_FOR_TWO` and `TWO_FOR_AMOUNT`, multi-bundle `THREE_FOR_TWO`, legacy `TWO_FOR_AMOUNT` odd-quantity division (`quantity_as_int / 2`), `KILO` percentage discounts, aggregated cart additions vs. separate receipt lines, `Teller.product_with_name`, `Receipt` defensive copies, custom `ReceiptPrinter(columns=30)`, and `SupermarketCatalog` exceptions.
- **Phase 3 Unit Tests (`14` tests):** Added across `test_teller_catalog.py` (`3`), `test_offer_strategies.py` (`4`), `test_receipt_formatter.py` (`4`), and `test_receipt_and_models.py` (`3`).

### Framework, Command, and Final Results
- **Framework:** `pytest` (`9.2.0`) with `unittest.TestCase` and `approvaltests` (`21.1.0`)
- **Command:** `cd python && pytest -v`
- **Final Integrated Result on `develop`:** **`42 passed in 0.65s`** (0 failures, 0 skipped).

External behavior remained 100% preserved throughout all four refactorings, including legacy `TWO_FOR_AMOUNT` arithmetic (`floor_bundle_count=False`), verified by running the full suite after every individual refactoring and again after all four PRs were merged into `develop`.

---

## 7. Git and GitHub Version Control

The repository was forked from `swkWien/SupermarketReceipt-Refactoring-Kata` into `shahmeer-codes/SCD-Group-Group-7-Refactoring`. A `develop` branch was created from the `with_tests` baseline (`72ee9d3`), and `main` was kept untouched during all development phases.

Four non-overlapping `refactor/*` feature branches were created from `develop`, each containing focused commits and unit tests, and merged into `develop` via Pull Requests `#1`, `#2`, `#3`, and `#4` (`98ec2b7`, `be08bdb`, `f689779`, `5e566a8`). Across the project, more than 25 commits were recorded on `develop` covering characterization tests, baseline analysis, UML modeling, four feature refactorings, unit tests, and progress reports.

At the time of writing this report, the final `develop -> main` Pull Request, `v1.0.0` Git tag, and GitHub Release `v1.0.0` are pending final review and execution on GitHub.

---

## 8. Group Reflection

Working on a real legacy codebase demonstrated how easily business logic can become tangled with data containers and presentation code when features are added incrementally without refactoring. Writing characterization tests before touching any production code proved essential: they gave the team confidence to decompose `ShoppingCart.handle_offers` and `ReceiptPrinter` while immediately catching subtle edge cases such as legacy float division in `TWO_FOR_AMOUNT`. Structuring the work into non-overlapping `refactor/*` branches off `develop` and integrating through Pull Requests prevented merge conflicts across the four modules and kept the commit history auditable. A key practical challenge was coordinating GitHub identity and Pull Request reviews across team members when local tooling (`gh` CLI) was unavailable, which reinforced the importance of clear documentation, explicit attribution, and disciplined branch management.
