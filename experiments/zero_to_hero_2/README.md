# Experiment 1 — Learning Tic-Tac-Toe From Scratch

## Research Question

Can a tabular Q-learning agent improve its Tic-Tac-Toe strategy by learning from 1,000 games against a human?

## Experiment Setup

- Games: 1,000
- Algorithm: Tabular Q-learning
- Learning rate (alpha): 0.10
- Discount factor (gamma): 0.95
- Exploration rate (epsilon): 0.15
- Random seed: 42
- Checkpoint interval: 100 games

The experiment started with a fresh Q-table.

## Results

| Outcome | Games |
|---|---:|
| Human wins | 727 |
| AI wins | 63 |
| Draws | 210 |

## Fixed-Position Evaluation

The agent was evaluated on the same 400 board positions at each checkpoint.

| Metric | Before training | After 1,000 games |
|---|---:|---:|
| Optimal moves | 63.25% | 63.50% |
| Correct blocks | 41.43% | 54.29% |
| Winning opportunities taken | 50.98% | 48.53% |
| Fork opportunities taken | 64.73% | 61.35% |

## Key Findings

### 1. Defensive improvement

Correct blocking increased on the fixed-position benchmark.

### 2. Opening-specific learning

The agent developed useful responses to some corner openings.

### 3. Limited generalization

The agent did not reliably transfer learned behavior between rotationally equivalent board positions.

### 4. Failure of targeted repetition

During the final 40 games, the human repeatedly opened in the bottom-left corner when starting first.

The AI selected the center response in only 3 of 24 opportunities.

Repeated exposure did not resolve this opening weakness.

## Limitations

- The human opponent's playing strategy changed during training.
- The dataset contains only one 1,000-game training run.
- Exploration and random Q-value tie-breaking affect decisions.
- Individual Q-values do not establish general strategic understanding.
- The fixed-position evaluation does not demonstrate substantial overall optimal-play improvement.

## Conclusion

The agent demonstrated measurable defensive improvement and learned some position-specific preferences.

However, the experiment does not establish that it learned a general optimal Tic-Tac-Toe strategy.

A follow-up experiment will investigate symmetry-aware Q-learning.

## Reproducibility

Experiment configuration is available in `config.json`.

Raw human gameplay logs and trained model checkpoints are retained locally and are not included in this repository.
