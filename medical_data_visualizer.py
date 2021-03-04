import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')


# Add 'overweight' column
bmi = (df['weight']/((df['height'])/100)**2)
df['overweight'] = np.where(bmi > 25, 1, 0)


# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = np.where(df['cholesterol'] < 2, 0, 1)
df['gluc'] = np.where(df['gluc'] < 2, 0, 1)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=['cardio'] , value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the collumns for the catplot to work correctly.
    df_cat_2 = pd.DataFrame(df_cat.groupby(["cardio","variable","value"])["value"].count())
    df_cat_2 = df_cat_2.rename(columns = {"value": "total"})
    df_cat_2 = df_cat_2.reset_index()

    fig, ax = plt.subplots(figsize=(12,10))

    # Draw the catplot with 'sns.catplot()'
    g = sns.catplot(x="variable", y="total", col="cardio", hue="value", kind = "bar", data=df_cat_2)

    fig = g.fig

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df_heat = df[(df['ap_lo'] <= df['ap_hi'])
      & (df['height'] >= df['height'].quantile(0.025))
      & (df['height'] <= df['height'].quantile(0.975))
      & (df['weight'] >= df['weight'].quantile(0.025))
      & (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # Calculate the correlation matrix
    corr = round(df_heat.corr(),1)

    mask = np.triu(np.ones_like(corr))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12,10))

    # Draw the heatmap with 'sns.heatmap()'
    ax = sns.heatmap(corr, annot=True, mask=mask, vmax=.3, fmt=".1f")


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig