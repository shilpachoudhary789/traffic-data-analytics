#                    traffic analysis project

# importing necessary libraries
import pandas as pd
import numpy as np

traffic = pd.read_csv(r"C:/Users/hp/Downloads/Project_284/Project_284/Traffic_Volume_Log.csv")
signals = pd.read_csv(r"C:/Users/hp/Downloads/Project_284/Project_284/Signal_Timing_Config.csv")
pt_delay = pd.read_csv(r"C:/Users/hp/Downloads/Project_284/Project_284/Public_Transport_Delay_Log.csv")


#   eda 
#traffic data set 

# first moment business decision

traffic['vehicle_count_total'].mean() # output 11.204
traffic['vehicle_count_total'].median() # output 9.0

# mode 

print("mode for intersection name :", traffic.intersection_name.mode()[0])
print("mode for zone :", traffic.zone.mode()[0])
print("mode for vehicle type :", traffic.vehicle_type.mode()[0])

'''Intersection (Mode) → Ameerpet Junction → most common intersection in dataset.
Zone (Mode) → Hyderabad → most frequent traffic zone.
Vehicle Type (Mode) → 2W → two-wheelers are the most common vehicles.'''

# second moment business decision

traffic['vehicle_count_total'].std() #output 6.25
traffic['vehicle_count_total'].var() # output 39.09

# third moment business decision
 
traffic['vehicle_count_total'].skew() #output 1.022

#fourth moment business decision

traffic['vehicle_count_total'].kurt() #output 0.208

'''
Mean → 11.20 → average traffic count.
Median → 9.0 → typical value.
Std Dev → 6.25 → moderate spread.
Variance → 39.09 → spread measure.
Skewness → 1.02 → positively skewed (few high traffic values pull right).
Kurtosis → 0.21 → light-tailed, few extreme peaks.
'''

# transport delay log data set

# first moment business decision

pt_delay['delay_minutes'].mean() #output 5.14
pt_delay['delay_minutes'].median() # output 5.07

# top delay reasons

pt_delay["delay_reason"].value_counts().head()

# second moment business decision

pt_delay['delay_minutes'].std() #output 2.85
pt_delay['delay_minutes'].var() #output 8.13

# third moment business decision

pt_delay['delay_minutes'].skew() # output 0.25

# fourth moment business decision

pt_delay['delay_minutes'].kurt() # output -0.21

'''Mean → 5.15 min
Median → 5.07 min → close to mean → symmetric distribution
Mode (Reason) → “Other” most common cause (772), then Traffic (769)
Std Dev → 2.85 → moderate spread
Variance → 8.14 → spread measure
Skewness → 0.25 → slight right skew
Kurtosis → –0.21 → light tails (fewer extremes)'''


# graphical representation

# traffic data set

# importing necessary libraries
import matplotlib.pyplot as plt
import seaborn as sns

# hourly traffic

traffic['hour'] = traffic['timestamp_utc'].dt.hour # get hour details from time stamp

plt.figure(figsize = (8,4))
sns.lineplot(x = "hour", y = "vehicle_count_total", data = traffic, estimator = "mean")
#estimator aggregates the values into one for plotting
plt.title(" average traffic volume by hour")
plt.xlabel("hour of the day")
plt.ylabel("average behicle count")
plt.show()

''' Traffic volume peaks sharply during 8–10 AM and 5–8 PM, 
showing clear morning and evening rush hours. '''
    
# weekday vs weekend

# weekday column creation
traffic['weekday'] = traffic['timestamp_utc'].dt.day_name()

traffic['is_weekend'] = traffic['weekday'].isin(['Saturday','Sunday'])
plt.figure(figsize = (6,4))
sns.boxplot(x = "is_weekend", y = "vehicle_count_total", data = traffic)
plt.title("traffic : weekday vs weekend")
plt.show()

''' Weekday and weekend traffic volumes are almost similar, 
though both show outliers with occasional very high vehicle counts.'''

# peak vs non peak

plt.figure(figsize = (6,4))
sns.boxplot(x = "is_peak_hour", y = "vehicle_count_total", data = traffic)
plt.title("traffic : peak vs non peak hours")
plt.show()

''' Traffic is much higher during peak hours compared
 to non-peak, with median vehicle counts nearly double. '''

# Vehicle type 
plt.figure(figsize=(6,4))
sns.barplot(x="vehicle_type", y="vehicle_count_total", data=traffic, estimator="mean")
plt.title("Avg Traffic Volume by Vehicle Type")
plt.show()

