# Task 07 — Maximum Tolerable Serial Fraction

Given `P=8192` and required scaled speedup `S(P)≥7500`:

\[
S(P)=P-\alpha(P-1).
\]

Solve the inequality:

\[
8192-\alpha(8191)\ge7500
\]
\[
-\alpha(8191)\ge-692
\]
\[
\alpha\le\frac{692}{8191}.
\]

Therefore,

\[
\boxed{\alpha_{max}=\frac{692}{8191}\approx0.0844824=8.44824\%}.
\]

At this boundary, `S=7500` exactly. Any larger serial fraction violates the stated performance requirement. The result assumes the Gustafson model's serial fraction is measured on the parallel system and remains applicable at 8,192 cores.
