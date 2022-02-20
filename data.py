"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: Cloning Superinvestors                                                                     -- #
# -- script: data.py : python script for data collection                                                 -- #
# -- author: diegolazareno                                                                               -- #
# -- license: GPL-3.0 License                                                                            -- #
# -- repository: https://github.com/diegolazareno/Cloning_Superinvestors                                 -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""

# Required libraries
import pandas as pd


def readData(filePath : "csv file path", sheetName : "Superinvestor's name"):
    """
    readData reads a csv file. 
    
    *filePath: is the csv file path.
    *sheetName: is the superinvestor's name.
    
    Returns:
    *data: a DataFrame that contains the data from the csv file.
    
    """
    
    data = pd.read_excel(filePath, sheet_name = sheetName)
    
    return data

