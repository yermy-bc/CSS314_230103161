# Task 20 — Parallel Graph Traversal and Irregular Workloads

## BFS

BFS proceeds in levels. Each level expands a frontier and discovers neighboring vertices. The frontier size varies with graph structure, so processors may receive very different amounts of work. High-degree vertices can create hotspots, while sparse frontiers can leave processors idle.

## PageRank

PageRank repeatedly updates vertex scores using incoming edges. Power-law degree distributions create uneven work: a small number of high-degree vertices have many edges. Implementations need synchronization or carefully designed pull/push strategies, reductions, and repeated memory access over irregular adjacency structures.

## Why weak scaling is difficult

- **Load imbalance:** equal vertex counts do not imply equal edge counts.
- **Irregular memory access:** cache misses and remote NUMA/remote-node accesses rise.
- **Synchronization:** frontier queues, visited flags, and convergence checks contend.
- **Communication:** edges crossing partitions require remote data exchange.
- **Data dependence:** the next work set depends on current values/frontier.

Dense linear algebra has regular blocks, predictable arithmetic, and well-understood communication patterns. Graph workloads have irregular access and data-dependent work. Increasing graph size and P together therefore does not guarantee constant per-node work or constant elapsed time. Partition quality, graph structure, and algorithm choice strongly affect observed `α(P)`.
