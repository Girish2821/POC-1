import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Plot style for better view
sns.set_style("whitegrid")

# 1. Data Loading into Python
try:
    df = pd.read_csv('C:\\Users\\Girish\\Downloads\\Freight\\freight.csv')
    print("Data Loaded Successfully")
except FileNotFoundError:
    print("Error: File not found.Please ensure file is present")
    exit()

# 2. Data cleaning and preparations
# Drop rows where Shipment Delay, Delivery Status, Actual Shipment Time, Planner Time of Travel are NaN

initial_rows = len(df)
df_cleaned = df.dropna(subset=['Shipment_Delay','Delivery_Status','Actual_Shipment_Time',"Planned_TimeofTravel"]).copy()
cleaned_rows = len(df_cleaned)

print(f"Initial Rows : {initial_rows}")
print(f"Rows after dropping NaNs in key column : {cleaned_rows}")
print(f"Number of rows dropped : {initial_rows - cleaned_rows}")

# Making Delivery Status of type Integer, this makes things easier in terms of understanding and also clearer interpretation
df_cleaned['Delivery_Status'] = df_cleaned['Delivery_Status'].astype(int)


#----- Shipment Volume Analysis--------
print("-------Shipment Volume --------- \n")

#Overall Shipment Volume
total_shipments = len(df_cleaned)
print(f"Total Shipments Analyzed : {total_shipments}\n")

#Shipment Volume by Carrier
print("Shipment Volumne by Carrier :\n")
carrier_volume = df_cleaned['Carrier_Name'].value_counts().reset_index() #converting a series into DataFrame
carrier_volume.columns = ['Carrier_Name','Shipment_Count']
print(carrier_volume.to_markdown(index=False, numalign="left", stralign="left")) # This gives you a console / terminal aligned.
print("\n")

