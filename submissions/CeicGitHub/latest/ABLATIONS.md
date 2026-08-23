# Ablation Study

## Final submission

The final submission uses a compact convolutional neural network trained
from scratch. No pretrained weights, external datasets, or hidden test
labels were used.

## Scoring formula

The estimated challenge score was calculated as:

`final_score = 0.70 * macro_f1 + 0.20 * accuracy + 0.10 * efficiency`

where:

`efficiency = min(1.0, 100000 / trainable_parameters)`

## Final architecture

- Model: TinyDSResNet
- Input resolution: 96 x 96 RGB
- Number of classes: 5
- Trainable parameters: 96,605
- Efficiency score: 1.000000
- Parameter constraint below 100,000: PASS
- Convolution type: depthwise-separable convolution
- Normalization: Batch Normalization
- Activation: SiLU
- Residual connections: enabled
- Classification head: global average pooling, dropout and linear layer
- Pretrained weights: none

## Data augmentation

The selected training augmentation includes:

- Random resized crop
- Random horizontal flip
- Mild color jitter
- Small random rotation
- Occasional grayscale conversion
- Random erasing
- Dataset-specific normalization

## Optimization

- Optimizer: AdamW
- Learning-rate schedule: OneCycleLR
- Loss: cross-entropy with label smoothing
- Exponential Moving Average: enabled
- Automatic mixed precision: enabled
- Gradient clipping: enabled
- Random seed: 42

## Validation experiments

| Experiment | Accuracy | Macro F1 | Estimated score |
|---|---:|---:|---:|
| Original SimpleCNN baseline | 0.5550 | 0.5436 | 0.5915 |
| V1 TinyDSResNet | 0.8440 | 0.841849 | 0.858094 |
| V2 MixUp/CutMix | 0.8230 | 0.820980 | 0.839286 |
| V3 focal fine-tuning | 0.8240 | 0.821863 | 0.840104 |
| V1 translated-flip TTA | 0.8520 | 0.849743 | 0.865220 |
| V1 TTA and logit calibration | 0.8600 | 0.859036 | 0.873325 |

## Selected validation configuration

- Validation accuracy: 0.8600
- Validation macro F1: 0.859036
- Estimated local final score: 0.873325
- Selected TTA: five translated views and horizontal flips
- Total test-time views: 10
- Cat logit adjustment: +0.550
- Dog logit adjustment: +0.175

MixUp, CutMix and focal-loss fine-tuning were rejected because their
validation scores were lower than the V1 model.

## Final training

After model and hyperparameter selection, the V1 EMA checkpoint was
fine-tuned using all available labeled images:

- Original training images: 3,000
- Original validation images: 1,000
- Final labeled images: 4,000
- Final fine-tuning epochs: 18
- Final checkpoint: final_tiny_ds_resnet_ema.pt

The validation metrics reported above were measured before combining the
training and validation sets. Hidden test labels were never used.

## Test prediction

- Test images: 2,500
- Mean prediction confidence: 0.8592
- Minimum prediction confidence: 0.2929
- Maximum prediction confidence: 0.9998

Predicted class distribution:

| Class | Label | Predictions |
|---|---:|---:|
| airplane | 0 | 501 |
| bird | 1 | 559 |
| car | 2 | 529 |
| cat | 3 | 435 |
| dog | 4 | 476 |

## Reproducibility

The model uses deterministic random seeds where supported. CUDA operations
may still introduce small numerical differences between independent runs.
The submitted CSV follows the exact ID order in `sample_submission.csv`.
