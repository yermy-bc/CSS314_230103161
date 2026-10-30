import argparse, csv, statistics, time, json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def run():
    params=json.loads((ROOT/'results/salted_params.json').read_text()); data=np.ones(params['buffer_elements'],dtype=np.float64)
    result=[]
    for stride in [1,2,4,8,16,32,64,128]:
        times=[]; count=len(data[::stride])
        for trial in range(10):
            t=time.perf_counter_ns(); v=float(np.add.reduce(data[::stride])); elapsed=time.perf_counter_ns()-t
            assert v==count
            if trial>=5:times.append(elapsed)
        median=statistics.median(times)
        result.append({'stride':stride,'elements_touched':count,'median_time_ns':int(median),'ns_per_element':round(median/count,6)})
        print('stride',stride,'ns/element',round(median/count,3))
    with (ROOT/'results/stride_results.tsv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=result[0].keys(),delimiter='\t');w.writeheader();w.writerows(result)
if __name__=='__main__':run()
