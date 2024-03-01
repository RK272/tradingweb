from src.entity.artifact_entity import ModelEvaluationArtifact
from src.exception import SensorException
from src.logger import logging
import sys
from src.utils.main_utils import  load_object
from src.entity.config_entity import  ModelPusherConfig

class model_pred:

    def __init__(self, modelpusherconfig:ModelPusherConfig
                ):

        try:
            self.modelpusherconfig =modelpusherconfig


        except Exception as e:
            raise SensorException(e, sys)
    def modelprediction(self,df):
        try:
           best_modelpath = self.modelpusherconfig.saved_model_path
           print(best_modelpath)
           latest_model = load_object(file_path=best_modelpath)
           print(latest_model)
           y_trained_pred = latest_model.predict(df)
           print("ronni")
           print(y_trained_pred)
           return y_trained_pred
        except Exception as e:
            raise SensorException(e, sys)