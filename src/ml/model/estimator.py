from src.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import pandas as pd
import datetime
from datetime import datetime
from src.constant.training_pipeline import TARGET_COLUMN
class TargetValueMapping:
    def __init__(self):
        self.neg: int = 0
        self.pos: int = 1

    def to_dict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self.to_dict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class SensorModel:

    def __init__(self,preprocessor,preprocessor2, model):
        try:
            self.preprocessor = preprocessor
            self.preprocessor2=preprocessor2
            self.model = model
        except Exception as e:
            raise e

    def predict(self, x):
        try:
            result_df3= self.preprocessor.transform(x)
            result_df33 = self.preprocessor2.transform(x)
            date_format = "%Y-%m-%d %H:%M:%S"
            result_df33['NumericTimestamp1'] = result_df33['DateTime'].apply(
                lambda x: datetime.strptime(x, date_format).timestamp())

            result_df3['NumericTimestamp'] = result_df3['DateTime'].apply(
                lambda x: datetime.strptime(x, date_format).timestamp())
            df3 = result_df3
            df33 = result_df33
            matching_rows_large = df33[df33['NumericTimestamp1'].isin(df3['NumericTimestamp'])]

            # Get the remaining rows from the larger DataFrame
            df33 = df33[~df33['NumericTimestamp1'].isin(df3['NumericTimestamp'])]
            df33 = df33.reset_index(drop=True)
            num_rows = len(df33)
            new_column_name = 'result'

            # Set the first 4272 rows to 0, leaving the rest unchanged
            df33[new_column_name] = 0
            df33.loc[:num_rows - 1, new_column_name] = 0
            num_rows1 = len(df3)
            new_column_name = 'result'

            # Set the first 4272 rows to 0, leaving the rest unchanged
            df3[new_column_name] = 1
            df3.loc[:num_rows - 1, new_column_name] = 1
            combined_df = pd.concat([df3, df33], ignore_index=True)
            train_df = combined_df.drop(columns=['DateTime', 'NumericTimestamp', 'NumericTimestamp1'], axis=1)
            train_df = train_df.sample(frac=1, random_state=42).reset_index(drop=True)
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)

            #target_feature_train_df = train_df[TARGET_COLUMN]
            #target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            y_hat = self.model.predict(input_feature_train_df)

            return y_hat
        except Exception as e:
            raise e
class SensorModel1:

    def __init__(self, model):
        try:
            #elf.preprocessor = preprocessor
            #self.preprocessor2=preprocessor2
            self.model = model
        except Exception as e:
            raise e

    def predict(self, x):
        try:


            # Set the first 4272 rows to 0, leaving the rest unchanged

            #target_feature_train_df = train_df[TARGET_COLUMN]
            #target_feature_train_df = target_feature_train_df.replace(TargetValueMapping().to_dict())

            y_hat = self.model.predict(x)

            return y_hat
        except Exception as e:
            raise e


class ModelResolver:

    def __init__(self, model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise e

    def get_best_model_path(self, ) -> str:
        try:
            timestamps = list(map(int, os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path = os.path.join(self.model_dir, f"{latest_timestamp}", MODEL_FILE_NAME)
            return latest_model_path
        except Exception as e:
            raise e

    def is_model_exists(self) -> bool:
        try:
            if not os.path.exists(self.model_dir):
                return False

            timestamps = os.listdir(self.model_dir)
            if len(timestamps) == 0:
                return False

            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as e:
            raise e
