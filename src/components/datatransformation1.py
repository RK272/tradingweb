from sklearn.base import BaseEstimator, TransformerMixin
import pandas_ta as ta
import pandas as pd

class NameDropper(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X.drop(['datetime'], axis=1)

class rsi(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self


    def transform(self, X):
        X['rsi']=ta.rsi(X.close,length=14)
        X['rsi9'] = ta.rsi(X.close, length=9)
        X['ema20']=ta.ema(X.close,length=20)
        X['ema5'] = ta.ema(X.close, length=5)
        #X['ema100']=ta.ema(X.close,length=100)
        #X['ema200'] = ta.ema(X.close, length=200)
        return X

class generate_rsi_crosover_sucsess(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        crossed_40 = False
        crossed_40_rsi = None
        crossed_40_data = None
        filtered_data = []
        for index, row in X.iterrows():
            if row['rsi'] > 40 and not crossed_40 and (index == 0 or X.loc[index - 1, 'rsi'] < 40):
                crossed_40 = True
                crossed_40_rsi = row['rsi']
                crossed_40_date = row['datetime']
                crossed_40rsi5m = row['rsi9']
                crossed_4015min = row['ema20']
                crossed_401h = row['ema5']

            elif crossed_40 and row['rsi'] < 40:
                crossed_40 = False
            elif crossed_40 and row['rsi'] >= 60 and row['rsi'] >= crossed_40_rsi:
                filtered_data.append({'DateTime': crossed_40_date, 'RSI_Crossed_40': crossed_40_rsi,
                     'rsi9m': crossed_40rsi5m, 'EMA20': crossed_4015min, 'EMA5': crossed_401h})
                crossed_40 = False

        # Create a new DataFrame from the filtered data
        result_df1 = pd.DataFrame(filtered_data)
        print("jocky")
        print(result_df1)
        print("kakki")
        return result_df1


class generate_rsi_crosover_sucsess1(BaseEstimator,TransformerMixin):
    def fit(self,X,y=None):
        return self
    def transform(self,X):
        crossed_40 = False
        crossed_40_rsi = None
        crossed_40_data = None
        filtered_data = []
        for index, row in X.iterrows():
            if row['rsi'] > 40 and not crossed_40 and (index == 0 or X.loc[index - 1, 'rsi'] < 40):
                crossed_40 = True
                crossed_40_rsi = row['rsi']
                crossed_40_date = row['datetime']
                crossed_40rsi5m = row['rsi9']
                crossed_4015min = row['ema20']
                crossed_401h = row['ema5']

            elif crossed_40 and row['rsi'] < 40:
                crossed_40 = False


                filtered_data.append({'DateTime': crossed_40_date, 'RSI_Crossed_40': crossed_40_rsi,
                     'rsi9m': crossed_40rsi5m, 'EMA20': crossed_4015min, 'EMA5': crossed_401h})


        # Create a new DataFrame from the filtered data
        result_df1 = pd.DataFrame(filtered_data)
        print("jocky")
        print(result_df1)
        print("kakki")
        return result_df1




"""class GenerateRSICrossoverSuccess(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        crossed_40 = False
        crossed_40_rsi = None
        crossed_40_rsi9m = None
        crossed_40_ema5 = None
        crossed_40_ema20 = None
        filtered_data = []

        for index, row in X.iterrows():
            if row['rsi'] > 40 and not crossed_40 and (index == 0 or X.loc[index - 1, 'rsi'] < 40):
                crossed_40_rsi = row['rsi']
                crossed_40_date = pd.to_datetime(
                    row['datetime']).timestamp()  # Convert datetime string to timestamp (float)
                crossed_40_rsi9m = row['rsi9']
                crossed_40_ema5 = row['ema5']
                crossed_40_ema20 = row['ema20']

                filtered_data.append(
                    {'datetime': float(crossed_40_date), 'RSI_Crossed_40': crossed_40_rsi, 'RSI_9': crossed_40_rsi9m,
                     'ema5': crossed_40_ema5, 'ema20': crossed_40_ema20})

        return pd.DataFrame(filtered_data)"""

