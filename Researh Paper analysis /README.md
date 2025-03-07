# Moore Dataset Analysis

## Overview
This project is the replication of the research paper [IEEE Explore](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9583839&tag=1) on Moore Cross Dataset. It aims to extract insights and visualize key trends. The analysis involves data preprocessing, statistical modeling, and visualization.

## Table of Contents
- [1. Dataset Information](#1-dataset-information)
- [2. Data Combination](#2-data-combination)
- [3. Data Processing](#3-data-processing)
- [4. Setup Instructions](#4-setup-instructions)
- [5. Conclusion](#5-conclusion)

---

## 1. Dataset Information
- **Name:** Moore Dataset
- **Format:** BIDS format
- **Attributes:** Various features related to Moore’s analysis
- **Target Variable:** User (Participant)

## 2. Data Combination
- The script **`dataset_combination_script.py`** combines multiple `.tsv` files into a single dataset that consolidates session data from all users.

## 3. Data Processing
- The script **`VR_data_processing.py`** processes the combined dataset to extract 90-dimensional feature vectors.
- The 90-dimensional vectors are structured as follows:
  - **3 Devices**: Head, Left Hand, Right Hand
  - **6 Features per Device**: 3 Position Coordinates (X, Y, Z) + 3 Euler Rotations (X, Y, Z)
  - **5 Statistical Measures per Feature**: Max, Min, Median, Mean, Standard Deviation
  - **Total Dimensions**: 3 × 6 × 5 = **90**
- Data is processed in 1-second segments to capture meaningful patterns in user behavior.

## Processed Data Output
- The processed dataset is saved as **`processed_dataset(90-Features).csv`** in the `DataSets/` directory.
- Each row in this dataset represents a single second of VR tracking data transformed into a 90-dimensional feature vector.

## 4. Setup Instructions

## How to Use
1. **Combine Session Data**: Run `dataset_combination_script.py` to merge all `.tsv` session files. Dont foget to replacr your root directory path in the code.
2. **Process VR Data**: Run `VR_data_processing.py` to generate the 90-dimensional feature vectors.
3. **Our analysis** based on the processed dataset is stated in the `Moore_Dataset_Analysis.ipynb` for all three models.
## 5. Conclusion

## Model Evaluation Results

### Moore et al. method #1 (position info, K-Nearest Neighbour)
**Train-Test Split:**
- Trained on the training set and tested on training set  
  - Learning: Our (92.33%) vs Theirs (80.42%)
- Trained on the retention set and tested on retention set  
  - Retention: Our (88.78%) vs Theirs (89.42%)

**Notes:**
- Substantial improvement in learning session (+11.91%)
- Minimal decline in retention session (-0.64%)
- Used same feature normalization (M=0, SD=1)
- Performance gap suggests our implementation may handle training data better

**Evaluation:**
- I used normal accuracy to evaluate the performance of the model
- Our model demonstrates excellent learning capacity with significantly higher accuracy during training.
- The slight retention drop indicates good generalization with minimal overfitting concerns.

---

## Moore et al. method #1 (position info, Random Forest)
**Train-Test Split:**
- Trained on the training set and tested on training set  
  - Learning: Our (95.89%) vs Theirs (89.33%)
- Trained on the retention set and tested on retention set  
  - Retention: Our (94.00%) vs Theirs (95.50%)

**Notes:**
- Considerable improvement in learning session (+6.56%)
- Slight decrease in retention session (-1.50%)
- Used 100 estimators with scikit-learn defaults.
- Applied 20 Monte-Carlo cross-validations within session data.

**Evaluation:**
- I used normal accuracy to evaluate the performance of the model
- Our RF implementation shows excellent training performance with strong generalization capability.
- High overall accuracy makes this a reliable identification method.

---

## Moore et al. method #1 (position info, Gradient Boosting Model)
**Train-Test Split:**
- Trained on the training set and tested on training set  
  - Learning: Our (95.56%) vs Theirs (90.83%)
- Trained on the retention set and tested on retention set  
  - Retention: Our (93.33%) vs Theirs (95.83%)

**Notes:**
- Notable improvement in learning session (+4.73%)
- More pronounced decrease in retention session (-2.50%)
- Trained on only 1 Monte-Carlo cross-validation within session data
- Performed sub session-level plurality voting

**Evaluation:**
- Our GBM implementation shows strong learning capabilities but the largest retention gap among all methods.
- This suggests some potential overfitting despite excellent training accuracy.

---
## **Contributors**
- **Atharv Patil** - Data Analysis & Visualization

## References
- Original Research Paper: ["Analyzing User Behavior in Virtual Reality Using Machine Learning"](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=9583839&tag=1)

---
🚀 **This project enables efficient VR data processing for behavioral analysis and machine learning applications.**

