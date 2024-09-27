import csv
import io

import requests
import datetime
from time import sleep
import pandas as pd
import analyse
import utils

baseurl = "https://www.nseindia.com/"
url = f"https://www.nseindia.com/api/option-chain-equities?symbol=__stock__"
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}


def capture_options(stock, session, cookies):
    return_data = {}
    response = session.get(url.replace('__stock__', stock), headers=headers, timeout=5, cookies=cookies)
    print("{stock} URL Done......".format(stock=stock))
    json_data = response.json() if response and response.status_code == 200 else None

    if json_data and 'records' in json_data:
        expiryDates = json_data['records']['expiryDates']
        for expiryDate in expiryDates:
            print(expiryDate)
            return_list = []
            for data in json_data['records']['data']:
                if 'PE' in data and expiryDate in data['expiryDate']:
                    # Filtering by key
                    filtered_data = utils.iterate_nested_json_for_loop(data['PE'])
                    return_list.append(stock + ',' + filtered_data + ',PE')

                if 'CE' in data and expiryDate in data['expiryDate']:
                    # Filtering by key
                    filtered_data = utils.iterate_nested_json_for_loop(data['CE'])
                    return_list.append(stock + ',' + filtered_data + ',CE')

            return_data[expiryDate] = return_list

    print("{stock} capture Done......".format(stock=stock))
    return return_data


if __name__ == '__main__':
    print('Start......')
    stocks = ['ITC', 'ADANIPORTS', 'ICICIBANK', 'TCS', 'TATAMOTORS', 'SBI', 'RELIANCE']

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
                return_data = capture_options(stock, session, cookies)
                for expiryDate in return_data:
                    expiryDateStr = datetime.datetime.strptime(expiryDate, '%d-%b-%Y').strftime('%Y%m%d')
                    file_name = expiryDateStr + '_options_data.csv'
                    with open(file_name, 'a') as outfile:
                        for line in return_data[expiryDate]:
                            outfile.write(x_label + ',' + line)
                            outfile.write('\n')

                    dataframe = pd.DataFrame([str.split(",") for str in return_data[expiryDate]])
                    cols = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
                    dataframe.drop(dataframe.columns[cols], axis=1, inplace=True)
                    dataframe.columns = ["stock", "strike", "openint", "price", "type"]

                    dataframe['runid'] = x_label
                    # set dtypes for each column
                    dataframe['runid'] = dataframe['runid'].astype(int)
                    dataframe['strike'] = dataframe['strike'].astype(int)
                    dataframe['openint'] = dataframe['openint'].astype(float)
                    dataframe['price'] = dataframe['price'].astype(float)
                    try:
                        loss_data = analyse.calculate_loss(stock, dataframe)
                        file_name = expiryDateStr + '_loss_data.csv'
                        with open(file_name, 'a') as outfile:
                            for data in loss_data:
                                line = ','.join(str(x) for x in data)
                                outfile.write(stock + ',' + line + '\n')
                    except Exception as err:
                        print(f"calculate_loss - Unexpected {err=}, {type(err)=}")

            print('sleep(900) ......')
            sleep(900)

        except Exception as err:
            print(f"main - Unexpected {err=}, {type(err)=}")
            print('sleep(60) ......')
            sleep(60)
