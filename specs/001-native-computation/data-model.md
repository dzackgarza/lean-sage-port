# Specification data and ownership

Use the existing models in `tools/inventory/src/sage_inventory/models.py`.

| Record | Identity | Relationship |
| --- | --- | --- |
| Source revision | commit plus reported Sage version | fixes the indexed source |
| Source entity | module and qualified declaration name | module supplies path and manual placement; the ledger supplies its reconnaissance state |
| Capability | intrinsic dotted operation id | selects source entities and consumes capability outputs |
| Reuse component | upstream component id | names declarations, revisions and computability evidence |
| Catalogue entry | upstream stable id | names mathematical semantics or language operation |
| Domain | reference-manual section | names a domain; routes to capability files and the `remaining` query |
| Reading batch | worklog batch id | names the modules read; a source-reconciled batch lets records close their entities |

The `sage` selectors and indexed paths locate source doctests. The `tests` field supplies only
additional source pointers and comparison details. The `depends_on` field identifies computational
inputs; reuse entries separately identify already supplied mathematics. A capability record and
a successful source validator do not assert that a native implementation exists.

Runtime object and map ownership is specified in `docs/architecture.md`. Concrete Lean types
come from their existing mathematical and computational owners, not from this inventory model.
