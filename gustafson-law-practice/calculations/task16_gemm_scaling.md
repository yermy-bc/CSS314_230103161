# Task 16 — Dense Matrix Multiplication (GEMM)

For `C=A×B`, three dense `N×N` matrices are involved. Arithmetic work is `Θ(N³)` and matrix storage is `Θ(N²)`. With ideal parallel distribution over `P` processors, compute time is proportional to

\[
T_P\propto\frac{N^3}{P}.
\]

To keep this time constant as `P` grows:

\[
\frac{N(P)^3}{P}=constant
\Rightarrow N(P)^3\propto P
\Rightarrow\boxed{N(P)\propto P^{1/3}}.
\]

| Processor multiplier | Required matrix-dimension multiplier |
|---:|---:|
| 1× | 1× |
| 8× | 2× |
| 64× | 4× |
| 512× | 8× |
| 1,000× | 10× |

This assumes compute dominates and communication is negligible or effectively overlapped. Distributed GEMM must also communicate matrix blocks; network bandwidth and topology can make actual scaling weaker.
