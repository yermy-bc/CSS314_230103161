# Task 17 — 3D 7-Point Stencil Scaling

A cubic domain contains `N³` cells. Interior updates require `Θ(N³)` operations. Boundary exchange across the six faces is proportional to surface area, `Θ(N²)`.

The global surface-to-volume ratio is

\[
\frac{\Theta(N^2)}{\Theta(N^3)}=\Theta(1/N).
\]

If the *global* grid volume grows proportionally to processor count, then `N³∝P` and `N∝P^(1/3)`. Therefore the global surface-to-volume ratio decreases as

\[
\boxed{\Theta(P^{-1/3})}.
\]

However, in conventional 3D weak scaling, each processor owns a fixed local subdomain. The local subdomain dimensions remain fixed, so each processor's halo surface and local volume remain fixed; the per-processor communication-to-computation ratio is approximately constant, not progressively better. The global ratio can be misleading because the number of subdomain interfaces also increases.

**Conclusion:** global surface/volume improves with a larger cubic domain, but standard fixed-local-volume weak scaling does not automatically improve each node's communication ratio. Network contention and synchronization may still worsen.
