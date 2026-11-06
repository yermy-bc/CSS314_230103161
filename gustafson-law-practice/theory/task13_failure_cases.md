# Task 13 — When Gustafson's Assumption Fails

Gustafson's ideal weak scaling requires the larger workload to add mostly parallel work while keeping elapsed time nearly constant. Two important counterexamples are below.

## Case 1: All-pairs N-body force calculation

The direct method computes interactions for every particle pair, requiring `O(N²)` work. If the particle count grows with processor count, the total arithmetic grows quadratically. Communication and data exchange also grow, and each processor may need increasingly expensive access to particle state. Maintaining constant iteration time requires enough compute and communication capacity to keep pace; a naive linear increase `N∝P` makes total work grow as `P²`, faster than aggregate compute `P`.

A different scaling choice such as `N∝√P` can keep ideal per-processor arithmetic approximately constant, but then the global workload is not growing linearly with P. The exact behavior depends on decomposition and communication.

## Case 2: Parallel BFS on a power-law graph

Breadth-first search on an irregular graph has data-dependent frontiers. High-degree hubs create load imbalance; frontier expansion requires synchronization and potentially many remote memory accesses. Increasing graph size can increase the frontier, edge traffic, contention, and number of synchronization events. A few hot vertices can become bottlenecks even when the total edge count is distributed.

## Why constant runtime breaks

In both cases, the serial/overhead fraction is not invariant. Communication, synchronization, load imbalance, and memory stalls grow with scale. Therefore `α(P)` rises or useful per-processor work is no longer constant. The ideal Gustafson formula remains a useful baseline, but measured performance needs an overhead term such as Task 12's `C(P)`.
