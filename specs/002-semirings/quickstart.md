# Acceptance path for Semirings

1. Read `inventory/sage/baseline.yaml` and `inventory/capabilities/semirings.toml`. Resolve each `sage` selector through `inventory/sage/index/entities.jsonl.gz` and its module path through `modules.jsonl`. The source revision fixes the doctest corpus.
2. Build the public native library and its acceptance executable with `just test` (`AGENTS.md`).
3. Run selected Sage doctests in the reference environment described by `docs/oracles.md`. For further runtime inputs, compare native and Sage results with the same base, min/max orientation and matrix data.
4. Check exact values, semiring identities, morphism source/target and composition, retained matrix indices, and documented failures. For cycle means on small rational matrices, independently enumerate directed cycles and compare exact means.
5. Record revision, environment, inputs, setup and nested computation times in acceptance logs, as required by the constitution. A passing source-index or schema check alone does not establish a native computation.

Expected outcome: all six contracts in `contracts/semiring-computations.md` execute through the public Lean operations and satisfy the source-selected cases within their exact domains.
