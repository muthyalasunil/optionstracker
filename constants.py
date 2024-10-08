baseurl = "https://www.nseindia.com/"
options_url = f"https://www.nseindia.com/api/option-chain-equities?symbol=__stock__"
stock_url = 'https://www.nseindia.com/api/quote-equity?symbol=__stock__'
stock_trd_url = 'https://www.nseindia.com/api/quote-equity?symbol=__stock__&section=trade_info'

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) '
                         'Chrome/80.0.3987.149 Safari/537.36',
           'accept-language': 'en,gu;q=0.9,hi;q=0.8', 'accept-encoding': 'gzip, deflate, br'}

option_columns = ["runid", "stock", "strike", "openint", "coi", "pcio", "vol", "iv",
                  "lp", "chg", "pchg", "tbuy", "tsell", "bqty", "bprc", "aqty", "aprc",
                  "price", "type"]
loss_columns = ['stock', 'runid', 'price', 'tstrike', 'nstrike', 'vol_ce', 'vol_pe', 'iv_ce', 'iv_pe', 'oi_ce', 'oi_pe']

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

stockInfo = {
    "info": {
        "symbol": "TATAMOTORS",
        "companyName": "Tata Motors Limited",
        "industry": "Passenger Cars & Utility Vehicles",
        "activeSeries": [
            "EQ"
        ],
        "debtSeries": [],
        "isFNOSec": True,
        "isCASec": False,
        "isSLBSec": True,
        "isDebtSec": False,
        "isSuspended": False,
        "tempSuspendedSeries": [],
        "isETFSec": False,
        "isDelisted": False,
        "isin": "INE155A01022",
        "slb_isin": "INE155A01022",
        "isMunicipalBond": False,
        "isTop10": False,
        "identifier": "TATAMOTORSEQN"
    },
    "metadata": {
        "series": "EQ",
        "symbol": "TATAMOTORS",
        "isin": "INE155A01022",
        "status": "Listed",
        "listingDate": "22-Jul-1998",
        "industry": "Passenger Cars & Utility Vehicles",
        "lastUpdateTime": "08-Oct-2024 09:35:45",
        "pdSectorPe": 10.11,
        "pdSymbolPe": 10.17,
        "pdSectorInd": "NIFTY 50",
        "pdSectorIndAll": [
            "NIFTY 50",
            "NIFTY RURAL",
            "NIFTY AUTO",
            "NIFTY 200",
            "NIFTY100 LIQUID 15",
            "NIFTY GROWTH SECTORS 15",
            "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP",
            "NIFTY INDIA CORPORATE GROUP INDEX - TATA GROUP 25% CAP",
            "NIFTY100 EQUAL WEIGHT",
            "NIFTY50 EQUAL WEIGHT",
            "NIFTY ALPHA LOW-VOLATILITY 30",
            "NIFTY LARGEMIDCAP 250",
            "NIFTY200 MOMENTUM 30",
            "NIFTY100 ESG SECTOR LEADERS",
            "NIFTY500 MULTICAP 50:25:25",
            "NIFTY INDIA MANUFACTURING",
            "NIFTY MOBILITY",
            "NIFTY200 ALPHA 30",
            "NIFTY TOTAL MARKET",
            "NIFTY500 LARGEMIDSMALL EQUAL-CAP WEIGHTED",
            "NIFTY TRANSPORTATION & LOGISTICS",
            "NIFTY500 MULTICAP INDIA MANUFACTURING 50:30:20",
            "NIFTY100 ESG",
            "NIFTY500 EQUAL WEIGHT",
            "NIFTY EV & NEW AGE AUTOMOTIVE",
            "NIFTY 100",
            "NIFTY 500"
        ]
    },
    "securityInfo": {
        "boardStatus": "Main",
        "tradingStatus": "Active",
        "tradingSegment": "Normal Market",
        "sessionNo": "-",
        "slb": "Yes",
        "classOfShare": "Equity",
        "derivatives": "Yes",
        "surveillance": {
            "surv": None,
            "desc": None
        },
        "faceValue": 2,
        "issuedSize": 3680884120
    },
    "sddDetails": {
        "SDDAuditor": "-",
        "SDDStatus": "-"
    },
    "priceInfo": {
        "lastPrice": 899.95,
        "change": -27.9,
        "pChange": -3.00695155466939,
        "previousClose": 927.85,
        "open": 916,
        "close": 0,
        "vwap": 901.31,
        "stockIndClosePrice": 0,
        "lowerCP": "835.10",
        "upperCP": "1020.60",
        "pPriceBand": "No Band",
        "basePrice": 927.85,
        "intraDayHighLow": {
            "min": 893.85,
            "max": 918,
            "value": 899.95
        },
        "weekHighLow": {
            "min": 613.7,
            "minDate": "09-Oct-2023",
            "max": 1179,
            "maxDate": "30-Jul-2024",
            "value": 899.95
        },
        "iNavValue": None,
        "checkINAV": False,
        "tickSize": 0.05
    },
    "industryInfo": {
        "macro": "Consumer Discretionary",
        "sector": "Automobile and Auto Components",
        "industry": "Automobiles",
        "basicIndustry": "Passenger Cars & Utility Vehicles"
    },
    "preOpenMarket": {
        "preopen": [
            {
                "price": 835.1,
                "buyQty": 0,
                "sellQty": 661
            },
            {
                "price": 836,
                "buyQty": 0,
                "sellQty": 10000
            },
            {
                "price": 838.75,
                "buyQty": 0,
                "sellQty": 1000
            },
            {
                "price": 840,
                "buyQty": 0,
                "sellQty": 10
            },
            {
                "price": 916,
                "buyQty": 0,
                "sellQty": 0,
                "iep": True
            },
            {
                "price": 977.25,
                "buyQty": 6,
                "sellQty": 0
            },
            {
                "price": 992,
                "buyQty": 1,
                "sellQty": 0
            },
            {
                "price": 1000,
                "buyQty": 1,
                "sellQty": 0
            },
            {
                "price": 1020.6,
                "buyQty": 3215,
                "sellQty": 0
            }
        ],
        "ato": {
            "buy": 11990,
            "sell": 18288
        },
        "IEP": 916,
        "totalTradedVolume": 167255,
        "finalPrice": 916,
        "finalQuantity": 167255,
        "lastUpdateTime": "08-Oct-2024 09:07:23",
        "totalBuyQuantity": 84921,
        "totalSellQuantity": 259001,
        "atoBuyQty": 11990,
        "atoSellQty": 18288,
        "Change": -11.85,
        "perChange": -1.2771460904241,
        "prevClose": 927.85
    }
}
tradeInfo = {
    "noBlockDeals": True,
    "bulkBlockDeals": [
        {
            "name": "Session I"
        },
        {
            "name": "Session II"
        }
    ],
    "marketDeptOrderBook": {
        "totalBuyQuantity": 865327,
        "totalSellQuantity": 644416,
        "bid": [
            {
                "price": 909.75,
                "quantity": 29
            },
            {
                "price": 909.6,
                "quantity": 1
            },
            {
                "price": 909.55,
                "quantity": 61
            },
            {
                "price": 909.5,
                "quantity": 390
            },
            {
                "price": 909.45,
                "quantity": 374
            }
        ],
        "ask": [
            {
                "price": 909.95,
                "quantity": 87
            },
            {
                "price": 910,
                "quantity": 8016
            },
            {
                "price": 910.05,
                "quantity": 111
            },
            {
                "price": 910.1,
                "quantity": 249
            },
            {
                "price": 910.15,
                "quantity": 713
            }
        ],
        "tradeInfo": {
            "totalTradedVolume": 68.11,
            "totalTradedValue": 614.55,
            "totalMarketCap": 334942.05,
            "ffmc": 192931.592581769,
            "impactCost": 0.02,
            "cmDailyVolatility": "1.9",
            "cmAnnualVolatility": "36.3",
            "marketLot": "",
            "activeSeries": "EQ"
        },
        "valueAtRisk": {
            "securityVar": 12.07,
            "indexVar": 0,
            "varMargin": 12.07,
            "extremeLossMargin": 3.5,
            "adhocMargin": 0,
            "applicableMargin": 15.57
        }
    },
    "securityWiseDP": {
        "quantityTraded": 11772546,
        "deliveryQuantity": 4886267,
        "deliveryToTradedQuantity": 41.51,
        "seriesRemarks": None,
        "secWiseDelPosDate": "07-OCT-2024 EOD"
    }
}

stock_columns = [
    "runid",
    "stock",
    "pdSymbolPe",
    "lastPrice",
    "change",
    "pChange",
    "previousClose",
    "open",
    "close",
    "vwap",
    "stockIndClosePrice",
    "lowerCP",
    "upperCP",
    "basePrice",
    "dmin",
    "dmax",
    "dvalue",
    "w52min",
    "w52max",
    "w52value",
    "tickSize",
    "poatobuy",
    "poatosell"
    "poIEP",
    "pototalTradedVolume",
    "pofinalPrice",
    "pofinalQuantity",
    "pototalBuyQuantity",
    "pototalSellQuantity",
    "poatoBuyQty",
    "poatoSellQty",
    "poChange",
    "poperChange",
    "poprevClose",
    "totalBuyQuantity",
    "totalSellQuantity",
    "totalTradedVolume",
    "totalTradedValue",
    "totalMarketCap",
    "ffmc",
    "impactCost",
    "cmDailyVolatility",
    "cmAnnualVolatility",
    "quantityTraded",
    "deliveryQuantity",
    "deliveryToTradedQuantity"]
