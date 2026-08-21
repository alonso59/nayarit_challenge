# Nayarit STL-5 Challenge — Ablation Study

**Student:** Ricardo Torres Lopez  
**ID:** RicardoTL1975  
**Model:** ImprovedCNN V2  
**Development process:** Approximately 25 iterative experiments, starting near a 0.18 score and progressively improving the pipeline to the current model.

---

## 1. Project setup and dataset loading

| Item | Current implementation | Purpose |
|---|---|---|
| Dataset discovery | Automatic search for the challenge `dataset` folder | Makes the notebook portable in Colab/local environments |
| Training set | 3,000 labeled images | Model optimization |
| Validation set | 1,000 labeled images | Model selection and local evaluation |
| Test set | 2,500 unlabeled images | Final challenge predictions |
| Number of classes | 5 | STL-5 challenge classification |
| Hidden test labels | Never used | Prevents test leakage |

This section was kept simple and deterministic so that later improvements could be compared fairly.

---

## 2. Reproducibility

| Setting | Value | Reason |
|---|---:|---|
| Random seed | 42 | Reproducible experiments |
| Device | CUDA when available | Faster CNN training |
| Deterministic setup | Fixed Python, NumPy and PyTorch seeds | Reduces uncontrolled variation |

A fixed seed was important during the approximately 25 development attempts because it made model changes easier to compare.

---

## 3. Dataset preprocessing and augmentation

| Component | Current value / method | Expected contribution |
|---|---|---|
| Image size | 96 × 96 | Preserves useful spatial detail |
| Training batch size | 64 | Good balance between stability and GPU memory |
| Normalization mean | (0.452328, 0.447057, 0.417794) | Challenge-specific normalization |
| Normalization std | (0.261057, 0.256317, 0.275009) | Challenge-specific scaling |
| Random crop | Padding = 8, reflect mode | Translation robustness |
| Horizontal flip | p = 0.5 | Adds viewpoint diversity |
| Color jitter | brightness/contrast/saturation = 0.15 | Improves color robustness |
| Hue jitter | 0.03 | Small color variation |
| Random erasing | p = 0.15 | Reduces dependence on small local features |
| Validation augmentation | None | Keeps validation measurement clean |

The final augmentation policy is deliberately moderate. Stronger augmentation could reduce training accuracy without necessarily improving hidden-test performance.

---

## 4. ImprovedCNN architecture

| Layer / block | Configuration | Main role |
|---|---|---|
| Conv block 1 | Conv 3→32 + BatchNorm + SiLU + MaxPool | Low-level feature extraction |
| Conv block 2 | Conv 32→64 + BatchNorm + SiLU + MaxPool | Mid-level feature extraction |
| Conv block 3 | Conv 64→128 + BatchNorm + SiLU | Higher-level features |
| Pooling | AdaptiveAvgPool2d(1) | Compact global representation |
| Regularization | Dropout = 0.20 | Reduces overfitting |
| Classifier | Linear 128→5 | Five-class prediction |
| Trainable parameters | 94,117 | Below the 95,000-parameter limit |
| Parameter constraint | PASS | Challenge requirement satisfied |

The architecture reaches 94,117 trainable parameters, using almost all of the available parameter budget without exceeding the challenge limit.

---

## 5. Stable training with EMA

| Training component | Current setting | Contribution |
|---|---|---|
| Maximum epochs | 60 | Gives the scheduler enough time to converge |
| Loss | CrossEntropyLoss | Multi-class classification objective |
| Label smoothing | 0.05 | Reduces overconfidence |
| Optimizer | AdamW | Stable optimization with decoupled weight decay |
| Initial learning rate | 1.5e-3 | Effective starting point for this CNN |
| Weight decay | 5e-4 | Regularization |
| LR scheduler | CosineAnnealingLR | Smooth learning-rate reduction |
| Minimum LR | 3e-5 | Allows late-stage fine tuning |
| Gradient clipping | max norm = 5.0 | Protects against unstable updates |
| EMA decay | 0.995 | Smooths model weights |
| Checkpoint criterion | Validation macro F1 | Prioritizes balanced class performance |
| Best EMA epoch | 49 | Best validation checkpoint |

