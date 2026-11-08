# Experiment 2 — Learning Tic-Tac-Toe from Human Gameplay

## Research Question

Can a symmetry-aware Q-learning agent improve its Tic-Tac-Toe decisions through additional human gameplay and demonstrations?

More importantly, does the learned behavior generalize beyond the human who trained it?

## Method

This experiment extends the original tabular Q-learning agent with symmetry-aware state-action representations.

The project investigates:
- Q-learning from human gameplay
- Symmetry-based representation of board positions
- Learning preferences from recorded human moves
- Evaluation against a frozen final model

The agent was not supplied with a hardcoded optimal Tic-Tac-Toe strategy.

## Experiment Results

### Additional Human Gameplay

| Outcome | Games |
|---|---:|
| Human wins | 81 |
| AI wins | 41 |
| Draws | 178 |
| Total | 300 |

### Human Demonstrations

| Dataset | Recorded moves |
|---|---:|
| All demonstrations | 1,234 |
| Training | 972 |
| Test | 262 |

The training and test files are separate. Game-level separation and evaluation independence require further verification.

### Frozen Final Challenge

| Outcome | Games |
|---|---:|
| Human wins | 4 |
| AI wins | 14 |
| Draws | 82 |
| Total | 100 |

The final challenge used the trained model with exploration disabled and training=False for action selection. No Q-learning update call was observed in the reviewed final gameplay path.

Equal-valued actions could still be selected randomly.

## Independent Opponent Benchmark

Two frozen models were evaluated against three scripted opponents, with
1,000 games as X and 1,000 games as O per model-opponent combination.

| Opponent | Baseline W/D/L | Final W/D/L |
|---|---|---|
| Random | 1192 / 597 / 211 | 1364 / 474 / 162 |
| Tactical | 379 / 1255 / 366 | 324 / 1413 / 263 |
| Minimax | 0 / 1743 / 257 | 0 / 1826 / 174 |

Across 627 symmetry-canonical nonterminal states, expected optimal-action
accuracy was 69.85% for the baseline and 75.07% for the final model.

The final model lost fewer games to all three opponent types in this
benchmark, but these results do not establish generalization to unseen
human players. The benchmark uses deterministic random seeds and is not
a statistical uncertainty analysis.

## Interpretation

The results are consistent with improvement in certain game-playing behaviors.

However, the final challenge was conducted against the human participant involved in training.

Therefore, these results do not establish:
- Optimal Tic-Tac-Toe play
- Generalization to unseen human opponents
- Superiority over a minimax opponent
- Performance independent of opponent strategy

The additional gameplay and frozen challenge also differ in experimental conditions and should not be interpreted as a controlled before-and-after comparison.

## Reproducibility

The original implementation and Experiment 2 Python scripts are available in this repository's experiment branch.

The final model is published as JSON, alongside the independent-opponent benchmark code and recorded results.

The benchmark currently loads local pickle checkpoints, including the baseline model. A portable JSON-based inference loader is still needed for independent reproduction. Full gameplay datasets are not yet published.

The reported counts were checked against the author's local game files and score records.

## Planned Validation

1. Verify train/test separation at the game level.
2. Export the frozen model to a safe, portable format.
3. Compare the agent with random, tactical, and minimax baselines.
4. Evaluate against new human opponents.
5. Report optimal-move accuracy and win/draw/loss rates.
6. Publish reproducible evaluation scripts and model checksums.

## Limitations

This is a small-scale independent machine learning experiment, not evidence of general artificial intelligence.

The primary contribution is the experimental investigation of reinforcement learning, symmetry, human demonstrations, and generalization.
