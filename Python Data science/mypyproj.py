import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


file = r"C:\Users\PREDATOR\OneDrive\Documents\python_data\mypyproj.xlsx"  
df = pd.read_excel(file, sheet_name='C-08ST')


df_cleaned = df[4:].copy()
df_cleaned.columns = df.iloc[3]
df_cleaned.reset_index(drop=True, inplace=True)


df_cleaned.columns = ['Table Name', 'State Code', 'District Code', 'Area Name',
                      'T/R/U','Age-group', 'Population', 'Male', 'Female']

df_cleaned['Population'] = pd.to_numeric(df_cleaned['Population'], errors='coerce')
df_cleaned['Male'] = pd.to_numeric(df_cleaned['Male'], errors='coerce')
df_cleaned['Female'] = pd.to_numeric(df_cleaned['Female'], errors='coerce')


print("Data type of Population:", type(df_cleaned['Population'][0]))


def categorize_population(pop):
    if pd.isna(pop):
        return 'Unknown'
    elif pop > 5_00_000:
        return 'High'
    elif pop > 100_000:
        return 'Medium'
    else:
        return 'Low'

df_cleaned['Population Group'] = df_cleaned['Population'].apply(categorize_population)


def gender_ratio(male, female):
    if pd.isna(male) or pd.isna(female) or (male + female) == 0:
        return None
    return round((female / (male + female)) * 1000, 2)

df_cleaned['Gender Ratio (F/1000M)'] = df_cleaned.apply(
    lambda row: gender_ratio(row['Male'], row['Female']), axis=1
)


population_array = np.array(df_cleaned['Population'].dropna())


print("Mean Population:", np.mean(population_array))


urban_data = df_cleaned[df_cleaned['T/R/U'] == 'Urban']
rural_data = df_cleaned[df_cleaned['T/R/U'] == 'Rural']


print("Missing values:\n", df_cleaned.isnull().sum())


top_castes = df_cleaned.groupby('Age-group')['Population'].sum().sort_values(ascending=False).head(10)
top_castes.plot(kind='barh', color='skyblue')
plt.title("Top 10 Schedule Age-group by Population")
plt.xlabel("Population")
plt.ylabel("Age-group")
plt.tight_layout()
plt.show()


plt.figure(figsize=(10, 5))
sns.boxplot(data=df_cleaned[['Population', 'Male', 'Female']],
            palette={'Population': 'skyblue', 'Male': 'lightgreen', 'Female': 'salmon'})
plt.title("Boxplot of Population Data")
plt.show()



plt.figure(figsize=(8, 6))
sns.heatmap(df_cleaned[['Population', 'Male', 'Female']].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.show()



sns.histplot(df_cleaned['Gender Ratio (F/1000M)'].dropna(), kde=True, color='green')
plt.title("Distribution of Gender Ratio")
plt.xlabel("Gender Ratio (F/1000M)")
plt.show()


df_plot = df_cleaned.dropna(subset=['Male', 'Female', 'Age-group']).copy()
df_plot['Age-group'] = df_plot['Age-group'].astype(str)
# Plot
plt.figure(figsize=(12, 6))
sns.scatterplot(data=df_plot, x='Male', y='Female', hue='Age-group', palette='tab10', s=60)
plt.title("Male vs Female Population by Age-group")
plt.xlabel("Male Population")
plt.ylabel("Female Population")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()



sns.scatterplot(data=df_cleaned, x='Male', y='Female', hue='T/R/U')
plt.title("Male vs Female Population by Region Type")
plt.xlabel("Male")
plt.ylabel("Female")
plt.show()





print(df_cleaned[['Population', 'Male', 'Female']].describe())


print("Correlation Matrix:")
print(df_cleaned[['Population', 'Male', 'Female']].corr())


print("Covariance Matrix:")
print(df_cleaned[['Population', 'Male', 'Female']].cov())


z_scores = np.abs(stats.zscore(df_cleaned[['Population', 'Male', 'Female']].dropna()))
outliers = (z_scores > 3)
print("Outlier Rows Detected:", outliers.any(axis=1).sum())


print("Mean Female Population:", df_cleaned['Female'].mean())
print("Standard Deviation:", df_cleaned['Female'].std())


urban_female = df_cleaned[df_cleaned['T/R/U'] == 'Urban']['Female'].dropna()
rural_female = df_cleaned[df_cleaned['T/R/U'] == 'Rural']['Female'].dropna()
t_stat, p_val = stats.ttest_ind(urban_female, rural_female, equal_var=False)
print("T-test Result — t-stat:", t_stat, "p-value:", p_val)


gender_table = pd.crosstab(df_cleaned['T/R/U'], df_cleaned['Population Group'])
chi2_stat, p, dof, expected = stats.chi2_contingency(gender_table)
print("Chi-Squared Test — χ²:", chi2_stat, "p-value:", p)



region_summary = df_cleaned.groupby('T/R/U')[['Population', 'Male', 'Female']].mean()
print("Urban vs Rural Mean Comparison:\n", region_summary)


region_counts = df_cleaned['T/R/U'].value_counts()
region_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=['orange', 'lightblue', 'green'])
plt.title("Region Type Distribution")
plt.ylabel('')
plt.show()



sns.violinplot(x='T/R/U', y='Female', data=df_cleaned)
plt.title("Distribution of Female Population by Region Type")
plt.show()


sns.violinplot(x='T/R/U', y='Male', data=df_cleaned)
plt.title("Distribution of Female Population by Region Type")
plt.show()








