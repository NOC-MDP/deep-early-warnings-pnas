#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 12:46:55 2020

Organise climate data in same format as in Dakos 2008
Use time ranges and transition times as given in Table S1 Dakos 2008

@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd

import glob
import re


# ----------------
# Import and organise data
# –------------------


def create_tsid(transition, list_df):
    df = pd.read_csv(
        f"data/mldr10_1_{transition['run_id']}_monthly.csv",
        header=0,
        names=["Age", "Proxy", ],
    )
    # convert to days
    df["Age"] = df["Age"] * 365
    df = (
        df[(df["Age"] <= transition["end_age"] * 365) & (df["Age"] >= transition["start_age"] * 365)]
        .sort_values("Age", ascending=False)
        .reset_index(drop=True)
    )
    df["Record"] = f"NM_{transition['run_id']}"
    df["Transition"] = transition["transition"] * 365
    df["Climate proxy"] = "Mixed Layer Depth"
    df["tsid"] = transition["tsid"]
    list_df.append(df)


# df.plot(x='Age',y='Proxy')

def organise_data():
    list_df = []

    transitions = [
        {"run_id": "58.0_-40.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 615,
         "tsid": 1},
        {"run_id": "58.0_-38.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 507,
         "tsid": 2},
        {"run_id": "58.0_-36.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 602,
         "tsid": 3},
        {"run_id": "58.0_-34.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 746,
         "tsid": 4},
        {"run_id": "58.0_-32.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 759,
         "tsid": 5},
        {"run_id": "59.25_-40.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 590,
         "tsid": 6},
        {"run_id": "59.25_-38.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 508,
         "tsid": 7},
        {"run_id": "59.25_-36.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 519,
         "tsid": 8},
        {"run_id": "59.25_-34.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 843,
         "tsid": 9},
        {"run_id": "59.25_-32.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 686,
         "tsid": 10},
        {"run_id": "60.5_-40.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 603,
         "tsid": 11},
        {"run_id": "60.5_-38.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 601,
         "tsid": 12},
        {"run_id": "60.5_-36.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 602,
         "tsid": 13},
        {"run_id": "60.5_-34.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 543,
         "tsid": 14},
        {"run_id": "60.5_-32.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 926,
         "tsid": 15},
        {"run_id": "61.75_-40.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 604,
         "tsid": 16},
        {"run_id": "61.75_-38.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 603,
         "tsid": 17},
        {"run_id": "61.75_-36.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 506,
         "tsid": 18},
        {"run_id": "61.75_-34.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 495,
         "tsid": 19},
        {"run_id": "61.75_-32.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 688,
         "tsid": 20},
        {"run_id": "63.0_-40.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 529,
         "tsid": 21},
        {"run_id": "63.0_-38.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 685,
         "tsid": 22},
        {"run_id": "63.0_-36.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 685,
         "tsid": 23},
        {"run_id": "63.0_-34.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 758,
         "tsid": 24},
        {"run_id": "63.0_-32.0",
         "start_age": 1,
         "end_age": 1212,
         "transition": 746,
         "tsid": 25},

    ]

    for transition in transitions:
        create_tsid(transition, list_df)

    # ------------
    # Concatenate dataframes
    # --------------

    df_full = pd.concat(list_df)
    df_full.to_csv("data/transition_data.csv", index=False)

if __name__ == "__main__":
    organise_data()
# len(df[df['Age']>=df['Transition'].iloc[0]])


