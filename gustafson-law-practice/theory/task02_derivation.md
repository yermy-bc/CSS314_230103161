# Task 02 — Derivation of Gustafson's Scaled Speedup

## Definitions

On a parallel machine with `P` processors, normalize the observed parallel runtime to one:

\[
T_P=s+p=1,\quad s=\alpha,\quad p=1-\alpha.
\]

Here `s` is the serial time fraction and `p` is the parallel time fraction *as observed on the P-processor machine*. During the same parallel elapsed time, the parallel part represents `P` processor-time units of work, while the serial part represents one unit.

## Serial-equivalent workload

If the same scaled workload ran sequentially, the serial section would take `s` time units and the parallelizable work would take `Pp` time units. Therefore,

\[
T_1^{scaled}=s+Pp.
\]

The parallel runtime is one, so scaled speedup is

\[
S(P)=\frac{T_1^{scaled}}{T_P}
=\frac{s+Pp}{1}=s+Pp.
\]

Since `s+p=1`, substitute `p=1-s`:

\[
S(P)=s+P(1-s)=s+P-Ps.
\]

Rearrange:

\[
S(P)=P-s(P-1)=P-\alpha(P-1).
\]

This proves both common forms:

\[
\boxed{S(P)=s+pP=P-\alpha(P-1)}.
\]

## Interpretation

At `P=1`, `S(1)=1`. For `α=0`, ideal speedup is `P`. For `α=1`, speedup is one. The model assumes that the measured serial fraction remains representative as the problem and processor count scale; real communication and contention can violate that assumption.
