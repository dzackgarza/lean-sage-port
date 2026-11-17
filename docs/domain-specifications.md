# Domain specifications

The pinned Sage manual taxonomy is indexed in [`inventory/domains.toml`](../inventory/domains.toml). Each linked capability file states intrinsic operations, exact domains, reuse evidence, source selectors, and acceptance comparisons. A blank contract cell means that the section has no capability record yet; it remains in scope when its disposition is mathematical. This index is a route to contracts, not a completion claim.

The baseline source is [`inventory/sage/index/`](../inventory/sage/index/) at the revision in its `summary.json`. `entities.jsonl.gz` locates each selected Sage method and its doctests; `modules.jsonl` locates its source file. Run the repository's `sage-inventory unaccounted` command for a section to see the live entity-level gap. [`inventory/coverage.json`](../inventory/coverage.json) owns the measured counts. Reuse evidence lives in [`inventory/reuse/`](../inventory/reuse/) and reference-engine provenance in [`inventory/references/`](../inventory/references/).

## Mathematical domains

| Sage manual section | Capability contracts |
| --- | --- |
| Algebras (`algebras`) | — |
| Anderson Motives (`anderson_motives`) | — |
| Arithmetic Subgroups of {\rm SL}_2(\ZZ) (`arithgroup`) | — |
| Elliptic and Hyperelliptic Curves (`arithmetic_curves`) | [`arithmetic-geometry.toml`](../inventory/capabilities/arithmetic-geometry.toml) |
| Asymptotic Expansions (`asymptotic`) | — |
| Symbolic Calculus (`calculus`) | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Categories (`categories`) | — |
| Coding Theory (`coding`) | — |
| Combinatorics (`combinat`) | — |
| Mathematical Constants (`constants`) | — |
| Cryptography (`cryptography`) | — |
| Plane and Space Curves (`curves`) | — |
| Diophantine Approximation (`diophantine_approximation`) | — |
| Combinatorial and Discrete Geometry (`discrete_geometry`) | — |
| Drinfeld Modular Forms (`drinfeld_modular`) | — |
| Drinfeld Modules (`drinfeld_modules`) | — |
| Discrete Dynamics (`dynamics`) | — |
| Euclidean Spaces and Vector Calculus (`euclidean_spaces`) | — |
| Finite Rings and Fields (`finite_rings`) | [`finite-rings.toml`](../inventory/capabilities/finite-rings.toml) |
| Function Fields (`function_fields`) | — |
| Elementary and Special Functions (`functions`) | — |
| Game Theory (`game_theory`) | — |
| Games (`games`) | — |
| Graph Theory (`graphs`) | [`graphs.toml`](../inventory/capabilities/graphs.toml) |
| Groups (`groups`) | [`groups.toml`](../inventory/capabilities/groups.toml) |
| General Hecke Algebras and Hecke Modules (`hecke`) | — |
| Chain Complexes and their Homology (`homology`) | [`homological-algebra.toml`](../inventory/capabilities/homological-algebra.toml) |
| Hyperbolic Geometry (`hyperbolic_geometry`) | — |
| Knot Theory (`knots`) | — |
| L-Functions (`lfunctions`) | — |
| Symbolic Logic (`logic`) | — |
| Manifolds and Differential Geometry (`manifolds`) | — |
| Matrices and Spaces of Matrices (`matrices`) | [`lattices.toml`](../inventory/capabilities/lattices.toml), [`linear-algebra.toml`](../inventory/capabilities/linear-algebra.toml) |
| Matroid Theory (`matroids`) | — |
| Modular Abelian Varieties (`modabvar`) | — |
| Modular Forms (`modfrm`) | — |
| Modular Symbols (`modsym`) | — |
| Vectors and Modules (`modules`) | — |
| Monoids (`monoids`) | — |
| Noncommutative Polynomials (`noncommutative_polynomial_rings`) | — |
| Number Fields (`number_fields`) | — |
| Numerical Optimization (`numerical`) | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Modules over Ore rings (`oremodules`) | — |
| p-adic Numbers (`padics`) | — |
| Commutative Polynomials (`polynomial_rings`) | [`polynomial-algorithms.toml`](../inventory/capabilities/polynomial-algorithms.toml), [`polynomials.toml`](../inventory/capabilities/polynomials.toml) |
| Power Series and Laurent Series (`power_series`) | — |
| Probability (`probability`) | — |
| Quadratic Forms (`quadratic_forms`) | — |
| Quaternion Algebras (`quat_algebras`) | — |
| Quivers (`quivers`) | — |
| Resolutions (`resolutions`) | — |
| Parametrized Surfaces (`riemannian_geometry`) | — |
| Rings (`rings`) | — |
| Real and Complex Numbers (`rings_numerical`) | [`numerical-analysis.toml`](../inventory/capabilities/numerical-analysis.toml) |
| Integers and Rational Numbers (`rings_standard`) | [`integers-and-rationals.toml`](../inventory/capabilities/integers-and-rationals.toml) |
| SAT solvers (`sat`) | — |
| Schemes (`schemes`) | — |
| Semirings (`semirings`) | — |
| Sets (`sets`) | — |
| Statistics (`stats`) | — |
| Tensors on Free Modules of Finite Rank (`tensor_free_modules`) | — |
| Cell Complexes, Simplicial Complexes, and Simplicial Sets (`topology`) | [`topology.toml`](../inventory/capabilities/topology.toml) |
| Discrete Valuations (`valuations`) | — |

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
