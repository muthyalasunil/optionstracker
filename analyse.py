import matplotlib.pyplot as mp
import pandas as pd
import seaborn as sb
import datetime
import glob
from dateutil.relativedelta import relativedelta
import numpy as np
from constants import option_columns, loss_columns, stock_columns


def process_data(filename):
    # dataframe = pd.read_csv(filename)
    # 201512, ITC, 520, 787, -75, -8.7, 2643, 17.53, 6.7, -5.25, -43.93, 347200, 310400, 3200, 6.6, 6400, 6.75, 514.55, PE
    dataframe = pd.read_csv(filename, names=option_columns)
    dataframe = dataframe.fillna(0)
    dataframe = dataframe[(dataframe['price'] > 0)]
    # cols = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
    cols = ["coi", "pcio", "vol", "iv", "lp", "chg", "pchg", "tbuy", "tsell", "bqty", "bprc", "aqty", "aprc"]
    # dataframe.drop(dataframe.columns[cols], axis=1, inplace=True)
    dataframe = dataframe[["runid", "stock", "strike", "openint", "price", "vol", "iv", "type"]]
    # dataframe.columns = ["runid", "stock", "strike", "openint", "price", "type"]
    unique_stock_set = set(dataframe['stock'])

    for stock in unique_stock_set:
        rslt_df = dataframe.loc[dataframe['stock'] == stock]
        return_data = calculate_loss(stock, rslt_df)
        file_out = filename.replace('options', 'loss')
        with open(file_out, 'a') as outfile:
            for data in return_data:
                line = ','.join(str(x) for x in data)
                outfile.write(stock + ',' + line + '\n')


def calculate_loss(stock, rslt_df):
    return_data = []
    unique_runid_set = sorted(set(rslt_df['runid']))
    for runid in unique_runid_set:
        try:
            rslt_df_max = rslt_df.loc[rslt_df['runid'] == runid]
            rslt_df_max = rslt_df_max[["price", "strike", "openint", "vol", "iv", "type"]]

            rslt_df_pe = rslt_df_max.loc[rslt_df_max['type'] == 'PE']
            rslt_df_pe = rslt_df_pe.rename(
                columns={'openint': 'openint_pe', 'price': 'price_pe', 'vol': 'vol_pe', 'iv': 'iv_pe'})

            rslt_df_ce = rslt_df_max.loc[rslt_df_max['type'] == 'CE']
            rslt_df_ce = rslt_df_ce.rename(
                columns={'openint': 'openint_ce', 'price': 'price_ce', 'vol': 'vol_ce', 'iv': 'iv_ce'})

            rslt_df_loss = rslt_df_ce.merge(rslt_df_pe, how='outer', left_on='strike', right_on='strike')
            rslt_df_loss = rslt_df_loss.fillna(0)

            rslt_df_loss['loss_ce'] = 0
            rslt_df_loss['loss_pe'] = 0
            price = rslt_df_loss['price_pe'].max()
            l_strike = price * 0.9
            h_strike = price * 1.1
            rslt_df_loss = rslt_df_loss[(rslt_df_loss['strike'] > l_strike) & (rslt_df_loss['strike'] < h_strike)]
            rslt_df_loss = rslt_df_loss[(rslt_df_loss['openint_ce'] > 0) & (rslt_df_loss['openint_pe'] > 0)]

            unique_strike_set = set(rslt_df_loss['strike'])
            for strike in unique_strike_set:
                for idx, row in rslt_df_loss.iterrows():
                    if row['strike'] > strike:
                        rslt_df_loss.at[idx, 'loss_ce'] = row['loss_ce'] + (row['strike'] - strike) * row[
                            'openint_ce']
                    if row['strike'] < strike:
                        rslt_df_loss.at[idx, 'loss_pe'] = row['loss_pe'] + (strike - row['strike']) * row[
                            'openint_pe']

            # rslt_df_loss = rslt_df_loss[(rslt_df_loss['loss_ce'] > 0) | (rslt_df_loss['loss_pe'] > 0)]
            rslt_df_loss['loss'] = abs(rslt_df_loss['loss_ce'] + rslt_df_loss['loss_pe'])
            rslt_df_loss['netloss'] = abs(rslt_df_loss['loss_ce'] - rslt_df_loss['loss_pe'])

            max_oi_ce = rslt_df_loss['openint_ce'].max()
            max_oi_pe = rslt_df_loss['openint_pe'].max()
            min_tloss = rslt_df_loss['loss'].min()
            min_nloss = rslt_df_loss['netloss'].min()
            max_v_ce = rslt_df_loss['vol_ce'].max()
            max_v_pe = rslt_df_loss['vol_pe'].max()
            max_iv_ce = rslt_df_loss['iv_ce'].max()
            max_iv_pe = rslt_df_loss['iv_pe'].max()

            tstrike = rslt_df_loss[(rslt_df_loss['loss'] == min_tloss)]['strike'].values[0]
            nstrike = rslt_df_loss[(rslt_df_loss['netloss'] == min_nloss)]['strike'].values[0]
            oi_ce = rslt_df_loss[(rslt_df_loss['openint_ce'] == max_oi_ce)]['strike'].values[0]
            oi_pe = rslt_df_loss[(rslt_df_loss['openint_pe'] == max_oi_pe)]['strike'].values[0]

            vol_ce = rslt_df_loss[(rslt_df_loss['vol_ce'] == max_v_ce)]['strike'].values[0]
            vol_pe = rslt_df_loss[(rslt_df_loss['vol_pe'] == max_v_pe)]['strike'].values[0]
            iv_ce = rslt_df_loss[(rslt_df_loss['iv_ce'] == max_iv_ce)]['strike'].values[0]
            iv_pe = rslt_df_loss[(rslt_df_loss['iv_pe'] == max_iv_pe)]['strike'].values[0]

            return_data.append(
                [runid, price, tstrike, nstrike, vol_ce, vol_pe, iv_ce, iv_pe, oi_ce, oi_pe])
            # print(return_data[-1])

        except Exception as err:
            print(f"calc_loss - Unexpected {err=}, {type(err)=}")
            print("error calculating loss {stock} - {runid}......".format(stock=stock, runid=runid))
            with pd.option_context('display.max_rows', None, 'display.max_columns',
                                   None):  # more options can be specified also
                print(rslt_df_loss)
        finally:
            pass

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


