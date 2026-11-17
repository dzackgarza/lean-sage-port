# Requirements checklist: native computation architecture

**Feature**: [master specification](../spec.md)
**Review ownership**: Independent technical reviewer. A checked item means requirements quality,
not successful implementation.

- [ ] CHK001 Are runtime domain parameters and their equality/transport rules explicit? [FR-005]
- [ ] CHK002 Does each representation name its existing mathematical object and interpretation? [FR-004]
- [ ] CHK003 Are defining maps and selected generators retained in construction results? [US2]
- [ ] CHK004 Is generic operation selection tied to actual hypotheses and an existing owner? [FR-012]
- [ ] CHK005 Do the experiments distinguish rings from fields and reject invalid hypotheses? [US2]
- [ ] CHK006 Do source tests and same-input oracles determine expected results? [FR-006, FR-011]
- [ ] CHK007 Are semantic prerequisites separated from executable algorithm inputs? [FR-008]
- [ ] CHK008 Are unsupported domains and unresolved interfaces visible rather than silently narrowed? [SC-007]
