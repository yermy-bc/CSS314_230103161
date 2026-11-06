# Task 12 — Gustafson Model with Communication Penalty

## Model extension

Let `α0` be the non-communication serial fraction and let `C(P)` be communication time, normalized to the baseline parallel runtime. A simple additive model is

\[
T_P=\alpha_0+(1-\alpha_0)+C(P)=1+C(P).
\]

The useful parallel fraction is no longer the whole `1−α0`; communication consumes elapsed time without necessarily producing additional useful work. A normalized effective parallel-time fraction can be written

\[
\alpha_{eff}(P)=\frac{\alpha_0+C(P)}{1+C(P)}.
\]

Substitute into Gustafson's expression:

\[
\boxed{S_{G,C}(P)=P-\alpha_{eff}(P)(P-1)}.
\]

Equivalently,

\[
S_{G,C}(P)=1+(P-1)\frac{1-\alpha_0}{1+C(P)}.
\]

The second form makes the penalty visible: as communication time rises, the useful scaled contribution falls.

## Example communication functions

Possible idealized forms include

\[
C(P)=\beta\log_2(P),\qquad
C(P)=\gamma\sqrt{P},\qquad
C(P)=\delta(P-1).
\]

The coefficients must be measured for the target interconnect and application. These are candidate models, not universal laws.

## Assumptions and limitations

This additive formulation assumes communication is exposed (not hidden by overlap) and is measured in units of the original parallel runtime. If communication overlaps computation, only the unhidden portion should be included. A more detailed model should separate latency, message count, bytes transferred, topology, and synchronization.