def get_files_names():
    file_names = []
    xtime = datetime.datetime.now()
    files = glob.glob("./*_options_data.csv")
    for i in range(3):
        next_nmonth = xtime + relativedelta(months=i)
        x_label = next_nmonth.strftime("%Y%m")
        for file_name in files:
            if x_label in file_name:
                file_names.append(file_name)

    return file_names


def plot_all_values(file_names):
    rslt_df1 = pd.read_csv(file_names[0])

    rslt_df1.columns = loss_columns
    rslt_df1 = rslt_df1[["stock", "run", "price", "nstrike1"]]

    rslt_df2 = pd.read_csv(file_names[1])
    rslt_df2.columns = loss_columns
    rslt_df2 = rslt_df2[["stock", "run", "nstrike2"]]
    rslt_df = pd.merge(
        left=rslt_df1,
        right=rslt_df2,
        how='left',
        left_on=['stock', 'run'],
        right_on=['stock', 'run'],
    )

    rslt_df3 = pd.read_csv(file_names[2])
    rslt_df3.columns = loss_columns
    rslt_df3 = rslt_df3[["stock", "run", "nstrike3"]]
    rslt_df = pd.merge(
        left=rslt_df,
        right=rslt_df3,
        how='left',
        left_on=['stock', 'run'],
        right_on=['stock', 'run'],
    )

    unique_stock_set = set(rslt_df['stock'])
    for stock in unique_stock_set:
        loss_df = rslt_df.loc[rslt_df['stock'] == stock]
        mp.title(stock)
        # Create an axes object
        axes = mp.gca()

        # pass the axes object to plot function
        loss_df.plot(linestyle='solid', y='price', ax=axes);
        loss_df.plot(linestyle='dashdot', y='nstrike1', ax=axes);
        loss_df.plot(linestyle='dashed', y='nstrike2', ax=axes);
        loss_df.plot(linestyle='dotted', y='nstrike3', ax=axes);
        mp.show()


