# Domain specifications

The pinned Sage manual taxonomy is indexed in [`inventory/domains.toml`](../inventory/domains.toml). Each linked capability file states intrinsic operations, exact domains, reuse evidence, source selectors, and acceptance comparisons. A blank contract cell means that the section has no capability record yet; it remains in scope when its disposition is mathematical. This index is a route to contracts, not a completion claim.

The dependency-ordered milestone that owns each section is recorded in [`specs/004-milestones/plan.md`](../specs/004-milestones/plan.md). The milestone assignment determines which section's capabilities are prerequisites for which others. It does not determine completion order within a section.

The baseline source is [`inventory/sage/index/`](../inventory/sage/index/) at the revision in its `summary.json`. `entities.jsonl.gz` locates each selected Sage method and its doctests; `modules.jsonl` locates its source file. Run the repository's `sage-inventory unaccounted` command for a section to see the live entity-level gap. [`inventory/coverage.json`](../inventory/coverage.json) owns the mathematical capability counts; given the category inventory as its last argument, the `coverage` command also counts the `categories` section's entities as `by_category_record`, so its `unaccounted` total is the whole-manual remainder. Category framework accounting is measured in detail by [`inventory/categories/coverage.json`](../inventory/categories/coverage.json) and the `sage-inventory category-coverage` command, because category classes and framework operations are audited against the `lean-categories` catalogue before they are assigned to domain capability records. Reuse evidence lives in [`inventory/reuse/`](../inventory/reuse/) and reference-engine provenance in [`inventory/references/`](../inventory/references/).
The exhaustive entity-level reconnaissance view is [`inventory/reconnaissance.json`](../inventory/reconnaissance.json); it is an accounting ledger, not an implementation-coverage claim.
For the category-first work, [`inventory/categories/coverage.json`](../inventory/categories/coverage.json) separates source-reconciled entities, catalogue mappings, explicit ownership gaps, provisional entries, and unaccounted entities. The detailed ledger is [`inventory/categories/reconciliation.json`](../inventory/categories/reconciliation.json); a zero `unaccounted` count does not mean Sage category semantics are implemented: `ownership_gaps` are explicit absent catalogue relationships that still require their mathematical owner.

## Mathematical domains

