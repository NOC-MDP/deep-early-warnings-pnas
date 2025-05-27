#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 11:58:49 2020

Compute ROC curves comparing EWS to ML prections
for the Dakos climate transitions

Use len 1500 classifier with tseries 3.

Export ROC data for plotting

Late predictions are made in [0.8,1]*(time interval)
Early predictions are made in [0.6,0.8]*(time interval)


@author: Thomas M. Bury
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import scipy.stats as stats
import os


# Function to compute ROC data from truth and indicator vals
# and return a df.
def roc_compute(truth_vals, indicator_vals):
    # Compute ROC curve and threhsolds using sklearn
    fpr, tpr, thresholds = metrics.roc_curve(truth_vals, indicator_vals)

    # Compute AUC (area under curve)
    auc = metrics.auc(fpr, tpr)

    # Put into a DF
    dic_roc = {"fpr": fpr, "tpr": tpr, "thresholds": thresholds, "auc": auc}
    df_roc = pd.DataFrame(dic_roc)

    return df_roc

def compute_roc(bool_pred_early=False,five_hundred = False):
    os.makedirs("data/roc/1500", exist_ok=True)
    os.makedirs("data/roc/500", exist_ok=True)
    # --------
    # Import EWS and ML data
    # –------------

    # Import EWS data
    df_ews_forced = pd.read_csv("data/ews/df_ews_forced.csv")
    df_ews_null = pd.read_csv("data/ews/df_ews_null.csv")

    # Import kendall tau data
    df_ktau_forced = pd.read_csv("data/ews/df_ktau_forced.csv")
    df_ktau_null = pd.read_csv("data/ews/df_ktau_null.csv")

    if five_hundred:
        # Import ML predictions
        df_ml_forced = pd.read_csv("data/ml_preds/500/parsed/df_ml_forced.csv")
        df_ml_null = pd.read_csv("data/ml_preds/500/parsed/df_ml_null.csv")
    else:
        # Import ML predictions
        df_ml_forced = pd.read_csv("data/ml_preds/1500/parsed/df_ml_forced.csv")
        df_ml_null = pd.read_csv("data/ml_preds/1500/parsed/df_ml_null.csv")

    # Add column for truth values (1 for forced, 0 for null)
    df_ktau_forced["truth value"] = 1
    df_ktau_null["truth value"] = 0

    df_ml_forced["truth value"] = 1
    df_ml_null["truth value"] = 0


    # ---------------------------
    # Get predictions from trajectories
    # --------------------------


    # Time interval relative to transition point for where to make predictions
    # as proportion of dataset
    if bool_pred_early:
        pred_interval_rel = np.array([0.6, 0.8])
    else:
        # Late interval for predictions
        pred_interval_rel = np.array([0.8, 1])


    # Initialise lists
    list_df_ktau_preds = []
    list_df_ml_preds = []
    tsid_vals = df_ml_forced["tsid"].unique()
    for tsid in tsid_vals:

        # Get EWS data to get start and transition time
        df = df_ews_forced[df_ews_forced["tsid"] == tsid]
        t_start = df["Time"].iloc[0]
        t_transition = df["Time"].iloc[-1]

        # Get prediction interval in time
        t_pred_start = t_start + (t_transition - t_start) * pred_interval_rel[0]
        t_pred_end = t_start + (t_transition - t_start) * pred_interval_rel[1]

        # Get ktau and ML predictions specific to this tsid
        # and within prediction interval
        df_ktau_forced_final = df_ktau_forced[
            (df_ktau_forced["tsid"] == tsid)
            & (df_ktau_forced["Time"] >= t_pred_start)
            & (df_ktau_forced["Time"] <= t_pred_end)
        ]

        df_ktau_null_final = df_ktau_null[
            (df_ktau_null["tsid"] == tsid)
            & (df_ktau_null["Time"] >= t_pred_start)
            & (df_ktau_null["Time"] <= t_pred_end)
        ]

        df_ml_forced_final = df_ml_forced[
            (df_ml_forced["tsid"] == tsid)
            & (df_ml_forced["Time"] >= t_pred_start)
            & (df_ml_forced["Time"] <= t_pred_end)
        ]

        df_ml_null_final = df_ml_null[
            (df_ml_null["tsid"] == tsid)
            & (df_ml_null["Time"] >= t_pred_start)
            & (df_ml_null["Time"] <= t_pred_end)
        ]

        # Extract 10 evenly spaced predictions for each transition
        # We do this so some transitions don't input more data to the ROC
        # than others.
        n_predictions = 10

        # Ktau forced trajectories
        idx = np.round(np.linspace(0, len(df_ktau_forced_final) - 1, n_predictions)).astype(
            int
        )
        list_df_ktau_preds.append(df_ktau_forced_final.iloc[idx])

        # Ktau null trajectories
        for null_number in np.arange(1, 4):
            df = df_ktau_null_final[df_ktau_null_final["Null number"] == null_number]
            idx = np.round(np.linspace(0, len(df) - 1, n_predictions)).astype(int)
            list_df_ktau_preds.append(df.iloc[idx])

        # if tsid == 4:
        #     continue
        # ML forced trajectories
        idx = np.round(np.linspace(0, len(df_ml_forced_final) - 1, n_predictions)).astype(
            int
        )
        list_df_ml_preds.append(df_ml_forced_final.iloc[idx])

        # ML null trajectories
        for null_number in np.arange(1, 11):
            df = df_ml_null_final[df_ml_null_final["Null number"] == null_number]
            idx = np.round(np.linspace(0, len(df) - 1, n_predictions)).astype(int)
            list_df_ml_preds.append(df.iloc[idx])


    # Concatenate data
    df_ktau_preds = pd.concat(list_df_ktau_preds)
    df_ml_preds = pd.concat(list_df_ml_preds)
    df_ml_preds["bif_prob"] = (
        df_ml_preds["fold_prob"] + df_ml_preds["hopf_prob"] + df_ml_preds["branch_prob"]
    )

    # -------------------
    # Get data on ML favoured bifurcation for each forced trajectory
    # -------------------

    # For each prediction, select the bifurcation that the ML gives greatest weight to
    df_ml_preds["fav_bif"] = df_ml_preds[
        ["fold_prob", "hopf_prob", "branch_prob", "null_prob"]
    ].idxmax(axis=1)

    # Count each bifurcation choice for forced trajectories
    counts = df_ml_preds[df_ml_preds["truth value"] == 1]["fav_bif"].value_counts()

    fold_count = counts["fold_prob"] if "fold_prob" in counts.index else 0
    hopf_count = counts["hopf_prob"] if "hopf_prob" in counts.index else 0
    branch_count = counts["branch_prob"] if "branch_prob" in counts.index else 0
    null_count = counts["null_prob"] if "null_prob" in counts.index else 0

    df_counts = pd.DataFrame(
        {
            "fold": [fold_count],
            "hopf": [hopf_count],
            "branch": [branch_count],
            "null": [null_count],
        }
    )
    if five_hundred:
        # Export data on bifurcation prediction counts
        filepath = "data/roc/500/df_bif_pred_counts_{}.csv".format(
            "early" if bool_pred_early else "late"
        )
    else:
        # Export data on bifurcation prediction counts
        filepath = "data/roc/1500/df_bif_pred_counts_{}.csv".format(
            "early" if bool_pred_early else "late"
        )

    df_counts.to_csv(filepath, index=False)

    print("Exported bifurcation count data to {}".format(filepath))



    # --------------------
    # Functions to compute ROC
    # –--------------------





    # ---------------------
    ## Compute ROC data
    # –--------------------

    # Initiliase list for ROC dataframes for predicting May fold bifurcation
    list_roc = []

    # # Assign indicator and truth values for ML prediction
    # indicator_vals = df_ml_preds['bif_prob']
    # truth_vals = df_ml_preds['truth value']
    # df_roc = roc_compute(truth_vals,indicator_vals)
    # df_roc['ews'] = 'ML bif'
    # list_roc.append(df_roc)


    # Assign indicator and truth values for ML prediction
    indicator_vals = df_ml_preds["bif_prob"]
    truth_vals = df_ml_preds["truth value"]
    df_roc = roc_compute(truth_vals, indicator_vals)
    df_roc["ews"] = "ML bif"
    list_roc.append(df_roc)


    # Assign indicator and truth values for variance
    indicator_vals = df_ktau_preds["ktau_variance"]
    truth_vals = df_ktau_preds["truth value"]
    df_roc = roc_compute(truth_vals, indicator_vals)
    df_roc["ews"] = "Variance"
    list_roc.append(df_roc)


    # Assign indicator and truth values for variance
    indicator_vals = df_ktau_preds["ktau_ac"]
    truth_vals = df_ktau_preds["truth value"]
    df_roc = roc_compute(truth_vals, indicator_vals)
    df_roc["ews"] = "Lag-1 AC"
    list_roc.append(df_roc)

    # Concatenate roc dataframes
    df_roc_dakos_climate = pd.concat(list_roc, ignore_index=True)


    # Export ROC data
    if five_hundred:
        filepath = "data/roc/500/df_roc_dakos_{}.csv".format("early" if bool_pred_early else "late")
    else:
        filepath = "data/roc/1500/df_roc_dakos_{}.csv".format("early" if bool_pred_early else "late")

    df_roc_dakos_climate.to_csv(
        filepath,
        index=False,
    )


    # -------------
    # Plotly fig
    # ----------------

    df_roc = df_roc_dakos_climate


    import plotly.graph_objects as go

    fig = go.Figure()

    # ML bif plot
    df_trace = df_roc[df_roc["ews"] == "ML bif"]
    fig.add_trace(
        go.Scatter(
            x=df_trace["fpr"],
            y=df_trace["tpr"],
            mode="lines",
            name="ML bif (AUC={})".format(df_trace.round(2)["auc"].iloc[0]),
        )
    )

    # Variance plot
    df_trace = df_roc[df_roc["ews"] == "Variance"]
    fig.add_trace(
        go.Scatter(
            x=df_trace["fpr"],
            y=df_trace["tpr"],
            name="Variance (AUC={})".format(df_trace.round(2)["auc"].iloc[0]),
        )
    )

    # Lag-1  AC plot
    df_trace = df_roc[df_roc["ews"] == "Lag-1 AC"]
    fig.add_trace(
        go.Scatter(
            x=df_trace["fpr"],
            y=df_trace["tpr"],
            name="Lag-1 AC (AUC={})".format(df_trace.round(2)["auc"].iloc[0]),
        )
    )

    # Line y=x
    fig.add_trace(
        go.Scatter(
            x=np.linspace(0, 1, 100),
            y=np.linspace(0, 1, 100),
            showlegend=False,
            line={"color": "black", "dash": "dash"},
        )
    )

    fig.update_xaxes(
        title="False positive rate",
        range=[-0.01, 1],
    )
    fig.update_yaxes(
        title="True positive rate",
    )

    fig.update_layout(
        legend=dict(
            x=0.6,
            y=0,
        ),
        width=600,
        height=600,
        title="ROC, NEMO-MEDUSA Model",
    )
    if five_hundred:
        fig.write_image(
            "figures/figs_roc/500/roc_paleo_{}.png".format("early" if bool_pred_early else "late")
        )
    else:
        fig.write_image(
            "figures/figs_roc/1500/roc_paleo_{}.png".format("early" if bool_pred_early else "late")
        )

if __name__ == "__main__":
    compute_roc()