# Task 01 — Strong Scaling vs. Weak Scaling

## Amdahl's fixed-size model

Amdahl (1967) asks how much faster a *fixed total problem* can finish when it is divided among more processors. Let `s` be the serial fraction and `1-s` the parallel fraction. For `P` processors, normalized execution time is

\[
T_A(P)=s+\frac{1-s}{P},\qquad
S_A(P)=\frac{1}{s+(1-s)/P}.
\]

The workload dimension is held constant: `W(P)=W_0`. As `P → ∞`, the parallel part approaches zero, but the serial part remains. Thus `S_A(P) → 1/s` for `s>0`. Adding processors cannot remove the fixed serial work.

## Gustafson's fixed-time model

Gustafson (1988) asks a different question: if a parallel computer is available, how much *larger problem* can be solved in approximately the same elapsed time? The parallel execution time is normalized to one unit. The serial fraction observed on the parallel machine is `α`; the parallel fraction is `1-α`. The scaled serial-equivalent work is

\[
S_G(P)=\alpha+(1-\alpha)P=P-\alpha(P-1).
\]

The workload is allowed to grow with `P`. For an ideally weak-scaled workload, `W(P)≈P W_0` while the per-processor work and wall-clock time remain approximately constant. Consequently, `S_G(P)` grows approximately linearly, with slope `1-α`.

## What happens as P tends to infinity?

- **Amdahl:** `W(P)=W_0` remains fixed. `S_A(P)→1/s`, a finite ceiling.
- **Gustafson:** the problem dimension grows with the machine, ideally `W(P)∝P`. `S_G(P)→∞` linearly when `α<1`.

“Fixed-size” and “fixed-time” describe the question being asked, not a claim that every real program achieves ideal scaling. Gustafson's model is useful only when the application can accept a larger workload without causing a disproportionate rise in communication, synchronization, memory pressure, or serial work.

## Philosophical and physical difference

Amdahl emphasizes the unavoidable serial component of a fixed job. Gustafson emphasizes useful work that can be added while keeping elapsed time bounded. They are not contradictory: they model different workload policies. Amdahl is the appropriate baseline for a fixed-size job; Gustafson is appropriate for a growing scientific or data workload.

## References

- Amdahl, G. M. (1967). *Validity of the single processor approach to achieving large scale computing capabilities*. AFIPS.
- Gustafson, J. L. (1988). *Reevaluating Amdahl's law*. Communications of the ACM, 31(5), 532–533.
