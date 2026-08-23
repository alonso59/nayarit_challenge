# Ablation Experiments Report - CNN Challenge

## Experiment 1: Lightweight Baseline Architecture
* **Objective:** Establish a baseline with very few parameters using Global Average Pooling and Dropout.
* **Changes made:** 
  * Designed a 3-convolutional-block CNN.
  * Added BatchNorm after each convolution.
  * Replaced the traditional Flatten layer with AdaptiveAvgPool2d (Global Average Pooling).
  * Set 20 epochs instead of 5.
* **Expected result:** Achieve a decent Accuracy using very few parameters, ensuring maximum efficiency score.
* **Actual results:** Train Acc 64.77% | Val Acc 58.87%. The model learns well but the accuracy is still low. The 6% gap indicates decent generalization, but it lacks capacity or data variety to improve its metrics.

## Experiment 2: Capacity Increase (Wider Network)
* **Objective:** Give the model more learning capacity, as the training accuracy from Exp 1 (64%) indicates potential underfitting.
* **Changes made:** Doubled the number of filters in all convolutional layers (from 16-32-64 to 32-64-128). Kept Global Average Pooling to avoid blowing up the dense layer parameters.
* **Actual results:** Train Acc 72.58% | Val Acc 66.43%. The hypothesis was correct: increasing filters allowed better capture of data features, achieving a ~7.5% increase in the validation metric while maintaining a healthy generalization gap.

## Experiment 3: Data Augmentation
* **Objective:** Prevent overfitting and force the model to learn more robust features (spatial and illumination invariance).
* **Changes made:** In `src/augmentations.py`, added `RandomHorizontalFlip` (p=0.5), `RandomRotation` (15 degrees), and `ColorJitter` (0.2). Kept the "wide" architecture and 20 epochs.
* **Actual results:** Train Acc 65.94% | Val Acc 62.21%. Metrics dropped compared to Exp 2. Introducing Data Augmentation made the learning task more complex, and the model didn't fully converge in just 20 epochs.

## Experiment 4: Increased Epochs
* **Objective:** Give the model time to converge now that the dataset is more complex due to Data Augmentation.
* **Changes made:** Increased epochs from 20 to 50 in `config.yaml`.
* **Actual results:** Train Acc 70.98% | Val Acc 63.26%. Training for more epochs helped recover performance compared to Exp 3, but did not surpass Exp 2 (66.43%). Decided to stop iterating due to diminishing returns and use the Experiment 2 checkpoint for the final submission, prioritizing the efficiency score (model with few parameters).

Note: This file logs our Ablation Experiments.