# Karp–Flatt Scalability Diagnostics — Laboratory Results

**Student:** Ainat Yermurat
**Student ID:** 230103161
**Git branch:** practice-230103161
**Course:** Parallel Computing
**Instructor:** Sufyan bin Uzayr

## Hardware and Environment

- CPU model: Not provided.
- Logical CPU cores: Run python -c "import os; print(os.cpu_count())"
- Worker counts: 1, 2, 4
- Measurements: Actual student-reported runtimes.

## Formulas

Speedup: S(p) = T1 / Tp

Karp–Flatt: e(p) = (p * Tp / T1 - 1) / (p - 1)

Parallel efficiency: E(p) = S(p) / p

## Experimental Results

| Experiment | T1 (s) | T2 (s) | T4 (s) | e(2) | e(4) | Architectural Diagnosis |
|---|---:|---:|---:|---:|---:|---|
| A: Serial Tail | 6.099 | 3.706 | 2.323 | 0.215 | 0.175 | Relatively stable serial fraction; intentional sequential bottleneck |
| B: Lock Contention | 3.326 | 11.934 | 12.252 | 6.176 | 4.578 | Severe lock contention and shared-state coordination overhead |
| C: Privatized State | 0.645 | 0.437 | 0.339 | 0.355 | 0.367 | Faster execution through local accumulation; scaling remains sublinear |

## Speedup and Parallel Efficiency

| Experiment | S(2) | S(4) | E(2) | E(4) |
|---|---:|---:|---:|---:|
| A | 1.646x | 2.625x | 82.29% | 65.64% |
| B | 0.279x | 0.271x | 13.93% | 6.79% |
| C | 1.476x | 1.903x | 73.80% | 47.57% |

## Experiment A: Stubborn Serial Tail

The one-worker baseline required 6.099 seconds. With two and four workers, runtime decreased to 3.706 and 2.323 seconds, respectively. The resulting Karp–Flatt scores were e(2) = 0.215 and e(4) = 0.175.

The ratio e(4)/e(2) = 0.811 is within the instructor's accepted range of [0.80, 1.25]. This supports a relatively stable serial component. The deliberate 0.40-second pause is a fixed sequential bottleneck, although multiprocessing overhead also affects the measurements. The scores are above the illustrative 0.10–0.14 range.

## Experiment B: Contention Traffic Jam

The one-worker runtime was 3.326 seconds, while two and four workers required 11.934 and 12.252 seconds. This represents negative speedup: increasing the worker count caused execution to become slower.

The Karp–Flatt scores were e(2) = 6.176 and e(4) = 4.578. These unusually high scores are consistent with serious shared-lock contention. Although T4 > T1, the measured e(4) is lower than e(2), so the instructor's requirement for a strongly increasing Karp–Flatt score is not satisfied in this run.

## Experiment C: Privatization Fix

The privatized implementation required 0.645 seconds with one worker, 0.437 seconds with two workers, and 0.339 seconds with four workers.

The four-worker speedup was 1.903x, with parallel efficiency of 47.57%. Privatization eliminates per-increment shared-lock operations and reduces coordination costs. However, the results do not achieve the required efficiency above 70%, and e(4) = 0.367 is higher than the expected near-zero value.

Experiments B and C use different total iteration counts in the handout (2 million and 20 million), so their absolute runtimes are not a like-for-like comparison of identical workloads.

## Instructor Rubric Verification

| Criterion | Observation | Result |
|---|---|---|
| A: e(4)/e(2) within [0.80, 1.25] | 0.811 | PASS |
| B: T4 > T1 | 12.252 > 3.326 | PASS |
| B: e(4) much greater than e(2) | 4.578 < 6.176 | NOT MET |
| C: T4 < T1 | 0.339 < 0.645 | PASS |
| C: E4 > 70% | 47.57% | NOT MET |

## Conclusion

Experiment A shows scalability limitations caused by a fixed serial bottleneck. Experiment B demonstrates severe lock contention, with multiprocessing becoming slower as more workers compete for a shared counter. Experiment C demonstrates how privatizing state and applying a final reduction can improve execution time, although the measured performance does not reach the target near-linear scaling. The results were recorded as measured, without fabricating or adjusting benchmark values. Repeating Experiments B and C under controlled conditions may help identify variability and improve diagnosis.
