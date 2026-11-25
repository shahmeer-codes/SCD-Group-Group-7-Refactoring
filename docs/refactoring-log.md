# Refactoring Log — Phase 3

> **Identity & Attribution Note:** All Phase 3 branches and commits below were prepared and pushed under `shahmeer-codes` (`ranashahmeerarshad@gmail.com`) because `gh` CLI is not installed in this environment and collaborator accounts (`Ahmad-naqvi`, `mughal-codes`, `shahnawz-tech`) cannot be impersonated. Each member's branch is pushed to `origin` with a ready-to-open Pull Request URL targeting `develop`.

---

## 1. Member 1 (`shahmeer-codes`) — Teller & Catalog Contract
- **Original Code Smell:** Feature Envy & Incomplete Abstraction (`Teller.product_with_name` accessing `self.catalog.products`, which was absent from `SupermarketCatalog`; `Teller.checks_out_articles_from` mixing item-pricing loop with checkout orchestration).
- **Original Implementation:**
  ```python
  # python/teller.py
  def product_with_name(self, name):
      return self.catalog.products.get(name, None)
  ```
- **Refactoring Technique:** **Move Method** (`product_with_name` into `SupermarketCatalog` / `FakeCatalog`) and **Extract Method** (`_add_cart_items_to_receipt` in `Teller`).
- **New Implementation:** `SupermarketCatalog` defines `product_with_name(name)`, `FakeCatalog` implements it via `self.products.get(name, None)`, and `Teller` delegates lookup and uses `_add_cart_items_to_receipt(the_cart, receipt)`.
- **Relevant Files:** `python/catalog.py`, `python/teller.py`, `python/tests/fake_catalog.py`, `python/tests/test_teller_catalog.py`
- **Feature Branch:** `refactor/teller-catalog-contract`
- **Commit Hashes:** `c827f23`, `df98093`
- **PR Link:** [PR #1](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/1) (Merged: `98ec2b7`)
- **Test Results:** `cd python && pytest -v` — **31 passed in 0.63s**

---

## 2. Member 2 (`Ahmad-naqvi` — prepared by `shahmeer-codes`) — Decompose Offer Calculation
- **Original Code Smell:** Long Method, Switch Statement on `SpecialOfferType`, Duplicated multi-buy math, Magic Numbers (`2`, `3`, `5`, `100.0`), and Cryptic Naming (`p`, `x`, `number_of_x`, `discount_n`) in `ShoppingCart.handle_offers`.
- **Original Implementation:** 39-line `ShoppingCart.handle_offers` with mixed `if`/`elif` and sequential `if` blocks over `SpecialOfferType`.
- **Refactoring Technique:** **Replace Conditional with Polymorphism** (`OfferStrategy` hierarchy), **Decompose Conditional**, **Extract Method**, **Replace Magic Number with Symbolic Constant**, and **Rename Variable**.
- **New Implementation:** Extracted `OfferStrategy`, `ThreeForTwoStrategy`, `PercentDiscountStrategy`, `BundleForAmountStrategy`, and `OFFER_STRATEGIES` into `python/offer_strategies.py`; `ShoppingCart.handle_offers` delegates cleanly via strategy lookup while preserving exact legacy `TWO_FOR_AMOUNT` division behavior.
- **Relevant Files:** `python/offer_strategies.py`, `python/shopping_cart.py`, `python/tests/test_offer_strategies.py`
- **Feature Branch:** `refactor/decompose-offer-calculation`
- **Commit Hashes:** `a493feb`, `e0135a3`
- **PR Link:** [PR #2](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/2) (Merged: `be08bdb`)
- **Test Results:** `cd python && pytest -v` — **32 passed in 0.67s**

---

## 3. Member 3 (`mughal-codes` — prepared by `shahmeer-codes`) — Receipt Printer Cleanup
- **Original Code Smell:** Tightly Coupled Presentation Logic (`ReceiptPrinter` mixing value formatting with 40-column plain-text layout), Magic Numbers (`40`, `1`), and Imperative String Building (`for i in range(whitespace_size): line += " "`).
- **Original Implementation:** Monolithic `ReceiptPrinter` with character-by-character padding loop and `%` string formatting.
- **Refactoring Technique:** **Extract Class** (`ReceiptFormatter`), **Replace Magic Number with Symbolic Constant** (`DEFAULT_COLUMNS = 40`, `SINGLE_ITEM_QUANTITY = 1`), and **Replace Loop with Pipeline / Expression** (`" " * whitespace_size`, `"".join(lines)`).
- **New Implementation:** `ReceiptFormatter` encapsulates `format_price`, `format_quantity`, and `format_discount_label`; `ReceiptPrinter` delegates formatting and uses symbolic constants and clean string joining.
- **Relevant Files:** `python/receipt_printer.py`, `python/tests/test_receipt_formatter.py`
- **Feature Branch:** `refactor/receipt-printer-cleanup`
- **Commit Hashes:** `cf9882b`, `a7b99a1`
- **PR Link:** [PR #3](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/3) (Merged: `f689779`)
- **Test Results:** `cd python && pytest -v` — **32 passed in 0.62s**

---

## 4. Member 4 (`shahnawz-tech` — prepared by `shahmeer-codes`) — Receipt & Domain Models
- **Original Code Smell:** Imperative summation loops in `Receipt.total_price()` and lack of docstrings / `__repr__` diagnostics on domain objects (`Product`, `ProductQuantity`, `Offer`, `Discount`, `ReceiptItem`).
- **Original Implementation:** Two manual `for` loops in `Receipt.total_price()` and bare `__init__`-only model classes.
- **Refactoring Technique:** **Replace Loop with Pipeline (`sum`)**, **Extract Method** (`items_total()`, `discounts_total()`), and **Encapsulate / Clarify Domain Models** (`__repr__` and docstrings).
- **New Implementation:** `Receipt` exposes `items_total()` and `discounts_total()` using `sum(...)`, and `total_price()` returns `self.items_total() + self.discounts_total()`. Domain classes in `model_objects.py` and `ReceiptItem` include clear docstrings and `__repr__`.
- **Relevant Files:** `python/receipt.py`, `python/model_objects.py`, `python/tests/test_receipt_and_models.py`
- **Feature Branch:** `refactor/receipt-and-domain-models`
- **Commit Hashes:** `f0b9fb1`, `a0a23cc`
- **PR Link:** [PR #4](https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/4) (Merged: `5e566a8`)
- **Test Results:** `cd python && pytest -v` — **31 passed in 0.64s**
