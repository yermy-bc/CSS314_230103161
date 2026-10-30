"""Experiment A: fixed serial bottleneck and CPU-parallel work."""
import math
import time
from multiprocessing import Pool


def heavy_math(n: int) -> float:
    return sum(math.sin(i) * math.cos(i) for i in range(1, n))


def run_experiment(workers: int, total_chunks: int = 16,
                   chunk_size: int = 2_000_000) -> float:
    if workers < 1:
        raise ValueError('workers must be at least one')
    start = time.perf_counter()
    time.sleep(0.40)  # Deliberate serialized master-process section.
    with Pool(processes=workers) as pool:
        results = pool.map(heavy_math, [chunk_size] * total_chunks)
    assert len(results) == total_chunks
    return time.perf_counter() - start


if __name__ == '__main__':
    for p in (1, 2, 4):
        print(f'P={p} Runtime={run_experiment(p):.3f}s', flush=True)
