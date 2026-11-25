# Baseline Analysis — Phase 1

## 1. Project Overview

- **Assignment:** Software Construction and Development (SCD) — Legacy Code Refactoring
- **Group:** Group 7
- **Repository:** `SCD-Group-Group-7-Refactoring` (`https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring.git`)
- **Legacy Kata:** *The Supermarket Receipt Refactoring Kata* (forked from Emily Bache's kata with GDCR22 feature requirements in `README.md`)
- **Selected Implementation:** Python (`python/` directory)

The system models a supermarket checkout flow:
1. Products (`Product`, `ProductUnit`) are registered in a catalog (`SupermarketCatalog` / `FakeCatalog` in tests).
2. A customer adds items and quantities (`ProductQuantity`) to a `ShoppingCart`.
3. A `Teller` registers `Offer`s (`SpecialOfferType`) and checks out the cart, producing a `Receipt` containing `ReceiptItem`s and `Discount`s.
4. `ReceiptPrinter` formats the `Receipt` into a fixed-width plain-text receipt.

Other language directories (`c`, `cpp`, `csharp`, `csharp-ms`, `go`, `java`, `kotlin`, `php`, `ruby`, `swift`, `typescript`) exist in the repository and are **out of scope** for this assignment.

---

## 2. Selected Python Implementation Inventory

| File | Responsibility |
| --- | --- |
| `python/model_objects.py` | Domain models and enums: `Product`, `ProductQuantity`, `ProductUnit`, `SpecialOfferType`, `Offer`, `Discount`. |
| `python/catalog.py` | Abstract/stub `SupermarketCatalog` (`add_product`, `unit_price` raising `Exception` in unit tests). |
| `python/shopping_cart.py` | `ShoppingCart` storing `_items` and `_product_quantities`, and evaluating discounts in `handle_offers`. |
| `python/teller.py` | `Teller` managing `offers`, `checks_out_articles_from`, and `product_with_name`. |
| `python/receipt.py` | `ReceiptItem` and `Receipt` (accumulating items, discounts, and computing `total_price`). |
| `python/receipt_printer.py` | `ReceiptPrinter` formatting receipts into 40-column plain text. |
| `python/texttest_fixture.py` | CLI runner for TextTest characterization tests. |
| `python/requirements.txt` | Dependencies: `approvaltests`, `python-dateutil`, `pytest-approvaltests`. |

---

## 3. Identified Code Smells

### Smell 1: Long Method & Complex Conditional Logic
- **Location:** `python/shopping_cart.py` — `ShoppingCart.handle_offers` (lines 30–68)
- **Why it is a problem:** `handle_offers` is 39 lines long and mixes an `if`/`elif` block (`THREE_FOR_TWO`, `TWO_FOR_AMOUNT`) with four separate sequential `if` blocks (`FIVE_FOR_AMOUNT`, `THREE_FOR_TWO` again, `TEN_PERCENT_DISCOUNT`, `FIVE_FOR_AMOUNT` again). Control flow is hard to follow, and `x` is initialized to `1` and reassigned across disjoint branches before `number_of_x = math.floor(quantity_as_int / x)` is computed.
- **Problematic snippet:**
  ```python
  if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
      x = 3
  elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
      x = 2
      if quantity_as_int >= 2:
          total = offer.argument * (quantity_as_int / x) + quantity_as_int % 2 * unit_price
          ...
  if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
      x = 5
  number_of_x = math.floor(quantity_as_int / x)
  if offer.offer_type == SpecialOfferType.THREE_FOR_TWO and quantity_as_int > 2:
      ...
  ```
- **Fowler Refactoring Technique:** **Decompose Conditional** & **Extract Method**
- **Proposed Improvement:** Split each offer calculation into a dedicated, clearly named helper method (or strategy) and use mutually exclusive `if`/`elif` branches.
- **Expected Effect:** Shorter, single-purpose methods, lower cyclomatic complexity, and easier verification of each offer rule.

### Smell 2: Switch Statement / Lack of Polymorphism on Type Code
- **Location:** `python/shopping_cart.py` — `ShoppingCart.handle_offers` branching on `SpecialOfferType` (`python/model_objects.py`, lines 21–25)
- **Why it is a problem:** Every time a new offer type is introduced (such as the planned *discounted bundles* feature in `README.md`), `handle_offers` must be modified with new conditional branches, violating the Open/Closed Principle.
- **Problematic snippet:**
  ```python
  if offer.offer_type == SpecialOfferType.THREE_FOR_TWO ...
  if offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT ...
  if offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT ...
  ```
- **Fowler Refactoring Technique:** **Replace Conditional with Polymorphism** (Strategy pattern per offer type)
- **Proposed Improvement:** Represent offer calculation behavior in dedicated offer/discount strategy classes or polymorphic `Offer` subclasses/handlers mapped by `SpecialOfferType`.
- **Expected Effect:** New offer types can be added without modifying existing checkout or cart logic.

### Smell 3: Feature Envy & Inappropriate Intimacy
- **Location:**
  - `python/shopping_cart.py` — `ShoppingCart.handle_offers` (lines 30–68)
  - `python/teller.py` — `Teller.product_with_name` (lines 28–29) & `python/catalog.py` — `SupermarketCatalog` (lines 2–8)
- **Why it is a problem:**
  1. `ShoppingCart.handle_offers` reaches heavily into `Offer` (`offer_type`, `argument`), `SupermarketCatalog.unit_price`, and `Receipt.add_discount`. A shopping cart should manage items, not calculate promotional pricing.
  2. `Teller.product_with_name` directly accesses `self.catalog.products.get(name, None)`, assuming a `.products` dictionary attribute that does not exist on `SupermarketCatalog` in `catalog.py` (only on `FakeCatalog` in `tests/fake_catalog.py`).
- **Problematic snippet:**
  ```python
  # teller.py
  def product_with_name(self, name):
      return self.catalog.products.get(name, None)
  ```
- **Fowler Refactoring Technique:** **Move Method** (and **Extract Class** / interface alignment)
- **Proposed Improvement:** Define `product_with_name` on `SupermarketCatalog` (and implement it on `FakeCatalog`), and move offer evaluation responsibility out of `ShoppingCart` into an offer/pricing collaborator invoked by `Teller`.
- **Expected Effect:** Clearer class boundaries, reduced coupling, and a consistent `SupermarketCatalog` contract.

### Smell 4: Duplicated Code & Magic Numbers
- **Location:**
  - `python/shopping_cart.py` (lines 42–66)
  - `python/receipt_printer.py` (`columns=40` on line 5, `item.quantity != 1` on line 26, `"%.2f"` / `'%.3f'` on lines 40, 46)
- **Why it is a problem:** The discount formula `unit_price * quantity - (...)` and `Discount(p, ..., -...)` construction are repeated across `TWO_FOR_AMOUNT`, `THREE_FOR_TWO`, and `FIVE_FOR_AMOUNT`. Magic numbers (`2`, `3`, `5`, `100.0`, `40`, `1`) and hardcoded format strings obscure business meaning.
- **Problematic snippet:**
  ```python
  discount_n = unit_price * quantity - total
  discount = Discount(p, "2 for " + str(offer.argument), -discount_n)
  ...
  discount_total = unit_price * quantity - (
      offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
  discount = Discount(p, str(x) + " for " + str(offer.argument), -discount_total)
  ```
- **Fowler Refactoring Technique:** **Replace Magic Number with Symbolic Constant** & **Extract Method**
- **Proposed Improvement:** Extract shared bundle/multi-buy discount calculation helpers and replace literal constants (`DEFAULT_COLUMNS = 40`, `SINGLE_ITEM_QUANTITY = 1`, `PERCENTAGE_DIVISOR = 100.0`, etc.) with named constants.
- **Expected Effect:** Eliminates duplication and makes business rules self-documenting.

### Smell 5: Cryptic Variable Naming & Imperative Loops
- **Location:**
  - `python/shopping_cart.py` (`p`, `x`, `number_of_x`, `discount_n`, `discount_total`)
  - `python/receipt_printer.py` (`format_line_with_whitespace`, lines 30–37)
  - `python/receipt.py` (`Receipt.total_price`, lines 15–21)
- **Why it is a problem:** Single-letter and inconsistent names (`p`, `x`, `discount_n`) make financial math difficult to verify (note also line 45 uses `quantity_as_int / x` instead of floor division). `format_line_with_whitespace` builds padding via a character-by-character `for` loop, and `Receipt.total_price` manually accumulates totals in two loops.
- **Problematic snippet:**
  ```python
  # receipt_printer.py
  whitespace_size = self.columns - len(name) - len(value)
  for i in range(whitespace_size):
      line += " "
  ```
- **Fowler Refactoring Technique:** **Rename Method / Variable** & **Replace Loop with Pipeline (`sum` / string multiplication)**
- **Proposed Improvement:** Use descriptive names (`product`, `bundle_size`, `bundle_count`, `discount_amount`), use `" " * max(0, whitespace_size)` (preserving exact output), and use `sum(...)` in `Receipt.total_price()`.
- **Expected Effect:** Improved readability and fewer opportunities for subtle arithmetic or formatting bugs.

### Smell 6: Tightly Coupled Presentation Logic (Divergent Change Risk)
- **Location:** `python/receipt_printer.py` — `ReceiptPrinter` (lines 3–56)
- **Why it is a problem:** `ReceiptPrinter` mixes receipt iteration/data formatting with 40-column plain-text layout. Adding the requested *HTML receipt* feature (`README.md`) would currently require duplicating the traversal and number-formatting logic.
- **Fowler Refactoring Technique:** **Extract Class** / **Extract Method** (separating formatting primitives from receipt rendering)
- **Proposed Improvement:** Separate receipt data/number formatting helpers from plain-text line layout so future renderers (e.g., HTML) can reuse formatting without duplication.
- **Expected Effect:** Prepares the codebase cleanly for new output formats without altering current plain-text output.

---

## 4. Four-Member Responsibility Distribution

| Member | GitHub Username | Assigned Code Smell | Refactoring Technique | Files / Functions | Proposed Branch |
| --- | --- | --- | --- | --- | --- |
| Me (Owner) | `shahmeer-codes` | Coordination, baseline integration & Feature Envy / Incomplete Abstraction in Teller–Catalog | Move Method, Extract Method | `python/teller.py` (`Teller`), `python/catalog.py` (`SupermarketCatalog`), `python/tests/fake_catalog.py` (`FakeCatalog`) | `refactor/teller-catalog-contract` |
| Member 2 | `Ahmad-naqvi` | Long Method, Switch Statement & Cryptic Naming in `handle_offers` | Decompose Conditional, Extract Method, Replace Conditional with Polymorphism, Rename Variable | `python/shopping_cart.py` (`ShoppingCart.handle_offers`) | `refactor/decompose-offer-calculation` |
| Member 3 | `mughal-codes` | Tightly Coupled Presentation, Magic Numbers & Imperative String Building | Extract Class / Method, Replace Magic Number with Symbolic Constant | `python/receipt_printer.py` (`ReceiptPrinter`) | `refactor/receipt-printer-cleanup` |
| Member 4 | `shahnawz-tech` | Imperative Loops & Weak Domain Encapsulation in Receipt and Models | Replace Loop with Pipeline, Encapsulate Field, Rename Method | `python/receipt.py` (`Receipt`, `ReceiptItem`), `python/model_objects.py` (`Offer`, `Discount`, `Product`) | `refactor/receipt-and-domain-models` |

---

## 5. Characterization Testing Strategy

- **Testing Framework:** `pytest` (running `unittest.TestCase` suites) with `approvaltests` (`pytest-approvaltests`) and golden files in `python/tests/approved_files/`. Optional `TextTest` suite exists in `python/texttest/`.
- **Command:** `cd python && pytest -v`
- **Baseline Execution Result:** **28 passed in 0.60s**:
  - `tests/test_supermarket.py`: 12 approval tests (empty cart, normal items, `THREE_FOR_TWO`, `TWO_FOR_AMOUNT`, `FIVE_FOR_AMOUNT`, `TEN_PERCENT_DISCOUNT`, loose weight).
  - `tests/test_receipt_printer.py`: 6 approval tests (line items, quantities, loose weight, totals, discounts, full receipt).
  - `tests/test_characterization.py`: 10 characterization unit tests added in Phase 2 covering below-threshold offers (`THREE_FOR_TWO` with 2 items, `TWO_FOR_AMOUNT` with 1 item), multi-bundle `THREE_FOR_TWO` (6 items), `TWO_FOR_AMOUNT` with 3 items (preserving the existing `quantity_as_int / x` behavior), `TEN_PERCENT_DISCOUNT` at 20% on `KILO` items, aggregated cart items vs. separate receipt lines, `Teller.product_with_name` found/missing, `Receipt` defensive copies, `ReceiptPrinter(columns=30)`, and `SupermarketCatalog` base exceptions.

---

## 6. Target Object-Oriented Design & UML Reference

The target refactored design is captured in:
- **PlantUML Source:** [design-model.puml](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/design-model.puml)
- **Rendered Class Diagram:** [design-model.png](file:///c:/Users/Shahmeer/Desktop/ahmad%20project/SCD-Group-Group-7-Refactoring/docs/design-model.png)

### How the Target Design Addresses Phase 1 Code Smells
1. **Catalog–Teller Contract (`SupermarketCatalog`, `FakeCatalog`, `Teller`):** Moves `product_with_name` onto `SupermarketCatalog` (implemented by `FakeCatalog`), eliminating `Teller`'s direct access to `catalog.products`. Extracts `_add_cart_items_to_receipt` in `Teller` to clarify checkout orchestration.
2. **Polymorphic Offer Strategies (`OfferStrategy`, `ThreeForTwoStrategy`, `PercentDiscountStrategy`, `BundleForAmountStrategy`):** Replaces the 39-line `if`/`elif` block in `ShoppingCart.handle_offers` with clean strategy objects. `BundleForAmountStrategy(bundle_size)` unifies `TWO_FOR_AMOUNT` and `FIVE_FOR_AMOUNT`, eliminating duplicated multi-buy formulas and magic numbers.
3. **Separated Receipt Presentation (`ReceiptFormatter`, `ReceiptPrinter`):** Extracts `format_price`, `format_quantity`, and `format_discount_label` into `ReceiptFormatter` and replaces magic numbers (`DEFAULT_COLUMNS = 40`) and character-by-character padding loops, preparing the codebase for future HTML receipt output without duplicating formatting logic.
4. **Domain Encapsulation (`Receipt`, `model_objects`):** Simplifies `Receipt.total_price()` using pipeline summation while preserving defensive copies of `items` and `discounts`.

---

## 7. Proposed Git Branching Strategy

- **Observed Branches:** `with_tests` (current local & `origin/HEAD`), `origin/main`. No `develop` branch exists yet.
- **Intended Workflow:**
  ```text
  main
    |
  develop
    |
    |-- refactor/teller-catalog-contract
    |-- refactor/decompose-offer-calculation
    |-- refactor/receipt-printer-cleanup
    |-- refactor/receipt-and-domain-models
  ```
- **Integration Plan:**
  1. Create `develop` from the verified baseline (`with_tests` / `main` as agreed).
  2. Each member branches off `develop` into their assigned `refactor/*` feature branch.
  3. Each feature branch is merged into `develop` via its own Pull Request with tests passing.
  4. Final `develop` branch is merged into `main` via Pull Request.
- **Permissions / Protection Note:** Local Git inspection cannot verify GitHub branch-protection rules or collaborator write permissions; these should be checked in GitHub Repository Settings (`Settings -> Branches` and `Settings -> Collaborators`).
