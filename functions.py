"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Cloning Superinvestors                                                                     -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: diegolazareno                                                                               -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/diegolazareno/Cloning_Superinvestors                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# Required libraries
import pandas as pd
import yfinance as yf
import datetime as dt
import numpy as np

def dataWrangling(data : "Superinvestor's activity"):
    """
    dataWrangling manipulates superinvestor's data.
    
    *data: is a DataFrame that contains the superinvestor's activity.
        
    Returns:
    *activity: a dictionary whose keys contain the superinvestor's activity by quarters.
    *dates: a list with the dates in which the superinvestor took action.
    
    """
    
    # Dates manipulation
    dates = list(data[data["History"] != "≡"]["History"])
    dateFormat = lambda x : x[-4 :] + "-12-31" if x[: 2] == "Q4" else (x[-4 :] + "-09-30" if x[: 2] == "Q3" 
                    else(x[-4 :] + "-06-30" if x[: 2] == "Q2" else x[-4 :] + "-03-31"))
    dates = list(map(lambda date : dateFormat(date), dates))
    
    # Activity by quarters
    idx = list(data[data["History"] != "≡"].index)
    activity = {}

    for i in range(len(idx)):
        if i != len(idx) - 1:
            activity[dates[i]] = data.iloc[idx[i] : idx[i + 1]]
    
        else:
            activity[dates[i]] = data.iloc[idx[i] :]
            
    return activity, dates[::-1]


def superInvestorCloning(superInvestor : "Superinvestor's activity", dates : "Dates"):
    """
    superInvestorCloning clones superinvestor's trades.
    
    *superInvestor: a dictionary whose keys contain the superinvestor's activity by quarters.
    *dates: a list with the dates in which the superinvestor took action.
        
    Returns:
    *cloning: is a DataFrame that contains the operations that result from cloning a superinvestor.
    
    """
    
    # Initial setup
    cloning = pd.DataFrame(columns = ["Ticker", "Timestamp (Buy)", "Buy Price", "Timestamp (Sell)", "Sell Price"])
    i = 0
    boughtStocks = []
    
    # Cloning
    for date in dates:   
        # Buy operations
        buyOperations = list(superInvestor[date][superInvestor[date]["Activity"] == "Buy"]["Stock"])
    
        for ticker in buyOperations:
            try:
                # Data cleaning
                stock = ticker.replace("\xa0", "")
                stock = stock[0 : stock.find("-")].replace(".", "-")
                
                # Buy operation
                cloning.loc[i, "Ticker"] = stock
                cloning.loc[i, "Timestamp (Buy)"] = pd.to_datetime(date) + dt.timedelta(45)
                cloning.loc[i, "Buy Price"] = yf.download(stock, start = cloning.loc[i, "Timestamp (Buy)"], progress = False)["Adj Close"][0]
            
                boughtStocks.append(stock)
                i += 1
            
            except:
                pass
        
        # Sell operations
        sellOperations = list(superInvestor[date][superInvestor[date]["Activity"] == "Sell 100.00%"]["Stock"])
    
        for ticker in sellOperations:
            # Data cleaning
            stock = ticker.replace("\xa0", "")
            stock = stock[0 : stock.find("-")].replace(".", "-")
        
            # Sell operation
            if stock in boughtStocks:
                try:
                    idx = list(cloning[cloning["Ticker"] == stock].index)
                
                    cloning.loc[idx[-1], "Timestamp (Sell)"] = pd.to_datetime(date) + dt.timedelta(45)
                    cloning.loc[idx[-1], "Sell Price"] = yf.download(stock, start = cloning.loc[idx[-1], "Timestamp (Sell)"], progress = False)["Adj Close"][0]
                
                except:
                    pass
            
    # Current holdings
    for i in range(len(cloning)):
    
        if cloning.loc[i, "Timestamp (Sell)"] is np.nan:
            try:
                cloning.loc[i, "Timestamp (Sell)"] = dt.datetime.today()
                cloning.loc[i, "Sell Price"] = yf.download(cloning.loc[i, "Ticker"], end = cloning.loc[i, "Timestamp (Sell)"], progress = False)["Adj Close"][-1]   
        
            except:
                pass
    
    # Performance
    cloning["Effective Return %"] = (cloning["Sell Price"] / cloning["Buy Price"] - 1) * 100
    cloning["CAGR %"] = ((cloning["Sell Price"] / cloning["Buy Price"]) ** (1 / ((cloning["Timestamp (Sell)"] - cloning["Timestamp (Buy)"]).dt.days.values / 360)) - 1) * 100
           
    return cloning


def metrics(cloning : "Superinvestor's cloning"):
    """
    metrics evaluates the cloning performance.
    
    *cloning: is a DataFrame that contains the operations that result from cloning a superinvestor.
    
    Returns:
    *metricsDF: a DataFrame with some relevant metrics that indicate the cloning performance.
        
    """
    
    metricsDF = pd.DataFrame({"Mean Effective Return %" :  cloning["Effective Return %"].mean(),
                              "Mean CAGR %" : cloning["CAGR %"], 
                               "Mean Holding Period (Years)" : ((cloning["Timestamp (Sell)"] - cloning["Timestamp (Buy)"]).dt.days.values / 360).mean()}, index = [0])
    
    return metricsDF
    