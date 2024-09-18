import matplotlib.pyplot as mp
import pandas as pd
import seaborn as sb
import numpy as np


def process_data(filename):
    dataframe = pd.read_csv(filename)
    dataframe = dataframe.fillna(0)
    # 121318,ITC,509.35,400,113,PE
    dataframe.columns = ["runid", "stock", "price", "strike", "openint", "type"]

    unique_stock_set = set(dataframe['stock'])

    for stock in unique_stock_set:
        rslt_df = dataframe.loc[dataframe['stock'] == stock]
        return_data = calculate_loss(rslt_df)

        # runid, price, min_loss_price, min_nloss_strike, min_loss_strike, max_oi_ce, max_oi_pe
        file_out = filename.replace('options', 'loss')
        with open(file_out, 'a') as outfile:
            for data in return_data:
                outfile.write(stock + ',' + str(data[0]) + ',' + str(data[1]) + ',' + str(data[2]) + ',' + str(
                    data[3]) + ',' + str(data[4]) + ',' + str(data[5]) + ',' + str(data[6]))
                outfile.write('\n')


def plot_trends(filename):
    rslt_df = pd.read_csv(filename)
    rslt_df.columns = ["stock", "run", "price", "loss", "nstrike", "strike", "max_oi_ce", "max_oi_pe"]
    unique_stock_set = set(rslt_df['stock'])

    for stock in unique_stock_set:
        loss_df = rslt_df.loc[rslt_df['stock'] == stock]
        mp.title(stock)
        # Create an axes object
        axes = mp.gca()

        # pass the axes object to plot function
        loss_df.plot(kind='line', y='price', ax=axes);
        loss_df.plot(kind='line', y='nstrike', ax=axes);
        loss_df.plot(kind='line', y='strike', ax=axes);
        loss_df.plot(kind='line', y='max_oi_ce', ax=axes);
        loss_df.plot(kind='line', y='max_oi_pe', ax=axes);
        mp.show()


def calculate_loss(rslt_df):
    return_data = []
    unique_runid_set = set(rslt_df['runid'])
    for runid in sorted(unique_runid_set):
        rslt_df_max = rslt_df.loc[rslt_df['runid'] == runid]
        rslt_df_max = rslt_df_max[["price", "strike", "openint", "type"]]

        rslt_df_pe = rslt_df_max.loc[rslt_df_max['type'] == 'PE']
        rslt_df_pe = rslt_df_pe.rename(columns={'openint': 'openint_pe', 'price': 'price_pe'})

        rslt_df_ce = rslt_df_max.loc[rslt_df_max['type'] == 'CE']
        rslt_df_ce = rslt_df_ce.rename(columns={'openint': 'openint_ce', 'price': 'price_ce'})

        rslt_df_loss = rslt_df_ce.merge(rslt_df_pe, left_on='strike', right_on='strike')
        rslt_df_loss = rslt_df_loss[(rslt_df_loss['openint_pe'] > 0) & (rslt_df_loss['openint_ce'] > 0)]

        unique_strike_set = set(rslt_df_loss['strike'])
        rslt_df_loss['loss_ce'] = 0
        rslt_df_loss['loss_pe'] = 0
        price = rslt_df_loss['price_pe'].max()

        for strike in unique_strike_set:
            perc_chg = abs((price - strike) / price)
            if perc_chg < 0.1:
                for idx, row in rslt_df_loss.iterrows():
                    if row['strike'] > strike:
                        rslt_df_loss.at[idx, 'loss_ce'] = row['loss_ce'] + (row['strike'] - strike) * row['openint_ce']
                    if row['strike'] < strike:
                        rslt_df_loss.at[idx, 'loss_pe'] = row['loss_pe'] + (strike - row['strike']) * row['openint_pe']

        rslt_df_loss = rslt_df_loss[(rslt_df_loss['loss_ce'] > 0) & (rslt_df_loss['loss_pe'] > 0)]
        rslt_df_loss['loss'] = abs(rslt_df_loss['loss_ce'] + rslt_df_loss['loss_pe'])
        rslt_df_loss['netloss'] = abs(rslt_df_loss['loss_ce'] - rslt_df_loss['loss_pe'])
        max_oi_ce = rslt_df_loss['openint_ce'].max()
        max_oi_pe = rslt_df_loss['openint_pe'].max()

        min_loss_price = rslt_df_loss['loss'].min()
        min_nloss_price = rslt_df_loss['netloss'].min()
        min_loss_strike = rslt_df_loss[(rslt_df_loss['loss'] == min_loss_price)]['strike'].values[0]
        min_nloss_strike = rslt_df_loss[(rslt_df_loss['netloss'] == min_nloss_price)]['strike'].values[0]
        max_oi_ce = rslt_df_loss[(rslt_df_loss['openint_ce'] == max_oi_ce)]['strike'].values[0]
        max_oi_pe = rslt_df_loss[(rslt_df_loss['openint_pe'] == max_oi_pe)]['strike'].values[0]


        return_data.append([runid, price, min_loss_price, min_nloss_strike, min_loss_strike, max_oi_ce, max_oi_pe])

    return return_data


def plot_values(rslt_df):
    unique_run_set = set(rslt_df['runid'])

    df = pd.DataFrame(unique_run_set, columns=["runid"])
    df = df.sort_values(by=['runid'])

    unique_strike_set = set(rslt_df['strike'])
    unique_price_set = set(rslt_df['price'])
    average = sum(unique_price_set) / len(unique_price_set)
    rslt_df.drop(['price'], axis=1, inplace=True)

    for strike in unique_strike_set:
        perc_chg = abs((average - strike) / average)

        if perc_chg < 0.05:
            temp_df = rslt_df.loc[rslt_df['strike'] == strike]
            temp_df = temp_df[['runid', 'openint']]
            temp_df = temp_df.rename(columns={"openint": strike})
            df = df.merge(temp_df, left_on='runid', right_on='runid')

    df.drop(['runid'], axis=1, inplace=True)

    print(df)
    df.plot(kind='line')
    mp.show()
    return


def temp(dataframe, unique_cusip_set, unique_txns_set):
    df = pd.DataFrame(unique_cusip_set, columns=["effective_date"])
    df = df.sort_values(by=['effective_date'])

    for txn_id in unique_txns_set:
        rslt_df = dataframe.loc[dataframe['txn_seq'] == txn_id]
        rslt_df = rslt_df[['effective_date', 'index_value']]
        rslt_df = rslt_df.rename(columns={"index_value": txn_id})
        df = df.merge(rslt_df, left_on='effective_date', right_on='effective_date')

    df_340 = pd.read_csv("idp_index_values.csv")
    df = df.merge(df_340, left_on='effective_date', right_on='effective_date')

    print(df)
    df.drop(['effective_date'], axis=1, inplace=True)
    corrM = df.corr()
    # print(corrM)

    # plotting correlation heatmap
    dataplot = sb.heatmap(corrM, cmap="YlGnBu", annot=True)

    # displaying heatmap
    mp.show()


if __name__ == '__main__':
    #plot_trends('20240926_loss_data.csv')
    process_data('20241128_options_data.csv')
