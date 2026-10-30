import argparse, csv, ctypes, multiprocessing as mp, statistics, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def worker_shared(arr,idx,K):
    for _ in range(K):arr[idx]+=1
def worker_private(arr,idx,K):
    local=0
    for _ in range(K):local+=1
    arr[idx]=local
def run_once(mode,P,K):
    # lock=False avoids a shared synchronized mutex, isolating false sharing.
    stride=8 if mode=='padded' else 1
    arr=mp.Array(ctypes.c_int64,64 if mode=='padded' else 8,lock=False)
    fn=worker_private if mode=='privatized' else worker_shared
    jobs=[mp.Process(target=fn,args=(arr,i*stride,K)) for i in range(P)]
    start=time.perf_counter()
    for job in jobs:job.start()
    for job in jobs:job.join()
    duration=time.perf_counter()-start
    if any(job.exitcode!=0 for job in jobs):raise RuntimeError('worker exited unsuccessfully')
    total=sum(arr[i*stride] for i in range(P));assert total==P*K,(total,P*K)
    return duration,total
def run(K=5_000_000,repeat=1):
    rows=[]
    for mode in ['unpadded','padded','privatized']:
        baseline=None
        for P in [1,2,4,8]:
            measurements=[run_once(mode,P,K) for _ in range(repeat)]
            sec=statistics.median(x[0] for x in measurements)
            if P==1:baseline=sec
            speedup=baseline/sec
            e=((P*sec/baseline)-1)/(P-1) if P>1 else None
            rows.append({'mode':mode,'workers':P,'iterations_per_worker':K,'total_count':P*K,'time_seconds':round(sec,6),'speedup':round(speedup,6),'karp_flatt_e':round(e,6) if e is not None else ''})
            print(mode,'P',P,'seconds',round(sec,3),'e',e)
    with (ROOT/'results/false_sharing_karp_flatt.tsv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter='\t');writer.writeheader();writer.writerows(rows)
if __name__=='__main__':
    mp.freeze_support();ap=argparse.ArgumentParser();ap.add_argument('--iterations',type=int,default=5_000_000);ap.add_argument('--repeat',type=int,default=1);a=ap.parse_args();run(a.iterations,a.repeat)
