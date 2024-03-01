import os
from src.constant.s3_bucket import TRAINING_BUCKET_NAME
#SAVED_MODEL_DIR =os.path.join("saved_models")
TARGET_COLUMN='result'
MODEL_FILE_NAME = "model.pkl"
MODEL_FILE_NAME1 = "model1.pkl"
PIPELINE_NAME:str ="stock"
ARTIFACT_DIR:str ="artifact"
DATA_INGESTION_DIR_NAME:str ="data_ingestion"
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"
"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "BANKNIFTY"

DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2

SAVED_MODEL_DIR =os.path.join("saved_models")
SCHEMA_FILE_PATH = os.path.join("config", "schema.yaml")
FILE_NAME: str = "stock.csv"

"""
Data Validation realted contant start with DATA_VALIDATION VAR NAME
"""

DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
PREPROCSSING_OBJECT2_FILE_NAME = "preprocessing1.pkl"
PREPROCSSING_OBJECT3_FILE_NAME = "train.csv"


"""
Model Trainer ralated constant start with MODE TRAINER VAR NAME
"""

MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.01
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.7
"""
Model evaluater  ralated constant start with MODE TRAINER VAR NAME
"""
MODEL_EVALUATION_DIR_NAME: str = "model_evaluation"
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.02
MODEL_EVALUATION_REPORT_NAME= "report.yaml"

MODEL_PUSHER_DIR_NAME = "model_pusher"
MODEL_PUSHER_SAVED_MODEL_DIR = SAVED_MODEL_DIR



#FYERS DATA

APP_ID="YFMQL3S3NX"
APP_TYPE="100"
SECRET_KEY="0C9MJWWZWN"
client_id= "YFMQL3S3NX-100"
FY_ID="XR22283"
APP_ID_TYPE="2"
TOTP_KEY="7AGEJ4CNT3GO6SYKIE5EM5II64VB36MP"
PIN="4936"

REDIRECT_URI="http://trade.fyers.in/api-login/redirect-uri/index.html"



# API endpoints

BASE_URL = "https://api-t2.fyers.in/vagator/v2"
BASE_URL_2 = "https://api.fyers.in/api/v2"
URL_SEND_LOGIN_OTP = BASE_URL + "/send_login_otp"   #/send_login_otp_v2
URL_VERIFY_TOTP = BASE_URL + "/verify_otp"
URL_VERIFY_PIN = BASE_URL + "/verify_pin"
URL_TOKEN = BASE_URL_2 + "/token"
URL_VALIDATE_AUTH_CODE = BASE_URL_2 + "/validate-authcode"
SUCCESS = 1
ERROR = -1