'''Buses, 2-wheelers, and trucks dominate average traffic volume, 
while bicycles contribute the least.'''

#  Zone-wise 
plt.figure(figsize=(8,4))
sns.barplot(x="zone", y="vehicle_count_total", data=traffic, estimator="mean")
plt.title("Traffic Volume by Zone")
plt.xticks(rotation=45)
plt.show()

''' Traffic volumes across Medchal, Hyderabad, and Rangareddy 
are almost equal, showing no major zone-specific differences..'''

# Top 10 busiest intersections 
top_int = traffic.groupby("intersection_name")["vehicle_count_total"].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(10,4))
top_int.plot(kind="bar")
plt.title("Top 10 Busiest Intersections")
plt.show()

''' Dilsukhnagar Junction records the highest average traffic, 
but all top 10 intersections show heavy volumes with only small differences. '''

# Signals Dataset

plt.figure(figsize=(6,4))
sns.barplot(x = "signal_phase", y = "duration_sec", data = signals, estimator = "mean")
plt.title("Signal Durations by Phase")
plt.show()

''' Red signals last the longest (~90s), much higher than green (~60s) 
and yellow (~5s), leading to longer waiting times than movement periods. '''

# Public Transport Delay Dataset

#  Histogram of delays
 plt.figure(figsize=(6,4))
sns.histplot(pt_delay["delay_minutes"], bins=20, kde=True)
plt.title("Distribution of Bus Delays (Minutes)")
plt.xlabel("Delay (minutes)")
plt.ylabel("Frequency")
plt.show()

''' Most bus delays fall between 3–7 minutes, with a peak around 
5 minutes; very long delays (10+ mins) are rare.'''

#  Boxplot of delays
plt.figure(figsize=(6,4))
sns.boxplot(y=pt_delay["delay_minutes"])
plt.title("Bus Delay Minutes - Boxplot")
plt.show()

''' Bus delays have a median of ~5 minutes, with most delays between 
3–7 minutes; a few cases exceed 12 minutes as outliers.'''

#  Delay reasons 
plt.figure(figsize=(8,4))
sns.barplot(x="delay_reason", y="delay_minutes", data=pt_delay, estimator="mean")
plt.title("Average Delay Minutes by Reason")
plt.xticks(rotation=45)
plt.show()

''' Average delays are quite similar across reasons (~5 minutes), 
with weather-related delays slightly higher than others'''

#  Count of delay reasons 
plt.figure(figsize=(8,4))
sns.countplot(x="delay_reason", data=pt_delay, order=pt_delay["delay_reason"].value_counts().index)
plt.title("Frequency of Delay Reasons")
plt.xticks(rotation=45)
plt.show()

'''The most frequent causes of bus delays are Other and Traffic,
 while Breakdowns are the least common.'''

# Copy traffic dataset
traffic_encoded = traffic.copy()

# Encoding categorical columns
from sklearn.preprocessing import LabelEncoder

# Initialize LabelEncoder
le = LabelEncoder()

traffic_encoded['zone'] = le.fit_transform(traffic_encoded['zone'])
traffic_encoded['vehicle_type'] = le.fit_transform(traffic_encoded['vehicle_type'])
traffic_encoded['is_weekend'] = traffic_encoded['is_weekend'].astype(int)
traffic_encoded['is_peak_hour'] = traffic_encoded['is_peak_hour'].astype(int)

# Correlation matrix
corr = traffic_encoded.corr(numeric_only=True)

# Heatmap
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.show()

'''Vehicle count is strongly correlated with peak hours (0.85),
confirming that congestion is mainly driven by rush hour timings, 
while weekend/zone effects are minimal.'''

# line plot

# Extract day of week 
traffic['day_of_week'] = traffic['date'].dt.day_name()

# Group by day
avg_by_day = traffic.groupby('day_of_week')['vehicle_count_total'].mean().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
)

plt.figure(figsize=(8,5))
sns.lineplot(x=avg_by_day.index, y=avg_by_day.values, marker="o")
plt.title("Average Traffic Volume by Day of Week")
plt.ylabel("Average Vehicle Count")
plt.xlabel("Day of the Week")
plt.show()

'''Traffic is slightly higher on weekdays, with Friday showing the peak, 
while weekends (especially Saturday) record lower volumes.'''

