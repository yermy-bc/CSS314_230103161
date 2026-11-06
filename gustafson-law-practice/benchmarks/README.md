# Benchmark programs

- `simulator.py`: theoretical Amdahl and Gustafson curves; writes CSV and a PNG overlay.
- `weak_scale_bench/weak_scale.py`: process-based weak-scaling benchmark with fixed work per process.
- `fit_gustafson.py`: summarizes repeated measurements, estimates `α` by least-squares fitting, and creates comparison plots.
- `results.csv`: raw measurements. Run the benchmark on the target machine before using results in the report. Use `--counts auto` to test every logical processor count from 1 through the host's reported maximum.

Run commands from the repository root. Python 3.10+ is recommended; install dependencies with `python -m pip install -r benchmarks/requirements.txt`.