# # Bolling-Allerod transition (BAT)
# df = pd.read_csv(
#     "data/gisp2/gisp2_temp_accum_alley2000.txt",
#     header=0,
#     names=["Age", "Proxy", "NA"],
#     sep="\s+",
#     nrows=1632,
# )
# df = df[["Age", "Proxy"]]
# df["Age"] = df["Age"] * 1000
# df = (
#     df[(df["Age"] <= 21000) & (df["Age"] >= 14600)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "Bolling-Allerod transition"
# df["Transition"] = 15000
# df["Climate proxy"] = "Temperature (C)"
# df["tsid"] = 2
# list_df.append(df)
#
#
# # End of Younger Dryas (EYD)
# df = pd.read_csv(
#     "data/cariaco2000/cariaco2000_pc56_greyscale.txt",
#     header=1,
#     names=["Age", "Proxy"],
#     sep="\s+",
#     # nrows=1632,
# )
# df = (
#     df[(df["Age"] <= 12500) & (df["Age"] >= 11200)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "End of Younger Dryas"
# df["Transition"] = 11600
# df["Climate proxy"] = "Grayscale (0-255)"
# df["tsid"] = 3
# list_df.append(df)
#
#
# # Desertification of north africa (DNA)
# df = pd.read_csv(
#     "data/demenocal2000/658C.terr.2.1.interp.csv",
#     header=0,
# )
# df["Age"] = df["Age(cal. yr BP)"]
# df["Proxy"] = df["terr% (interp)"]
# df = df[["Age", "Proxy"]]
# df = (
#     df[(df["Age"] <= 8300) & (df["Age"] >= 4800)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "Desertification of N. Africa"
# df["Transition"] = 5700
# df["Climate proxy"] = "Terrigeneous dust (%)"
# df["tsid"] = 4
# list_df.append(df)
#
#
# # End of glaciation 1 (EG1)
# df = pd.read_csv(
#     "data/deutnat/deutnat.txt",
#     sep="\s+",
#     encoding="latin1",
#     names=["Depth", "Age", "Proxy", "deltaTS"],
#     skiprows=range(0, 111),
# )
#
# df = df[["Age", "Proxy"]]
# df = (
#     df[(df["Age"] <= 58000) & (df["Age"] >= 12000)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "End of glaciation I"
# df["Transition"] = 17000
# df["Climate proxy"] = "d2H (%)"
# df["tsid"] = 5
# list_df.append(df)
#
#
# # End of glaciation II
# # df = pd.read_csv(
# #     "data/deutnat/deutnat.txt",
# #     header=85,
# #     names=["Depth", "Age", "Proxy", "deltaTS"],
# #     sep='\s+,
# #     # nrows=1632,
# # )
# df = pd.read_csv(
#     "data/deutnat/deutnat.txt",
#     sep="\s+",
#     encoding="latin1",
#     names=["Depth", "Age", "Proxy", "deltaTS"],
#     skiprows=range(0, 111),
# )
#
# df = df[["Age", "Proxy"]]
# df = (
#     df[(df["Age"] <= 151e3) & (df["Age"] >= 128e3)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "End of glaciation II"
# df["Transition"] = 135e3
# df["Climate proxy"] = "d2H (%)"
# df["tsid"] = 6
# list_df.append(df)
#
#
# # End of glaciation III
# # df = pd.read_csv(
# #     "data/deutnat/deutnat.txt",
# #     header=85,
# #     names=["Depth", "Age", "Proxy", "deltaTS"],
# #     sep='\s+,
# #     # nrows=1632,
# # )
# df = pd.read_csv(
#     "data/deutnat/deutnat.txt",
#     sep="\s+",
#     encoding="latin1",
#     names=["Depth", "Age", "Proxy", "deltaTS"],
#     skiprows=range(0, 111),
# )
# df = df[["Age", "Proxy"]]
# df = (
#     df[(df["Age"] <= 270000) & (df["Age"] >= 238000)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "End of glaciation III"
# df["Transition"] = 242000
# df["Climate proxy"] = "d2H (%)"
# df["tsid"] = 7
# list_df.append(df)
#
#
# # End of glaciation IV
# df = pd.read_csv(
#     "data/deutnat/deutnat.txt",
#     sep="\s+",
#     encoding="latin1",
#     names=["Depth", "Age", "Proxy", "deltaTS"],
#     skiprows=range(0, 111),
# )
# df = df[["Age", "Proxy"]]
# df = (
#     df[(df["Age"] <= 385300) & (df["Age"] >= 324600)]
#     .sort_values("Age", ascending=False)
#     .reset_index(drop=True)
# )
# # df.plot(x='Age',y='Proxy')
# df["Record"] = "End of glaciation IV"
# df["Transition"] = 334100
# df["Climate proxy"] = "d2H (%)"
# df["tsid"] = 8
# list_df.append(df)
