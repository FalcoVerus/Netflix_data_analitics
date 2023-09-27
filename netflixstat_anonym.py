import pandas
import seaborn as sns
import matplotlib.pyplot as plt

# Reading in the file
df = pandas.read_csv('ViewingActivity.csv')

# Go GDPR, change the input names to your netflix user names
df.replace('A', 'Jane', inplace=True)
df.replace('B', 'Jhon', inplace=True)
df.replace('C', 'Tarzan', inplace=True)
df.drop(df[df['Profile Name'] == 'Kids'].index, inplace=True)

# Fill missing values with a string
df['Attributes'].fillna('clicked', inplace=True)

# Split the Title column and drop the original
split_title = df['Title'].str.split(':', n=1, expand=True)
split_title.columns = [f'Main Title', f'Subtitle']
df = pandas.concat([df, split_title], axis=1)
df.drop('Title', axis=1, inplace=True)

# Writing back anonymized file if you want
df.to_csv('Tarzanonnetflix.csv', index=False)

# Convert to datetime format and convert to your time zone
df['Start Time'] = pandas.to_datetime(df['Start Time'], utc=True)
df = df.set_index('Start Time')
df.index = df.index.tz_convert('Europe/Berlin')
df = df.reset_index()

# Convert duration to timedelta
df['Duration'] = pandas.to_timedelta(df['Duration'])

# New dataframe for each of the users
janedf = df.loc[df['Profile Name'] == 'Jane']
jhondf = df.loc[df['Profile Name'] == 'Jhon']
tarzandf = df.loc[df['Profile Name'] == 'Tarzan']

# Calculating total watch times
jane_wt = janedf['Duration'].sum()
jhon_wt = jhondf['Duration'].sum()
tarzan_wt = tarzandf['Duration'].sum()

# How much autoplay for each user with NO user interaction
jane_apn = janedf[janedf['Attributes'].str.contains('None;', na=False)]
jhon_apn = jhondf[jhondf['Attributes'].str.contains('None;', na=False)]
tarzan_apn = tarzandf[tarzandf['Attributes'].str.contains('None;', na=False)]
jane_apns = jane_apn['Duration'].sum()
jhon_apns = jhon_apn['Duration'].sum()
tarzan_apns = tarzan_apn['Duration'].sum()
jane_h1 = jane_apns.total_seconds() / 3600
jhon_h1 = jhon_apns.total_seconds() / 3600
tarzan_h1 = tarzan_apns.total_seconds() / 3600

# How much autoplay for each user with user interaction
jane_apy = janedf[janedf['Attributes'].str.contains('User_Interaction;', na=False)]
jhon_apy = jhondf[jhondf['Attributes'].str.contains('User_Interaction;', na=False)]
tarzan_apy = tarzandf[tarzandf['Attributes'].str.contains('User_Interaction;', na=False)]
jane_apys = jane_apy['Duration'].sum()
jhon_apys = jhon_apy['Duration'].sum()
tarzan_apys = tarzan_apy['Duration'].sum()
jane_h2 = jane_apys.total_seconds() / 3600
jhon_h2 = jhon_apys.total_seconds() / 3600
tarzan_h2 = tarzan_apys.total_seconds() / 3600


# Watched without autosuggestion
jane_tot = janedf[janedf['Attributes'].str.contains('clicked', na=False)]
jhon_tot = jhondf[jhondf['Attributes'].str.contains('clicked', na=False)]
tarzan_tot = tarzandf[tarzandf['Attributes'].str.contains('clicked', na=False)]
jane_tots = jane_tot['Duration'].sum()
jhon_tots = jhon_tot['Duration'].sum()
tarzan_tots = tarzan_tot['Duration'].sum()
jane_h3 = jane_tots.total_seconds() / 3600
jhon_h3 = jhon_tots.total_seconds() / 3600
tarzan_h3 = tarzan_tots.total_seconds() / 3600

# Plotting watch times
categories = ['Autoplay', 'Autoplay-watched', 'Selected']
jane_th = [jane_h1, jane_h2, jane_h3]
jhon_th = [jhon_h1, jhon_h2, jhon_h3]
tarzan_th = [tarzan_h1, tarzan_h2, tarzan_h3]

total_wtdf = pandas.DataFrame({'User': ['Jane', 'Jhon', 'Tarzan'], 
                               'Autoplay': [jane_h1, jhon_h1, tarzan_h1],
                               'Autoplay-watched': [jane_h2, jhon_h2, tarzan_h2],                     
                               'Selected': [jane_h3, jhon_h3, tarzan_h3]})

fig, ax = plt.subplots(figsize=(10, 6))

# Define custom colors for the bars
# Would be nice to use seaborn, but plotting bars is complicated
# sns.barplot(x='User', y='Total watch time', data=total_wtdf)

colors = ['#FFFF00', '#FF5733', '#CC0000']

