import argparse, csv, json, math, multiprocessing as mp, statistics, time
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
_SHARED=None

def init_worker(shared,shape):
    global _SHARED
    _SHARED=np.frombuffer(shared,dtype=np.float64).reshape(shape)

def stencil_chunk(bounds):
    lo,hi=bounds
    a=_SHARED
    # Standard five-point stencil on interior cells, with constant zero boundaries.
    # Each output uses 4 neighbor additions and a multiply (5 FLOPs/cell).
    out=(a[lo-1:hi-1,1:-1]+a[lo+1:hi+1,1:-1]+a[lo:hi,:-2]+a[lo:hi,2:]+a[lo:hi,1:-1])*0.2
    return (lo,hi,out)

def one_stencil(N,P,seed,repeat=2):
    rng=np.random.default_rng(seed); a=rng.random((N,N),dtype=np.float64)
    raw=mp.RawArray('d',N*N)
    np.frombuffer(raw,dtype=np.float64)[:]=a.ravel()
    starts=np.linspace(1,N-1,P+1,dtype=int)
    ranges=[(int(starts[i]),int(starts[i+1])) for i in range(P) if starts[i]<starts[i+1]]
    samples=[];last=None
    for _ in range(repeat):
        start=time.perf_counter()
        with mp.Pool(processes=P,initializer=init_worker,initargs=(raw,(N,N))) as pool:
            pieces=pool.map(stencil_chunk,ranges)
        result=np.zeros_like(a)
        for lo,hi,b in pieces:result[lo:hi,1:-1]=b
        samples.append(time.perf_counter()-start);last=result
    reference=np.zeros_like(a)
    reference[1:-1,1:-1]=(a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:]+a[1:-1,1:-1])*0.2
    error=float(np.max(np.abs(reference-last)))
    assert np.allclose(reference,last,rtol=0,atol=1e-12),error
    checksum=float(np.sum(last))
    return statistics.median(samples),checksum,error

def run():
    params=json.loads((ROOT/'results/salted_params.json').read_text());profile=json.loads((ROOT/'results/host_profile.json').read_text())
    base=params['N'];physical=profile.get('physical_cores') or (profile.get('logical_threads') or 1)
    counts=[p for p in [1,2,4,8,16,32,64] if p<=physical]
    if 1 not in counts:counts.insert(0,1)
    rows=[];baseline=None
    for P in counts:
        sec,cs,err=one_stencil(base,P,params['seed'])
        if baseline is None:baseline=sec
        speed=baseline/sec
        serial=(P/speed-1)/(P-1) if P>1 else None
        rows.append(dict(mode='strong',P=P,N=base,work=(base-2)**2,time_seconds=round(sec,6),speedup=round(speed,6),efficiency_pct=round(speed/P*100,4),amdahl_s=round(serial,6) if serial is not None else '',amdahl_ceiling=round(1/serial,6) if serial and serial>0 else '',checksum=round(cs,9),max_abs_error=err))
        print('strong',P,'N',base,'seconds',round(sec,3))
    weak_base=None;work1=None
    for P in counts:
        N=math.ceil(base*math.sqrt(P))
        sec,cs,err=one_stencil(N,P,params['seed'])
        work=(N-2)**2
        if weak_base is None:weak_base=sec;work1=work
        scaled=(P*work1*weak_base)/(work*sec)
        rows.append(dict(mode='weak',P=P,N=N,work=work,time_seconds=round(sec,6),speedup=round(scaled,6),efficiency_pct=round(scaled/P*100,4),amdahl_s='',amdahl_ceiling='',checksum=round(cs,9),max_abs_error=err))
        print('weak',P,'N',N,'seconds',round(sec,3))
    with (ROOT/'results/scaling_metrics.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t');w.writeheader();w.writerows(rows)
    # Minimal compulsory traffic: 5 input double reads + 1 output double write per cell.
    # Optimistic if caches re-use neighbor values; actual DRAM traffic is machine-dependent.
    ai=5/(6*8)
    roof={'student_id':params['student_id'],'kernel':'five-point stencil, four additions plus multiply by 0.2','flops_per_output':5,'assumed_bytes_transferred_per_output':48,'theoretical_arithmetic_intensity_flops_per_byte':ai,'assumption':'Five 8-byte loads and one 8-byte store per interior output; no neighbor cache re-use accounted for. This is an upper bound on per-output traffic and gives a lower-bound AI.','hardware_peak_bandwidth_GB_s':None,'hardware_peak_flops_GFlops':None,'ridge_point_flops_per_byte':None,'roofline_classification':'Cannot determine quantitative Roofline regime without measured or manufacturer-specified bandwidth and peak FLOP/s. Low arithmetic intensity makes bandwidth limitation plausible.','cache':profile.get('cache'),'strong_scaling_worker_counts':counts,'weak_scaling_formula_used':'P * work_1 * T_weak_1 / (work_P * T_weak_P); exactly as written in the handout','caution':'The handout expression is NOT conventional Gustafson speedup; it may decrease as 1/P for ideal constant weak-scaling runtime. Results report the specified metric without relabeling it.'}
    (ROOT/'results/roofline_summary.json').write_text(json.dumps(roof,indent=2)+'\n')
if __name__=='__main__':mp.freeze_support();run()
