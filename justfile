# lean-sage-port — Sage's mathematical computation in native Lean 4.
#
# Lake owns Lean compilation, and Lean compilation runs in CI only: `test-ci` is the one recipe
# that compiles. The commit and push recipes are the static scans of the ai-review-ci checkout.
# `tools/inventory` (the `sage-inventory` command) owns the Sage index and the coverage measure.

ai_review_ci := env_var("HOME") / "ai-review-ci"

# Show available recipes
default:
    @just --list

# Run the fast local gate: no Lean compilation
test:
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . lean-no-sorry
    @cd tools/inventory && uv run --locked --quiet pytest -q

# Build the locked Lean targets and scan the sources; for CI
test-ci:
    lake exe cache get
    lake build
    test "$(.lake/build/bin/runtime-quotient 2 1,1,1 0,1)" = "$(printf '\nmaps=true')"
    test "$(.lake/build/bin/runtime-quotient 3 2,0,1 1,2)" = "$(printf '0,2\nmaps=true')"
    test "$(.lake/build/bin/runtime-quotient 3 1,1,1 2,0,1)" = "$(printf '2\nmaps=true')"
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . lean-no-sorry
    @cd tools/inventory && uv run --locked --quiet pytest -q

# Scan staged Lean source; the commit hook runs this
[private]
test-commit:
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . test-commit

# Scan Lean source before a push; the push hook runs this
[private]
test-push:
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . test-push
