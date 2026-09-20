# Verifier Calibration Report

- Verifier: `trace-support-verifier-v1`
- Question: `trace-support-v1`
- Rows: 242
- Label source: `derived-from-benchmark-oracle`

The trusted label is the deterministic grader. The verifier sees only the
trace, which is the information available in production. Accuracy alone
cannot tell you whether its confidence is safe to act on.

## Operating Policy

```text
Maximize coverage subject to precision >= 0.98
and at most 0 false accepts,
selected on the threshold_selection split.
```

**No threshold satisfies the constraint.** best achievable precision is 0.92 at threshold 0.65, below the required 0.98.

That is a result, not a bug. Precision does not improve as the threshold
rises, because the failures this verifier misses are the ones it is most
confident about. The next move is a stronger verifier, not a lower bar.

The tables below use the best achievable point (threshold **0.65**, coverage 1.0, precision 0.92) so the error
counts are visible. It is a reference point, not an approved operating policy.

## Slices

| Slice | n | +/- | Brier | Log loss | ECE | FA | FR |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| `adversarial_eval` | 122 | 17/105 | 0.5976 | 1.7705 | 0.6401 | 83 | 6 |
| `threshold_selection` | 50 | 46/4 | 0.1011 | 0.3963 | 0.0826 | 4 | 0 |
| `verifier_eval` | 50 | 43/7 | 0.1519 | 0.5715 | 0.1362 | 7 | 0 |
| `weak_baseline` | 20 | 0/20 | 0.0459 | 0.2411 | 0.2142 | 0 | 0 |

FA = false accepts, FR = false rejects, both at the selected threshold.

## Reliability: `adversarial_eval`

| Band | n | Mean confidence | Observed | Gap |
| --- | ---: | ---: | ---: | ---: |
| 0.2-0.4 | 10 | 0.2789 | 0.2 | +0.0789 |
| 0.4-0.6 | 2 | 0.5374 | 0.5 | +0.0374 |
| 0.6-0.8 | 41 | 0.6894 | 0.2927 | +0.3967 |
| 0.8-1.0 | 69 | 0.9126 | 0.029 | +0.8836 |

## Reliability: `threshold_selection`

| Band | n | Mean confidence | Observed | Gap |
| --- | ---: | ---: | ---: | ---: |
| 0.6-0.8 | 10 | 0.657 | 1.0 | -0.3430 |
| 0.8-1.0 | 40 | 0.9175 | 0.9 | +0.0175 |

## Reliability: `verifier_eval`

| Band | n | Mean confidence | Observed | Gap |
| --- | ---: | ---: | ---: | ---: |
| 0.6-0.8 | 8 | 0.657 | 1.0 | -0.3430 |
| 0.8-1.0 | 42 | 0.9302 | 0.8333 | +0.0968 |

## Reliability: `weak_baseline`

| Band | n | Mean confidence | Observed | Gap |
| --- | ---: | ---: | ---: | ---: |
| 0.2-0.4 | 20 | 0.2142 | 0.0 | +0.2142 |

## What This Set Cannot Tell You

Every label here is derived from the committed benchmark oracle, so no row
carries reviewer disagreement. Genuine ambiguity — the cases that most
deserve human adjudication — is absent by construction. The splits are also
small: fifty rows per scripted split. Treat the numbers as a worked
mechanism, and re-measure on your own labelled traces before trusting any
threshold in production.

