import pandas as pd
import json
import time
import pymongo
from pymongo import MongoClient
import pandas as pd
import datetime
import numpy as np
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

##3dfuyghiiiiiiiiiijkkkkkkkkjklddddddddddddddddddddddddddddddddddddddd


#gifffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

class fyersdatageneration:
    def __init__(self, fyersdataconfig1: fyersdataconfig):
        try:
            self.fyersdataconfig1 = fyersdataconfig1
        except Exception as e:
            raise SensorException(e, sys)

    def send_login_otp(self, fy_id, app_id):
        try:
            result_string = requests.post(url=self.fyersdataconfig1.URL_SEND_LOGIN_OTP, json={"fy_id": fy_id, "app_id": app_id})
            if result_string.status_code != 200:
                return [self.fyersdataconfig1.ERROR, result_string.text]
            result = json.loads(result_string.text)
            request_key = result["request_key"]
            return [self.fyersdataconfig1.SUCCESS, request_key]
        except Exception as e:
            return [self.fyersdataconfig1.ERROR, e]

    def verify_totp(self, request_key, totp):
        try:
            result_string = requests.post(url=self.fyersdataconfig1.URL_VERIFY_TOTP,
                                          json={"request_key": request_key, "otp": totp})
            if result_string.status_code != 200:
                return [self.fyersdataconfig1.ERROR, result_string.text]
            result = json.loads(result_string.text)
            request_key = result["request_key"]
            return [self.fyersdataconfig1.SUCCESS, request_key]
        except Exception as e:
            return [self.fyersdataconfig1.ERROR, e]

    def datageneration(self):
        session = accessToken.SessionModel(client_id=self.fyersdataconfig1.client_id,
                                           secret_key=self.fyersdataconfig1.SECRET_KEY,
                                           redirect_uri=self.fyersdataconfig1.REDIRECT_URI,
                                           response_type='code', grant_type='authorization_code')

        urlToActivate = session.generate_authcode()
        print(f'URL to activate APP:  {urlToActivate}')

        # Step 1 - Retrieve request_key from send_login_otp API
        send_otp_result = self.send_login_otp(fy_id=self.fyersdataconfig1.FY_ID, app_id=self.fyersdataconfig1.APP_ID_TYPE)

        if send_otp_result[0] != self.fyersdataconfig1.SUCCESS:
            print(f"send_login_otp failure - {send_otp_result[1]}")
            sys.exit()
        else:
            print("send_login_otp success")

        # Step 2 - Verify totp and get request key from verify_otp API
        for i in range(1, 3):
            request_key = send_otp_result[1]
            verify_totp_result = self.verify_totp(request_key=request_key,
                                                  totp=pyotp.TOTP(self.fyersdataconfig1.TOTP_KEY).now())
            if verify_totp_result[0] != self.fyersdataconfig1.SUCCESS:
                print(f"verify_totp_result failure - {verify_totp_result[1]}")
                time.sleep(1)
            else:
                print(f"verify_totp_result success {verify_totp_result}")
                break

        request_key_2 = verify_totp_result[1]

        # Step 3 - Verify pin and send back access token
        ses = requests.Session()
        payload_pin = {"request_key": f"{request_key_2}", "identity_type": "pin",
                       "identifier": f"{self.fyersdataconfig1.PIN}", "recaptcha_token": ""}
        res_pin = ses.post('https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()
        if 'data' in res_pin:
            print(res_pin['data'])
        else:
            print("No 'data' key found in res_pin dictionary")

        session = accessToken.SessionModel(client_id=self.fyersdataconfig1.client_id,
                                           secret_key=self.fyersdataconfig1.SECRET_KEY,
                                           redirect_uri=self.fyersdataconfig1.REDIRECT_URI,
                                           response_type='code', grant_type='authorization_code')

        urlToActivate = session.generate_authcode()
        print(f'URL to activate APP:  {urlToActivate}')

        # Step 1 - Retrieve request_key from send_login_otp API
        send_otp_result = self.send_login_otp(fy_id=self.fyersdataconfig1.FY_ID, app_id=self.fyersdataconfig1.APP_ID_TYPE)

        if send_otp_result[0] != self.fyersdataconfig1.SUCCESS:
            print(f"send_login_otp failure - {send_otp_result[1]}")
            sys.exit()
        else:
            print("send_login_otp success")

        # Step 2 - Verify totp and get request key from verify_otp API
        for i in range(1, 3):
            request_key = send_otp_result[1]
            verify_totp_result = self.verify_totp(request_key=request_key,
                                                  totp=pyotp.TOTP(self.fyersdataconfig1.TOTP_KEY).now())
            if verify_totp_result[0] != self.fyersdataconfig1.SUCCESS:
                print(f"verify_totp_result failure - {verify_totp_result[1]}")
                time.sleep(1)
            else:
                print(f"verify_totp_result success {verify_totp_result}")
                break

        request_key_2 = verify_totp_result[1]

        # Step 3 - Verify pin and send back access token
        ses = requests.Session()
        payload_pin = {"request_key": f"{request_key_2}", "identity_type": "pin",
                       "identifier": f"{self.fyersdataconfig1.PIN}", "recaptcha_token": ""}
        res_pin = ses.post('https://api-t2.fyers.in/vagator/v2/verify_pin', json=payload_pin).json()
        print(res_pin['data'])
        ses.headers.update({'authorization': f"Bearer {res_pin['data']['access_token']}"})

        authParam = {"fyers_id": self.fyersdataconfig1.FY_ID, "app_id": self.fyersdataconfig1.APP_ID,
                     "redirect_uri": self.fyersdataconfig1.REDIRECT_URI,
                     "appType": self.fyersdataconfig1.APP_TYPE, "code_challenge": "", "state": "None", "scope": "",
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

        fyers = fyersModel.FyersModel(client_id=self.fyersdataconfig1.client_id, token=access_token,
                                      log_path=os.getcwd())
        print(fyers.get_profile())
        return fyers

    def historical_bydate(self, symbol, sd, ed, interval=1):
        data = {"symbol": symbol, "resolution": "1", "date_format": "1", "range_from": str(sd),
                "range_to": str(ed), "cont_flag": "1"}
        fyers_instance = self.datageneration()
        nx = fyers_instance.history(data)
        cols = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        df = pd.DataFrame.from_dict(nx['candles'])
        df.columns = cols
        df['datetime'] = pd.to_datetime(df['datetime'], unit="s")
        df['datetime'] = df['datetime'].dt.tz_localize('utc').dt.tz_convert('Asia/Kolkata')
        df['datetime'] = df['datetime'].dt.tz_localize(None)
        return df

    def fyersinitiation3(self, sd, enddate, symbol):
        df = pd.DataFrame()
        print('don')
        print(sd)
        print(type(sd))
        sd = datetime.datetime.strptime(sd, "%Y-%m-%d").date()  # Convert string to datetime.date
        print("ko")
        print(type(sd))
        enddate = datetime.datetime.strptime(enddate, "%Y-%m-%d").date()  # Convert string to datetime.date
        print(symbol)

        n = abs((sd - enddate).days)
        ab = None

        while ab == None:
            sd_date = sd
            ed_date = enddate
            sd_str = sd_date.strftime("%Y-%m-%d")
            ed_str = ed_date.strftime("%Y-%m-%d")
            print(type(sd))

            sd = ed_date - datetime.timedelta(days=n)  # Remove .date() conversion
            ed = sd_date.strftime("%Y-%m-%d")

            dx = self.historical_bydate(symbol, sd, ed)
            df = df.append(dx)
            n = n - 100 if n > 100 else 0
            print(n)
            if n == 0:
                ab = "done"

        df = df.drop(columns=['volume'])
        df.to_csv('1RELIANCE3.csv', index=False)

    def fyersinitiation(self, symbol):
        mongo_db_url = "mongodb+srv://rithin:076ecHwHg60yETd9@cluster0.ctrleyy.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(mongo_db_url)
        DATABASE_NAME = "TRADERZSPOT"
        DB = client[DATABASE_NAME]
        collection = DB[symbol]
        #df = pd.DataFrame(list(collection.find()))
        df = pd.DataFrame(list(collection.find()))
        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"], axis=1)
        df.replace({"na": np.nan}, inplace=True)

        print("iam the fgdh")
        print(df)
        df.to_csv('1RELIANCE3.csv', index=False)
