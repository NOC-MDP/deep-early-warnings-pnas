from pathlib import Path
import os

def delete_all_files_in_dir(directory_path):
    dir_path = Path(directory_path)
    try:
        for file in dir_path.iterdir():
            if file.is_file():
                file.unlink()
    except FileNotFoundError:
        os.makedirs(directory_path, exist_ok=True)

def clean(five_hundred:bool):
    # delete any existing files from previous runs
    try:
        os.remove("data/transition_data.csv")
    except FileNotFoundError:
        pass
    if five_hundred:
        # TODO handle missing directories (do we make it or just ignore?)
        delete_all_files_in_dir("data/ml_preds/500")
        delete_all_files_in_dir("data/ml_preds/500/parsed")
        delete_all_files_in_dir("data/roc/500")
        delete_all_files_in_dir("figures/figs_roc/500")
    else:
        delete_all_files_in_dir("data/ml_preds/1500")
        delete_all_files_in_dir("data/ml_preds/1500/parsed")
        delete_all_files_in_dir("data/roc/1500")
        delete_all_files_in_dir("figures/figs_roc/1500")
    delete_all_files_in_dir("data/resids")
    delete_all_files_in_dir("data/ews")
