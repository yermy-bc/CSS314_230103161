import argparse, json, statistics, time, hashlib
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def naive(A,B):
    M=A.shape[0]; C=np.zeros((M,M))
    for i in range(M):
        for j in range(M):
            C[i,j]=np.dot(A[i,:],B[:,j])
    return C
def interchanged(A,B):
    M=A.shape[0];C=np.zeros((M,M))
    for i in range(M):
        for k in range(M):
            C[i,:]+=A[i,k]*B[k,:]
    return C
def run():
    p=json.loads((ROOT/'results/salted_params.json').read_text()); M=p['N']//2
    rng=np.random.default_rng(p['seed']);A=rng.random((M,M));B=rng.random((M,M))
    times={};outputs={}
    for name,func in [('naive_ijk',naive),('interchanged_ikj',interchanged)]:
        samples=[]
        for trial in range(3):
            t=time.perf_counter();C=func(A,B);samples.append(time.perf_counter()-t)
        times[name]=round(statistics.median(samples),6);outputs[name]=C
        print(name,times[name])
    # Floating-point reductions can differ in order; test explicit tolerance.
    maxerr=float(np.max(np.abs(outputs['naive_ijk']-outputs['interchanged_ikj'])))
    digest=lambda x:hashlib.sha256(np.round(x,6).tobytes()).hexdigest()
    result={'student_id':p['student_id'],'N':p['N'],'M':M,'median_seconds':times,'speedup':times['naive_ijk']/times['interchanged_ikj'],'max_absolute_error':maxerr,'within_abs_tolerance_1e-12':bool(np.allclose(outputs['naive_ijk'],outputs['interchanged_ikj'],rtol=0,atol=1e-12)),'digests_round_6':{k:digest(v) for k,v in outputs.items()},'digests_equal':digest(outputs['naive_ijk'])==digest(outputs['interchanged_ikj'])}
    (ROOT/'results/loop_interchange.json').write_text(json.dumps(result,indent=2)+'\n');print('maximum error',maxerr)
if __name__=='__main__':run()
