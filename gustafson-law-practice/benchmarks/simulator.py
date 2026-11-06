#!/usr/bin/env python3
"""Generate Amdahl/Gustafson CSV data and speedup/efficiency overlay plots."""
import argparse, csv
from pathlib import Path
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--alpha", type=float, default=0.04, help="single serial fraction")
    ap.add_argument("--alphas", default="", help="optional comma-separated serial fractions")
    ap.add_argument("--max-p", type=int, default=16384)
    ap.add_argument("--output-dir", default="plots")
    args = ap.parse_args()
    alphas = [float(x) for x in args.alphas.split(",") if x.strip()] if args.alphas else [args.alpha]
    if any(not 0.001 <= a <= 0.20 for a in alphas):
        ap.error("all alpha values must be between 0.001 and 0.20")
    if not 1 <= args.max_p <= 65536:
        ap.error("max-p must be between 1 and 65536")
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for alpha in alphas:
        for p in range(1, args.max_p + 1):
            sg = p - alpha * (p - 1)
            sa = 1.0 / (alpha + (1 - alpha) / p)
            rows.append({"P": p, "alpha": alpha, "gustafson_speedup": sg,
                         "gustafson_efficiency": sg/p, "amdahl_speedup": sa,
                         "amdahl_efficiency": sa/p})
    with (out / "scaling_simulation.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    # Plot speedup curves for each requested alpha.
    plt.figure()
    for alpha in alphas:
        ps = list(range(1, args.max_p + 1))
        plt.plot(ps, [p-alpha*(p-1) for p in ps], label=f"Gustafson α={alpha:g}")
        plt.plot(ps, [1/(alpha+(1-alpha)/p) for p in ps], linestyle=":", label=f"Amdahl α={alpha:g}")
    plt.plot(range(1,args.max_p+1), range(1,args.max_p+1), "--", label="Ideal linear")
    plt.xscale("log", base=2); plt.yscale("log", base=2)
    plt.xlabel("Processor count P"); plt.ylabel("Speedup")
    plt.title("Amdahl and Gustafson speedup")
    plt.grid(True, which="both", alpha=.25); plt.legend(); plt.tight_layout()
    plt.savefig(out/"scaling_comparison.png", dpi=300); plt.close()
    print(f"Exported {len(rows)} rows to {out/'scaling_simulation.csv'}")
    print(f"Plot: {out/'scaling_comparison.png'}")
if __name__ == "__main__": main()
