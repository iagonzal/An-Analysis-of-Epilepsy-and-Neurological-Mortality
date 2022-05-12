#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:48:22 2022

@author: irvinggonzalez
"""
#%% Imports modules

import pandas as pd

import matplotlib.pyplot as plt

import seaborn as sns

#%% Loads and cleans neurological data

raw = pd.read_csv("Underlying Cause of Death, 1999-2020.txt", sep="\t")

print(len(raw))

print(raw["Notes"])

has_note = raw["Notes"].isna()==False

neuro = raw[has_note==False]

neuro = raw.drop(columns="Notes")

neuro = neuro.dropna(subset="Year")

print(len(neuro))

#%% Loads and cleans epilepsy data

epilepsy = pd.read_csv("Underlying Cause of Death, 1999-2020 Epilepsy.txt", sep="\t")

print(len(epilepsy))

print(epilepsy["Notes"])

has_notes = epilepsy["Notes"].isna()==False

epi = epilepsy.drop(columns="Notes")

epi = epi.dropna(subset="Year")

print(len(epi))

#%% Redefines columns for future usage

new_columns_neuro = {"State Code": "State Code",
                     "Year Code":"neuro_year_code", 
                     "Crude Rate": "neuro_crude_rate"
                     ,"Population":"neuro_pop",
                     "Deaths":"neuro_deaths"
                     }

neuro = neuro.rename(columns=new_columns_neuro)

new_columns_epi = {"State Code":"epi_state_code",
                     "Year Code":"epi_year_code", 
                     "Crude Rate": "epi_crude_rate"
                     ,"Population":"epi_pop",
                     "Deaths":"epi_deaths"
                     }

epi = epi.rename(columns=new_columns_epi)

#%% Merges neuro and epi dataframes and drops useless columns

neuro_epi = neuro.merge(epi, 
                             on=["State", "Year"], how="left", 
                             validate="1:1", indicator=True)

neuro_epi = neuro_epi.drop(columns="epi_crude_rate")
neuro_epi = neuro_epi.drop(columns="neuro_crude_rate")
neuro_epi = neuro_epi.drop(columns="epi_state_code")

#%% Computes death rates for neuro and epi deaths in each state

neuro_epi['neuro_death_rate'] = neuro_epi['neuro_deaths']/neuro_epi['neuro_pop'] * 1000000
neuro_epi['epi_death_rate'] = neuro_epi['epi_deaths']/neuro_epi['epi_pop'] * 1000000

#%% Computes epi to neuro death rate ratio for each state

neuro_epi['epi_to_neuro_ratio'] = neuro_epi['epi_death_rate']/neuro_epi['neuro_death_rate'] * 100

#%% Groups and calculates the average neuro and epi death rates

grouped = neuro_epi.groupby("State")

average = grouped[["neuro_death_rate","epi_death_rate"]].mean()

#%% Groups and calculates the average neuro and epi death counts

grouped_death_counts = neuro_epi.groupby("State")

average_death_counts = grouped_death_counts[["neuro_deaths","epi_deaths"]].mean()

#%% Sets the resolution of the upcoming figures and sets the theme to white

plt.rcParams['figure.dpi'] = 300

sns.set_theme(style="white")

#%% Basic scatterplot for neuro and epi death rates

average.plot.scatter(x="neuro_death_rate",y="epi_death_rate")
plt.title('Epilepsy Death Rates Scattered on Neurological Death Rates')
plt.savefig("neuro_epi_death_rate_scatter.png")

#%% Basic scatterplot for neuro and epi death counts

average_death_counts.plot.scatter(x="neuro_deaths",y="epi_deaths")
plt.title('Epilepsy Death Counts Scattered on Neurological Death Counts')
plt.savefig("neuro_epi_death_counts_scatter.png")

#%% Visualize: Line graph of neuro death rates

sns.lineplot(data=neuro_epi, x="Year", y="neuro_death_rate")
plt.title('Average Neurological Death Rate Linegraph')
plt.savefig("neuro_death_rate_line_graph.png")

#%% Visualize: Line graph of epi death rates

sns.lineplot(data=neuro_epi, x="Year", y="epi_death_rate")
plt.title('Average Epilepsy Death Rate Linegraph')
plt.savefig("epi_death_rate_line_graph.png")

#%% Visualize: Line graphs of neuro death counts

sns.lineplot(data=neuro_epi, x="Year", y="neuro_deaths")
plt.title('Average Neurological Death Count Linegraph')
plt.savefig("neuro_death_count_line_graph.png")

#%% Visualize: Line graphs of epi death counts

sns.lineplot(data=neuro_epi, x="Year", y="epi_deaths")
plt.title('Average Epilepsy Death Count Linegraph')
plt.savefig("epi_death_count_line_graph.png")

#%% Visualize: Histogram of average neuro and epi death rate frequency per state

fig, (ax1,ax2) = plt.subplots(1,2)
average["neuro_death_rate"].plot.hist(ax=ax1)
ax1.set_title("Cases of Neurological Deaths")
average["epi_death_rate"].plot.hist(ax=ax2)
ax2.set_title("Cases of Epilepsy Deaths")
fig.tight_layout()
fig.savefig("death_frequency.png")

#%% Summary statistics sorting of average death rates

average.sort_values(by=['neuro_death_rate'], inplace=True)
print(average)

average.sort_values(by=['epi_death_rate'], inplace=True)
print(average)

#%% Summary statistics sorting of average death counts

average_death_counts.sort_values(by=['neuro_deaths'], inplace=True)
print(average_death_counts)

average_death_counts.sort_values(by=['epi_deaths'], inplace=True)
print(average_death_counts)
