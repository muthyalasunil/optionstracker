import csv

nested_json = {
    "strikePrice": 1400,
    "expiryDate": "26-Sep-2024",
    "underlying": "ADANIPORTS",
    "identifier": "OPTSTKADANIPORTS26-09-2024PE1400.00",
    "openInterest": 2330,
    "changeinOpenInterest": 129,
    "pchangeinOpenInterest": 5.86097228532485,
    "totalTradedVolume": 9698,
    "impliedVolatility": 23.18,
    "lastPrice": 12.35,
    "change": 1.2,
    "pChange": 10.762331838565,
    "totalBuyQuantity": 572400,
    "totalSellQuantity": 104400,
    "bidQty": 400,
    "bidprice": 12.2,
    "askQty": 400,
    "askPrice": 12.3,
    "underlyingValue": 1410.9
}


def iterate_nested_json_for_loop(json_obj):
    line = ""
    for key, value in json_obj.items():
        if isinstance(value, dict):
            iterate_nested_json_for_loop(value)
        else:
            try:
                line += str(round(value, 2)) + ','
            except Exception as err:
                pass
    return line[:-1]


def rewrite_runid(filename):
    with open(filename, 'r') as file, open(filename + '.bak', 'w') as outfile:
        csvreader = csv.reader(file)
        for row in csvreader:
            if int(row[0]) < 10011314:
                if int(row[0]) < 181518:
                    row[0] = '10' + row[0]
                else:
                    row[0] = '09' + row[0]
            line = ','.join(str(x) for x in row)
            outfile.write(line + '\n')


if __name__ == '__main__':
    rewrite_runid('20241226_options_data.csv')
