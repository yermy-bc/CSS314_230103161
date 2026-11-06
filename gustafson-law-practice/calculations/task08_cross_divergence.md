# Task 08 — Amdahl vs. Gustafson at P = 128

Given `s=α=0.08` and `P=128`.

## Amdahl fixed-size prediction

\[
S_A=\frac{1}{s+(1-s)/P}
=\frac{1}{0.08+0.92/128}
=\frac{1}{0.0871875}
\approx11.4695.
\]

## Gustafson scaled prediction

\[
S_G=P-\alpha(P-1)
=128-0.08(127)=117.84.
\]

## Percentage discrepancy

Using Amdahl as the reference denominator:

\[
\Delta\%=\frac{S_G-S_A}{S_A}\times100
\approx\frac{117.84-11.4695}{11.4695}\times100
\approx927.4\%.
\]

Gustafson's prediction is about 10.27 times the Amdahl prediction. The percentage depends on the chosen denominator; this report explicitly uses Amdahl as the baseline.

## Explanation

Amdahl distributes a fixed total workload over more processors. Gustafson assumes the problem is expanded so that the parallel execution time stays approximately constant. Their predictions diverge because the workload assumptions differ, not because one algebraic law disproves the other.
