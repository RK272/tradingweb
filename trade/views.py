from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
import pandas as pd
import pandas_ta as ta

from django.http import JsonResponse
from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import SensorException
from src.configuration.mongo_db_connection import MongoDBClient
from src.exception import SensorException
import os,sys
import numpy as np
from src.components.model_prediction import model_pred
import os
from src.entity.config_entity import fyersdataconfig
import pandas as pd
from src.utils.main_utils import  load_object

from src.components.fyers import fyersdatageneration

from src.entity.artifact_entity import ModelEvaluationArtifact
from src.ml.model.estimator import ModelResolver
from src.logger import logging
from src.pipeline import training_pipeline
from src.pipeline.training_pipeline import TrainPipeline
import os
from src.utils.main_utils import read_yaml_file
from src.constant.training_pipeline import SAVED_MODEL_DIR
from wsgiref import simple_server
import os,sys
import csv
import pandas as pd
import json
import time
import pandas as pd
import datetime
import pytz
import os
import requests
import pyotp
from urllib.parse import parse_qs, urlparse
import sys
from fyers_api import fyersModel
from fyers_api import accessToken
from src.entity.config_entity import fyersdataconfig
from src.exception import SensorException
from django.contrib.auth.decorators import login_required
import numpy as np
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
import time
import pandas as pd
import datetime
import pytz
import os
import requests
import pyotp
from urllib.parse import parse_qs,urlparse
import sys
from fyers_api import fyersModel
from fyers_api import accessToken
from src.entity.config_entity import fyersdataconfig
from src.exception import SensorException
from src.logger import logging
from src.pipeline import training_pipeline
from src.pipeline.training_pipeline import TrainPipeline
import os
from src.utils.main_utils import read_yaml_file
from src.constant.training_pipeline import SAVED_MODEL_DIR
from wsgiref import simple_server
import requests
from django.contrib.auth.models import User
import pyotp
import datetime
import time
from urllib.parse import urlparse, parse_qs
import os
import pandas as pd
import pymongo
import json
from django.http import JsonResponse
import csv
import logging
import sys  #
from src.components.model_prediction import model_pred
import os
from src.entity.config_entity import fyersdataconfig
import pandas as pd
from src.utils.main_utils import  load_object


from src.components.fyers import fyersdatageneration

# Create your views here.
from src.configuration.mongo_db_connection import MongoDBClient
print("done")
from src.exception import SensorException
import os,sys
import numpy as np
from src.logger import logging
from src.pipeline import training_pipeline
from src.pipeline.training_pipeline import TrainPipeline
import os
from src.utils.main_utils import read_yaml_file
from src.constant.training_pipeline import SAVED_MODEL_DIR
from src.components.model_prediction import model_pred
import os
from src.entity.config_entity import fyersdataconfig
import pandas as pd
from src.utils.main_utils import  load_object
from src.ml.model.estimator import ModelResolver
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.http import JsonResponse

def home(request):
    return render(request, 'trade/index.html')
def about(request):
    return render(request, 'trade/about.html')
def login(request):
    return render(request, 'trade/login.html')

@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def prediction(request):

    if request.method == 'POST':
        start_date = request.POST.get("startDate")
        end_date = request.POST.get("endDate")
        symbol = request.POST.get("symbol")
        print(start_date)
        print(type(start_date))
        train_pipeline = TrainPipeline(start_date, end_date, symbol)
        train_pipeline.run_pipeline()
        print("all done")
        output={
            'output':'sucess'
        }

        return render(request,'trade/prediction.html',output)


    else:
        return render(request, 'trade/prediction.html')
@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def training(request):
    if request.method == 'POST':
        try:


            RSI_Crossed_40 = request.POST.get('14rsicrossed40')
            rsi9m = request.POST.get('rsi9m')
            EMA20 = request.POST.get('EMA20')
            EMA5 = request.POST.get('EMA5')
            print(EMA5)

            data_dict = {
                'RSI_Crossed_40': [RSI_Crossed_40],
                'rsi9m': [rsi9m],
                'EMA20': [EMA20],
                'EMA5': [EMA5]
            }

            df = pd.DataFrame(data_dict)

            model_resolver = ModelResolver(model_dir=SAVED_MODEL_DIR)
            if not model_resolver.is_model_exists():
                return JsonResponse({"error": "Model is not available"}, status=500)

            best_model_path = model_resolver.get_best_model_path()
            model = load_object(best_model_path)  # Replace load_model with your model loading logic

            train_arr = df.values  # Convert DataFrame to numpy array
            print(train_arr)
            prediction_result = model.predict(train_arr)

            if prediction_result[0]==1:
                a="sucsess"
            else:
                a='failed'

            output = {
                'output': a
            }

            return render(request, 'trade/training.html', output)


        except Exception as e:
            return render(request, 'trade/training.html', {'output': 'error'})
    else:
        return render(request, 'trade/training.html')
