# Task 14 — Isoefficiency and Gustafson Scaling

## Definition

An isoefficiency function describes how fast total problem size `W` must grow with processor count `P` to maintain a chosen parallel efficiency. In a cost model,

\[
T_P = T_{work}/P + T_{overhead},
\qquad
E=\frac{T_{work}}{P T_P}.
\]

Constant efficiency requires overhead not to grow faster than the useful work in a way that reduces the ratio.

## Gustafson-compliant weak scaling

Under ideal weak scaling, each processor receives a fixed local workload `w`. Thus

\[
W(P)=Pw=\Theta(P).
\]

If per-processor work and overhead per processor remain bounded and communication does not introduce a growing global bottleneck, wall-clock time remains bounded and efficiency can remain constant. Therefore the idealized isoefficiency relation is

\[
\boxed{W(P)=\Theta(P)}.
\]

## Critical qualification

This linear relation is not a universal isoefficiency theorem for every parallel program. For an actual algorithm, the isoefficiency function must be derived from its overhead function (communication, synchronization, and imbalance). If overhead grows as `P log P`, for example, a larger workload may be needed to maintain the same efficiency. Gustafson's linear weak-scaling assumption is the ideal target; algorithm-specific isoefficiency may be superlinear.
