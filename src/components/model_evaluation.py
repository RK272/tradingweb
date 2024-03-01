from src.exception import SensorException
from src.logger import logging
from src.entity.artifact_entity import DataValidationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact,DataTransformationArtifact
from src.entity.config_entity import ModelEvaluationConfig
import os, sys
from src.ml.metric.classification_metric import get_regression_score
from src.ml.model.estimator import SensorModel
from src.utils.main_utils import save_object, load_object, write_yaml_file
from src.ml.model.estimator import ModelResolver
from src.constant.training_pipeline import TARGET_COLUMN
from src.ml.model.estimator import TargetValueMapping
import pandas as pd
import numpy as np


class ModelEvaluation:

    def __init__(self, model_eval_config: ModelEvaluationConfig,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact,
                 data_transformation_artifact:DataTransformationArtifact):

        try:
            self.model_eval_config = model_eval_config
            self.data_validation_artifact = data_validation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            valid_train_file_path = self.data_transformation_artifact.transformed_train_file_path1

            #valid_test_file_path = self.data_validation_artifact.valid_test_file_path
            #preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
            #print(preprocessor)
            # valid train and test file dataframe
            df = pd.read_csv(valid_train_file_path)
            #test_df = pd.read_csv(valid_test_file_path)
           # print("traindf")
            #print(train_df)
           # print("testdf")
            #print(test_df)

            #df = pd.concat([train_df, test_df])
           # print("df    ")
            #print(df)
            y_true = df[TARGET_COLUMN]
            y_true=y_true.replace(TargetValueMapping().to_dict())

            df=df.drop(columns=[TARGET_COLUMN], axis=1)
            #print("0")
            #print(df)
            #preprocessor.fit(df)
            #print("1")
            #df = preprocessor.transform(df)
            #print(df)
            #train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]


            train_model_file_path = self.model_trainer_artifact.trained_model_file_path
            model_resolver = ModelResolver()
            is_model_accepted = True

            if not model_resolver.is_model_exists():
                model_evaluation_artifact = ModelEvaluationArtifact(
                    is_model_accepted=is_model_accepted,
                    improved_accuracy=None,
                    best_model_path=None,
                    trained_model_path=train_model_file_path,
                    train_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,
                    best_model_metric_artifact=None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact

            latest_model_path = model_resolver.get_best_model_path()
            latest_model = load_object(file_path=latest_model_path)
            train_model = load_object(file_path=train_model_file_path)
            print("rit")
            print(df)

            y_trained_pred = train_model.predict(df)
            print(y_trained_pred)
            print(df)
            #df=df.drop(columns=["high","low"], axis=1)
            print(df)
            y_latest_pred = latest_model.predict(df)

            trained_metric = get_regression_score(y_true, y_trained_pred)
            latest_metric = get_regression_score(y_true, y_latest_pred)

            improved_accuracy = trained_metric.f1_score - latest_metric.f1_score
            if self.model_eval_config.change_threshold < improved_accuracy:
                # 0.02 < 0.03
                is_model_accepted = True
            else:
                is_model_accepted = False

            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted=is_model_accepted,
                improved_accuracy=improved_accuracy,
                best_model_path=latest_model_path,
                trained_model_path=train_model_file_path,
                train_model_metric_artifact=trained_metric,
                best_model_metric_artifact=latest_metric)

            model_eval_report = model_evaluation_artifact.__dict__

            # save the report
            write_yaml_file(self.model_eval_config.report_file_path, model_eval_report)
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact

        except Exception as e:
            raise SensorException(e, sys)