@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def updatedb(request):
    if request.method == 'POST':
        try:
            start_date = request.POST.get("startDate")
            end_date = request.POST.get("endDate")
            symbol = request.POST.get("symbol")

            fyersdataconfig1 = fyersdataconfig()

            def send_login_otp(fy_id, app_id):
                try:
                    result_string = requests.post(url=fyersdataconfig1.URL_SEND_LOGIN_OTP,
                                                  json={"fy_id": fy_id, "app_id": app_id})
                    if result_string.status_code != 200:
                        return [fyersdataconfig1.ERROR, result_string.text]
                    result = result_string.json()  # Use .json() instead of json.loads
                    request_key = result["request_key"]
                    return [fyersdataconfig1.SUCCESS, request_key]
                except Exception as e:
                    return [fyersdataconfig1.ERROR, str(e)]

            def verify_totp(request_key, totp):
                try:
                    result_string = requests.post(url=fyersdataconfig1.URL_VERIFY_TOTP,
                                                  json={"request_key": request_key, "otp": totp})
                    if result_string.status_code != 200:
                        return [fyersdataconfig1.ERROR, result_string.text]
                    result = result_string.json()  # Use .json() instead of json.loads
                    request_key = result["request_key"]
                    return [fyersdataconfig1.SUCCESS, request_key]
                except Exception as e:
                    return [fyersdataconfig1.ERROR, str(e)]

            def datageneration():
                session = accessToken.SessionModel(client_id=fyersdataconfig1.client_id,
                                                   secret_key=fyersdataconfig1.SECRET_KEY,
                                                   redirect_uri=fyersdataconfig1.REDIRECT_URI,
                                                   response_type='code', grant_type='authorization_code')

                urlToActivate = session.generate_authcode()
                print(f'URL to activate APP:  {urlToActivate}')
                send_otp_result = send_login_otp(fy_id=fyersdataconfig1.FY_ID,
                                                 app_id=fyersdataconfig1.APP_ID_TYPE)

                if send_otp_result[0] != fyersdataconfig1.SUCCESS:
                    print(f"send_login_otp failure - {send_otp_result[1]}")
                    # sys.exit()  # Remove this line
                else:
                    print("send_login_otp success")

                # Step 2 - Verify totp and get request key from verify_otp API
                for i in range(1, 3):
                    request_key = send_otp_result[1]
                    verify_totp_result = verify_totp(request_key=request_key,
                                                     totp=pyotp.TOTP(fyersdataconfig1.TOTP_KEY).now())
                    if verify_totp_result[0] != fyersdataconfig1.SUCCESS:
                        print(f"verify_totp_result failure - {verify_totp_result[1]}")
                        time.sleep(1)
                    else:
                        print(f"verify_totp_result success {verify_totp_result}")
                        break

                request_key_2 = verify_totp_result[1]

                # Step 3 - Verify pin and send back access token
                ses = requests.Session()
                payload_pin = {"request_key": f"{request_key_2}", "identity_type": "pin",
                               "identifier": f"{fyersdataconfig1.PIN}", "recaptcha_token": ""}
                res_pin = ses.post('https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()
                if 'data' in res_pin:
                    print(res_pin['data'])
                else:
                    print("No 'data' key found in res_pin dictionary")

                session = accessToken.SessionModel(client_id=fyersdataconfig1.client_id,
                                                   secret_key=fyersdataconfig1.SECRET_KEY,
                                                   redirect_uri=fyersdataconfig1.REDIRECT_URI,
                                                   response_type='code', grant_type='authorization_code')

                urlToActivate = session.generate_authcode()
                print(f'URL to activate APP:  {urlToActivate}')

                # Step 1 - Retrieve request_key from send_login_otp API
                send_otp_result = send_login_otp(fy_id=fyersdataconfig1.FY_ID,
                                                 app_id=fyersdataconfig1.APP_ID_TYPE)

                if send_otp_result[0] != fyersdataconfig1.SUCCESS:
                    print(f"send_login_otp failure - {send_otp_result[1]}")
                    # sys.exit()  # Remove this line
                else:
                    print("send_login_otp success")

                # Step 2 - Verify totp and get request key from verify_otp API
                for i in range(1, 3):
                    request_key = send_otp_result[1]
                    verify_totp_result = verify_totp(request_key=request_key,
                                                     totp=pyotp.TOTP(fyersdataconfig1.TOTP_KEY).now())
                    if verify_totp_result[0] != fyersdataconfig1.SUCCESS:
                        print(f"verify_totp_result failure - {verify_totp_result[1]}")
                        time.sleep(1)
                    else:
                        print(f"verify_totp_result success {verify_totp_result}")
                        break

                request_key_2 = verify_totp_result[1]

                # Step 3 - Verify pin and send back access token
                ses = requests.Session()
                payload_pin = {"request_key": f"{request_key_2}", "identity_type": "pin",
                               "identifier": f"{fyersdataconfig1.PIN}", "recaptcha_token": ""}
                res_pin = ses.post('https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()
                print(res_pin['data'])
                ses.headers.update({'authorization': f"Bearer {res_pin['data']['access_token']}"})

                authParam = {"fyers_id": fyersdataconfig1.FY_ID, "app_id": fyersdataconfig1.APP_ID,
                             "redirect_uri": fyersdataconfig1.REDIRECT_URI,
                             "appType": fyersdataconfig1.APP_TYPE, "code_challenge": "", "state": "None",
                             "scope": "",
                             "nonce": "", "response_type": "code", "create_cookie": True}
                authres = ses.post('https://api.fyers.in/api/v2/token', json=authParam).json()
                print(authres)
                url = authres['Url']
                print(url)
                parsed = urlparse(url)
                auth_code = parse_qs(parsed.query)['auth_code'][0]
                session.set_token(auth_code)
                response = session.generate_token()
                access_token = response["access_token"]
                print(access_token)

                fyers = fyersModel.FyersModel(client_id=fyersdataconfig1.client_id, token=access_token,
                                              log_path=os.getcwd())
                print(fyers.get_profile())
                return fyers

                # Implementation goes here...

            def historical_bydate(symbol, sd, ed, interval=1):
                data = {"symbol": symbol, "resolution": "1", "date_format": "1", "range_from": str(sd),
                        "range_to": str(ed), "cont_flag": "1"}
                fyers_instance = datageneration()  # Assuming datageneration is defined elsewhere
                nx = fyers_instance.history(data)
                cols = ['datetime', 'open', 'high', 'low', 'close', 'volume']
                df = pd.DataFrame.from_dict(nx['candles'])
                df.columns = cols
                df['datetime'] = pd.to_datetime(df['datetime'], unit="s")
                df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
                df['datetime'] = df['datetime'].dt.tz_localize(None)
                return df
                # Implementation goes here...

            df = pd.DataFrame()

            sd = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
            enddate = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

            n = abs((sd - enddate).days)
            ab = None

            while ab is None:
                sd_date = sd
                ed_date = sd_date + datetime.timedelta(days=99 if n > 99 else n)  # Update end date here
                sd_str = sd_date.strftime("%Y-%m-%d")
                ed_str = ed_date.strftime("%Y-%m-%d")

                dx = historical_bydate(symbol, sd_date, ed_date)  # Pass the start and end dates here
                df = df.append(dx)

                n -= 100 if n > 100 else n
                if n == 0:
                    ab = "done"
                else:
                    sd = ed_date + datetime.timedelta(days=1)  # Update start date for the next iteration

            # Drop the 'volume' column
            df = df.drop(columns=['volume'], axis=1)

            # Save DataFrame to CSV
            df.to_csv('1RELIANCE66.csv', index=False)

            # Insert data into MongoDB
            client = pymongo.MongoClient(
                "mongodb+srv://rithin:076ecHwHg60yETd9@cluster0.ctrleyy.mongodb.net/?retryWrites=true&w=majority")
            DATABASE_NAME = "TRADERZSPOT"
            DB = client[DATABASE_NAME]
            collection = symbol

            if collection in DB.list_collection_names():
                c = DB[collection]
                with open('1RELIANCE66.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = list(reader)
                    c.insert_many(data)
                    pipeline = [
                        {"$group": {"_id": "$datetime", "count": {"$sum": 1}, "ids": {"$addToSet": "$_id"}}},
                        {"$match": {"count": {"$gt": 1}}}
                    ]
                    duplicate_documents = c.aggregate(pipeline)

                    # Remove duplicates, keeping one occurrence
                    for document in duplicate_documents:
                        del document['ids'][0]  # Keep the first occurrence
                        c.delete_many({"_id": {"$in": document['ids']}})
                        print(f"Removed duplicates for datetime {document['_id']}.")
            else:
                c = DB[collection]
                with open('1RELIANCE66.csv', 'r') as file:
                    reader = csv.DictReader(file)
                    data = list(reader)
                    c.insert_many(data)

            print("all done")
            output = {
                'output': 'success'
            }

            return render(request, 'trade/updatedb.html', output)

        except Exception as e:
            print(e)
            logging.exception(e)
            return render(request, 'trade/updatedb.html', {'output': 'error'})
    else:
        return render(request, 'trade/updatedb.html')
@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def contact(request):
    return render(request, 'trade/contact.html')

from django.shortcuts import render
import pandas as pd
import json

@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def candlestick_chart_view(request):
    if request.method == 'POST':



        symbol = request.POST.get("symbol")
        client = MongoClient("mongodb+srv://rithin:076ecHwHg60yETd9@cluster0.ctrleyy.mongodb.net/?retryWrites=true&w=majority")
        DATABASE_NAME = "TRADERZSPOT"
        DB = client[DATABASE_NAME]
        collection_name = symbol

        collection = client[DATABASE_NAME][collection_name]
        df = pd.DataFrame(list(collection.find()))

        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"], axis=1)
        df.replace({"na": np.nan}, inplace=True)
        print(df)
        df['time'] = pd.to_datetime(df['datetime'])
        df['time'] = (df['time'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
        df = df[['time', 'open', 'high', 'low', 'close']].copy()
        #df.to_csv('expensewebsite/static/js/torc5.csv', index=False)
        #df=pd.read_csv("expensewebsite/static/js/torc5.csv")

        #window = 10
        #df['sma'] = df['close'].rolling(window=window).mean()
       # print(df)
        #period = 5
        #df['ema'] = ta.ema(df['close'], length=period)
        #print("ri")




        #df = df.drop(df.index[:10])

        # Reset index if needed
        #df = df.reset_index(drop=True)
        #df['long'] = False
        #df['short'] = False

        # Check for crossover conditions
        #for i in range(1, len(df)):
            #if df['ema'][i] > df['sma'][i] and df['ema'][i - 1] <= df['sma'][i - 1]:
                #df.at[i, 'long'] = True
            #elif df['ema'][i] < df['sma'][i] and df['ema'][i - 1] >= df['sma'][i - 1]:
                #df.at[i, 'short'] = True
        #df['rsi'] = ta.rsi(df['close'])
        #df = df.drop(range(15))
        #df = df.reset_index(drop=True)
        #print(df)

        df.to_csv('expensewebsite/static/js/TORC6.csv', index=False)
        input_file='expensewebsite/static/js/TORC6.csv'
        output_file='expensewebsite/static/js/data.csv'
        with open(output_file, 'w', newline='') as clear_file:
            clear_file.write('')  # This will clear the content of the file

        # Now copy content from input file to output file, skipping the header
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            # Skip the first row (header) from the input file
            next(reader)

            # Copy remaining rows from input file to output file
            for row in reader:
                writer.writerow(row)
    #df=pd.read_csv('1min.csv')
    #df['datetime'] = pd.to_datetime(df['datetime'])
    #df['timestamp'] = (df['datetime'] - pd.Timestamp("1970-01-01")) // pd.Timedelta('1ms')
    #df11 = df[['timestamp', 'open', 'high', 'low', 'close']].copy()

    #df11.to_csv('expensewebsite/static/js/torc2.csv', index=False)
    # Sample DataFrame creation (Replace this with your DataFrame)

    return render(request, 'trade/cad.html')

@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def tab(request):
    if request.method == 'POST':



        symbol = request.POST.get("symbol")
        client = MongoClient("mongodb+srv://rithin:076ecHwHg60yETd9@cluster0.ctrleyy.mongodb.net/?retryWrites=true&w=majority")
        DATABASE_NAME = "TRADERZSPOT"
        DB = client[DATABASE_NAME]
        collection_name = symbol

        collection = client[DATABASE_NAME][collection_name]
        df = pd.DataFrame(list(collection.find()))
        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"], axis=1)
        df.replace({"na": np.nan}, inplace=True)
        df1=df.tail(10)
        df1.to_csv('expensewebsite/static/js/kon1.csv')
        df.to_csv('expensewebsite/static/js/kon.csv')


    return render(request, 'trade/tab.html')


@login_required(login_url='http://127.0.0.1:8000/authentication/login')
def trainRouteClient(request):

    try:
        if request.method =='POST':

            start_date = request.POST.get("startDate")
            end_date = request.POST.get("endDate")
            symbol =request.POST.get("symbol")
            print(start_date)
            print(type(start_date))
            train_pipeline = TrainPipeline(start_date,end_date,symbol)
            train_pipeline.run_pipeline()
            return JsonResponse({"message": "Training pipeline successfully executed."})


    except Exception as e:
        print(e)
        logging.exception(e)
        return JsonResponse({"error": str(e)}, status=500)
