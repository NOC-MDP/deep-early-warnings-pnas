#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 10:49:34 2020

Organise ML data output into a single dataframe

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import glob
import re
import os

def organise_ml_data(parameter:str,region:str,five_hundred=False):
    # # ML model number
    # ml_number = "Protocol3_Jan21_len500"


    # 500 or 1500 point classifier used
    # classifier_length = 500
    # Spacing between ML data points
    # ml_spacing = int(classifier_length / 50)
    if five_hundred:
        os.makedirs(f"{region}/results/{parameter}/ml_preds/500/parsed/", exist_ok=True)
        path = f"{region}/results/{parameter}/ml_preds/500/"
    else:
        os.makedirs(f"{region}/results/{parameter}/ml_preds/1500/parsed/", exist_ok=True)
        path = f"{region}/results/{parameter}/ml_preds/1500/"

    # # Import EWS data (need time values for plot)
    # df_ews = pd.read_csv("data/ews/df_ews_forced.csv")

    # Import all ML predictions

    # Get all file names
    all_files = glob.glob(path + "*.csv")
    # Don't include df files
    all_files = [f for f in all_files if f.find("ensemble") != -1]
    all_files_null = sorted([f for f in all_files if f.find("null") != -1])
    all_files_forced = sorted([f for f in all_files if f.find("null") == -1])


    # ----------------
    # Organise data for forced trajectories
    # -----------------

    # Collect ML data for forced trajectories
    list_df_ml = []
    for filename in all_files_forced:
        print(f"organize for {filename}")
        df = pd.read_csv(
            filename,
        )

        tsid = int(filename.split("_")[-1].split(".")[0])

        # Add info to dataframe
        df["tsid"] = tsid

        # Append dataframe to list
        list_df_ml.append(df)

    # Concatenate dfs
    df_ml_forced = pd.concat(list_df_ml)
    # sort by type, then latitude
    df_ml_forced.sort_values(["tsid", "Time"], inplace=True, na_position="first")

    if five_hundred:
        # # Export ML dataframe
        filepath = f"{region}/results/{parameter}/ml_preds/500/parsed/"
        df_ml_forced.to_csv(filepath + "df_ml_forced.csv", index=False)
    else:
        # # Export ML dataframe
        filepath = f"{region}/results/{parameter}/ml_preds/1500/parsed/"
        df_ml_forced.to_csv(filepath + "df_ml_forced.csv", index=False)

    # ----------------
    # Organise data for null trajectories
    # -----------------

    # Collect ML data for null trajectories
    list_df_ml = []
    for filename in all_files_null:
        print(f"organize for {filename}")
        df = pd.read_csv(
            filename,
        )

        tsid = int(filename.split("_")[-2])
        null_number = int(filename.split("_")[-1].split(".")[0])

        # Add info to dataframe
        df["tsid"] = tsid
        df["Null number"] = null_number
        # Append dataframe to list
        list_df_ml.append(df)

    # Concatenate dfs
    df_ml_null = pd.concat(list_df_ml)
    # sort by type, then latitude
    df_ml_null.sort_values(
        ["tsid", "Null number", "Time"], inplace=True, na_position="first"
    )

    if five_hundred:
        # # Export ML dataframe
        filepath = f"{region}/results/{parameter}/ml_preds/500/parsed/"
        df_ml_null.to_csv(filepath + "df_ml_null.csv", index=False)

    else:
        # # Export ML dataframe
        filepath = f"{region}/results/{parameter}/ml_preds/1500/parsed/"
        df_ml_null.to_csv(filepath + "df_ml_null.csv", index=False)
# ------
if __name__ == "__main__":
    organise_ml_data(parameter="CHL",region="Labrador_Sea")
