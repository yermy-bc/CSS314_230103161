# Task 09 — Multi-Component Workload

The parallel execution-time fractions are:
- Initial disk I/O and parameter broadcast: 2%
- Boundary synchronization/message passing: 6%
- Core domain computation: 92%

The task asks to aggregate the first two non-compute phases as the serial/non-parallel fraction:

\[
\alpha=0.02+0.06=0.08.
\]

Use `S(P)=P−0.08(P−1)`.

| P | Calculation | Scaled speedup |
|---:|---|---:|
| 512 | `512 − 0.08×511` | 471.12 |
| 2,048 | `2048 − 0.08×2047` | 1,884.24 |

The model's aggregate `α=8%` treats both I/O/broadcast and synchronization as non-scaled overhead. In a real application, communication can partly overlap computation or scale with processor count; therefore this aggregation is a simplifying assumption specified by the exercise.
