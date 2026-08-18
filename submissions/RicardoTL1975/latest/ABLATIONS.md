# Ablation / Experiment Report

## Student Information
- **Student Name**: Ricardo_Torres_Lopez
- **Student ID**: RicardoTL75

## Final Model
- **Model Name**: CNN_Challenge
- **Number of Parameters**: 53,485
- **Parameter Constraint (<95,000)**: PASS
- **Best Validation Accuracy**: 0.8368
- **Validation F1-macro at Best Accuracy**: 0.8366
- **Best Validation Epoch**: 81

## Implemented Experiments / Design Changes

### Experiment 1 — Data Augmentation
The training pipeline uses:
- RandomHorizontalFlip
- RandomRotation(10)
- ColorJitter for brightness and contrast

Validation data uses deterministic normalization without random augmentation.

### Experiment 2 — Regularization
The final CNN uses:
- Dropout(0.4)
- Dropout(0.3)
- Batch Normalization
- AdamW with weight decay = 5e-4
- CrossEntropyLoss with label smoothing = 0.1

### Experiment 3 — Learning-Rate Schedule
The training configuration uses CosineAnnealingLR to progressively reduce the learning rate during training.

### Experiment 4 — Early Stopping and Best-Checkpoint Selection
Training uses early stopping. The checkpoint with the best validation accuracy is saved as:
`best_model_optimized.pth`

For the competition submission, that best checkpoint is loaded before generating predictions.

## Final Architecture
- 3 convolutional blocks
- Convolution channels: 8, 16, 32
- Batch Normalization
- ReLU activation
- Max Pooling
- Fully connected layers: 64 -> 32 -> 5
- Dropout: 0.4 and 0.3
- Kaiming initialization

## Results
The notebook records:
- **Parameters**: 53,485
- **Best Validation Accuracy**: 0.8368
- **Validation F1-macro at the same best-accuracy epoch**: 0.8366

## Important Note
This report describes the experiments and techniques actually implemented in the notebook.
No unsupported numeric improvement claims are included for individual ablations.

## Submission Files
The ZIP must contain exactly:
- `predictions.csv`
- `ABLATIONS.md`
