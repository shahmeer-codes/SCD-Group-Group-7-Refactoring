# Member 4 Progress Report — `shahnawz-tech`

- **Assigned Responsibility:** Refactoring `Receipt` (`python/receipt.py`) and domain models (`python/model_objects.py`) to replace imperative summation loops and improve domain object clarity.
- **Attribution Note:** Implementation and commits were prepared on the feature branch under `shahmeer-codes` because `gh` CLI is unavailable and collaborator accounts cannot be impersonated. `shahnawz-tech` should review the branch, verify the diff, and open/approve the PR into `develop`.
- **Implementation:**
  - Extracted `items_total()` and `discounts_total()` using `sum(...)` pipelines in `Receipt`, and simplified `total_price()`.
  - Added concise docstrings and `__repr__` methods to `ReceiptItem`, `Product`, `ProductQuantity`, `Offer`, and `Discount`.
  - Added unit tests in `python/tests/test_receipt_and_models.py`.
- **Feature Branch:** `refactor/receipt-and-domain-models` (pushed to `origin`)
- **Actual Git Commits (Prepared by `shahmeer-codes`):**
  - `f0b9fb1` — `refactor: extract items_total and discounts_total pipelines in Receipt`
  - `a0a23cc` — `refactor: add docstrings and __repr__ to domain models and add tests`
- **Pull Request:** Open PR targeting `develop` at `https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/new/refactor/receipt-and-domain-models`
- **Tests:** `cd python && pytest -v` -> **31 passed in 0.64s**
- **Outstanding Work:** `shahnawz-tech` to review, open PR into `develop`, and complete peer review/merge.
