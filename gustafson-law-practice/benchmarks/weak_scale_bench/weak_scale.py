#!/usr/bin/env python3
"""Fixed-work-per-process weak-scaling benchmark using multiprocessing."""
import argparse, csv, multiprocessing as mp, os, platform, sys, time
from pathlib import Path

def worker(args):
    seed, work = args
    # Deterministic floating-point workload; each process performs the same work.
    x = (seed + 1) * 0.000001
    acc = 0.0
    for i in range(work):
        x = (x * 1.000000119 + 0.00000031) % 1.0
        acc += x
    return acc

def run_once(processes, work):
    tasks = [(i, work) for i in range(processes)]
    start = time.perf_counter()
    with mp.Pool(processes=processes) as pool:
        values = pool.map(worker, tasks)
    elapsed = time.perf_counter() - start
    # Consume results so the work cannot be treated as unused.
    checksum = sum(values)
    return elapsed, checksum

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counts", default="1,2,4,8")
    ap.add_argument("--repeats", type=int, default=5)
    ap.add_argument("--work", type=int, default=500000)
    ap.add_argument("--output", default="benchmarks/results.csv")
    args = ap.parse_args()
    if args.counts.strip().lower() == "auto":
        counts = list(range(1, (os.cpu_count() or 1) + 1))
    else:
        counts = sorted(set(int(x.strip()) for x in args.counts.split(",") if x.strip()))
    if len(counts) < 5: ap.error("provide at least five distinct process counts")
    if min(counts) < 1: ap.error("process counts must be >= 1")
    if args.repeats < 5: ap.error("use at least five repetitions")
    if args.work < 1: ap.error("work must be positive")
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for p in counts:
        for run in range(1, args.repeats + 1):
            elapsed, checksum = run_once(p, args.work)
            rows.append({"processes": p, "run": run, "work_per_process": args.work,
                         "runtime_seconds": f"{elapsed:.9f}", "checksum": f"{checksum:.12f}",
                         "cpu_count_logical": os.cpu_count(),
                         "platform": platform.platform(), "python": sys.version.split()[0]})
            print(f"P={p:>3} run={run} time={elapsed:.6f}s")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader(); writer.writerows(rows)
    print(f"Saved {len(rows)} measurements to {out}")
if __name__ == "__main__": main()
