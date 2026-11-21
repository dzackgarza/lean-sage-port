# lean-sage-port — Sage's mathematical computation in native Lean 4.
#
# The feedback loop is local and incremental. `lean-setup` prepares the locked Lean environment
# once per lock; after it, `check-lean` elaborates one file in seconds and `test` rebuilds only
# what changed. CI runs the same `test` on a clean machine. `tools/inventory` (the
# `sage-inventory` command) owns the Sage index and the coverage measure.

ai_review_ci := env_var("HOME") / "ai-review-ci"

# Packages are shared machine-wide per Mathlib revision, so that every checkout of one lock reuses
# one Mathlib cache and one build of Hex.
mathlib_rev := `jq -r '.packages[] | select(.name == "mathlib") | .rev[0:7]' lake-manifest.json`
lean_packages := env_var("HOME") / ".local/share/lean" / ("mathlib-" + mathlib_rev) / "packages"

# Lake compares each package's `git remote get-url` with the manifest URL. A global
# `url.*.insteadOf` rewrite makes them differ, and Lake then resets every remote and logs it on
# each call. Lake reads the repository configuration only.
lake := "env GIT_CONFIG_GLOBAL=/dev/null lake --log-level=error"

# Show available recipes
default:
    @just --list

# Prepare the locked Lean environment: package checkouts at their locked revisions, Mathlib cache
lean-setup:
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p "{{lean_packages}}" .lake
    ln -sfn "{{lean_packages}}" .lake/packages
    jq -r '.packages[] | "\(.name) \(.url) \(.rev)"' lake-manifest.json | while read -r name url rev; do
        repo="{{lean_packages}}/$name"
        [ -d "$repo/.git" ] || { git init -q "$repo"; git -C "$repo" remote add origin "$url"; }
        head="$(git -C "$repo" rev-parse -q --verify HEAD || true)"
        [ "$head" = "$rev" ] && [ -z "$(git -C "$repo" status --porcelain)" ] && continue
        git -C "$repo" cat-file -e "$rev^{commit}" 2>/dev/null || git -C "$repo" fetch -q --depth=1 origin "$rev"
        git -C "$repo" update-ref --no-deref HEAD "$rev"
        git -C "$repo" read-tree -u --reset HEAD
    done
    {{lake}} exe cache get

# Elaborate one Lean file; Lake first rebuilds the modules that it imports and that changed
check-lean file:
    {{lake}} lean {{file}}

# The gate: incremental Lean build, probe executables, sorry scan, inventory tests
test:
    {{lake}} build
    test "$(.lake/build/bin/runtime-quotient 2 1,1,1 0,1)" = "$(printf '\nmaps=true')"
    test "$(.lake/build/bin/runtime-quotient 3 2,0,1 1,2)" = "$(printf '0,2\nmaps=true')"
    test "$(.lake/build/bin/runtime-quotient 3 1,1,1 2,0,1)" = "$(printf '2\nmaps=true')"
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . lean-no-sorry
    @cd tools/inventory && uv run --locked --quiet pytest -q

# The gate on a clean CI machine, whose `.lake` comes from the CI cache
test-ci:
    {{lake}} exe cache get
    @just test

# Scan staged Lean source; the commit hook runs this
[private]
test-commit:
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . test-commit
    @just test

# Scan Lean source before a push; the push hook runs this
[private]
test-push:
    @just -f {{ai_review_ci}}/justfiles/lean.just -d . test-push
