"""Experiment C: process-local accumulation with one final reduction."""
import time
from multiprocessing import Pool


def private_worker(iterations: int) -> int:
    local_sum = 0
    for _ in range(iterations):
        local_sum += 1
    return local_sum


def run_privatized(p: int, total_increments: int = 20_000_000) -> float:
    if p < 1 or total_increments % p:
        raise ValueError('p must divide total_increments and be >= 1')
    tasks = [total_increments // p] * p
    start = time.perf_counter()
    with Pool(processes=p) as pool:
        values = pool.map(private_worker, tasks)
    total = sum(values)
    elapsed = time.perf_counter() - start
    assert total == total_increments, (total, total_increments)
    return elapsed


if __name__ == '__main__':
    for p in (1, 2, 4):
        print(f'P={p} Runtime={run_privatized(p):.3f}s', flush=True)
