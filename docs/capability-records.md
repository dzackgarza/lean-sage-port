# Capability records

A capability record states one mathematical operation or construction that the target must
compute. The records live in `inventory/capabilities/*.toml`. `sage-inventory schema` prints the
fields. `inventory/capabilities/integers-and-rationals.toml` is the worked example.

`inventory/sage/release.toml` pins the official Sage release and records why the existing index
can serve that release for the files it scans. The index keeps the fork commit it actually read.
This equivalence covers Python/Cython source, reference-manual placement and package metadata;
it does not assert that the broader Sage source tree or a compiled Sage runtime is identical.

## What one record is

A record is an operation at its natural generality, not a Sage method.

| Sage has | The record is |
| --- | --- |
| `Integer.gcd`, `Rational.gcd`, `arith.misc.gcd`, `Polynomial.gcd` over a field | `euclidean.gcd`: one record, for Euclidean domains |
| `Integer.is_prime`, `arith.misc.is_prime` | `integers.primality-proving` |
| `IntegerRing.quotient`, `Ring.quotient` | `rings.quotient-ring` |

- The first segment of the id names the mathematical area where the operation is defined in
  general (`euclidean`, `modular`, `rings`, `lattices`). It does not name the Sage module.
- Search the existing files for the operation before you add a record. When a record exists, add
  your Sage entities to its `sage` selectors.
- A special case gets its own record only when its algorithm or its contract differs. Name it in
  the `generalizes` list of the generic record.
- Sage's class structure is not an ontology. An object (the integers, a polynomial ring) is one
  construction record; its methods belong to the operations they compute.

## Fields

| Field | Content |
| --- | --- |
| `statement` | The operation in mathematical terms: given what, return what. |
| `domain` | The hypotheses and the objects that the operation applies to. |
| `contract` | Input and output as mathematical types, the normalization of the result, and the structure that the result keeps (defining maps, chosen generators). |
| `exactness` | `exact`, `approximate` (the result has an error bound), `heuristic` (the result can be wrong), `conditional` (correct under a named hypothesis such as GRH). Give the bound, failure mode or hypothesis in `exactness_notes`. |
| `algorithms` | Algorithm families. `sources` names the function that Sage calls (`FLINT fmpz_factor`, `PARI qfbclassno`) and the literature. |
| `depends_on` | Capabilities whose result the algorithm consumes. |
| `sage` | Selectors of the Sage entities that this record accounts for. |
| `catalogue` | Ids of the `lean-categories` catalogue objects and operations that the capability computes (`obj.rings.integers`, `mor.sets.gcd`). `[]` states that the catalogue has none. |
| `tests` | Relevant existing Sage doctests or test-suite cases, oracle comparison details, and any supplemental checks with the gap they cover. Source tests are located through `sage` selectors and the index; do not copy the test corpus into records. |
| `reuse` | `status`, component ids from `inventory/reuse/*.toml`, and the evidence. |
| `backends` | The engines that Sage delegates to. The index gives them per module (`modules.jsonl`, field `backends`). |
| `license_notes` | Needed when the only reference implementation has a licence that restricts a translation. `inventory/references/` has the licences. |

## Rules

**Reuse source tests and oracle computations.** Every capability inherits the baseline Sage
doctests of its selected entities. Resolve `sage` selectors through `entities.jsonl.gz` for
the qualified name and source line, and `modules.jsonl` for the source path. Keep their input
conditions, optional-package requirements, expected failures, precision and assumptions.
The indexed revision identifies the source of these tests. Related suite cases can be cited
in `tests` by path and test name.

For additional runtime inputs in the stated domain, compare the native result with the same
operation in Sage or its reference engine. Use exact equality for canonical exact results.
For bases, generators, factorizations and presentations, compare the represented mathematical
object and retained maps rather than incidental ordering or representation. Numerical comparisons
use the operation's precision, error-bound or error-estimate contract. Conditional and heuristic
computations retain their assumptions and certification status.

The `tests` field adds only source pointers and comparison details that the selectors do not
already supply. A new mathematical check must identify a specific gap in the existing tests or
oracle comparison. Reconnaissance records these reusable sources and comparison rules; executable
test translation belongs with the operation's implementation. A source test count is not evidence
that a native operation has passed those tests.

The generated `inventory/capability-evidence.json` report expands every selector into its matched
entities, source path and line, source doctest count, references and module backends. Its
`oracle_inputs` entries are the concrete Sage inputs or independent mathematical comparisons that
the native implementation must reproduce. A record with no source doctests must state those
inputs explicitly from the source or contract; it must not claim that a selector alone supplies
an oracle. The report also lists wildcard selectors and overlapping entity associations explicitly;
these are review data, not hidden coverage.

**Account for every entity of the source.** The denominator is every entity of the index: each
class, module-level function and `def` or `cpdef` method, public or underscore, of every module
under `src/sage`. The reference manual is generated from the source and documents a subset of it;
a module that the manual does not list is in scope like any other, and the ledger names the
manual sections whose modules import it. Module-level aliases such as `ZZ = IntegerRing()` are
instances, not entities: the class that they instantiate carries the functionality.

