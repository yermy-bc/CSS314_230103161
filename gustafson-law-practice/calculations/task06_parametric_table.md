# Task 06 — Parametric Speedup (α = 0.04)

Use `S(P)=P−α(P−1)` and `E(P)=S(P)/P`, with `α=0.04`.

| P | S(P) | E(P) | Efficiency |
|---:|---:|---:|---:|
| 16 | 15.40 | 0.962500 | 96.2500% |
| 64 | 61.48 | 0.960625 | 96.0625% |
| 256 | 245.80 | 0.960156 | 96.0156% |
| 1,024 | 983.08 | 0.960039 | 96.0039% |
| 4,096 | 3,932.20 | 0.960010 | 96.0010% |
| 16,384 | 15,728.32 | 0.960002 | 96.0002% |

Example for `P=16`:

\[
S=16-0.04(15)=15.4,\qquad E=15.4/16=0.9625.
\]

Efficiency decreases slightly toward `1−α=0.96`, not toward zero. The absolute speedup continues to grow almost linearly. This is the ideal weak-scaling prediction; real systems may incur additional communication and memory overhead.