| Sage manual section | Milestone | Capability contracts |
| --- | --- | --- |
| Algebras (`algebras`) | M3 | [`algebras.toml`](../inventory/capabilities/algebras.toml), [`combinatorics.toml`](../inventory/capabilities/combinatorics.toml) |
| Anderson Motives (`anderson_motives`) | M11 | [`recon-anderson_motives.toml`](../inventory/capabilities/recon-anderson_motives.toml) |
| Arithmetic Subgroups of {\rm SL}_2(\ZZ) (`arithgroup`) | M11 | [`recon-arithgroup.toml`](../inventory/capabilities/recon-arithgroup.toml) |
| Elliptic and Hyperelliptic Curves (`arithmetic_curves`) | M10 | [`arithmetic-geometry.toml`](../inventory/capabilities/arithmetic-geometry.toml), [`arithmetic_curves.toml`](../inventory/capabilities/arithmetic_curves.toml) |
| Asymptotic Expansions (`asymptotic`) | M12 | [`asymptotic.toml`](../inventory/capabilities/asymptotic.toml) |
| Symbolic Calculus (`calculus`) | M12 | [`calculus.toml`](../inventory/capabilities/calculus.toml), [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Categories (`categories`) | M0 | [`sage-categories.toml`](../inventory/categories/sage-categories.toml) |
| Coding Theory (`coding`) | M13 | [`recon-coding.toml`](../inventory/capabilities/recon-coding.toml) |
| Combinatorics (`combinat`) | M8 | [`combinatorics.toml`](../inventory/capabilities/combinatorics.toml) |
| Mathematical Constants (`constants`) | M12 | [`calculus.toml`](../inventory/capabilities/calculus.toml) |
| Cryptography (`cryptography`) | M13 | [`cryptography.toml`](../inventory/capabilities/cryptography.toml) |
| Plane and Space Curves (`curves`) | M10 | [`curves.toml`](../inventory/capabilities/curves.toml) |
| Diophantine Approximation (`diophantine_approximation`) | M7 | [`diophantine.toml`](../inventory/capabilities/diophantine.toml) |
| Combinatorial and Discrete Geometry (`discrete_geometry`) | M9 | [`discrete_geometry.toml`](../inventory/capabilities/discrete_geometry.toml), [`polynomial-rings.toml`](../inventory/capabilities/polynomial-rings.toml) |
| Drinfeld Modular Forms (`drinfeld_modular`) | M11 | [`drinfeld_modular.toml`](../inventory/capabilities/drinfeld_modular.toml) |
| Drinfeld Modules (`drinfeld_modules`) | M11 | [`recon-drinfeld_modules.toml`](../inventory/capabilities/recon-drinfeld_modules.toml) |
| Discrete Dynamics (`dynamics`) | M8 | [`dynamics.toml`](../inventory/capabilities/dynamics.toml) |
| Euclidean Spaces and Vector Calculus (`euclidean_spaces`) | M12 | [`euclidean-spaces.toml`](../inventory/capabilities/euclidean-spaces.toml) |
| Finite Rings and Fields (`finite_rings`) | M1 | [`finite-rings.toml`](../inventory/capabilities/finite-rings.toml) |
| Function Fields (`function_fields`) | M7 | [`function_fields.toml`](../inventory/capabilities/function_fields.toml) |
| Elementary and Special Functions (`functions`) | M12 | [`functions.toml`](../inventory/capabilities/functions.toml) |
| Game Theory (`game_theory`) | M13 | [`recon-game_theory.toml`](../inventory/capabilities/recon-game_theory.toml) |
| Games (`games`) | M13 | [`recon-games.toml`](../inventory/capabilities/recon-games.toml) |
| Graph Theory (`graphs`) | M8 | [`graphs.toml`](../inventory/capabilities/graphs.toml) |
| Groups (`groups`) | M6 | [`groups.toml`](../inventory/capabilities/groups.toml) |
| General Hecke Algebras and Hecke Modules (`hecke`) | M11 | [`hecke.toml`](../inventory/capabilities/hecke.toml) |
| Chain Complexes and their Homology (`homology`) | M5 | [`homological-algebra.toml`](../inventory/capabilities/homological-algebra.toml), [`homology.toml`](../inventory/capabilities/homology.toml) |
| Hyperbolic Geometry (`hyperbolic_geometry`) | M9 | [`hyperbolic_geometry.toml`](../inventory/capabilities/hyperbolic_geometry.toml) |
| Knot Theory (`knots`) | M9 | [`knots.toml`](../inventory/capabilities/knots.toml) |
| L-Functions (`lfunctions`) | M11 | [`recon-lfunctions.toml`](../inventory/capabilities/recon-lfunctions.toml) |
| Symbolic Logic (`logic`) | M13 | [`recon-logic.toml`](../inventory/capabilities/recon-logic.toml) |
| Manifolds and Differential Geometry (`manifolds`) | M9 | [`manifolds.toml`](../inventory/capabilities/manifolds.toml) |
| Matrices and Spaces of Matrices (`matrices`) | M4 | [`lattices.toml`](../inventory/capabilities/lattices.toml), [`linear-algebra.toml`](../inventory/capabilities/linear-algebra.toml), [`matrices.toml`](../inventory/capabilities/matrices.toml) |
| Matroid Theory (`matroids`) | M8 | [`matroids.toml`](../inventory/capabilities/matroids.toml) |
| Modular Abelian Varieties (`modabvar`) | M11 | [`modabvar.toml`](../inventory/capabilities/modabvar.toml) |
| Modular Forms (`modfrm`) | M11 | [`modfrm.toml`](../inventory/capabilities/modfrm.toml) |
| Modular Symbols (`modsym`) | M11 | [`modsym.toml`](../inventory/capabilities/modsym.toml) |
| Vectors and Modules (`modules`) | M4 | [`modules.toml`](../inventory/capabilities/modules.toml) |
| Monoids (`monoids`) | M14 | [`monoids.toml`](../inventory/capabilities/monoids.toml) |
| Noncommutative Polynomials (`noncommutative_polynomial_rings`) | M13 | [`noncommutative-polynomials.toml`](../inventory/capabilities/noncommutative-polynomials.toml), [`polynomial-rings.toml`](../inventory/capabilities/polynomial-rings.toml) |
| Number Fields (`number_fields`) | M7 | [`number-fields.toml`](../inventory/capabilities/number-fields.toml) |
| Numerical Optimization (`numerical`) | M12 | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml), [`numerical.toml`](../inventory/capabilities/numerical.toml) |
| Modules over Ore rings (`oremodules`) | M13 | [`oremodules.toml`](../inventory/capabilities/oremodules.toml), [`recon-oremodules.toml`](../inventory/capabilities/recon-oremodules.toml) |
| p-adic Numbers (`padics`) | M7 | [`padics.toml`](../inventory/capabilities/padics.toml) |
| Commutative Polynomials (`polynomial_rings`) | M2–M3 | [`polynomial-algorithms.toml`](../inventory/capabilities/polynomial-algorithms.toml), [`polynomials.toml`](../inventory/capabilities/polynomials.toml) |
| Power Series and Laurent Series (`power_series`) | M2 | [`power-series.toml`](../inventory/capabilities/power-series.toml) |
| Probability (`probability`) | M12 | [`probability.toml`](../inventory/capabilities/probability.toml) |
| Quadratic Forms (`quadratic_forms`) | M4 | [`quadratic-forms.toml`](../inventory/capabilities/quadratic-forms.toml) |
| Quaternion Algebras (`quat_algebras`) | M3 | [`quaternions.toml`](../inventory/capabilities/quaternions.toml) |
| Quivers (`quivers`) | M8 | [`quivers.toml`](../inventory/capabilities/quivers.toml) |
| Resolutions (`resolutions`) | M5 | [`resolutions.toml`](../inventory/capabilities/resolutions.toml) |
| Parametrized Surfaces (`riemannian_geometry`) | M9 | [`riemannian_geometry.toml`](../inventory/capabilities/riemannian_geometry.toml) |
| Rings (`rings`) | M3 | [`rings.toml`](../inventory/capabilities/rings.toml) |
| Real and Complex Numbers (`rings_numerical`) | M12 | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml), [`rings_numerical.toml`](../inventory/capabilities/rings_numerical.toml) |
| Integers and Rational Numbers (`rings_standard`) | M1 | [`integers-and-rationals.toml`](../inventory/capabilities/integers-and-rationals.toml) |
| SAT solvers (`sat`) | M13 | [`recon-sat.toml`](../inventory/capabilities/recon-sat.toml) |
| Schemes (`schemes`) | M10 | [`schemes.toml`](../inventory/capabilities/schemes.toml) |
| Semirings (`semirings`) | M2 | [`linear-algebra.toml`](../inventory/capabilities/linear-algebra.toml), [`semirings.toml`](../inventory/capabilities/semirings.toml) |
| Sets (`sets`) | M14 | [`sets.toml`](../inventory/capabilities/sets.toml) |
| Statistics (`stats`) | M12 | [`stats.toml`](../inventory/capabilities/stats.toml) |
| Tensors on Free Modules of Finite Rank (`tensor_free_modules`) | M4 | [`tensor-free-modules.toml`](../inventory/capabilities/tensor-free-modules.toml) |
| Cell Complexes, Simplicial Complexes, and Simplicial Sets (`topology`) | M9 | [`topology.toml`](../inventory/capabilities/topology.toml) |
| Discrete Valuations (`valuations`) | M7 | [`padics.toml`](../inventory/capabilities/padics.toml), [`valuations-and-padics.toml`](../inventory/capabilities/valuations-and-padics.toml) |