# data preprocessing

# type casting
#traffic volume log data set
traffic.dtypes
#changing the data type
traffic = traffic.astype({'record_id':'string','intersection_id':'string',
                          'intersection_name':'string','zone':'string',
                          'vehicle_type':'string'})
traffic['timestamp_utc'] = pd.to_datetime(traffic['timestamp_utc'])
traffic['date'] = pd.to_datetime(traffic['date'])
traffic.info()

#signal timming config data set
signals.dtypes
signals = signals.astype({'config_id':'string','intersection_id':'string',
                          'signal_phase':'string'})
signals['effective_start_ts'] = pd.to_datetime(signals['effective_start_ts'])
signals['effective_end_ts'] = pd.to_datetime(signals['effective_end_ts'])
signals.info()

#public_transport delay data set
pt_delay.dtypes
pt_delay = pt_delay.astype({'delay_id':'string','route_id':'string','bus_id':'string',
                            'intersection_id':'string','stop_id':'string',
                            'delay_reason':'string'})
datetime_col = ['scheduled_arrival_ts','actual_arrival_ts','date']
for col in datetime_col:
    pt_delay[col] = pd.to_datetime(pt_delay[col])
pt_delay.info()


#removing duplicates
duplicate = traffic.duplicated() #finding duplicates and storing them as booleans
sum(duplicate) # gets the count of duplicates
# there are no duplicates
duplicate = signals.duplicated()
sum(duplicate)
# no duplicates
duplicate = pt_delay.duplicated()
sum(duplicate)
# no duplicates


# missing values / null values
# there are no null values


#outlier treatment
# outlier treatment on numerical columns
import seaborn as sns

# traffic volume log
sns.boxplot(traffic.vehicle_count_total)
# there are outliers

IQR = traffic['vehicle_count_total'].quantile(0.75) - traffic['vehicle_count_total'].quantile(0.25)

# Calculating the lower and upper limits for outlier detection based on IQR
lower_limit = traffic['vehicle_count_total'].quantile(0.25) - (IQR * 1.5)
upper_limit = traffic['vehicle_count_total'].quantile(0.75) + (IQR * 1.5)

# each value is outlier or not
outliers_df = np.where(traffic['vehicle_count_total'] > upper_limit, True, np.where(traffic['vehicle_count_total'] < lower_limit, True, False))

traffic['is outlier'] = outliers_df

traffic['is outlier'].sum()
#there are 37 outliers

#winsorization method for outliers
from feature_engine.outliers import Winsorizer
winsor_iqr = Winsorizer(capping_method = 'iqr', 
                        tail = 'both', 
                        fold = 1.5, 
                        variables = ['vehicle_count_total'])

# Fitting the Winsorizer model to the vehicle count column and transforming the data
tf = winsor_iqr.fit_transform(traffic[['vehicle_count_total']])

sns.boxplot(tf.vehicle_count_total) #no more outliers
traffic['vehicle count after outlier treatment'] = tf['vehicle_count_total']


#signal timming congif
sns.boxplot(signals.duration_sec)
# no outliers

#public transport delay log
sns.boxplot(pt_delay.delay_minutes)
#there are outliers

IQR = pt_delay['delay_minutes'].quantile(0.75) - pt_delay['delay_minutes'].quantile(0.25)

# Calculating the lower and upper limits for outlier detection based on IQR
lower_limit = pt_delay['delay_minutes'].quantile(0.25) - (IQR * 1.5)
upper_limit = pt_delay['delay_minutes'].quantile(0.75) + (IQR * 1.5)

# each value is outlier or not
outliers_df = np.where(pt_delay['delay_minutes'] > upper_limit, True, np.where(pt_delay['delay_minutes'] < lower_limit, True, False))

pt_delay['is outlier'] = outliers_df

pt_delay['is outlier'].sum()
#there are 13 outliers

#winsorization method for outliers
from feature_engine.outliers import Winsorizer
winsor_iqr = Winsorizer(capping_method = 'iqr', 
                        tail = 'both', 
                        fold = 1.5, 
                        variables = ['delay_minutes'])

# Fitting the Winsorizer model to the delay minutes column and transforming the data
ptd = winsor_iqr.fit_transform(pt_delay[['delay_minutes']])

sns.boxplot(ptd.delay_minutes) #no more outliers

pt_delay['delay minutes after outlier treatment'] = ptd['delay_minutes']












