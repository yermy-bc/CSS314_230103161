# Task 04 — Asymptotic Parallel Efficiency

## Gustafson efficiency

Given

\[
S_G(P)=P-\alpha(P-1)=\alpha+(1-\alpha)P,
\]

divide by `P`:

\[
E_G(P)=\frac{S_G(P)}P=(1-\alpha)+\frac{\alpha}{P}.
\]

Taking the limit:

\[
\boxed{\lim_{P\to\infty}E_G(P)=1-\alpha}.
\]

For a fixed `α`, the efficiency approaches a positive constant. It does not approach one unless `α=0`.

## Amdahl efficiency

For Amdahl speedup

\[
S_A(P)=\frac{1}{s+(1-s)/P},
\]

the efficiency is

\[
E_A(P)=\frac{S_A(P)}P
=\frac{1}{Ps+(1-s)}.
\]

For `s>0`,

\[
\boxed{\lim_{P\to\infty}E_A(P)=0}.
\]

If `s=0`, efficiency is one for all `P`.

## Deduction

The limits differ because Amdahl holds total work fixed: processors eventually have little useful parallel work. Gustafson grows the workload with processor count: each processor continues to perform a comparable amount of parallel work. The Gustafson limit is still bounded by the serial fraction measured on the parallel system.
