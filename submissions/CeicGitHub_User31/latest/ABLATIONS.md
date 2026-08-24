# Ablation Study

## Final submission

The final submitted model is DeepSEResNetV5, a compact convolutional
neural network trained from scratch. No pretrained weights, external
datasets, hidden test labels, or test-time training were used.

## Challenge scoring

The estimated score is calculated as:

`final_score = 0.70 * macro_f1 + 0.20 * accuracy + 0.10 * efficiency`

where:

`efficiency = min(1.0, 100000 / trainable_parameters)`

## Final architecture

- Architecture: DeepSEResNetV5
- Input: 96 x 96 RGB
- Classes: 5
- Trainable parameters: 94,676
- Efficiency: 1.000000
- Parameter constraint at or below 100,000: PASS
- Residual bottleneck blocks: 9
- Squeeze-and-Excitation: enabled
- Stochastic depth during primary training: enabled
- Activation: SiLU
- Normalization: Batch Normalization
- Final head: global average pooling, dropout and linear classifier
- Pretrained weights: none

## Optimization

Primary V5 training:

- Optimizer: SGD with Nesterov momentum
- Schedule: OneCycleLR
- Epochs: 200
- Label smoothing: enabled
- Exponential Moving Average: enabled
- Automatic mixed precision: enabled
- Gradient clipping: enabled
- DataLoader workers: 0

SAM refinement:

- Starting point: best V5 EMA checkpoint
- SAM refinement epochs: 25
- Best SAM epoch: 19
- SAM rho: 0.03
- Selected variant: EMA

Final all-labeled refinement:

- Labeled images: 4,000
- Epochs: 12
- Optimizer: SGD with SAM
- SAM rho: 0.02
- Final checkpoint: final_deep_se_resnet_v5_ema.pt

## Data augmentation

- Reflect-padded random crop
- Random horizontal flip
- Moderate RandAugment during primary training
- Mild ColorJitter during SAM refinement
- Random erasing
- Dataset-specific normalization

## Validation experiments

| Experiment | Accuracy | Macro F1 | Estimated score |
|---|---:|---:|---:|
| V1 TinyDSResNet raw | 0.8440 | 0.841849 | 0.858094 |
| V4 CompactResNet | 0.8720 | 0.872297 | 0.885008 |
| V4 SAM | 0.8760 | 0.876284 | 0.888599 |
| V4 weight soup | 0.8760 | 0.876367 | 0.888657 |
| Large teacher ablation | 0.8680 | 0.868185 | not selected |
| V5 DeepSEResNet | 0.8770 | 0.877536 | 0.889675 |
| V5 SAM | 0.8850 | 0.885160 | 0.896612 |

The large teacher was trained only as an ablation. It was rejected because
its validation performance was lower than the compact student, and it was
not used for final distillation or test prediction.

## Test-time augmentation

The following methods were evaluated on validation:

| TTA | Accuracy | Macro F1 | Estimated score |
|---|---:|---:|---:|
| None | 0.8850 | 0.885160 | 0.896612 |
| Horizontal flip | 0.8770 | 0.877079 | 0.889356 |
| Translated flip | 0.8730 | 0.873014 | 0.885710 |
| Multiscale flip | 0.8650 | 0.865449 | 0.878815 |

All TTA methods reduced validation performance. The final submission
therefore uses one deterministic unmodified view per test image.

## Calibration

No class-logit biases, forced class quotas, or probability calibration
were applied. Cat and dog errors were approximately symmetric on
validation, so a global class bias was not justified.

## Selected validation result

These metrics were measured before combining training and validation:

- Validation accuracy: 0.8850
- Validation macro F1: 0.885160
- Estimated local score: 0.896612
- Trainable parameters: 94,676
- Efficiency: 1.000000

After model selection, the selected checkpoint was refined using all
4,000 labeled train and validation images. Hidden test labels were not
used for training or model selection.

## Test prediction summary

- Test images: 2,500
- Mean confidence: 0.8588
- Minimum confidence: 0.2716
- Maximum confidence: 0.9999

| Class | Label | Predictions |
|---|---:|---:|
| airplane | 0 | 494 |
| bird | 1 | 480 |
| car | 2 | 509 |
| cat | 3 | 493 |
| dog | 4 | 524 |

## Reproducibility

Random seeds were fixed where supported. CUDA kernels may produce small
numerical variations between independent executions. The prediction IDs
follow the exact order of `sample_submission.csv`.
