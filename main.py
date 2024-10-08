import csv
import io

import requests
import datetime
from time import sleep
import pandas as pd
import analyse
import utils
from constants import options_url, stock_url, baseurl, headers, stock_trd_url


def capture_options(stock, session, cookies):
    return_data = {}
    response = session.get(options_url.replace('__stock__', stock), headers=headers, timeout=5, cookies=cookies)
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

    print("{stock} options capture Done......".format(stock=stock))
    return return_data


def capture_stock(stock, session, cookies):
    return_data = []
    response = session.get(stock_url.replace('__stock__', stock), headers=headers, timeout=5, cookies=cookies)
    json_data = response.json() if response and response.status_code == 200 else None

    if json_data and 'metadata' in json_data:
        return_data.append(json_data['metadata']['pdSymbolPe'])

    if json_data and 'priceInfo' in json_data:
        priceInfo = utils.iterate_nested_json_for_loop(json_data['priceInfo'])
        return_data += priceInfo.split(",")

    if json_data and 'preOpenMarket' in json_data:
        preOpenMarket = utils.iterate_json_for_loop(json_data['preOpenMarket'])
        return_data += preOpenMarket.split(",")

    response = session.get(stock_trd_url.replace('__stock__', stock), headers=headers, timeout=5, cookies=cookies)
    json_data = response.json() if response and response.status_code == 200 else None
    if json_data and 'marketDeptOrderBook' in json_data:
        marketDeptOrderBook = utils.iterate_json_for_loop(json_data['marketDeptOrderBook'])
        return_data += marketDeptOrderBook.split(",")
        tradeInfo = utils.iterate_nested_json_for_loop(json_data['marketDeptOrderBook']['tradeInfo'])
        return_data += tradeInfo.split(",")

    if json_data and 'securityWiseDP' in json_data:
        securityWiseDP = utils.iterate_json_for_loop(json_data['securityWiseDP'])
        return_data += securityWiseDP.split(",")

    print("{stock} capture Done......".format(stock=stock))

    return return_data


if __name__ == '__main__':
    print('Start......')
    stocks = ['ITC', 'ADANIPORTS', 'ICICIBANK', 'TCS', 'TATAMOTORS', 'SBIN', 'RELIANCE']

    file_path = '_options_data.json'

    for x in range(25):
        xtime = datetime.datetime.now()
        x_label = xtime.strftime("%m%d%H%M")
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
                    dataframe.columns = ["stock", "strike", "openint", "coi", "pcio", "vol", "iv",
                                         "lp", "chg", "pchg", "tbuy", "tsell", "bqty", "bprc", "aqty", "aprc",
                                         "price", "type"]
                    dataframe = dataframe[["stock", "strike", "openint", "price", "vol", "iv", "type"]]
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

                try:
                    return_data = capture_stock(stock, session, cookies)
                    f_label = xtime.strftime('%Y%m')
                    file_name = f_label + '_stock_data.csv'

                    with open(file_name, 'a') as outfile:
                        line = ','.join(str(x) for x in return_data)
                        outfile.write(x_label + ',' + stock + ',' + line + '\n')
                except Exception as err:
                    print(f"capture_stock - Unexpected {err=}, {type(err)=}")

            print('sleep(900) ......')
            sleep(900)

        except Exception as err:
            print(f"main - Unexpected {err=}, {type(err)=}")
            print('sleep(60) ......')
            sleep(60)
