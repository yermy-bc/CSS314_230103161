# Task 10 — Memory Growth and 3D Grid Capacity

## Given

Under weak scaling, total memory grows with node count:

\[
M(P)=cP.
\]

Each node is capped at 32 GB. Therefore:
- 64 nodes: `64×32 = 2,048 GB` (2.048 TB in decimal units).
- 512 nodes: `512×32 = 16,384 GB` (16.384 TB in decimal units).

For a cubic grid with `N³` cells and `b` bytes stored per cell:

\[
bN^3\le M_{total},\qquad
\boxed{N_{max}=\left\lfloor(M_{total}/b)^{1/3}\right\rfloor}.
\]

## Illustrative 8-byte-per-cell capacity

If one scalar double-precision value (8 bytes) is stored per grid cell, using decimal GB (`1 GB = 10^9 bytes`):

| Nodes | Total memory (GiB) | Maximum ideal cubic N |
|---:|---:|---:|
| 64 | 2,048 | 6,349 |
| 512 | 16,384 | 12,699 |

If the instructor intends GiB rather than decimal GB, the corresponding dimensions are approximately 6,502 and 13,004. These are ideal upper bounds before operating-system use, halos/ghost cells, temporary arrays, multiple physical variables, metadata, and safety headroom. If a solver stores `q` double arrays per cell, use `b=8q` bytes per cell. For example, 10 arrays reduce the dimension by a factor of approximately `10^(1/3)`.

## Important limitation in the question

The prompt does not specify bytes per grid cell or number of fields. Thus there is no unique numeric `N` without an assumption. The table explicitly assumes one 8-byte value per cell and uses binary GiB. In a weak-scaled domain decomposition, each node's local memory remains approximately constant; increasing node count increases total grid capacity.
