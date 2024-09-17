import csv
import io

import requests
import datetime
from time import sleep
import pandas as pd
import analyse

baseurl = "https://www.nseindia.com/"
url = f"https://www.nseindia.com/api/option-chain-equities?symbol=__stock__"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}


def capture_options(stock, session, cookies):
    return_data = []
    response = session.get(url.replace('__stock__', stock), headers=headers, timeout=5, cookies=cookies)
    print("{stock} URL Done......".format(stock=stock))
    expiryDate = ''
    json_data = response.json() if response and response.status_code == 200 else None

    if json_data and 'records' in json_data:
        expiryDates = json_data['records']['expiryDates']
        expiryDate = expiryDates[0]
        print(expiryDate)

        for data in json_data['records']['data']:
            if 'PE' in data and expiryDate in data['expiryDate']:
                # Filtering by key
                filtered_data = "{stock},{price},{strikePrice},{openInterest},PE".format(stock=stock,
                                                                                         strikePrice=data['PE'][
                                                                                             'strikePrice'],
                                                                                         openInterest=data['PE'][
                                                                                             'openInterest'],
                                                                                         price=data['PE'][
                                                                                             'underlyingValue'])
                return_data.append(filtered_data)

            if 'CE' in data and expiryDate in data['expiryDate']:
                # Filtering by key
                filtered_data = "{stock},{price},{strikePrice},{openInterest},CE".format(stock=stock,
                                                                                         strikePrice=data['CE'][
                                                                                             'strikePrice'],
                                                                                         openInterest=data['CE'][
                                                                                             'openInterest'],
                                                                                         price=data['CE'][
                                                                                             'underlyingValue'])

                return_data.append(filtered_data)

                # line = "{strikePrice},{openInterest}".format(strikePrice=strikePrice, openInterest=openInterest)

    print("{stock} capture Done......".format(stock=stock))
    return expiryDate, return_data


if __name__ == '__main__':
    print('Start......')
    stocks = ['ITC', 'ADANIPORTS', 'ICICIBANK']

    file_path = '_options_data.json'

    for x in range(25):
        xtime = datetime.datetime.now()
        x_label = xtime.strftime("%d%H%M")
        print(x_label)
        try:
            session = requests.Session()
            request = session.get(baseurl, headers=headers, timeout=5)
            print('Done baseurl ......')
            cookies = dict(request.cookies)

            for stock in stocks:
                expiryDate, return_data = capture_options(stock, session, cookies)
                expiryDateStr = datetime.datetime.strptime(expiryDate, '%d-%b-%Y').strftime('%Y%m%d')
                file_name = expiryDateStr + '_options_data.csv'
                with open(file_name, 'a') as outfile:
                    for line in return_data:
                        outfile.write(x_label + ',' + line)
                        outfile.write('\n')

                dataframe = pd.DataFrame([str.split(",") for str in return_data])
                dataframe.columns = ["stock", "price", "strike", "openint", "type"]
                dataframe['runid'] = x_label
                # set dtypes for each column
                dataframe['runid'] = dataframe['runid'].astype(int)
                dataframe['strike'] = dataframe['strike'].astype(int)
                dataframe['openint'] = dataframe['openint'].astype(float)
                dataframe['price'] = dataframe['price'].astype(float)

                loss_data = analyse.calculate_loss(dataframe)
                file_name = expiryDateStr + '_loss_data.csv'
                with open(file_name, 'a') as outfile:
                    for data in loss_data:
                        outfile.write(stock + ',' + str(data[0])+ ',' + str(data[1])+ ',' + str(data[2])+ ',' + str(data[3]))
                        outfile.write('\n')

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")

        sleep(900)