# Top 10 Busiest Routes (Source-to-destination)
print("Top 10 Busiest Routes (Source - to- Destination) ")
busiest_routes = df_cleaned.groupby(['Source','Destination']).size().reset_index(name='Shipment_Count')
busiest_routes = busiest_routes.sort_values(by='Shipment_Count',ascending=False).head(10)
print(busiest_routes.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")

# Shipment Volume by Day of Week
print("Shipment Volume by Day of Week (1 = Monday, 7 = Sunday) : \n")
dayofweek_volume = df_cleaned['DayOfWeek'].value_counts().sort_index().reset_index()
dayofweek_volume.columns = ['DayOfWeek','Shipment_Count']
print(dayofweek_volume.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")

# Shipment Volume by Month
print("Shipment Volume by Month : \n")
month_volume = df_cleaned['Month'].value_counts().sort_index().reset_index()
month_volume.columns = ['Month','Shipment_Count']
print(month_volume.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")


# Delay Analysis
print("Delay Analysis : \n")

# Overall Average Delay
overall_avg_delay = df_cleaned['Shipment_Delay'].mean()
print(f"Overall Average Shipment Delay (minutes) : {overall_avg_delay:.2f}\n")

# On-Time Delivery (OTD) Rate
# 0 - On Time, 1 - Delayed
print("On-Time Delivery (OTD) Rate : \n")
delivery_status_counts = df_cleaned['Delivery_Status'].value_counts(normalize=True) * 100
otd_rate = delivery_status_counts.get(0,0) # Get percentage for 0 (On-Time), default to 0 if not present
delayed_rate = delivery_status_counts.get(1,0 )  # Get percentage for 1 (Delayed), default to 0 if not present

print(f"Percentage On-Time Deliveries : {otd_rate:.2f}%")
print(f"Percentage Delayed Deliveries : {delayed_rate:.2f}%\n")


# Average Delay by Carrier
print("Average Shipment Delay by Carrier : \n")
carrier_delay = df_cleaned.groupby('Carrier_Name')['Shipment_Delay'].mean().reset_index()
carrier_delay.columns = ['Carrier_Name','Average_Delay_Minutes']
carrier_delay = carrier_delay.sort_values(by="Average_Delay_Minutes",ascending=False).head(10)
carrier_delay['Average_Delay_Minutes'] = carrier_delay['Average_Delay_Minutes'].round(2)
print(carrier_delay.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")


# Top 10 routes which have Highest Average Delay
print("Top 10 Routes with Highest Average Delay : \n")
route_delay = df_cleaned.groupby(['Source','Destination'])['Shipment_Delay'].mean().reset_index()
route_delay.columns = ['Source','Destination','Average_Delay_Minutes']
route_delay = route_delay.sort_values(by="Average_Delay_Minutes",ascending=False).head(10)
route_delay['Average_Delay_Minutes'] = route_delay['Average_Delay_Minutes'].round(2)
print(route_delay.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")

# Average Delay by Day of the Week
print("Average Shipment Delay by Day of the Week (1= Monday, 7 = Sunday) : \n")
dayofweek_delay = df_cleaned.groupby('DayOfWeek')['Shipment_Delay'].mean().sort_index().reset_index()
dayofweek_delay.columns = ['DayOfWeek','Average_Delay_Minutes']
dayofweek_delay['Average_Delay_Minutes'] =dayofweek_delay['Average_Delay_Minutes'].round(2)
print(dayofweek_delay.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")

# Average Delay by Month
print("Average Shipment Dealy by Month : \n")
month_delay = df_cleaned.groupby('Month')['Shipment_Delay'].mean().sort_index().reset_index()
month_delay.columns = ['Month','Average_Delay_Minutes']
month_delay['Average_Delay_Minutes'] = month_delay['Average_Delay_Minutes'].round(2)
print(month_delay.to_markdown(index=False,numalign="left",stralign="left"))
print("\n")

# Graphical Plots

# Plot 1 : Shipment Volume by Carrier
carrier_volume = df_cleaned['Carrier_Name'].value_counts().reset_index()
carrier_volume.columns = ['Carrier_Name','Shipment_Count']
plt.figure(figsize=(12,6))
sns.barplot(x='Carrier_Name',y='Shipment_Count',data=carrier_volume,hue = 'Carrier_Name',palette='viridis',legend=False)
plt.title('Shipment Volume by Carrier',fontsize=12)
plt.xlabel('Carrier Name',fontsize=12)
plt.ylabel('Number of Shipment',fontsize=12)
plt.xticks(rotation=45,ha='right')
plt.tight_layout()
#plt.savefig('Shipment_volume_by_carrier.png')
#plt.close()
plt.show()

# Plot 2 : Shipment Volume by Week
dayofweek_volume = df_cleaned['DayOfWeek'].value_counts().sort_index().reset_index()
dayofweek_volume.columns = ['DayOfWeek','Shipment_Count']
plt.figure(figsize=(10,6))
sns.barplot(x='DayOfWeek',y='Shipment_Count',data=dayofweek_volume,hue='DayOfWeek',palette='cividis',legend=False)
plt.title('Shipment Volume by Day of Week', fontsize = 16)
plt.xlabel('Day of the Week (1 = Monday 7 = Sunday)', fontsize = 12)
plt.ylabel('Number of Shipments',fontsize=12)
plt.xticks(ticks=range(7),labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
plt.tight_layout()
#plt.savefig('Shipment_volume_by_dayofweek.png')
plt.show()
#plt.close()

# Plot 3 : Shipment by Month
month_volume = df_cleaned['Month'].value_counts().sort_index().reset_index()
month_volume.columns = ['Month','Shipment_Count']
plt.figure(figsize=(12,6))
sns.barplot(x='Month',y='Shipment_Count',data=month_volume,hue='Month',palette='plasma',legend=False)
plt.title('Shipment Volume by Month',fontsize = 16)
plt.xlabel('Month',fontsize=12)
plt.ylabel('Number of Shipments',fontsize=12)
plt.xticks(ticks=range(0,12),labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.tight_layout()
#plt.savefig('Shipments_Volume_Month.png')
plt.show()
#plt.close()

# Plot 4 : Average Shipment Dealy by Carrier
carrier_delay = df_cleaned.groupby('Carrier_Name')['Shipment_Delay'].mean().reset_index()
carrier_delay.columns = ['Carrier_Name','Average_Delay_Minutes']
carrier_delay = carrier_delay.sort_values(by='Average_Delay_Minutes',ascending=False)
plt.figure(figsize=(12,6))
sns.barplot(x='Carrier_Name',y='Average_Delay_Minutes',data=carrier_delay,hue='Carrier_Name',palette='rocket',legend=False)
plt.title('Average Shipment Delay by Carrier',fontsize=16)
plt.xlabel('Carrier Name',fontsize=12)
plt.ylabel('Average Delay (Minutes)',fontsize=-12)
plt.xticks(rotation=45,ha = 'right')
plt.tight_layout()
#plt.savefig('average_delay_by_carrier.png')
plt.show()
#plt.close()

# Plot 5 : On-Time Delivery vs Delayed Shipments
delivery_status_counts = df_cleaned['Delivery_Status'].value_counts(normalize=True) * 100
delivery_status_df = delivery_status_counts.reset_index()
delivery_status_df.columns = ['Delivery_Status','Percentage']
# Map 0 to 'On-Time' and 1 to 'Delayed'
delivery_status_df['Delivery_Status_Label'] = delivery_status_df['Delivery_Status'].map({0 : 'On-Time', 1: 'Delayed'})
plt.figure(figsize=(8,8))
plt.pie(delivery_status_df['Percentage'],labels=delivery_status_df['Delivery_Status_Label'],autopct='%1.1f%%',startangle=90,colors=['#66c2a5','#fc8d62'])
plt.title('Percentage of On-Time vs Delayed Shipments',fontsize=16)
plt.tight_layout()
#plt.savefig('on_time_vs_delayed_shipment.png')
plt.show()
#plt.close()

# Plot 6 : Average Shipment Delay by Day of Week
dayofweek_delay = df_cleaned.groupby('DayOfWeek')['Shipment_Delay'].mean().sort_index().reset_index()
dayofweek_delay.columns = ['DayOfWeek','Average_Delay_Minutes']
plt.figure(figsize=(10,6))
sns.barplot(x='DayOfWeek',y='Average_Delay_Minutes',data=dayofweek_delay,hue='DayOfWeek',palette='magma',legend=False)
plt.title('Average Shipment Delay by Day of Week',fontsize = 16)
plt.xlabel('Day Of Week (1=Monday, 7=Sunday)',fontsize=12)
plt.ylabel('Average Delay (Minutes)',fontsize=12)
plt.xticks(ticks=range(0,7),labels=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'])
plt.tight_layout()
#plt.savefig('Average_Delay_by_DayOfWeek.png')
plt.show()
#plt.close()


# Plot 7 : Average Shipment Delay by Month
month_delay = df_cleaned.groupby('Month')['Shipment_Delay'].mean().sort_index().reset_index()
month_delay.columns = ['Month','Average_Delay_Minutes']
plt.figure(figsize=(12,6))
sns.barplot(x='Month',y='Average_Delay_Minutes',data=month_delay,hue='Month',palette='coolwarm',legend=False)
plt.title('Average Shipment Delay by Month',fontsize=16)
plt.xlabel('Month',fontsize=12)
plt.ylabel('Average Delay (Minutes)',fontsize=-12)
plt.xticks(ticks=range(0,12),labels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
plt.tight_layout()
#plt.savefig('average_delay_by_month.png')
plt.show()
#plt.close()
