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

**Account for every entity.** A section is complete when
`sage-inventory unaccounted <index> <capabilities> <section> <categories>` prints nothing. A public
entity with no mathematical content goes to an `[[exclusion]]` with its reason: `infrastructure`,
`external-interface`, `presentation`, `data` or `deprecated`. The entities of the `categories`
section are accounted for by the category and operation records of
`inventory/categories/sage-categories.toml`, which name each indexed entity against the
`lean-categories` catalogue; pass that file so the measure counts them as `by_category_record`
rather than as a remainder.

**A selector names an entity that the record owns.** Do not select an unrelated entity to make a
record valid. When an algorithm depends on an operation of another section, write that record in
the file of its own section, with the selectors of its real Sage entities.

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
uv run sage-inventory coverage ../../inventory/sage/index ../../inventory/capabilities ../../inventory/reuse ../../inventory/coverage.json ../../inventory/categories/sage-categories.toml
uv run sage-inventory unaccounted ../../inventory/sage/index ../../inventory/capabilities <section> ../../inventory/categories/sage-categories.toml
```

`coverage` fails on a duplicate id, an unknown `depends_on` or `generalizes` id, an unknown reuse
component, an unknown catalogue id, and a selector that matches no entity.
