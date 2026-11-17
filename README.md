# lean-sage-port

Native Lean computation for the mathematical functionality documented by SageMath.

Start with the [project constitution](.specify/memory/constitution.md) and the
[master product specification](specs/001-native-computation/spec.md).
The [Spec Kit plan](specs/001-native-computation/plan.md) and
[requirements checklist](specs/001-native-computation/checklists/requirements.md)
define the specification work and its unresolved requirements.

The [domain guide](docs/domain-specifications.md) routes the complete Sage manual taxonomy
to capability records, source tests and reuse evidence. [Capability record rules](docs/capability-records.md)
define source accounting and oracle comparisons. The [architecture contract](docs/architecture.md)
identifies the runtime experiments needed before accepting the design.

Run `just test` for the local inventory gate. Lean compilation runs in CI through `just test-ci`.
Current work is owned by [the reconnaissance issue](https://github.com/dzackgarza/lean-sage-port/issues/1).
