# Ablation Study

## Student information

- **Student name:** Ricardo Torres Lopez
- **Student ID:** RicardoTL1975

## Final model

- **Architecture:** `ImprovedCNN` with three convolution stages (32, 64, and 128 channels), Batch Normalization, SiLU activation, Max Pooling, global average pooling, dropout, and a five-class linear layer.
- **Trainable parameters:** 94,117
- **Parameter constraint below 95,000:** PASS
- **Best validation accuracy without TTA:** 0.7990
- **Best validation macro F1 without TTA:** 0.7989
- **Best EMA epoch:** 49
- **Selected TTA mode:** `none`
- **Validation accuracy with selected TTA:** 0.7990
- **Validation macro F1 with selected TTA:** 0.7989
- **Final fine-tuning samples:** 4,000
- **Fine-tuning epochs:** 15
- **Final checkpoint:** `final_stl5_v3_ema_model.pt`

## Experiments

| Experiment | Main change | Params | Val accuracy | Val F1 macro | Comment |
|---|---|---:|---:|---:|---|
| Baseline | Original SimpleCNN, 5 epochs, no active augmentation | 93,893 | 0.5550 | 0.5436 | The model was undertrained and had limited regularization. |
| Experiment 1 | BatchNorm, SiLU, moderate augmentation, AdamW, cosine scheduler, label smoothing, 50 epochs | 94,117 | 0.7860 | 0.7852 | Longer and more stable training produced the largest improvement over the baseline. |
| Experiment 2 | Added EMA weight averaging and trained for 60 epochs | 94,117 | 0.7990 | 0.7989 | EMA reduced changes between epochs and improved both validation metrics. |
| Final V3 | Validation-driven TTA selection and low-LR fine-tuning of the best EMA model with all labeled images | 94,117 | 0.7990 | 0.7989 | TTA is used only when it improves validation F1. Fine-tuning starts from the best checkpoint instead of random weights. |

## Error analysis

The validation confusion matrix indicates:

- The class with the lowest recall is **cat**, with recall 0.6850.
- The most frequent off-diagonal error is **cat → dog**, with 38 validation images.
- Per-class recall: airplane=0.8800, bird=0.7450, car=0.9500, cat=0.6850, dog=0.7350.
- Accuracy and macro F1 are close, which suggests that the model does not obtain its result by ignoring one class.

## Conclusion

The largest improvement came from replacing the short baseline training with a better optimization and augmentation pipeline. Validation macro F1 increased from 0.5436 to 0.7852. EMA then increased it to 0.7989 while making validation more stable.

V3 adds two conservative changes. First, it compares normal inference, horizontal-flip TTA, and translated-plus-flipped TTA on validation, then selects `none` because it obtained the best validation macro F1 (0.7989). Second, the final model starts from the best EMA checkpoint and is fine-tuned with all 4,000 labeled images using a lower learning rate. This preserves the representation learned during model selection while using every public label before hidden-test prediction.

The final model remains below the parameter limit and uses only one 94,117-parameter network at inference.

## Submission files

The submission ZIP contains exactly:

- `predictions.csv`
- `ABLATIONS.md`
