# Task 18 — N-Body: Direct Method vs. Barnes–Hut

## Direct all-pairs method

The direct force calculation performs `Θ(N²)` pair interactions. With ideal load balance over `P` processors,

\[
T_P\propto N^2/P.
\]

To keep compute time per iteration constant, `N²/P=constant`, so

\[
\boxed{N=\Theta(P^{1/2})}.
\]

The workload grows more slowly than P. If instead `N∝P` under weak scaling, per-processor pair work grows as `N²/P=Θ(P)` and runtime rises.

## Barnes–Hut tree code

The Barnes–Hut method is approximately `Θ(N log N)` for typical distributions, though pathological distributions and tree construction details can change behavior. Idealized fixed-time scaling requires

\[
N\log N/P=constant
\Rightarrow N\log N=\Theta(P).
\]

Asymptotically, `N=Θ(P/log P)` up to lower-order logarithmic corrections.

## Serial/parallel ratio

Tree construction, root traversal, global reductions, and distribution of particles may form serial or coordination costs. For the direct method, pair interactions dominate at large N and can be partitioned relatively regularly. Barnes–Hut reduces arithmetic but introduces irregular tree traversal and communication. Thus the ratio of overhead to useful computation may rise in the tree method even while its asymptotic arithmetic complexity is better.

These are ideal compute-only scaling relations, not guaranteed wall-clock predictions. Spatial distribution, tree balance, communication, and memory locality must be measured.
