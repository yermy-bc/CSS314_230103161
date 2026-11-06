# Task 19 — Monte Carlo Weak Scaling

Monte Carlo paths are close to embarrassingly parallel: each path can be simulated independently. If each processor generates a fixed number of paths, local work is constant and the total number of paths grows with P.

## Sources of non-zero serial fraction

1. PRNG initialization and stream/seed assignment.
2. Combining partial sums or histograms.
3. Output formatting, serialization, and file I/O.
4. Final result validation and metadata handling.

## Reduction-tree impact

A binary tree reduction over P participants has `ceil(log₂P)` communication stages. If each stage costs latency `L` and the reduction communicates a fixed-size value, an approximate exposed reduction time is

\[
T_{red}(P)\approx L\lceil\log_2P\rceil + T_{bytes}.
\]

If local simulation time is `T_local`, the effective serial/overhead fraction can be approximated by

\[
\alpha(P)=\frac{T_{setup}+T_{red}(P)+T_{output}}
{T_{local}+T_{setup}+T_{red}(P)+T_{output}}.
\]

Then

\[
S(P)=P-\alpha(P)(P-1).
\]

The tree depth grows logarithmically, but this does not mean the reduction is literally serial on one processor; it is a communication critical path. The expression is a simple effective-overhead approximation. For large path counts, local computation can dominate and the reduction fraction can become small.
