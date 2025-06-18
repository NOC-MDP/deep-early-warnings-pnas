# Results of NEMO MEDUSA model prediction.
The following is the initial results from the CLASS NEMO MEDUSA model run SSP370. It shows a series of ROC curves for three regions for 5 parameters:
- Mixed Layer Depth
- Surface Temperature
- Dissolved Inorganic Nitrate
- Chlorophyll
- Sea surface height

## Labrador Sea

### Early Prediction (60 - 80%)

![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/Labrador_Sea/figures/1500_LAB_combined_early.png)

### Late Prediction (80 - 100%)


![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/Labrador_Sea/figures/1500_LAB_combined_late.png)

## Irminger Sea

### Early Prediction (60 - 80 %)

![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/Irminger_Sea/figures/1500_IR_combined_early.png)

### Late Prediction (80 - 100%)

![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/Irminger_Sea/figures/1500_IR_combined_late.png)

## West Scotland

### Early Prediction (60 - 80 %)

![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/West_Scotland/figures/1500_WS_combined_early.png)

### Late Prediction (80 - 100%)

![image](https://github.com/NOC-MDP/deep-early-warnings-pnas/blob/main/test_empirical/NEMO-MEDUSA/West_Scotland/figures/1500_WS_combined_late.png)

----------------

# Deep learning for early warning signals of tipping points
This repository contains code to reproduce results in the publication

#### *Deep learning for early warning signals of tipping points*. [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-1595-9444)Thomas M. Bury, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-0791-7896)R. I. Sujith, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-4923-2537)Induja Pavithran, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/[0000-0002-2100-0312](https://orcid.org/0000-0002-2100-0312))Marten Scheffer, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6725-7498)Timothy M. Lenton, Madhur Anand, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0001-6214-6601)Chris T. Bauch. *Proceedings of the National Academy of Sciences* 2021, 118 (39) e2106140118; DOI: 10.1073/pnas.2106140118

To apply the techniques developed in this article, please check out the Python package [ewstools](https://github.com/ThomasMBury/ewstools) and its tutorials. To perform a reproducible run of the article, please read on.

## Requirements

Python 3.9+ and Tensorflow 2.15.0 are required. To install other dependencies, please run

```setup
pip install --upgrade pip
pip install -r requirements.txt
```
within a new virtual environment.

The bifurcation continuation software AUTO-07P is required to generate the training data. Installation instructions are provided at
http://cmvl.cs.concordia.ca/auto/.


## Directories

**./dl_train:** Code to train the DL classifiers

**./figures_pnas:** Code to generate figures used in manuscript.

**./test_models:** Code to simulate and compute early warning signals for the test models. These include the Consumer-Resource model, May's harvesting model and an SEIRx model.

**./test_empirical:** Code to pre-process and compute early warning signals for the empirical datasets used in the study.

**./training_data:** Code to generate training data for the deep learning algorithm.


## Workflow

The results in the paper are obtained from the following workflow:

1. **Generate the training data**.
   We generate two sets of training data. One for the 500-classifier and the other for the 1500-classifier. The 500-classifier (1500-classifier) is trained on 500,000 (200,000) time series, each of length 500 (1500) data points. Run

   ```bash
   bash training_data/run_single_batch.sh $batch_num $ts_len
   ```

   where `$batch_num` is a batch number (integer) and `$ts_len` is a time series length (500 or 1500). This generates 4,000 time series, consisting of 1000 time series for each possible outcome (fold, Hopf, transcritical, null). Each time series is saved as a csv file. This alone can take up to 1000 minutes (~17 hours) on a single CPU. We therefore run multiple batches in parallel on a CPU cluster at the University of Waterloo. This cluster uses the Slurm workload manager. The script to submit the 125 batches (125x4000=500k time series) for the 500-classifier is `submit_multi_batch_500.py`. The script to submit the 50 batches (50x4000=200k time series) for the 1500-classifier is `submit_multi_batch_1500.py`.

   Once every batch has been generated, the output data from each batch is combined using

   ```bash
   bash combine_batches.sh $num_batches $ts_len
   ```

   where `$num_batches` is the total number of batches being used. This also stacks the `labels.csv` and `groups.csv` files, and compresses the folder containing the time series data.

   The final compressed output comes out at 5.87GB for the 500-classifier and 5.38GB for the 1500-classifier. Both datasets are archived on Zenodo at [https://zenodo.org/record/5527154#.YU9SuGZKhqs](https://zenodo.org/record/5527154#.YU9SuGZKhqs).

2. **Train the DL classifiers**. 
   20 neural networks are trained using the training data. 10 networks use time series that are padded on both the left and the right with zeros (model_type=1). 10 networks use time series that are padded only on the left with zeros (model_type=2). Results reported in the paper take the average prediction from these 20 networks.  To train a single neural network of a given model_type and index kk, run

   ```bash
   python ./dl_train/DL_training.py $model_type $kk
   ```

   This will export the trained model (including weights, biases and architecture) to the directory `./dl_train/best_models/`. We run this for model_type in [1,2] and kk in [1,2,3,...,10]. Taking model_type and kk as command line parameters allows training of multiple neural networks in parallel if one has access to mulitple GPUs. The code currently trains networks using the 1500-length time series. To train using the 500-length time series, adjust the parameters lib_size and ts_len, as indicated in the comments of the code. Time to train a single neural network using a GPU is approx. 24 hours.

3. **Simulate mathematical models and compute CSD-based EWS**. 
   Scripts to simulate the mathematical models and compute CSD-based EWS are in the `./test_models/` directory. For example, to simulate trajectories of May's harvesting model going through a fold bifurcation, run

   ```bash
   python ./test_models/may_fold_1500/sim_may_fold.py
   ```

   Null trajectories are simulated with `sim_may_fold_null.py`. The same file notation is used for the other models. These scripts also detrend the time series and compute the variance and lag-1 autocorrelation. Kendall tau metrics are computed with `compute_ktau.py`.

4. **Process empirical data and compute CSD-based EWS**. 
   Scripts to process the empirical data are availalble in the `./test_empirical/` directory. This involves resampling, detrending, and computing the CSD-based EWS - variance and lag-1 autocorrelation.

5. **Compute DL predictions**. 
   We now feed the residual data from the models and the empirical data into the neural networks to obtain predictions. This is achieved with the scripts `dl_apply.py`, available in each of the `test_models` and `test_empirical` subdirectories. These scripts take around 20 minutes to run each (Mac M1, 2020). Computation time can be reduced by only importing 2 classifiers (1 of each type) instead of all 20. Then run `organise_ml_data.py` to concatenate the deep learning predictions.

6. **Compute ROC statistics**. 
   To compare the performance of the DL classifiers and the CSD-based EWS, we compute ROC statistics. This is achieved with the scripts `compute_roc.py`, available in each of the `test_models` and `test_empirical` subdirectories.


## Data sources

The empirical data used in this study are available from the following sources:
1. **Sedimentary archive** data from the Mediterranean Sea are available at the [PANGAEA](https://doi.pangaea.de/10.1594/PANGAEA.923197) data repository. Data were preprocessed according to the study [Hennekam, Rick, et al. "Early‐warning signals for marine anoxic events." Geophysical Research Letters 47.20 (2020): e2020GL089183.](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL089183)
2. **Thermoacoustic instability** data are available in this repository [here](test_empirical/thermoacoustic/data/thermo_experiments). Data were collected by Induja Pavithran and R. I. Sujith and were first published in [Pavithran, I. and Sujith, R.I. "Effect of rate of change of parameter on early warning signals for critical transitions" Chaos: An Interdisciplinary Journal of Nonlinear Science 31.1 (2021): 013116.](https://aip.scitation.org/doi/full/10.1063/5.0025533?casa_token=isaRQyMz9J0AAAAA%3AnT4dG70bROSFkRSDm-7U6wDx20NTnSFuyUqAsobZKEjkwrnneG8ienGwLPkKmj56ZU7f3-aRH5F-&)
3. **Paleoclimate transition** data are available from the [World Data Center for Paleoclimatology](http://www.ncdc.noaa.gov/paleo/data.html), National Geophysical Data Center, Boulder, Colorado. Data were preprocessed according to the study [Dakos, Vasilis, et al. "Slowing down as an early warning signal for abrupt climate change." Proceedings of the National Academy of Sciences 105.38 (2008): 14308-14312.](https://www.pnas.org/content/105/38/14308.short)


## License
Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

Copyright © 2021, Thomas Bury (McGill University), Chris Bauch (University of Waterloo), Madhur Anand (University of Guelph)
