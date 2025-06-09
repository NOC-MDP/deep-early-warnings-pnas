from organise_data import organise_data
from compute_ews import compute_ews
from generate_nulls_ar1 import generate_nulls_ar1
from compute_ktau import compute_ktau
from dl_apply_len1500 import dl_apply_len1500
from dl_apply_len500 import dl_apply_len500
from organise_ml_data import organise_ml_data
from compute_roc import compute_roc
from clean import clean
import sys
from loguru import logger

# captures print statements and converts them to log info statements
class StreamToLoguru:
    def __init__(self, level="INFO"):
        self.level = level
        self._buffer = ""

    def write(self, message):
        if message.strip():  # Ignore empty lines
            logger.log(self.level, message.strip())

    def flush(self):
        pass  # No need to implement flush for loguru


def main():
    parameter = "DIN"
    logger.info(f"Running for Parameter: {parameter}")
    five_hundred = False
    # Set up Loguru
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # Redirect stdout and stderr
    sys.stdout = StreamToLoguru("INFO")
    sys.stderr = StreamToLoguru("ERROR")

    logger.info("Starting NEMO-MEDUSA prediction")
    logger.info("cleaning output directories")
    clean(five_hundred=five_hundred,parameter=parameter)
    logger.success("Done")
    logger.info("organising data")
    organise_data(parameter=parameter)
    logger.success("Done")
    logger.info("computing ews")
    compute_ews(parameter=parameter)
    logger.success("Done")
    logger.info("generating nulls")
    generate_nulls_ar1(parameter=parameter)
    logger.success("Done")
    logger.info("computing ktau")
    compute_ktau(parameter=parameter)
    logger.success("Done")
    logger.info("generating ML predictions")
    #tsid_vals = [1, 2, 3,4,5]
    tsid_vals = list(range(1,25))
    if five_hundred:
        dl_apply_len500(tsid_vals=tsid_vals,parameter=parameter)
    else:
        dl_apply_len1500(tsid_vals=tsid_vals,parameter=parameter)
    logger.success("Done")
    logger.info("organising ML predictions")
    organise_ml_data(five_hundred=five_hundred,parameter=parameter)
    logger.success("Done")
    logger.info("computing roc")
    if five_hundred:
        compute_roc(bool_pred_early=True,five_hundred=True,parameter=parameter)
        compute_roc(bool_pred_early=False,five_hundred=True,parameter=parameter)
    else:
        compute_roc(bool_pred_early=True,parameter=parameter)
        compute_roc(bool_pred_early=False,parameter=parameter)
    logger.success("Ran all tasks successfully!")


if __name__ == "__main__":
    main()