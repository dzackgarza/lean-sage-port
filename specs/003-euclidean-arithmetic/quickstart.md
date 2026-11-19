# Acceptance path for Euclidean arithmetic

1. Read `inventory/sage/release.toml` and the three `euclidean.*` records in `inventory/capabilities/integers-and-rationals.toml`. Resolve their selectors through `inventory/sage/index/entities.jsonl.gz` and `modules.jsonl` to obtain the existing Sage doctests.
2. Include Sage's univariate polynomial doctests for `Polynomial.quo_rem`, `gcd`, `lcm` and `xgcd` over fields. Use their stated optional-package conditions.
3. Build the later native public operations in CI, as required by `AGENTS.md`. Run the selected source examples and compare further same-input integer, rational and field-polynomial cases with the Sage oracle in `docs/oracles.md`.
4. Check quotient reconstruction and decrease; signed integer remainder; zero-divisor failure; gcd/lcm divisibility and normalization; Bézout identities for pairs and lists. Compare coefficients by identity, not tuple equality.
5. Retain revision, environment, runtime inputs, setup and nested computation timing in the acceptance logs.

Expected result: the public operations satisfy `contracts/euclidean-operations.md` under each stated domain and normalize results without changing the coefficient object.
