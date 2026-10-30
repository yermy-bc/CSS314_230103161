"""Experiment B: deliberately contended shared counter protected by a mutex."""
import time
from multiprocessing import Process, Value, Lock


def contended_worker(shared_counter, lock, iterations: int) -> None:
    for _ in range(iterations):
        with lock:
            shared_counter.value += 1


def run_contended(p: int, total_increments: int = 2_000_000) -> float:
    if p < 1 or total_increments % p:
        raise ValueError('p must divide total_increments and be >= 1')
    increments_per_worker = total_increments // p
    counter = Value('i', 0)
    lock = Lock()
    processes = [Process(target=contended_worker,
                         args=(counter, lock, increments_per_worker)) for _ in range(p)]
    start = time.perf_counter()
    for proc in processes:
        proc.start()
    for proc in processes:
        proc.join()
    elapsed = time.perf_counter() - start
    if any(proc.exitcode != 0 for proc in processes):
        raise RuntimeError('One or more workers failed')
    assert counter.value == total_increments, (counter.value, total_increments)
    return elapsed


if __name__ == '__main__':
    for p in (1, 2, 4):
        print(f'P={p} Runtime={run_contended(p):.3f}s', flush=True)
