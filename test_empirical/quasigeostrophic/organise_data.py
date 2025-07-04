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
        f"data/qg{transition['run_id']}.eng.csv",
        header=0,
        names=["Age", "Proxy", ],
    )
    # convert to days
    df["Age"] = df["Age"] * 5
    df = (
        df[(df["Age"] <= transition["end_age"] * 5) & (df["Age"] >= transition["start_age"] * 5)]
        .sort_values("Age", ascending=False)
        .reset_index(drop=True)
    )
    df["Record"] = f"qg{transition['run_id']}"
    df["Transition"] = transition["transition"] * 5
    df["Climate proxy"] = "Kinetic Energy"
    df["tsid"] = transition["tsid"]
    list_df.append(df)


# df.plot(x='Age',y='Proxy')

def organise_data():
    list_df = []

    transitions = [
        {"run_id": "016",
         "start_age": 2000,
         "end_age": 3500,
         "transition": 2750,
         "tsid": 1},
        {"run_id": "017",
         "start_age": 400,
         "end_age": 1250,
         "transition": 800,
         "tsid": 2},
        {"run_id": "018",
         "start_age": 500,
         "end_age": 1500,
         "transition": 1000,
         "tsid": 3}, ]

    for transition in transitions:
        create_tsid(transition, list_df)

    # ------------
    # Concatenate dataframes
    # --------------

    df_full = pd.concat(list_df)
    df_full.to_csv("data/transition_data.csv", index=False)

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