def plot_trends(filename):
    rslt_df = pd.read_csv(filename)
    rslt_df.columns = ['stock', 'runid', 'price', 'tstrike', 'nstrike', 'vol_ce', 'vol_pe',
                       'iv_ce', 'iv_pe', 'oi_ce',
                       'oi_pe']
    unique_stock_set = set(rslt_df['stock'])

    for stock in unique_stock_set:
        loss_df = rslt_df.loc[rslt_df['stock'] == stock]
        fig, axs = mp.subplots(3)  # for n subplots
        axs[0].title.set_text(stock)
        # pass the axes object to plot function
        loss_df.plot(linestyle='solid', y='price', ax=axs[0]);
        loss_df.plot(linestyle='dashdot', y='nstrike', ax=axs[0]);
        loss_df.plot(linestyle='dashdot', y='tstrike', ax=axs[0]);
        loss_df.plot(linestyle='dotted', y='oi_ce', ax=axs[0]);
        loss_df.plot(linestyle='dotted', y='oi_pe', ax=axs[0]);

        loss_df.plot(linestyle='solid', y='price', ax=axs[1]);
        loss_df.plot(linestyle='dotted', y='vol_ce', ax=axs[1]);
        loss_df.plot(linestyle='dotted', y='vol_pe', ax=axs[1]);

        loss_df.plot(linestyle='solid', y='price', ax=axs[2]);
        loss_df.plot(linestyle='dotted', y='iv_ce', ax=axs[2]);
        loss_df.plot(linestyle='dotted', y='iv_pe', ax=axs[2]);

        mp.show()


def plot_oi(filename):
    rslt_df = pd.read_csv(filename)
    rslt_df.columns = ['stock', 'runid', 'price', 'tstrike', 'nstrike', 'vol_ce', 'vol_pe',
                       'iv_ce', 'iv_pe', 'oi_ce',
                       'oi_pe']
    unique_stock_set = set(rslt_df['stock'])

    for stock in unique_stock_set:
        loss_df = rslt_df.loc[rslt_df['stock'] == stock]
        nstrike = loss_df['nstrike'].values[-1]

        stock_df = pd.read_csv(filename.replace('loss', 'options'), names=option_columns)
        stock_df = stock_df.loc[stock_df['stock'] == stock]
        stock_df = stock_df.loc[stock_df['strike'] == nstrike]

        fig, axs = mp.subplots(3)  # for n subplots
        axs[0].title.set_text(stock + '_' + str(nstrike))

        pe_df = stock_df.loc[stock_df['type'] == 'PE']
        pe_df = pe_df.rename(columns={"openint": 'oi_pe', 'vol': 'vol_pe'})
        try:
            nstrike_vals = loss_df['nstrike'].values
            pe_df['nstrike'] = np.array(nstrike_vals)
            pe_df.plot(linestyle='dashdot', y='nstrike', ax=axs[2]);

        except Exception as err:
            print("shape {stock} - {loss}, {options}..".format(stock=stock, loss=loss_df.shape[0],
                                                               options=pe_df.shape[0]))

        ce_df = stock_df.loc[stock_df['type'] == 'CE']
        ce_df = ce_df.rename(columns={"openint": 'oi_ce', 'vol': 'vol_ce'})

        ce_df.plot(linestyle='dashdot', y='oi_ce', ax=axs[0]);
        ce_df.plot(linestyle='dashdot', y='vol_ce', ax=axs[1]);

        pe_df.plot(linestyle='dashdot', y='oi_pe', ax=axs[0]);
        pe_df.plot(linestyle='dashdot', y='vol_pe', ax=axs[1]);

        pe_df.plot(linestyle='solid', y='price', ax=axs[2]);

        mp.show()


def plot_stock(filename):
    rslt_df = pd.read_csv(filename, names=stock_columns)
    rslt_df = rslt_df[["runid", "stock", "lastPrice", "totalTradedVolume"]]
    unique_stock_set = set(rslt_df['stock'])
    for stock in unique_stock_set:
        s_rslt_df = rslt_df.loc[rslt_df['stock'] == stock]
        s_rslt_df1 = s_rslt_df[["runid", "totalTradedVolume"]]
        s_rslt_df1 = s_rslt_df1.set_index('runid').diff()

        fig, axs = mp.subplots(2)  # for n subplots
        axs[0].title.set_text(stock)
        s_rslt_df.plot(linestyle='solid', y='lastPrice', ax=axs[0]);
        s_rslt_df1.plot(kind="bar", ax=axs[1]);


        mp.show()


if __name__ == '__main__':
    '''
    files_names = get_files_names()
    for file_name in files_names:
        process_data(file_name)
        print(file_name)
    '''
    plot_stock('202410_stock_data.csv')
    # plot_oi('20241031_loss_data.csv')
    # plot_trends('20241031_loss_data.csv')
    # files_names = get_files_names()
    # print(files_names)
    # plot_all_values(files_names)
