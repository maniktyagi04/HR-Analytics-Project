import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# -------------------------------
# Theme
# -------------------------------

C = {
'primary':'#1B3A6B',
'accent':'#E84855',
'safe':'#2ECC71',
'warn':'#F39C12'
}

plt.rcParams.update({
'axes.spines.top':False,
'axes.spines.right':False,
'axes.titleweight':'bold'
})

# -------------------------------
# Load Cleaned Dataset
# -------------------------------

df = pd.read_csv('../data/processed/hr_cleaned.csv')


# -------------------------------
# Create Tableau Ready File
# -------------------------------

tableau = df.copy()

tableau.rename(columns={
'target':'Job_Change_Intent',
'experience_band':'Experience_Band',
'city_tier':'City_Tier',
'education_level':'Education_Level',
'company_size':'Company_Size',
'experience_num':'Experience_Years',
'training_hours':'Training_Hours'
}, inplace=True)

tableau.to_csv(
'../data/processed/hr_tableau_ready.csv',
index=False
)

print("hr_tableau_ready.csv exported successfully")


# -------------------------------
# KPI + Dashboard Validation
# -------------------------------

fig, axes = plt.subplots(
2,4,
figsize=(22,10)
)

axes = axes.flatten()


# ===============================
# KPI 1 Attrition Rate
# ===============================

attrition = tableau['Job_Change_Intent'].mean()*100

axes[0].text(
0.5,
0.5,
f'{attrition:.1f}%',
fontsize=34,
fontweight='bold',
ha='center'
)

axes[0].set_title('Attrition Rate')
axes[0].axis('off')


# ===============================
# KPI 2 Average Experience
# ===============================

avg_exp = tableau['Experience_Years'].mean()

axes[1].text(
0.5,
0.5,
f'{avg_exp:.1f} yrs',
fontsize=30,
fontweight='bold',
ha='center'
)

axes[1].set_title('Avg Experience')
axes[1].axis('off')


# ===============================
# KPI 3 Avg Training Hours
# ===============================

avg_train = tableau['Training_Hours'].mean()

axes[2].text(
0.5,
0.5,
f'{avg_train:.1f}',
fontsize=30,
fontweight='bold',
ha='center'
)

axes[2].set_title('Avg Training Hours')
axes[2].axis('off')


# ===============================
# Dashboard Title Block
# ===============================

axes[3].axis('off')

axes[3].text(
0.5,
0.6,
'Pre-Tableau\nValidation Dashboard',
ha='center',
fontsize=18,
fontweight='bold'
)


# ===============================
# Chart 1 Attrition by Experience
# ===============================

exp_attr = (
tableau.groupby(
'Experience_Band'
)['Job_Change_Intent']
.mean()*100
)

axes[4].bar(
exp_attr.index,
exp_attr.values,
color=C['primary']
)

for i,v in enumerate(exp_attr.values):
    axes[4].text(
        i,
        v+0.5,
        f'{v:.1f}%'
    )

axes[4].set_title(
'Attrition by Experience Band'
)

axes[4].set_ylabel('Attrition %')


# ===============================
# Chart 2 Education Distribution
# ===============================

edu = pd.crosstab(
tableau['Education_Level'],
tableau['Job_Change_Intent']
)

edu.plot(
kind='bar',
stacked=True,
ax=axes[5],
color=[C['safe'],C['accent']]
)

axes[5].set_title(
'Education Level Distribution'
)


# ===============================
# Chart 3 City Tier vs Attrition
# ===============================

city_attr = (
tableau.groupby(
'City_Tier'
)['Job_Change_Intent']
.mean()*100
)

axes[6].bar(
city_attr.index,
city_attr.values,
color=C['warn']
)

for i,v in enumerate(city_attr.values):
    axes[6].text(
        i,
        v+.5,
        f'{v:.1f}%'
    )

axes[6].set_title(
'City Tier vs Attrition'
)

axes[6].set_ylabel('Attrition %')


# ===============================
# Chart 4 Heatmap
# ===============================

pivot = (
tableau.pivot_table(
values='Job_Change_Intent',
index='Education_Level',
columns='Company_Size',
aggfunc='mean'
)*100
)

sns.heatmap(
pivot,
annot=True,
fmt='.1f',
cmap='YlOrRd',
ax=axes[7]
)

axes[7].set_title(
'Education vs Company Size Attrition'
)


# -------------------------------
# Final Save
# -------------------------------

plt.suptitle(
'HR Analytics KPI Validation Dashboard',
fontsize=18,
fontweight='bold'
)

plt.tight_layout()

plt.savefig(
'../data/processed/dashboard_validation.png',
dpi=150,
bbox_inches='tight'
)

plt.show()


# -------------------------------
# Final Data Quality Check
# -------------------------------

print("="*50)
print("FINAL CHECK")
print("="*50)

print(f"Rows: {len(tableau)}")
print(f"Columns: {len(tableau.columns)}")
print(f"Null Values: {tableau.isnull().sum().sum()}")
print(f"Attrition Rate: {attrition:.2f}%")
print(f"Avg Experience: {avg_exp:.1f}")
print(f"Avg Training Hours: {avg_train:.1f}")

print("="*50)
print("NB05 COMPLETE")
print("Import in Tableau -> Connect -> Text File -> hr_tableau_ready.csv")