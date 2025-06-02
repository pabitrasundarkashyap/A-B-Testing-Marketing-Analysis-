import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=pd.read_csv(r'C:\Users\Pabitra\Desktop\Technical Skils\Python\Jyputer\Data\marketing_AB.csv')
data.head()

data.shape
###Check Data types
print('-------------------Check Data types-------------------')
data.info()
#Counts unique data for each column
print('-------------------Counts unique data for each column-------------------')
print(data.nunique())
#Counts unique catergories for a column
print('-------------------Counts unique catergories for a column-------------------')
print(data['test group'].value_counts())
#Check Description
data.describe(include='all')

##Missing Value 
data.isnull().sum()

def filter_outliers(df,whisker=1.5):
    q1=df.quantile(0.25)
    q3=df.quantile(0.75)
    IQR=q3-q1
    #Define the lower bound and upper bound for non-outliers
    lower_bound=q1 - whisker*IQR
    upper_bound=q3 + whisker*IQR

    is_outlier=df[(df<lower_bound)|(df>upper_bound)]
    no_outlier=df[(df>lower_bound) & (df<upper_bound)]
    return is_outlier,no_outlier
    
outliers,no_outlier=filter_outliers(data['total ads'])
#outliers=pd.DataFrame(outliers)
#(outliers.index)
#print(no_outlier)
print(f"Outliers: {len(outliers)}")
print(f"No_outliers :{len(no_outlier)}")
print(f"Total records: {len(data)}")
print(f"Percentage of outliers: {(len(outliers)/len(data)*100)}")


outliers_df=data[data.index.isin(outliers.index)]
outliers_df
#sns.boxplot(outliers_df,x='test group',y='total ads')

#--------------No Outliers Data-------------
no_outliers_df=data[data.index.isin(no_outlier.index)]
sns.boxplot(no_outliers_df,x='test group',y='total ads')
plt.title("Total Ads seen by Test Group")
plt.xlabel("Test Group")
plt.ylabel("Total Ads")
plt.show()



#Calculate average seen ads
no_outliers_df_mean=no_outliers_df['total ads'].mean()
print(f"No_Outliers Avergae seen Ads : {no_outliers_df_mean:.2f}")

Overall_df_mean=data['total ads'].mean()
print(f"Overall Avergae seen Ads : {Overall_df_mean:.2f}")

#Average Conversion Rate
print("-------------Overall Outlayers--------------")
overall_df_conversion=data.groupby(['test group'])['converted'].value_counts(normalize=True)
#overall_df_conversion=data.groupby(['test group','converted']).agg({'converted':'count','converted':''})#.value_counts(normalize=True)
overall_df_conversion=pd.DataFrame(overall_df_conversion)

overall_df_conversion['proportion']=(overall_df_conversion['proportion']*100).round(2)
print(overall_df_conversion)
result_overall=overall_df_conversion.loc[('ad',True),'proportion']-overall_df_conversion.loc[('psa',True),'proportion']
print(f"Uplift : {result_overall:.2f}")

ad_converted = data[data['test group'] == 'ad']['converted'].sum()
ad_total = data[data['test group'] == 'ad'].shape[0]

psa_converted = data[data['test group'] == 'psa']['converted'].sum()
psa_total = data[data['test group'] == 'psa'].shape[0]

#Average Conversion Rate
print("-------------Without Outlayers--------------")
no_outliers_df_conversion=no_outliers_df.groupby(['test group'])['converted'].value_counts(normalize=True)
no_outliers_df_conversion=pd.DataFrame(no_outliers_df_conversion)
no_outliers_df_conversion['proportion']=(no_outliers_df_conversion['proportion']*100).round(2)
print(no_outliers_df_conversion)
result_no_outliers=no_outliers_df_conversion.loc[('ad',True),'proportion']-no_outliers_df_conversion.loc[('psa',True),'proportion']
print(f"Uplift : {result_no_outliers:.2f}")

#Average Conversion Rate
print("------------- Outlayers--------------")
outliers_df_conversion=outliers_df.groupby(['test group'])['converted'].value_counts(normalize=True)
outliers_df_conversion=pd.DataFrame(outliers_df_conversion)
outliers_df_conversion['proportion']=(outliers_df_conversion['proportion']*100).round(2)
print(outliers_df_conversion)


#Null Hypothesis  (H0): the conversion rate of ad group (experimental group) is equal to the conversion rate of PSA group (control group).
#Alternative Hypothesis  (H1): The conversion rate in the ad group is higher than in the PSA group  


from statsmodels.stats.proportion import proportions_ztest
# Z-test for proportions
ad_count = [ad_converted, psa_converted]
print(ad_count)
ad_nobs = [ad_total, psa_total]
print(ad_nobs)

z_stat, p_value = proportions_ztest(ad_count, ad_nobs, alternative='larger')

print(f"Z-statistic: {z_stat:.5f}")
print(f"P-value: {p_value:.5f}")


##The p-value is far below 0.05, so we reject the null hypothesis. 
##There is strong statistical evidence that the ad_group had a higher conversion rate than the PSA group. Therefore, the uplift is real and statistically significant.
