from src.utils.main_utils import load_numpy_array_data
from src.exception import SensorException
from src.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
import os,sys

from xgboost import XGBRFClassifier
from src.ml.metric.classification_metric import get_regression_score
from src.ml.model.estimator import SensorModel,SensorModel1
from src.utils.main_utils import save_object, load_object


class ModelTrainer:

    def __init__(self, model_trainer_config: ModelTrainerConfig,
                 data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise SensorException(e, sys)

    def perform_hyper_paramter_tunig(self):
        ...

    def train_model(self, x_train, y_train):
        try:
            xgb_clf = XGBRFClassifier()
            xgb_clf.fit(x_train, y_train)
            return xgb_clf
        except Exception as e:
            raise e

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model = self.train_model(x_train, y_train)
            model2=model

            y_train_pred = model.predict(x_train)
            print('diii')
            print(x_train)
            print(y_train_pred)
            print('koni')

            regression_train_metric = get_regression_score(y_true=y_train, y_pred=y_train_pred)
            print( regression_train_metric.f1_score)
            print('fo')

            if regression_train_metric.f1_score <= self.model_trainer_config.expected_accuracy:

                raise Exception("Trained model is not good to provide expected accuracy")

            y_test_pred = model.predict(x_test)
            regression_test_metric = get_regression_score(y_true=y_test, y_pred=y_test_pred)

            # Overfitting and Underfitting
            diff = abs(regression_train_metric.precision_score - regression_test_metric.precision_score)
            print(diff)
            if diff > self.model_trainer_config.overfitting_underfitting_threshold:

                raise Exception("Model is not good try to do more experimentation.")

            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            preprocessor2 = load_object(file_path=self.data_transformation_artifact.transformed_object2_file_path)

            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path, exist_ok=True)
            #sensor_model = SensorModel(preprocessor=preprocessor,preprocessor2=preprocessor2, model=model)
            #sensor_model = SensorModel1( model=model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=model)
            save_object(self.model_trainer_config.trained_model_file_path1, obj=model2)

            # model trainer artifact

            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=regression_train_metric,
                test_metric_artifact=regression_test_metric
               )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e, sys)