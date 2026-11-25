# Member 2 Progress Report — `Ahmad-naqvi`

- **Assigned Responsibility:** Refactoring `ShoppingCart.handle_offers` (Long Method, Switch Statement on `SpecialOfferType`, Duplicated Math, Magic Numbers, Cryptic Naming).
- **Attribution Note:** Implementation and commits were prepared on the feature branch under `shahmeer-codes` because `gh` CLI is unavailable and collaborator accounts cannot be impersonated. `Ahmad-naqvi` should review the branch, verify the diff, and open/approve the PR into `develop`.
- **Implementation:**
  - Created `OfferStrategy`, `ThreeForTwoStrategy`, `PercentDiscountStrategy`, `BundleForAmountStrategy`, and `OFFER_STRATEGIES` in `python/offer_strategies.py`.
  - Refactored `ShoppingCart.handle_offers` (`python/shopping_cart.py`) to delegate to `OFFER_STRATEGIES`.
  - Added unit tests in `python/tests/test_offer_strategies.py`.
- **Feature Branch:** `refactor/decompose-offer-calculation` (pushed to `origin`)
- **Actual Git Commits (Prepared by `shahmeer-codes`):**
  - `a493feb` — `refactor: extract OfferStrategy hierarchy to replace offer conditionals`
  - `e0135a3` — `refactor: delegate ShoppingCart.handle_offers to offer strategies and add tests`
- **Pull Request:** Open PR targeting `develop` at `https://github.com/shahmeer-codes/SCD-Group-Group-7-Refactoring/pull/new/refactor/decompose-offer-calculation`
- **Tests:** `cd python && pytest -v` -> **32 passed in 0.67s**
- **Outstanding Work:** `Ahmad-naqvi` to review, open PR into `develop`, and complete peer review/merge.
