import csv
import pandas as pd

import constants


def iterate_nested_json_for_loop(json_obj):
    line = ""
    for key, value in json_obj.items():
        if isinstance(value, dict):
            line += iterate_nested_json_for_loop(value) + ','
        else:
            try:
                line += str(round(value, 2)) + ','
            except Exception as err:
                try:
                    line += str(round(float(value), 2)) + ','
                except Exception as err:
                    try:
                        line += str(round(int(value), 2)) + ','
                    except Exception as err:
                        pass

    return line[:-1]


def iterate_json_for_loop(json_obj):
    line = ""
    for key, value in json_obj.items():
        try:
            line += str(round(value, 2)) + ','
        except Exception as err:
            try:
                line += str(round(float(value), 2)) + ','
            except Exception as err:
                try:
                    line += str(round(int(value), 2)) + ','
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
    rslt_df1 = pd.read_csv('202410_stock_data.csv', names=constants.stock_columns)
    print(rslt_df1.shape)
    print(rslt_df1)