total_wtdf.plot(x='User', kind='bar', stacked=True, ax=ax, color=colors)
plt.xlabel('Name of the user', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.ylabel('Watch time (hours)', fontsize=14, fontweight='bold', fontfamily='times new roman')
plt.title('Total watch time', fontsize=18, fontweight='bold', fontfamily='times new roman')

# Customizing legend
legend = plt.legend(labels=['Auto playing preview', 'Auto playing preview followed \nby user interaction', 'All other watching activity'], title='Time Unit')
legend.set_title('Time Unit')
title_text = legend.get_title()
title_text.set_fontsize(14)
title_text.set_fontweight('bold')
title_text.set_fontfamily('times new roman')

for text in legend.get_texts():
    text.set_fontsize=(12)
    text.set_fontweight=('normal')
    text.set_fontfamily=('times new roman')

# Add horizontal lines at marked hour values
marked_values = [100, 150, 200, 250, 300, 350, 400, 450]
for value in marked_values:
    plt.axhline(y=value, color='gray', linestyle='--', linewidth=1)

# Customizing text on the axis
plt.xticks(rotation=0, fontsize=12, fontweight='bold', fontfamily='Times New Roman')
plt.yticks(rotation=0, fontsize=12, fontfamily='Times New Roman')

# Save the watch time plot to a file
plt.tight_layout()
plt.savefig('watch_time_plot.png', bbox_inches='tight')

# Drop all the preview rows for the rest of the manipulation
janedf = janedf[~janedf['Main Title'].str.contains('Előzetes', case=False, regex=True)]
jhondf = jhondf[~jhondf['Main Title'].str.contains('Előzetes', case=False, regex=True)]
tarzandf = tarzandf[~tarzandf['Main Title'].str.contains('Előzetes', case=False, regex=True)]

# Use value_counts to count the occurrences of each string
jane_vc = janedf['Main Title'].value_counts()
jhon_vc = jhondf['Main Title'].value_counts()
tarzan_vc = tarzandf['Main Title'].value_counts()

# Get the string that repeats the most
jane_most_common_string = jane_vc.idxmax()

# Get the count of the most common string
jane_most_common_string_count = jane_vc.max()

#print(f"The most common string is '{jane_most_common_string}' with {jane_most_common_string_count} occurrences.")

# Get the first 10 most viewed and count their time
top_10_jane = jane_vc.head(10)
top_10_jhon = jhon_vc.head(10)
top_10_tarzan = tarzan_vc.head(10)

# Create a new DataFrame for the top 10 strings
top_10_janedf = janedf[janedf['Main Title'].isin(top_10_jane.index)]
top_10_jhondf = jhondf[jhondf['Main Title'].isin(top_10_jhon.index)]
top_10_tarzandf = tarzandf[tarzandf['Main Title'].isin(top_10_tarzan.index)]

# Group the data by Title
jane_most_v = top_10_janedf.groupby('Main Title')['Duration'].sum().reset_index()
jhon_most_v = top_10_jhondf.groupby('Main Title')['Duration'].sum().reset_index()
tarzan_most_v = top_10_tarzandf.groupby('Main Title')['Duration'].sum().reset_index()

# Convert timedelta duration to hours
jane_most_v['Duration'] = jane_most_v['Duration'].dt.total_seconds() / 3600
jhon_most_v['Duration'] = jhon_most_v['Duration'].dt.total_seconds() / 3600
tarzan_most_v['Duration'] = tarzan_most_v['Duration'].dt.total_seconds() / 3600

# Sorting by watch times
jane_most_vs = jane_most_v.sort_values(by='Duration')
jhon_most_vs = jhon_most_v.sort_values(by='Duration')
tarzan_most_vs = tarzan_most_v.sort_values(by='Duration')

# Create a bar plot for Jane
plt.figure(figsize=(10, 6))
colors = sns.color_palette('dark')
sns.barplot(x='Duration', y='Main Title', hue='Main Title', data=jane_most_vs, dodge=False, palette=colors)
plt.xlabel('Total Watch Time (hours)', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.ylabel('Main Title', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.title('Top 10 Most Viewed Titles by Jane', fontsize=18, fontweight='bold', fontfamily='times new roman')
plt.xticks(fontsize=12, fontfamily='Times New Roman')
plt.yticks(fontsize=12, fontfamily='Times New Roman')
plt.xticks(rotation=45, ha='right')

# Show the plot and save it to a file
plt.legend([], [], frameon=False)
plt.tight_layout()
plt.savefig('most_watched_jane.png', bbox_inches='tight')
plt.show()

# Create a bar plot for Jhon
plt.figure(figsize=(10, 6))
colors = sns.color_palette('dark')
sns.barplot(x='Duration', y='Main Title', hue='Main Title', data=jhon_most_vs, dodge=False, palette=colors)
plt.xlabel('Total Watch Time (hours)', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.ylabel('Main Title', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.title('Top 10 Most Viewed Titles by Jhon', fontsize=18, fontweight='bold', fontfamily='times new roman')
plt.xticks(fontsize=12, fontfamily='Times New Roman')
plt.yticks(fontsize=12, fontfamily='Times New Roman')
plt.xticks(rotation=45, ha='right')

# Show the plot and save it to a file
plt.legend([], [], frameon=False)  # Hide the legend
plt.tight_layout()
plt.savefig('most_watched_jhon.png', bbox_inches='tight')
plt.show()

# Create a bar plot for Jane
plt.figure(figsize=(10, 6))
colors = sns.color_palette('dark')
sns.barplot(x='Duration', y='Main Title', hue='Main Title', data=tarzan_most_vs, dodge=False, palette=colors)
plt.xlabel('Total Watch Time (hours)', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.ylabel('Main Title', fontsize=14, fontweight='bold', fontfamily='Times New Roman')
plt.title('Top 10 Most Viewed Titles by Tarzan', fontsize=18, fontweight='bold', fontfamily='times new roman')
plt.xticks(fontsize=12, fontfamily='Times New Roman')
plt.yticks(fontsize=12, fontfamily='Times New Roman')
plt.xticks(rotation=45, ha='right')

# Show the plot and save it to a file
plt.legend([], [], frameon=False)  # Hide the legend
plt.tight_layout()
plt.savefig('most_watched_tarzan.png', bbox_inches='tight')
plt.show()