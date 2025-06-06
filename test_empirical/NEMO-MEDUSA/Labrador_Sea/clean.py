from pathlib import Path
import os

def delete_all_files_in_dir(directory_path):
    dir_path = Path(directory_path)
    os.makedirs(dir_path, exist_ok=True)
    for file in dir_path.iterdir():
        if file.is_file():
            file.unlink()

def clean(five_hundred:bool,parameter:str):
    # delete any existing files from previous runs
    try:
        os.remove(f"data/{parameter}transition_data.csv")
    except FileNotFoundError:
        pass
    if five_hundred:
        ts_len = "500"
    else:
        ts_len = "1500"
    # TODO handle missing directories (do we make it or just ignore?)
    delete_all_files_in_dir(f"results/{parameter}/ml_preds/{ts_len}")
    delete_all_files_in_dir(f"results/{parameter}/ml_preds/{ts_len}/parsed")
    delete_all_files_in_dir(f"results/{parameter}/roc/{ts_len}")
    delete_all_files_in_dir(f"figures/figs_roc_{parameter}/{ts_len}")

    delete_all_files_in_dir(f"results/{parameter}/resids")
    delete_all_files_in_dir(f"results/{parameter}/ews")

if __name__ == "__main__":
    clean(five_hundred=False,parameter="CHL")