#!/usr/bin/env python3
"""Fit Gustafson alpha from weak-scaling measurements and create comparison plots."""
import argparse, csv, statistics
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--input",default="benchmarks/weak_scale_bench/results.csv")
    ap.add_argument("--output-dir",default="plots")
    args=ap.parse_args()
    grouped=defaultdict(list)
    with open(args.input,newline="",encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if not row.get("processes"): continue
            grouped[int(row["processes"])].append(float(row["runtime_seconds"]))
    if len(grouped)<5: raise SystemExit("Need at least five distinct process counts.")
    if 1 not in grouped: raise SystemExit("Include P=1 as the baseline.")
    ps=sorted(grouped)
    means={p:statistics.mean(grouped[p]) for p in ps}
    sds={p:statistics.stdev(grouped[p]) if len(grouped[p])>1 else 0.0 for p in ps}
    ses={p:sds[p]/(len(grouped[p])**0.5) for p in ps}
    t1=means[1]
    # Scaled speedup compares P copies of the single-worker workload with
    # the P-worker run: S(P) = P*T(1)/T(P).
    measured={p:p*t1/means[p] for p in ps}
    # Least-squares fit S(P)=P-alpha(P-1), with one fitted alpha.
    num=sum((p-1)*(p-measured[p]) for p in ps if p!=1)
    den=sum((p-1)**2 for p in ps if p!=1)
    alpha=max(0.0,min(1.0,num/den if den else 0.0))
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True)
    with (out/"benchmark_summary.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["processes","runs","mean_seconds","stddev_seconds","standard_error_seconds","measured_scaled_speedup","gustafson_fit","amdahl_fit"])
        for p in ps:
            w.writerow([p,len(grouped[p]),means[p],sds[p],ses[p],measured[p],
                        p-alpha*(p-1),1/(alpha+(1-alpha)/p)])
    # Propagate standard error in runtime: d(P*T1/T)/dT = -P*T1/T^2.
    yerr={p:p*t1*ses[p]/(means[p]**2) for p in ps}
    plt.figure()
    plt.plot(ps,ps,"--",label="Ideal linear")
    plt.plot(ps,[p-alpha*(p-1) for p in ps],label=f"Gustafson fit (alpha={alpha:.4f})")
    plt.plot(ps,[1/(alpha+(1-alpha)/p) for p in ps],label="Amdahl fixed-size curve")
    plt.errorbar(ps,[measured[p] for p in ps],yerr=[yerr[p] for p in ps],
                 fmt="o",capsize=4,label="Measured scaled speedup ± SE")
    plt.xlabel("Process count P"); plt.ylabel("Scaled speedup")
    plt.title("Empirical and theoretical scaling")
    plt.grid(True,alpha=.25); plt.legend(); plt.tight_layout()
    plt.savefig(out/"empirical_vs_theoretical.png",dpi=300); plt.close()
    print(f"Least-squares alpha: {alpha:.6f} ({alpha*100:.3f}%)")
    print(f"Summary: {out/'benchmark_summary.csv'}")
    print(f"Plot: {out/'empirical_vs_theoretical.png'}")
if __name__=="__main__": main()