### Current validation result

| Metric | Best value |
|---|---:|
| Validation accuracy | **0.7990** |
| Validation macro F1 | **0.7989** |
| Estimated local combined score | **1.1299** |

The current run reached its best checkpoint at epoch 49. Accuracy and macro F1 are almost identical, which suggests that performance is reasonably balanced across the five classes.

---

## 6. Learning curves and confusion matrix

| Diagnostic | What it checks |
|---|---|
| Training accuracy curve | Whether the model continues learning |
| Validation accuracy curve | Generalization performance |
| Validation macro-F1 curve | Balanced performance across classes |
| Training loss curve | Optimization stability |
| Confusion matrix | Which classes are most frequently confused |

The learning curves show a gradual improvement rather than a single unstable jump. EMA also helps reduce epoch-to-epoch variation.

---

## 7. Final training using all labeled images

| Item | Current implementation |
|---|---|
| Labeled images used | 4,000 |
| Training source | Original train + validation folders |
| Final model initialization | Fresh ImprovedCNN |
| Final weight averaging | EMA, decay = 0.995 |
| Final epochs | `max(25, best_epoch + 5)` = 54 |
| Optimizer | AdamW |
| Scheduler | CosineAnnealingLR |
| Hidden test labels | Not used |

After model selection, a fresh network is trained on all available labeled images. This increases the amount of supervised data available to the final challenge model.

---

## 8. Multi-view test-time augmentation

| TTA component | Current setting |
|---|---|
| Padding | 4 pixels, reflect mode |
| Translation views | 5 |
| Horizontal flip | Applied to every translated view |
| Total views per image | 10 |
| Combination | Mean of logits |
| Extra trainable parameters | 0 |

TTA improves prediction robustness without changing the architecture or violating the parameter constraint.

### Test prediction distribution

| Predicted class | Number of images |
|---:|---:|
| 0 | 504 |
| 1 | 445 |
| 2 | 516 |
| 3 | 488 |
| 4 | 547 |
| **Total** | **2,500** |

The distribution does not show an obvious collapse toward a single class.

---

## 9. Submission generation

| Requirement | Status |
|---|---|
| `predictions.csv` generated | PASS |
| Columns exactly `id,y_pred` | PASS |
| 2,500 unique test IDs | PASS |
| Predictions restricted to classes 0–4 | PASS |
| Test order matches sample submission | PASS |
| `ABLATIONS.md` included | PASS |
| ZIP contains only required files | PASS |

---

## Development history — approximately 25 attempts

This final notebook is the result of an iterative development process. I started with an early score of approximately **0.18** and made around **25 training/submission attempts**. I did not retain a reliable metric log for every individual attempt, so intermediate scores are intentionally not invented here.

| Development stage | Approx. attempt range | Main focus | Result |
|---|---:|---|---|
| Initial experiments | 1 | Basic CNN pipeline | Score around **0.18** |
| Architecture exploration | 2–8 | Channel sizes, activations and pooling | Progressive improvement |
| Generalization tuning | 9–14 | Normalization and augmentation | Better validation stability |
| Optimization tuning | 15–19 | AdamW, learning rate and regularization | More consistent convergence |
| Stability improvements | 20–23 | EMA, label smoothing and cosine scheduling | Smaller metric fluctuations |
| Final refinement | 24–25 | Full-data retraining and multi-view TTA | Current model: Acc **0.7990**, F1 **0.7989** |

The main lesson from these iterations is that the gain did not come from one isolated hyperparameter. The strongest result came from combining a compact architecture, moderate augmentation, stable optimization, EMA checkpointing, full-data retraining and test-time augmentation.

---

## Final conclusion

The current ImprovedCNN V2 provides the strongest result obtained during my approximately 25 iterations while staying within the challenge constraint of fewer than 95,000 trainable parameters. The validation results of **0.7990 accuracy** and **0.7989 macro F1** indicate strong and balanced classification performance.

Because this version already performs well, I would preserve it as the main submission rather than make aggressive architectural changes. Future experiments should be isolated and compared against this checkpoint instead of replacing it directly.
