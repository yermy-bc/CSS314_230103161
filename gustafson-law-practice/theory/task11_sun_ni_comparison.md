# Task 11 — Gustafson vs. Sun–Ni Memory-Bounded Speedup

## The three scaling models

- **Amdahl:** fixed total problem size.
- **Gustafson:** fixed parallel elapsed time; the workload grows with processor count.
- **Sun–Ni:** memory capacity limits the scaled workload. The available memory, rather than elapsed time alone, determines how much larger a problem can be run.

Gustafson's simplified scaled speedup is

\[
S_G(P)=a+(1-a)P,
\]

where `a` is the serial fraction measured on the parallel system.

## Sun–Ni memory-bounded formulation

Let `a` denote the serial fraction, `W` the baseline workload, `M` the memory capacity of one processor, and `g(M)` the application-specific relationship between memory and the workload that fits in it. With P processors and proportionally increased memory, the scaled workload is

\[
W^*=g(PM).
\]

The memory-bounded speedup can be expressed as

\[
S_{MB}(P)=
\frac{aW+(1-a)g(PM)}
{aW+(1-a)g(PM)/P}.
\]

Define the workload growth factor

\[
G(P)=\frac{g(PM)}{g(M)}.
\]

After normalizing the baseline workload, the simplified form is

\[
\boxed{S_{MB}(P)=
\frac{a+(1-a)G(P)}
{a+(1-a)G(P)/P}}.
\]

This shows how memory scaling controls the amount of work available to the parallel system.

## Special cases and comparison

- If `G(P)=1`, the workload does not grow. The expression reduces to Amdahl's fixed-size speedup.
- If `G(P)=P`, workload grows linearly with processor count. The expression reduces to Gustafson's scaled speedup.
- If `G(P)` grows more slowly than P, the memory-bounded model generally predicts less scalable workload capacity than the ideal Gustafson assumption.
- If application workload grows faster than P with available memory, Gustafson's linear workload-growth assumption can underestimate the amount of work that fits, although compute time and memory bandwidth still determine throughput.

For a power-law memory/workload relationship `g(M)=cM^b`, the growth factor is `G(P)=P^b`. The exponent `b` is application-dependent; it cannot be selected without knowing how the application's memory requirement relates to its problem dimension.

## Critical evaluation

Gustafson's Law can overestimate achievable throughput when the workload cannot grow linearly with memory, or when memory bandwidth, latency, communication, and synchronization become bottlenecks. It can underestimate workload capacity when memory growth permits a superlinear increase in supported work and the application can exploit it. Capacity is not the same as speed: a larger in-memory problem is useful only if the processor and memory systems can process it efficiently.

## References

- Sun, X.-H., & Ni, L. M. (1993). *Scalable Problems and Memory-Bounded Speedup*. Journal of Parallel and Distributed Computing, 19(1), 27–37. https://doi.org/10.1006/jpdc.1993.1087
- Sun, X.-H., & Lu, X. (2023). *The Memory-Bounded Speedup Model and Its Impacts in Computing*. Journal of Computer Science and Technology, 38(1).