## Other reference sections

These sections remain indexed to preserve the full manual denominator. Their entity-level exclusions or mathematical content must be judged in capability records; section routing alone does not exclude every entity.

| Sage manual section | Routing |
| --- | --- |
| Coercion (`coercion`) | implementation-support |
| Python Technicalities (`cpython`) | implementation-support |
| Data Structures (`data_structures`) | implementation-support |
| Databases (`databases`) | reference-data |
| Test Framework (`doctest`) | implementation-support |
| Documentation System (`documentation`) | implementation-support |
| History and License (`history_and_license`) | implementation-support |
| Interpreter Interfaces (`interfaces`) | implementation-support |
| C/C++ Library Interfaces (`libs`) | implementation-support |
| Utilities (`misc`) | implementation-support |
| Parallel Computing (`parallel`) | implementation-support |
| 3D Graphics (`plot3d`) | presentation |
| 2D Graphics (`plotting`) | presentation |
| Bibliographic References (`references`) | implementation-support |
| Command Line Interface (`repl`) | implementation-support |
| External Packages (`spkg`) | implementation-support |
| Parents and Elements (`structure`) | implementation-support |

For a domain feature, the implementation specification must name the owning catalogue object or operation, source declarations and algorithms, required computations, true mathematical comparisons, and dependencies. The capability file is the contract for each current operation; this index does not add a parallel task ledger.
