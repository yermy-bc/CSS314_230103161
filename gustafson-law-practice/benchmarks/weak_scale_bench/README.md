# Task 22 — Weak-scaling benchmark

Each worker performs the same number of deterministic floating-point iterations. As process count increases, total work grows proportionally to process count. This is a process-based synthetic benchmark, not a substitute for a domain-specific scientific application.

Example (select five process counts supported by your machine):

```bash
python benchmarks/weak_scale_bench/weak_scale.py --counts 1,2,3,4,5 --repeats 5 --work 500000 --output benchmarks/results.csv
```

The script records elapsed time for every repetition and basic runtime metadata. Multiprocessing startup is included in elapsed time, so interpret small workloads carefully. Increase `--work` if startup dominates.
