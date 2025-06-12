from scripts.organise_data import organise_data
from scripts.compute_ews import compute_ews
from scripts.generate_nulls_ar1 import generate_nulls_ar1
from scripts.compute_ktau import compute_ktau
from scripts.dl_apply_len1500 import dl_apply_len1500
from scripts.dl_apply_len500 import dl_apply_len500
from scripts.organise_ml_data import organise_ml_data
from scripts.compute_roc import compute_roc
from scripts.clean import clean
import sys
from loguru import logger
import click

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

@click.command()
@click.option('--parameter',required=True,help="parameter to use in prediction")
@click.option("--region",default="Labrador_Sea",help="region to apply predictions")
@click.option('--five_hundred',is_flag=True,help="run 500 length timeseries predictor if true 1500 if not")
def main(parameter:str,five_hundred:bool,region:str):
    # TODO get from the transitions json file
    tsid_vals = list(range(1,25))
    # valid parameter
    if parameter not in ["MLD", "CHL", "DIN", "TOS","ZOS"]:
        raise Exception(f"unknown parameter: {parameter}")
    logger.info(f"Running for Parameter: {parameter}")
    # valid region
    regions = ["Labrador_Sea","Irminger_Sea","West_Scotland"]
    if region not in regions:
        logger.error(f"{region} not in {regions}")
        raise Exception(f"unknown region: {region}")

    if five_hundred:
        logger.info("Running with 500 length timeseries predictor")
    else:
        logger.info("Running with 1500 length timeseries predictor")

    # Set up Loguru
    logger.remove()
    logger.add(sys.stderr, level="INFO")

    # Redirect stdout and stderr
    sys.stdout = StreamToLoguru("INFO")
    sys.stderr = StreamToLoguru("ERROR")

    logger.info("Starting NEMO-MEDUSA prediction")
    logger.info("cleaning output directories")
    clean(five_hundred=five_hundred,parameter=parameter,region=region)
    logger.success("Done")
    logger.info("organising data")
    organise_data(parameter=parameter,region=region)
    logger.success("Done")
    logger.info("computing ews")
    compute_ews(parameter=parameter,region=region)
    logger.success("Done")
    logger.info("generating nulls")
    generate_nulls_ar1(parameter=parameter,region=region)
    logger.success("Done")
    logger.info("computing ktau")
    compute_ktau(parameter=parameter,region=region)
    logger.success("Done")
    logger.info("generating ML predictions")

    if five_hundred:
        dl_apply_len500(tsid_vals=tsid_vals,parameter=parameter,region=region)
    else:
        dl_apply_len1500(tsid_vals=tsid_vals,parameter=parameter,region=region)
    logger.success("Done")
    logger.info("organising ML predictions")
    organise_ml_data(five_hundred=five_hundred,parameter=parameter,region=region)
    logger.success("Done")
    logger.info("computing roc")
    if five_hundred:
        compute_roc(bool_pred_early=True,five_hundred=True,parameter=parameter,region=region)
        compute_roc(bool_pred_early=False,five_hundred=True,parameter=parameter,region=region)
    else:
        compute_roc(bool_pred_early=True,parameter=parameter,region=region)
        compute_roc(bool_pred_early=False,parameter=parameter,region=region)
    logger.success("Ran all tasks successfully!")


if __name__ == "__main__":
    main()