Each entity has one state, computed by `sage-inventory coverage` and `sage-inventory
reconnaissance`:

| State | Condition |
| --- | --- |
| `unaccounted` | No record selects the entity. |
| `scoped` | A record selects it, but no source-reconciled batch of `inventory/reconnaissance-worklog.toml` names its module, or the only record is `scope-only`. |
| `reconciled` | A source-reconciled capability selects it, and a source-reconciled batch names its module. |
| `excluded` | An `[[exclusion]]` selects it, and a source-reconciled batch names its module. |
| `category-record` | A category or operation record of `inventory/categories/sage-categories.toml` names it. |

A record is a claim about source; the worklog batch is the record that the source was read. A
batch becomes `source-reconciled` only after each module that it names was read in full and every
entity of that module was given to a capability, an exclusion or a category record. A batch names
modules exactly; a package name or a pattern credits nothing. A part of the source is complete when
`sage-inventory remaining <index> <capabilities> <categories> <worklog> <part>` prints nothing.

An entity with no mathematical content goes to an `[[exclusion]]` with its reason:
`infrastructure`, `external-interface`, `presentation`, `data` or `deprecated`. The rationale
states what the module does, from its source. "Outside the manual" is a placement, not a reason.

**A selector names the entities that the record accounts for.** Underscore methods are part of
the operation: `_add_`, `_mul_` and `_richcmp_` implement the arithmetic and comparison that the
public operators reach, and `_element_constructor_` implements conversion. Do not select an
unrelated entity to make a record valid. A source entity may be accounted for by
more than one capability when Sage exposes the same operation family through multiple
mathematical constructions; `inventory/capability-evidence.json` reports those overlaps and they
must be resolved by the implementation's operation contract rather than silently ignored.
When an algorithm depends on an operation of another section, write that record in the file of
its own section, with the selectors of its real Sage entities.

**Separate algorithm alternatives from mandatory prerequisites.** `depends_on` records the
inputs needed by the selected complete computational route. Algorithm families can consume
additional inputs without making them universal prerequisites. For example, factorization
certifies prime factors using primality, while a complete trial-division primality decision
does not require a factorization implementation. Pocklington and ECPP may use factorization
internally; those inputs belong to their algorithm-specific specifications.

**Attach the record to the catalogue.** The catalogue ids are the component ids of
`inventory/reuse/lean-categories.toml` without the prefix `catalogue.`; each component states its
mathematics in the field `capability`. Name every object and operation that the record computes,
at any generality: `mor.sets.gcd` is the gcd on Z and attaches to `euclidean.gcd`. An empty list
is a claim that you searched the map and found none. It is a gap that the owner of the catalogue
receives.

**Cite what you read.** Take citation keys from the Sage docstring (the index field `references`)
or from the source that you opened. Give a section or algorithm number only when you read it;
otherwise name the chapter, or the key alone.

**Reuse status comes from the reuse maps.** `missing` means that a search of every file in
`inventory/reuse/` found no component; the evidence names what the search covered. A Mathlib
definition marked `noncomputable` is `formalized-not-executable`.

| Status | Meaning |
| --- | --- |
| `reusable` | A compiled Lean implementation exists and computes the operation. |
| `adaptable` | A compiled implementation exists for a nearby type or a special case. |
| `formalized-not-executable` | The definition and its theory exist; no compiled code computes it. |
| `specified-unimplemented` | An algorithm is specified or planned in a Lean project, with no code. |
| `missing` | No Lean component was found. |

**Use the existing inventories.** `AGENTS.md` names the tables of the research repository. For
lattices and quadratic forms, take the method groups and conventions from them. For Sage's category
framework, `inventory/categories/sage-categories.toml` gives the catalogue id of each category
method.

## Check

```bash
cd tools/inventory
uv run sage-inventory coverage ../../inventory/sage/index ../../inventory/capabilities ../../inventory/reuse ../../inventory/categories/sage-categories.toml ../../inventory/reconnaissance-worklog.toml ../../inventory/coverage.json
uv run sage-inventory reconnaissance ../../inventory/sage/index ../../inventory/capabilities ../../inventory/categories/sage-categories.toml ../../inventory/reconnaissance-worklog.toml ../../inventory/reconnaissance.json ../../inventory/reconnaissance-entities.jsonl.gz
uv run sage-inventory remaining ../../inventory/sage/index ../../inventory/capabilities ../../inventory/categories/sage-categories.toml ../../inventory/reconnaissance-worklog.toml <section-or-package>
```

`coverage` fails on a duplicate id, an unknown `depends_on` or `generalizes` id, an unknown reuse
component, an unknown catalogue id, a selector that matches no entity, a worklog entry that
matches no module, a source-reconciled batch that names anything but exact modules, and a worklog
for another commit.
