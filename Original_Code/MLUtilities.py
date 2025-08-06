
import sys
import os
import pickle
import time 
import re

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from pandasql import sqldf
import sqlalchemy

import pyodbc

import Utilities
import importlib
importlib.reload(Utilities)

def setDefaults(df):
    """dictionary for swapping nan test and observations  to defaults

    Args:
        df (dataframe): GenMed dataframe with observations and results. 

    Returns:
        _type_: _description_
    """
    
    replaceValues ={
        "FirstGammaGlutamylTransferase" : 20,
        'FirstBloodGlucose' : 5, # check
        'FirstBPDiastolic' : 80, # check  
        'FirstBPSystolic': 120 , # check 
        'FirstGCSScoreAdult': 15.0,
        'FirstLevelofConsciousness': 0, 
        'FirstO2Flow' : 0, # check  
        'FirstPulseRateBPM' : 80, # check
        #'FirstRespiration': 0, # check
        'FirstRespiration': 15, # check updated 09/01/2024 Amanda note
        'FirstSpO2': 98, # check
        'FirstTemperatureDegreesC':37.5,# check
        # 'FirstWeightKg', 
        'FirstUrinalysisBlood': 0, # check
        'FirstUrinalysisLeukocytes': 0,# check
        'FirstEstimatedGlomerularFiltrationRate': 90, # check
        #'FirstCreatinine',
        'FirstAlbumin':40, 
        'FirstTotalBilirubin':20, 
        'FirstAlkalinePhosphatase':40,
        'FirstAlanineAminotransferase':20, 
        'FirstAspartateAminotransferase':20,
        'FirstGammaGlutamylTransferase':20, 
        'FirstLactateDehydrogenase':200,
        'FirstHaemoglobin':130, 
        'FirstWhiteCellCount':8, 
        'FirstPlateletCount':300,
        'FirstNeutrophils':4, 
        'FirstDDimer':-1, 
        'FirstCreactiveprotein':5,
        'FirstTroponinT':3, 
        'FirstNTproBNP':50,
        'TRIAGE_CATEGORY':0,
        # 'FirstLactateBG':1.5
    }   
    
    
    
    GenMed_Entries_ObsRes_corr = df.copy()
    
    GenMed_Entries_ObsRes_corr['TRIAGE_CATEGORY'] = GenMed_Entries_ObsRes_corr['TRIAGE_CATEGORY'].replace('-99','0')

    missing_mask = GenMed_Entries_ObsRes_corr['FirstCreatinine'].isna()
    missing_dict = dict({'Male':90})
    GenMed_Entries_ObsRes_corr.loc[missing_mask, 'FirstCreatinine'] = GenMed_Entries_ObsRes_corr.loc[missing_mask, 'GENDERCODE'].map(missing_dict) 
    GenMed_Entries_ObsRes_corr['FirstCreatinine'] = GenMed_Entries_ObsRes_corr['FirstCreatinine'].fillna(70)
    GenMed_Entries_ObsRes_corr['FirstCreatinine'] = pd.to_numeric(GenMed_Entries_ObsRes_corr['FirstCreatinine']) #,errors='coerce')


    missing_mask = df['FirstWeightKg'].isna()
    missing_dict = dict({'Male':90})
    GenMed_Entries_ObsRes_corr.loc[missing_mask, 'FirstWeightKg'] = GenMed_Entries_ObsRes_corr.loc[missing_mask, 'GENDERCODE'].map(missing_dict) 
    GenMed_Entries_ObsRes_corr['FirstWeightKg'] = GenMed_Entries_ObsRes_corr['FirstWeightKg'].fillna(70)
    GenMed_Entries_ObsRes_corr['FirstWeightKg'] = pd.to_numeric(GenMed_Entries_ObsRes_corr['FirstWeightKg']) #,errors='coerce')

    for key in replaceValues:    
        # print(key) #,replaceValues[key])
        GenMed_Entries_ObsRes_corr[key] = GenMed_Entries_ObsRes_corr[key].fillna(replaceValues[key])
        GenMed_Entries_ObsRes_corr[key] = pd.to_numeric(GenMed_Entries_ObsRes_corr[key],errors='coerce')
        #print( GenMed_Entries_ObsRes_corr[key].unique())
        
    

    return GenMed_Entries_ObsRes_corr
    
