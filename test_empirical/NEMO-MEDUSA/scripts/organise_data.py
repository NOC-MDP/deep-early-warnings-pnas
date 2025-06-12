#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:55 2020

Organise climate data in same format as in Dakos 2008
Use time ranges and transition times as given in Table S1 Dakos 2008

@author: Thomas M. Bury
"""
import json

import numpy as np
import pandas as pd

import glob
import re

from lmfit import parameter


# ----------------
# Import and organise data
# –------------------


def create_tsid(transition, list_df,parameter:str,region:str):
    df = pd.read_csv(
        f"{region}/data/{parameter}/{parameter}_{transition['run_id']}_monthly.csv",
        header=0,
        names=["Age", "Proxy", ],
    )
    # TODO need to account for leap years ideally
    # convert to days

    def months_to_days(age_months):
        days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        full_years, remaining_months = divmod(age_months, 12)
        return full_years * sum(days_per_month) + sum(days_per_month[:remaining_months])

    df["Age"] = df["Age"].apply(months_to_days)
    df = (
        df[(df["Age"] <= months_to_days(transition["end_age"])) & (df["Age"] >= months_to_days(transition["start_age"]))]
        .sort_values("Age", ascending=False)
        .reset_index(drop=True)
    )
    df["Record"] = f"NM_{transition['run_id']}"
    df["Transition"] = months_to_days(transition["transition"])
    df["Climate proxy"] = parameter
    df["tsid"] = transition["tsid"]
    list_df.append(df)


# df.plot(x='Age',y='Proxy')

def organise_data(parameter:str,region:str):
    list_df = []

    with open(f"{region}/data/{parameter}/{parameter}_transitions.json") as f:
        transitions = json.load(f)

    for transition in transitions["transitions"]:
        create_tsid(transition, list_df,parameter,region=region)

    # ------------
    # Concatenate dataframes
    # --------------

    df_full = pd.concat(list_df)
    df_full.to_csv(f"{region}/data/{parameter}/{parameter}_transition_data.csv", index=False)

if __name__ == "__main__":
    organise_data(parameter="TOS",region="Labrador_Sea")
