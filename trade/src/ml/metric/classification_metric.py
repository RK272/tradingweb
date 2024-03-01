from src.entity.artifact_entity import regressionMetricArtifact
from src.exception import SensorException
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import os,sys
import numpy as np

def get_regression_score(y_true,y_pred)->regressionMetricArtifact:
    try:
        f1 = f1_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred,zero_division=1)
        recall_scor1e = recall_score(y_true, y_pred)




        regression_metric =  regressionMetricArtifact(
                    f1_score=f1,
                    precision_score=precision,
                    recall_score=recall_scor1e
                    )
        return regression_metric
    except Exception as e:
        raise SensorException(e,sys)