def setDefaultsLactate(df):
    """dictionary for swapping nan test and observations  to defaults

    Args:
        df (dataframe): GenMed dataframe with observations and results. 

    Returns:
        _type_: _description_
    """
    
    replaceValues ={
        "FirstGammaGlutamylTransferase" : 20,
        'FirstBloodGlucose' : 5, # check
        'FirstBPDiastolic' : 80, # check  
        'FirstBPSystolic': 120 , # check 
        'FirstGCSScoreAdult': 15.0,
        'FirstLevelofConsciousness': 0, 
        'FirstO2Flow' : 0, # check  
        'FirstPulseRateBPM' : 80, # check
        #'FirstRespiration': 0, # check
        'FirstRespiration': 15, # check updated 09/01/2024 Amanda note
        'FirstSpO2': 98, # check
        'FirstTemperatureDegreesC':37.5,# check
        # 'FirstWeightKg', 
        'FirstUrinalysisBlood': 0, # check
        'FirstUrinalysisLeukocytes': 0,# check
        'FirstEstimatedGlomerularFiltrationRate': 90, # check
        #'FirstCreatinine',
        'FirstAlbumin':40, 
        'FirstTotalBilirubin':20, 
        'FirstAlkalinePhosphatase':40,
        'FirstAlanineAminotransferase':20, 
        'FirstAspartateAminotransferase':20,
        'FirstGammaGlutamylTransferase':20, 
        'FirstLactateDehydrogenase':200,
        'FirstHaemoglobin':130, 
        'FirstWhiteCellCount':8, 
        'FirstPlateletCount':300,
        'FirstNeutrophils':4, 
        'FirstDDimer':-1, 
        'FirstCreactiveprotein':5,
        'FirstTroponinT':3, 
        'FirstNTproBNP':50,
        'TRIAGE_CATEGORY':0,
        'FirstLactateBG':1.5,
        'FirstBaseExcessBG':0.0
    }  
    

    GenMed_Entries_ObsRes_corr = df.copy()
    
    GenMed_Entries_ObsRes_corr['TRIAGE_CATEGORY'] = GenMed_Entries_ObsRes_corr['TRIAGE_CATEGORY'].replace('-99','0')

    missing_mask = GenMed_Entries_ObsRes_corr['FirstCreatinine'].isna()
    missing_dict = dict({'Male':90})
    GenMed_Entries_ObsRes_corr.loc[missing_mask, 'FirstCreatinine'] = GenMed_Entries_ObsRes_corr.loc[missing_mask, 'GENDERCODE'].map(missing_dict) 
    GenMed_Entries_ObsRes_corr['FirstCreatinine'] = GenMed_Entries_ObsRes_corr['FirstCreatinine'].fillna(70)
    GenMed_Entries_ObsRes_corr['FirstCreatinine'] = pd.to_numeric(GenMed_Entries_ObsRes_corr['FirstCreatinine']) #,errors='coerce')


    missing_mask = df['FirstWeightKg'].isna()
    missing_dict = dict({'Male':90})
    GenMed_Entries_ObsRes_corr.loc[missing_mask, 'FirstWeightKg'] = GenMed_Entries_ObsRes_corr.loc[missing_mask, 'GENDERCODE'].map(missing_dict) 
    GenMed_Entries_ObsRes_corr['FirstWeightKg'] = GenMed_Entries_ObsRes_corr['FirstWeightKg'].fillna(70)
    GenMed_Entries_ObsRes_corr['FirstWeightKg'] = pd.to_numeric(GenMed_Entries_ObsRes_corr['FirstWeightKg']) #,errors='coerce')

    for key in replaceValues:    
        # print(key,replaceValues[key])
        GenMed_Entries_ObsRes_corr[key] = GenMed_Entries_ObsRes_corr[key].fillna(replaceValues[key])
        GenMed_Entries_ObsRes_corr[key] = pd.to_numeric(GenMed_Entries_ObsRes_corr[key],errors='coerce')
        #print( GenMed_Entries_ObsRes_corr[key].unique())
        
    

    return GenMed_Entries_ObsRes_corr



def setNumeric(GenMed_Entries_ObsRes_corr):
    
    
    replaceValues = {
        "FirstGammaGlutamylTransferase" : 20,
        'FirstBloodGlucose' : 5, # check
        'FirstBPDiastolic' : 80, # check  
        'FirstBPSystolic': 120 , # check 
        'FirstGCSScoreAdult': 15.0,
        'FirstLevelofConsciousness': 0, 
        'FirstO2Flow' : 0, # check  
        'FirstPulseRateBPM' : 80, # check
        'FirstRespiration': 0, # check
        'FirstSpO2': 98, # check
        'FirstTemperatureDegreesC':37.5,# check
        'FirstWeightKg': 0, 
        'FirstUrinalysisBlood': 0, # check
        'FirstUrinalysisLeukocytes': 0,# check
        'FirstEstimatedGlomerularFiltrationRate': 90, # check
        'FirstCreatinine': 0,
        'FirstAlbumin':40, 
        'FirstTotalBilirubin':20, 
        'FirstAlkalinePhosphatase':40,
        'FirstAlanineAminotransferase':20, 
        'FirstAspartateAminotransferase':20,
        'FirstGammaGlutamylTransferase':20, 
        'FirstLactateDehydrogenase':200,
        'FirstHaemoglobin':130, 
        'FirstWhiteCellCount':8, 
        'FirstPlateletCount':300,
        'FirstNeutrophils':4, 
        'FirstDDimer':-1, 
        'FirstCreactiveprotein':5,
        'FirstTroponinT':3, 
        'FirstNTproBNP':50,
        'TRIAGE_CATEGORY':0,
    }   
    
    
    
    for key in replaceValues:    
        #print(key) #,replaceValues[key])
        #GenMed_Entries_ObsRes_corr[key] = GenMed_Entries_ObsRes_corr[key].fillna(replaceValues[key])
        GenMed_Entries_ObsRes_corr[key] = pd.to_numeric(GenMed_Entries_ObsRes_corr[key],errors='coerce')
    
    
    return GenMed_Entries_ObsRes_corr