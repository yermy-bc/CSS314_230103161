# Task 15 — Energy and Power under Weak Scaling

## Power model

Let each active processor consume `P_active` watts while computing and `P_idle` watts while idle. If all `P` nodes remain powered for elapsed time `T`, and a fraction `u` of each node's time is active, average power per node is

\[
\bar P_{node}=uP_{active}+(1-u)P_{idle}.
\]

Total energy is

\[
\boxed{E_P=P\,T\,[uP_{active}+(1-u)P_{idle}]}.
\]

For a simplified fully active weak-scaling workload (`u=1`), `E_P=P T P_active`.

## One core versus P cores

For identical wall-clock runtime `T`, one active core consumes approximately

\[
E_1=T P_{active}.
\]

P fully active cores consume

\[
E_P=P T P_{active},
\qquad E_P/E_1=P.
\]

Thus linear weak scaling can deliver P times as much work in the same time but may use approximately P times the processor energy, ignoring fixed system power and differences in per-core power.

## Interpretation

The comparison is not automatically an energy-efficiency loss: useful work also increases. Energy per unit work may remain similar if per-core efficiency is stable. Real systems must include memory, network, fans, power supplies, idle nodes, DVFS, and cooling. If nodes are underutilized, power gating or shutting down idle resources can materially change the result.
