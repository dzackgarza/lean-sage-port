# Domain specifications

The pinned Sage manual taxonomy is indexed in [`inventory/domains.toml`](../inventory/domains.toml). Each linked capability file states intrinsic operations, exact domains, reuse evidence, source selectors, and acceptance comparisons. A blank contract cell means that the section has no capability record yet; it remains in scope when its disposition is mathematical. This index is a route to contracts, not a completion claim.

The dependency-ordered milestone that owns each section is recorded in [`specs/004-milestones/plan.md`](../specs/004-milestones/plan.md). The milestone assignment determines which section's capabilities are prerequisites for which others. It does not determine completion order within a section.

The baseline source is [`inventory/sage/index/`](../inventory/sage/index/) at the revision in its `summary.json`. `entities.jsonl.gz` locates each selected Sage method and its doctests; `modules.jsonl` locates its source file. Run the repository's `sage-inventory unaccounted` command for a section to see the live entity-level gap. [`inventory/coverage.json`](../inventory/coverage.json) owns the measured counts. Reuse evidence lives in [`inventory/reuse/`](../inventory/reuse/) and reference-engine provenance in [`inventory/references/`](../inventory/references/).

## Mathematical domains

| Sage manual section | Milestone | Capability contracts |
| --- | --- | --- |
| Algebras (`algebras`) | M3 | — |
| Anderson Motives (`anderson_motives`) | M11 | — |
| Arithmetic Subgroups of {\rm SL}_2(\ZZ) (`arithgroup`) | M11 | — |
| Elliptic and Hyperelliptic Curves (`arithmetic_curves`) | M10 | [`arithmetic-geometry.toml`](../inventory/capabilities/arithmetic-geometry.toml) |
| Asymptotic Expansions (`asymptotic`) | M12 | — |
| Symbolic Calculus (`calculus`) | M12 | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Categories (`categories`) | M14 | — |
| Coding Theory (`coding`) | M13 | — |
| Combinatorics (`combinat`) | M8 | — |
| Mathematical Constants (`constants`) | M12 | — |
| Cryptography (`cryptography`) | M13 | — |
| Plane and Space Curves (`curves`) | M10 | — |
| Diophantine Approximation (`diophantine_approximation`) | M7 | — |
| Combinatorial and Discrete Geometry (`discrete_geometry`) | M9 | — |
| Drinfeld Modular Forms (`drinfeld_modular`) | M11 | — |
| Drinfeld Modules (`drinfeld_modules`) | M11 | — |
| Discrete Dynamics (`dynamics`) | M8 | — |
| Euclidean Spaces and Vector Calculus (`euclidean_spaces`) | M12 | — |
| Finite Rings and Fields (`finite_rings`) | M1 | [`finite-rings.toml`](../inventory/capabilities/finite-rings.toml) |
| Function Fields (`function_fields`) | M7 | — |
| Elementary and Special Functions (`functions`) | M12 | — |
| Game Theory (`game_theory`) | M13 | — |
| Games (`games`) | M13 | — |
| Graph Theory (`graphs`) | M8 | [`graphs.toml`](../inventory/capabilities/graphs.toml) |
| Groups (`groups`) | M6 | [`groups.toml`](../inventory/capabilities/groups.toml) |
| General Hecke Algebras and Hecke Modules (`hecke`) | M11 | — |
| Chain Complexes and their Homology (`homology`) | M5 | [`homological-algebra.toml`](../inventory/capabilities/homological-algebra.toml) |
| Hyperbolic Geometry (`hyperbolic_geometry`) | M9 | — |
| Knot Theory (`knots`) | M9 | — |
| L-Functions (`lfunctions`) | M11 | — |
| Symbolic Logic (`logic`) | M13 | — |
| Manifolds and Differential Geometry (`manifolds`) | M9 | — |
| Matrices and Spaces of Matrices (`matrices`) | M4 | [`lattices.toml`](../inventory/capabilities/lattices.toml), [`linear-algebra.toml`](../inventory/capabilities/linear-algebra.toml) |
| Matroid Theory (`matroids`) | M8 | — |
| Modular Abelian Varieties (`modabvar`) | M11 | — |
| Modular Forms (`modfrm`) | M11 | — |
| Modular Symbols (`modsym`) | M11 | — |
| Vectors and Modules (`modules`) | M4 | — |
| Monoids (`monoids`) | M14 | — |
| Noncommutative Polynomials (`noncommutative_polynomial_rings`) | M13 | — |
| Number Fields (`number_fields`) | M7 | — |
| Numerical Optimization (`numerical`) | M12 | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Modules over Ore rings (`oremodules`) | M13 | — |
| p-adic Numbers (`padics`) | M7 | — |
| Commutative Polynomials (`polynomial_rings`) | M2–M3 | [`polynomial-algorithms.toml`](../inventory/capabilities/polynomial-algorithms.toml), [`polynomials.toml`](../inventory/capabilities/polynomials.toml) |
| Power Series and Laurent Series (`power_series`) | M2 | — |
| Probability (`probability`) | M12 | — |
| Quadratic Forms (`quadratic_forms`) | M4 | — |
| Quaternion Algebras (`quat_algebras`) | M3 | [`quaternions.toml`](../inventory/capabilities/quaternions.toml) |
| Quivers (`quivers`) | M8 | — |
| Resolutions (`resolutions`) | M5 | — |
| Parametrized Surfaces (`riemannian_geometry`) | M9 | — |
| Rings (`rings`) | M3 | — |
| Real and Complex Numbers (`rings_numerical`) | M12 | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Integers and Rational Numbers (`rings_standard`) | M1 | [`integers-and-rationals.toml`](../inventory/capabilities/integers-and-rationals.toml) |
| SAT solvers (`sat`) | M13 | — |
| Schemes (`schemes`) | M10 | — |
| Semirings (`semirings`) | M2 | [`semirings.toml`](../inventory/capabilities/semirings.toml) |
| Sets (`sets`) | M14 | — |
| Statistics (`stats`) | M12 | — |
| Tensors on Free Modules of Finite Rank (`tensor_free_modules`) | M4 | — |
| Cell Complexes, Simplicial Complexes, and Simplicial Sets (`topology`) | M9 | [`topology.toml`](../inventory/capabilities/topology.toml) |
| Discrete Valuations (`valuations`) | M7 | — |

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
