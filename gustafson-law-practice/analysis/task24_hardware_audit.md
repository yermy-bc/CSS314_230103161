# Task 24 — Hardware Audit and Interpretation

## Required machine-specific information

Record the following on the computer where the benchmark is executed:

- CPU model and physical/logical core counts (`lscpu` on Linux; Task Manager / System Information on Windows).
- Cache hierarchy and sizes (for example, `lscpu -C` on Linux; CPU-Z on Windows).
- Memory type, speed, channel configuration, and installed capacity (CPU-Z or vendor specifications).
- NUMA topology (`numactl --hardware` on Linux).
- Operating system, Python version, power plan, and whether the machine was plugged in.

Do not copy a different machine's specifications into this report. The benchmark records Python and platform information automatically, but cache and memory-channel details should be checked using the operating system or a hardware utility.

## Interpreting deviations

- **Thermal throttling:** sustained load raises temperature and reduces clock frequency.
- **NUMA effects:** workers accessing remote memory can have higher latency and lower bandwidth.
- **Memory bandwidth saturation:** adding workers may not increase throughput once bandwidth is exhausted.
- **Process overhead:** Python multiprocessing has startup, scheduling, and serialization costs.
- **Background activity:** other applications add noise to wall-clock measurements.

## Experimental protocol

Use at least five distinct process counts and five independent repetitions per count. Keep the per-process workload constant. Run on AC power, close unrelated workloads, avoid changing power settings during the experiment, and report mean and standard deviation. Repeat the complete experiment if the machine throttles or a background task interrupts it.
