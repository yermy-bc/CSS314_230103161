# Task 03 — The Serial-Fraction Invariance Paradox

## The apparent contradiction

Amdahl's model uses a serial fraction measured for a fixed workload on a uniprocessor baseline. Gustafson's model uses the fraction of elapsed time that is serial on the parallel machine while it processes a scaled workload. These fractions have different reference frames and need not be numerically equal.

## Algebraic comparison

For a fixed workload, let the single-processor time be

\[
T_1=s_1+(1-s_1).
\]

On `P` processors, idealized time is `T_P=s_1+(1-s_1)/P`, giving Amdahl speedup `1/[s_1+(1-s_1)/P]`.

For a scaled workload, normalize observed parallel time to one and measure `α=T_{serial,P}/T_P`. The serial-equivalent workload is `α+P(1-α)`, hence

\[
S_G(P)=P-\alpha(P-1).
\]

The serial section may grow in absolute work as the overall problem grows, while its *fraction of parallel elapsed time* remains small. There is no mathematical requirement that `α=s_1`.

## Why the frame of reference matters

A fixed serial setup cost can be a large fraction of a small problem and a tiny fraction of a much larger problem. If the larger problem adds mostly parallel work, the measured serial fraction on the parallel run can remain small. This explains why a small `α` can coexist with very large scaled speedup.

This does **not** mean serial overhead disappears. It means the workload has changed. If setup, reductions, communication, or coordination grows quickly with `P`, then `α` will rise and the predicted speedup will fall.

## Critical conclusion

The paradox is resolved by distinguishing:
1. serial fraction relative to a fixed one-processor workload; and
2. serial fraction observed during a scaled parallel workload.

Comparing the two as if they were the same quantity produces a misleading contradiction.
