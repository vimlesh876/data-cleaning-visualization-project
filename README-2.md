# 🧹 Data Cleaning & Visualization Project

Raw retail sales dataset ko clean karke usse insights nikalne wala Python project.

## 📌 Project Overview
Is project mein ek raw dataset ko process kiya gaya hai:
- Missing values handle karna
- Duplicate rows remove karna
- Outliers detect aur cap karna
- Pandas, Matplotlib, Seaborn se visual dashboard banana

## 📂 Folder Structure
```
data-cleaning-project/
│
├── data/
│   └── raw_sales_data.csv        # original dirty dataset
│
├── outputs/
│   ├── cleaned_sales_data.csv    # cleaned dataset
│   ├── dashboard.png             # visual dashboard (6 charts)
│   └── summary_report.txt        # text summary of key findings
│
├── clean_and_visualize.py        # main script
└── README.md
```

## 🔑 Key Features
- Missing values ko column-wise smart logic se fill kiya gaya (median/mode/"Unknown")
- Duplicate rows detect aur remove kiye gaye
- IQR method se price outliers cap kiye gaye, aur unrealistic ages filter ki gayi
- 6-panel dashboard: Revenue by Category/Region, Price distribution, Monthly trend, Rating distribution, Age vs Revenue

## 📊 Expected Outcome
Data preprocessing, visualization aur data storytelling seekhna.

## ▶️ How to Run
```bash
pip install pandas matplotlib seaborn
python clean_and_visualize.py
```
Output `outputs/` folder mein save ho jayega.

## 🛠️ Tech Stack
- Python
- Pandas
- Matplotlib
- Seaborn
