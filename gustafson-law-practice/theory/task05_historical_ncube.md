# Task 05 — Reconstructing the nCUBE-10 Result

## Historical setting

Gustafson, Montry, and Benner reported results on a 1,024-processor MIMD hypercube. Their 1988 paper reports fixed-size speedups of 502–637× and scaled speedups of 1,009–1,020× when problem size per processor is held fixed. The central point was not that a fixed small job suddenly violated Amdahl's law. They evaluated a larger scientific workload that could use the available processors while keeping elapsed time practical. The reported serial fraction was approximately 0.4%, and the scaled speedup exceeded 1,000.

## Numerical reconstruction

Use `P=1024` and `α=0.004`:

\[
S_G=1024-0.004(1023)=1019.908.
\]

This is greater than 1,000. The corresponding Gustafson efficiency is

\[
E_G=1019.908/1024\approx0.996003=99.6003\%.
\]

For comparison only, if `0.004` were treated as Amdahl's fixed-work serial fraction:

\[
S_A=\frac{1}{0.004+0.996/1024}\approx202.7.
\]

The two figures answer different questions. The scaled result measures the capacity to solve a much larger problem in similar time; the Amdahl value estimates a fixed-size job.

## Why problem expansion matters

The larger workload exposes more parallel work. The serial fraction is measured relative to the parallel execution of that expanded workload, rather than assumed to be the fraction of a small baseline problem. Thus the Amdahl ceiling for a fixed job is not a ceiling on the amount of larger work that can be completed in a fixed time.

## Caution

The task sheet's 0.4% serial-fraction scenario gives a useful reconstruction (about 1,019.9×), consistent with the upper end of the published scaled-speedup range. The original paper's reported range is 1,009–1,020×; it also reports 502–637× for fixed-size runs. The task sheet's shorthand does not provide the full experiment configuration, input dimensions, compiler flags, or raw timing table. This reconstruction therefore explains the mathematical scenario; it does not claim to reproduce every historical measurement. For a fully sourced historical paper, consult the original Gustafson (1988) article and its cited technical report.

## Reference

Gustafson, J. L., Montry, G. R., & Benner, R. E. (1988). *Development of parallel methods for a 1024-processor hypercube*. SIAM Journal on Scientific and Statistical Computing, 9(4), 609–638. https://doi.org/10.1137/0909041

Gustafson, J. L. (1988). *Reevaluating Amdahl's law*. Communications of the ACM, 31(5), 532–533.
