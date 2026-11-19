# lean-sage-port

Native Lean computation for the mathematical functionality of the SageMath source.

Start with the [project constitution](.specify/memory/constitution.md) and the
[master product specification](specs/005-master-product-spec/product-spec.md).
The [reconnaissance specification](specs/001-native-computation/spec.md) and its
[plan](specs/001-native-computation/plan.md) define how the Sage source is indexed and read.
Reconnaissance covers every class, function and method of every module under `src/sage`; the
reference manual names the domains and documents a subset of that source.

The [domain guide](docs/domain-specifications.md) routes the Sage manual sections to capability
records, source tests and reuse evidence. [Capability record rules](docs/capability-records.md)
define source accounting, the reconnaissance states and oracle comparisons. The [architecture contract](docs/architecture.md)
identifies the runtime experiments needed before accepting the design.

Run `just test` for the local inventory gate. Lean compilation runs in CI through `just test-ci`.
Current work is owned by [the reconnaissance issue](https://github.com/dzackgarza/lean-sage-port/issues/1).
