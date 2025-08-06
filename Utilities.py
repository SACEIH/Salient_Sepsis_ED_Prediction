# Import Python Libraries 

import sys
import os
import pickle
import time 

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from pandasql import sqldf
import sqlalchemy
import snowflake.connector

import pyodbc

import Utilities
import importlib
importlib.reload(Utilities)



def getConnection():
    con = snowflake.connector.connect(
        account='wt61814.australia-east.privatelink',
        user="iain.bertram@sa.gov.au",
        database="DEV_DAP_CAE05_DB",
        warehouse="DEV_DAP_CAE05_M_WH",
        authenticator="externalbrowser",
        )

    return con

def getVisits(start_date, end_date, con):
    """
    Returns the visits table for processing as a data frame with variable types set appropriately.


    Args:
        Facility (str): String representing the hospital
        start_date (datetime): date/time to start data set
        end_date (datetime):date/time to end data set
        engine (sqlalchemy.engine): connection to the database

    Returns:
        panda.DataFrame: Visits Table Dataframe
    """

    visits_df = None

    query = sql_visit_query().format(start_date, end_date)
    # print(query)

    visits_df = pd.read_sql(query,con)

    # with engine.begin() as conn:
    #     visits_df = pd.read_sql_query(sqlalchemy.text(query), conn)

    # Drop Duplicates
    # visits_df.drop_duplicates(inplace=True)

    # Set default data types to make processing easier

    # visits_df['SAUHI'] = visits_df['SAUHI'].astype('Int64')
    # visits_df['VisitID'] = visits_df['VisitID'].astype('Int64')
    # visits_df["ChartGUID"] = visits_df["ChartGUID"].astype("Int64")
    # visits_df["ClientGUID"] = visits_df["ClientGUID"].astype("Int64")
    # visits_df["VisitGUID"] = visits_df["VisitGUID"].astype("Int64")

    # # visits_df['DischargeDispositionCode'] = visits_df['DischargeDispositionCode'].astype('Int64')
    # visits_df["AdmitDate"] = visits_df["AdmitDate"].apply(pd.to_datetime)
    # visits_df["DischargeDate"] = visits_df["DischargeDate"].apply(pd.to_datetime)

    # visits_df["VisitType"].replace("Emergency      ", "Emergency", inplace=True)
    # visits_df["VisitType"].replace("Inpatient      ", "Inpatient", inplace=True)

    # selectedList = ["Aboriginal", "Aboriginal and TSI", "TSI"]
    # idx = visits_df[visits_df.indigeneous.isin(selectedList)].index
    # visits_df["IndigenousFlag"] = 0
    # visits_df.loc[idx, "IndigenousFlag"] = 1

    return visits_df


def getDiagnosis( start_date, end_date, con):
    
    diagnoses_df = None
    query = queryDiagnosis().format(start_date, end_date)
    # print(query)
    diagnoses_df = pd.read_sql(query,con)
    
    
    diagnosis_HA_df = None 
    query = queryDiagnosisHA().format(start_date, end_date)
    # print(query)
    diagnoses_HA_df = pd.read_sql(query,con)
    
    return diagnoses_df,diagnoses_HA_df  

def getEDVisitReasons( start_date, end_date, con):
    visitReasons_df = None
    query = queryEDVisitReasons().format(start_date, end_date)
    # print(query)
    visitReasons_df = pd.read_sql(query,con)
 
    return visitReasons_df 



def addFlags(df):
    
    df["SepsisFlag"] = df.apply(lambda row: sepsis_flag(row['DIAGNOSIS_LIST']), axis = 1)
    df["COPDFlag"] = df.apply(lambda row: copd_flag(row['DIAGNOSIS_LIST']), axis = 1)
    df["PneumoniaFlag"] = df.apply(lambda row: pneumonia_flag(row['DIAGNOSIS_LIST']), axis = 1)
    df["PEFlag"] = df.apply(lambda row: PE_flag(row['DIAGNOSIS_LIST']), axis = 1)
    df["HeartFailureFlag"] = df.apply(lambda row: heartfailure_flag(row['DIAGNOSIS_LIST']), axis = 1)
    df["UTIFlag"] = df.apply(lambda row: uti_flag(row['DIAGNOSIS_LIST']), axis = 1)    
    
    df['SepsisFlag'] = df['SepsisFlag'].astype('Int64')
    df['COPDFlag'] = df['COPDFlag'].astype('Int64')
    df['PneumoniaFlag'] = df['PneumoniaFlag'].astype('Int64')
    df['PEFlag'] = df['PEFlag'].astype('Int64')
    df['HeartFailureFlag'] = df['HeartFailureFlag'].astype('Int64')
    df['UTIFlag'] = df['UTIFlag'].astype('Int64')

    
    df["HASepsisFlag"] = df.apply(lambda row: sepsis_flag(row['HA_DIAGNOSIS_LIST']), axis = 1)
    df['HASepsisFlag'] = df['HASepsisFlag'].astype('Int64')

    
    return df



def sepsis_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to Sepsis.

    Parameters
    ----------
    inputString: str
    space separated list of ICD10 diagnosis codes

    Returns
    -------
    SepsisFlag: int
        1 if a sepsis diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(
        [
            "A021",
            "A227",
            "A267",
            "A327",
            "A40",
            "A400",
            "A401",
            "A402",
            "A403",
            "A408",
            "A409",
            "A41",
            "A410",
            "A411",
            "A412",
            "A413",
            "A414",
            "A415",
            "A4150",
            "A4151",
            "A4152",
            "A4158",
            "A418",
            "A419",
            "A427",
            "B377",
            "O85",
            "P36",
            "P360",
            "P361",
            "P362",
            "P363",
            "P364",
            "P365",
            "P368",
            "P369",
            "R651",
        ]
    )
    # print())
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return 0
    #    return 1
    # else:
    #    return 0


def copd_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to COPD.

    Parameters
    ----------
    inputString: str
       space separated list of ICD10 diagnosis codes

    Returns
    -------
    COPDFlag: int
        1 if a sepsis diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(["J44", "J440", "J441", "J448", "J449"])
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return 0
    
    # return int(bool(diagnosisList & set(inputString.split())))


def PE_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to Pulmonary Embolism.

    Parameters
    ----------
    inputString: str
       space separated list of ICD10 diagnosis codes

    Returns
    -------
    PEFlag: int
        1 if a Pulmonary Embolism diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(["I26", "I260", "I269"])
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return 0
    


def heartfailure_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to Heart Failure.

    Parameters
    ----------
    inputString: str
       space separated list of ICD10 diagnosis codes

    Returns
    -------
    HFFlag: int
        1 if a Heart Failure diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(
        [
            "I110",
            "I130",
            "I50",
            "I500",
            "I509",
            "U822",
            "I501",
            "P290",
            "E1053",
            "E1153",
            "E1353",
            "E1453",
            "I255",
            "I42",
            "I420",
            "I421",
            "I422",
            "I425",
            "I426",
            "I427",
            "I428",
            "I429",
            "I43",
            "I430",
            "I431",
            "I432",
            "I438",
            "O903",
        ]
    )
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return None
    


def uti_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to UTI.

    Parameters
    ----------
    inputString: str
       space separated list of ICD10 diagnosis codes

    Returns
    -------
    UTIFlag: int
        1 if a UTI diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(
        [
            "N9952",
            "O23",
            "O233",
            "O234",
            "O862",
            "P393",
            "N390",
            "N136",
            "N10",
            "N11",
            "N111",
            "N118",
            "N119",
            "N12",
        ]
    )
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return 0
    


def pneumonia_flag(inputString):
    """
    Return 1 if one of a list of ICD10 diagnosis codes corresponds to Pneumonia.

    Parameters
    ----------
    inputString: str
       space separated list of ICD10 diagnosis codes

    Returns
    -------
    PneumoniaFlag: int
        1 if a Pneumonia diagnosis is included in the list, 0 otherwise
    """
    diagnosisList = set(
        [
            "B012",
            "B052",
            "B250",
            "J100",
            "J12",
            "J120",
            "J121",
            "J122",
            "J123",
            "J128",
            "J129",
            "J13",
            "J14",
            "J15",
            "J150",
            "J151",
            "J152",
            "J153",
            "J154",
            "J155",
            "J156",
            "J157",
            "J158",
            "J159",
            "J16",
            "J160",
            "J168",
            "J17",
            "J170",
            "J171",
            "J172",
            "J173",
            "J178",
            "J18",
            "J180",
            "J181",
            "J182",
            "J188",
            "J189",
            "J200",
            "J67",
            "J678",
            "J679",
            "J680",
            "J69",
            "J690",
            "J691",
            "J698",
            "J851",
            "J9582",
            "P23",
            "P230",
            "P231",
            "P232",
            "P233",
            "P234",
            "P235",
            "P236",
            "P238",
            "P239",
        ]
    )
    if not pd.isnull(inputString): # is not None:
        return int(bool(diagnosisList & set(inputString.split())))
    else:
        return 0
    

def LinkEmergencyInformation(df,visits_df):
    
    # i = 1
    
    df[['TRIAGE_CATEGORY','EDDIAGNOSISCODE','ED_VISIT_REASON','ED_VISITGUID']] = df.apply(lambda row: getEDInfo(row,visits_df), axis='columns', result_type='expand')
    
    # journeyCode =  df.iloc[i].JOURNEY_ID
    # print(journeyCode)
    
    # admitType =  df.iloc[i].ADMITTYPE
    # print(admitType)
    # ED_dischargedtm =  visits_df[(visits_df.JOURNEY_ID == journeyCode)& (visits_df.TYPECODE=='Emergency')].iloc[0].DISCHARGEDTM  
    # admitDtm = df.iloc[i].ADMITDTM
    # print(ED_dischargedtm)
    # print(    admitDtm )
    # print(timeDiff(ED_dischargedtm,admitDtm))
    
    # print(getEDInfo(df.iloc[100],visits_df))
    
    # print(visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')][['TRIAGE_CATEGORY','EDDIAGNOSISCODE','ED_VISIT_REASON']])
    
    
    
    return df

def getEDInfo(row,visits_df):
    
    TriageCategory = None # visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].TRIAGE_CATEGORY
    EDDiagnosis =   None  # visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].EDDIAGNOSISCODE
    EDVisitReason = None # visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].ED_VISIT_REASON
    ED_VISITGUID = None 
    
    admitType =  row.ADMITTYPE
    
    # count = 0
    
    # if (row.SOURCEOFREFERRAL == 'IP Casualty-Emergency'):
    if (admitType=='Emergency'):
    
        # count +=1
        # if count > 20: break
        journeyCode =  row.JOURNEY_ID
        admitDtm =row.ADMITDTM

        checkLength =  len(visits_df[(visits_df.JOURNEY_ID == journeyCode)& (visits_df.TYPECODE=='Emergency')].index)



        if (checkLength == 1):
            ED_dischargedtm = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].DISCHARGEDTM  
            if (timeDiff(admitDtm,ED_dischargedtm) < 24):
                TriageCategory = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].TRIAGE_CATEGORY
                EDDiagnosis = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].EDDIAGNOSISCODE
                EDVisitReason = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].ED_VISIT_REASON
                ED_VISITGUID = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].VISITGUID
        elif (checkLength >= 1):
            # print(journeyCode )
            EDList = []
            # print("Length - ",checkLength,row.SOURCEOFREFERRAL,journeyCode,row.CLIENTGUID,row.CHARTGUID,row.VISITGUID)
            tmp_df = visits_df[(visits_df.JOURNEY_ID == journeyCode)& (visits_df.TYPECODE=='Emergency')].copy()
            tmp_df = tmp_df.reset_index(drop=True)
            for i in range(checkLength):
                ED_dischargedtm = tmp_df.iloc[i].DISCHARGEDTM  
                # print(i,timeDiff(admitDtm,ED_dischargedtm))
                EDList.append(np.abs(timeDiff(admitDtm,ED_dischargedtm,)))
            # print(EDList,np.min(EDList),EDList.index(np.min(EDList)))
            i = EDList.index(np.min(EDList))
            ED_dischargedtm = tmp_df.iloc[i].DISCHARGEDTM  
            if (timeDiff(admitDtm,ED_dischargedtm) < 24):
                TriageCategory = tmp_df.iloc[i].TRIAGE_CATEGORY
                EDDiagnosis = tmp_df.iloc[i].EDDIAGNOSISCODE
                EDVisitReason = tmp_df.iloc[i].ED_VISIT_REASON
                ED_VISITGUID = tmp_df.iloc[i].VISITGUID

            
            
            #


        else: 
            if row.SOURCEOFREFERRAL == 'IP Casualty-Emergency' or  row.SOURCEOFREFERRAL == 'IP Inter-hospital transfer' : # Look for ED within 24 hours 
                # print('IP Casualty-Emergency -- ',journeyCode,row.CLIENTGUID,row.CHARTGUID)
                EDList = []
                # print("Length - ",checkLength,row.SOURCEOFREFERRAL,journeyCode,row.CLIENTGUID,row.CHARTGUID,row.VISITGUID)
                tmp_df = visits_df[(visits_df.CLIENTGUID == row.CLIENTGUID)& (visits_df.TYPECODE=='Emergency')].copy()
                tmp_df = tmp_df.reset_index(drop=True)
                
                if len(tmp_df.index)>0:
                
                    for i in range(len(tmp_df.index)):
                        ED_dischargedtm = tmp_df.iloc[i].DISCHARGEDTM  
                        # print(i,timeDiff(admitDtm,ED_dischargedtm))
                        EDList.append(np.abs(timeDiff(admitDtm,ED_dischargedtm,)))
                    # print(EDList,np.min(EDList),EDList.index(np.min(EDList)))
                    
                    i = EDList.index(np.min(EDList))
                    ED_dischargedtm = tmp_df.iloc[i].DISCHARGEDTM  
                    if (np.abs(timeDiff(admitDtm,ED_dischargedtm)) < 24):
                        TriageCategory = tmp_df.iloc[i].TRIAGE_CATEGORY
                        EDDiagnosis = tmp_df.iloc[i].EDDIAGNOSISCODE
                        EDVisitReason = tmp_df.iloc[i].ED_VISIT_REASON
                        ED_VISITGUID = tmp_df.iloc[i].VISITGUID
                    
                
            # elif:
                # print('IP Inter-hospital transfer -- ',journeyCode,row.CLIENTGUID,row.CHARTGUID)
            elif row.SOURCEOFREFERRAL == 'IP Administrative admission' :
                pass
            elif row.SOURCEOFREFERRAL=='IP Other':
                pass
            elif row.SOURCEOFREFERRAL == ' IP Outpatient department':
                pass
            else : 
                print('**** - ',row.SOURCEOFREFERRAL,journeyCode,row.CLIENTGUID,row.CHARTGUID)


        # try:

        #     ED_dischargedtm =  visits_df[(visits_df.JOURNEY_ID == journeyCode)& (visits_df.TYPECODE=='Emergency')].iloc[0].DISCHARGEDTM  
        #     admitDtm =row.ADMITDTM
        #     # print(ED_dischargedtm)
        #     # print(    admitDtm )
        #     # print(timeDiff(ED_dischargedtm,admitDtm))
        
        
        #     if (timeDiff(ED_dischargedtm,admitDtm) < 24):
        
        #         TriageCategory = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].TRIAGE_CATEGORY
        #         EDDiagnosis = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].EDDIAGNOSISCODE
        #         EDVisitReason = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].ED_VISIT_REASON
        #         ED_VISITGUID = visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')].iloc[0].VISITGUID
        # except:
        #     try:
        #         ChartGUID = row.CHARTGUID
        #         TriageCategory = visits_df[(visits_df.CHARTGUID == ChartGUID) & (visits_df.TYPECODE=='Emergency')].iloc[0].TRIAGE_CATEGORY
        #         EDDiagnosis = visits_df[(visits_df.CHARTGUID == ChartGUID) & (visits_df.TYPECODE=='Emergency')].iloc[0].EDDIAGNOSISCODE
        #         EDVisitReason = visits_df[(visits_df.CHARTGUID == ChartGUID) & (visits_df.TYPECODE=='Emergency')].iloc[0].ED_VISIT_REASON
        #     except:
        #         print(journeyCode,row.CLIENTGUID,ChartGUID)

            
            
            #print(journeyCode)
        
    return TriageCategory,EDDiagnosis,EDVisitReason,ED_VISITGUID
# visits_df[(visits_df.JOURNEY_ID == journeyCode) & (visits_df.TYPECODE=='Emergency')][['TRIAGE_CATEGORY','EDDIAGNOSISCODE','ED_VISIT_REASON']]
    

def sob_flag(df, row):
    """return flag if visit table has a shortness of breath in presenting problems. 

    Args:
        df (dataframe): emergency visits table 
        row (dataframe row): GenMed vists row that is being mapped to emergency visit

    Returns:
        int: 1 if Shortness of breath is noted. 
    """
    originalProblemList = ['Resp Distress / Shortness Of Breath', 'Respiratory Distress / S.O.B.',
                            'Resp.Distress/Short Of Breath', 'Resp.Distress/Shortness of Breath',
                            'Distress & Short Of Breath (Sob)']

    inputString = ' '
    try:
        inputString = df.loc[df.SunriseVisitIdCode==row['EDVisitID']].PresentingProblemDetails.values[0]
    except:
        inputString = ''

    if inputString in originalProblemList:
        return 1
    else:
        return 0

def timeDiff(first_dtm, second_dtm):
    """
    Calculates the datetime difference between two datetimes  in hours. 
    In this case the end date corresponds to ED discharge so if NAT 
    sets to zero as by definition goes straight to ward. 
    
    Parameters
    ----------
    first_dtm: datetime 
        datetime of first event
        
    second_dtm: datetime 
        datetime of second event
    
    Returns
    -------
    diff: float
        time difference measured in hours 
    """
    if pd.isna(first_dtm) == False:
        diff = (second_dtm - first_dtm)/np.timedelta64(1, 'h')
    else: 
        diff = 0.
    return diff

def linkClientInformation(GenMed_Encounters, Facility,start_date,end_date, engine ):
    """Link client information to GenMed encounters (replace  with SQL)

    Args:
        GenMed_Encounters (dataframe): GenMed encounters dataframe 
        Facility (str): String representing the hospital 
        start_date (datetime): date/time to start data set
        end_date (datetime):date/time to end data set
        engine (sqlalchemy.engine): connection to the database 

    Returns:
        panda.DataFrame: GenMed Table Dataframe 
    """
    with engine.begin() as conn:
        client_df = pd.read_sql_query(sqlalchemy.text(query_Client().format(Facility,start_date,end_date)), conn)

    client_df['SAUHI'] = client_df['SAUHI'].astype('Int64')
    client_df['BirthDate'] = client_df['BirthDate'].apply(pd.to_datetime)

    GenMed_Encounters["Gender"] = GenMed_Encounters.apply(lambda row: Gender(client_df, row['SAUHI']), axis = 1)
    GenMed_Encounters["IndigenousStatusDescription"] = GenMed_Encounters.apply(lambda row: Indigenous(client_df, row['SAUHI']), axis = 1)
    selectedList = ['Aboriginal','Aboriginal and TSI', 'TSI']
    idx = GenMed_Encounters[GenMed_Encounters.IndigenousStatusDescription.isin(selectedList)].index
    GenMed_Encounters['IndigenousFlag']=0
    GenMed_Encounters.loc[idx,'IndigenousFlag']=1

    GenMed_Encounters["AgeOnAdmission"] = GenMed_Encounters.apply(lambda row: ageOnAdmission(client_df, row['SAUHI'], row['AdmitDate']), axis = 1)

    return GenMed_Encounters.copy()


def Gender(df, Id):
    """Return sex from Client table 

    Args:
        df (dataframe): Clients dataframe
        Id (int): Sauhi

    Returns:
        str: Gender Code
    """
    #print(Id)
    try:
        return df.loc[df.SAUHI==Id]['Gender'].values[0]
    except:
        return 'Unknown'  #None
    
def Indigenous(df, Id):
    """Return Indigenous status  from Client table 

    Args:
        df (dataframe): Clients dataframe
        Id (int): Sauhi

    Returns:
        str: Indigenous status Code
    """
    #print(Id)
    try:
        return df.loc[df.SAUHI==Id]['IndigenousStatusDescription'].values[0]
    except:
        return None  #None
    

def ageOnAdmission(df ,Id, second_dtm):
    """Return age on admission in years

    Args:
        df (dataframe): Clients dataframe
        Id (int): Sauhi

    Returns:
        int: age on admission 
    """
    first_dtm = None 

    try:
        first_dtm = df.loc[df.SAUHI==Id]['BirthDate'].values[0]
    except:
        print(Id," Failed")

    if pd.isna(first_dtm) == False:
        tenure = (second_dtm - first_dtm)/np.timedelta64(1, 'Y')
    else: 
        tenure = 0.
    return int(tenure)


def linkResults(df, Facility, engine ):
    """Add associated test results and report times to GenMed table. 

    Args:
        df (dataframe): GenMed dataframe 
        Facility (str): String representing the hospital 
        engine (sqlalchemy.engine): connection to the database 

    Returns:
        panda.DataFrame: GenMed  Dataframe  with results added 
    """


    Res_Of_Interest = getResultsofInterest()
    listOfResKeys=list(Res_Of_Interest.keys())
    listofResKeys2 = listOfResKeys.copy()
    for i in range(len(listofResKeys2)):
        listofResKeys2[i] = listofResKeys2[i]+"Dtm"


    GenMed_Encounters_withObs = pd.concat(
        [df, pd.DataFrame([[None,]*(len(listOfResKeys)+len(listofResKeys2))],
        index=df.index,
        columns=listOfResKeys+listofResKeys2)], axis=1)

    length = len(GenMed_Encounters_withObs.index)
    numberCheck = re.compile(".*\d.*")

    
    for i in range(length):
        if i% 100==0: print(" count {}".format(i))
        #if i > 100: break
        sauhi = GenMed_Encounters_withObs.iloc[i].SAUHI
        visitGUID = GenMed_Encounters_withObs.iloc[i].VisitGUID
        start_date = pd.Timestamp(GenMed_Encounters_withObs.iloc[i].AdmitDate)  #.values[0])
        ed_start_date = pd.Timestamp(GenMed_Encounters_withObs.iloc[i].EDAdmitDate) #.values[0])
        if not pd.isnull(ed_start_date): start_date = ed_start_date
        start_date = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date = pd.Timestamp(GenMed_Encounters_withObs.iloc[i].DischargeDate) #.values[0])
        try:
            end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
        except:
            end_date = "2023-06-01 00:00:00"
            #end_date = end_date.strftime("%Y-%m-%d %H:%M:%S")
            
        
        
        retryFlag = True
        retry_count = 0 
        while retry_count<3 and retryFlag:
            try:           
        
                with engine.begin() as conn:
                    res2_df = pd.read_sql_query(sqlalchemy.text(query_Results().format(sauhi, start_date, end_date)), conn)
                    res2_df = res2_df.dropna(axis=0, subset='ObservationValue')
                    res2_df = res2_df.loc[res2_df['ObservationValue'].str.match(numberCheck)]
                    for key in Res_Of_Interest:
                        #print (key,Res_Of_Interest[key])
                        #res2_df.loc[res2_df.ObservationName==Res_Of_Interest[key]

                        ##tmp = res2_df.dropna(axis=0, subset=Res_Of_Interest[key])
                        ##tmp = tmp[tmp[Res_Of_Interest[key]].str.match(numberCheck)]
                        
                        lenRes = len(res2_df.loc[res2_df.ObservationName==Res_Of_Interest[key]])
                        #print(key, lenRes)
                        if (lenRes>0):
                            #tmpValue = tmp.iloc[0].ObservationValue
                            #tmpDate=   tmp.iloc[0].Report_DateTime	

                            tmpValue = res2_df.loc[res2_df.ObservationName==Res_Of_Interest[key]].iloc[0].ObservationValue
                            tmpDate=   res2_df.loc[res2_df.ObservationName==Res_Of_Interest[key]].iloc[0].Report_DateTime	
                            #print(tmpValue, tmpDate)
                            GenMed_Encounters_withObs.loc[GenMed_Encounters_withObs.VisitGUID==visitGUID, key] = tmpValue
                            GenMed_Encounters_withObs.loc[GenMed_Encounters_withObs.VisitGUID==visitGUID, key+'Dtm'] = tmpDate

                retryFlag=False
            except Exception as e:
                print("Exception")
                print(e)
                retry_count+=1 
                time.sleep(5) 
               

    return GenMed_Encounters_withObs



def getResultsofInterest():
    """list of Results to be included in table 

    Returns:
        dictionary: dictionary matching column name with test resulkt name 
    """
    return  {'FirstEstimatedGlomerularFiltrationRate':'.Estimated Glomerular Filtration Rate',      # 30533271
    'FirstCreatinine':'Creatinine - Serum',						   
    'FirstAlbumin':'Albumin Level',                                   
    'FirstTotalBilirubin':'Bilirubin Level Total',                           
    'FirstAlkalinePhosphatase':'Alkaline Phosphatase Level',        #        21705432       
    'FirstAlanineAminotransferase':'Alanine Aminotransferase Level',                 # 21705002 
    'FirstAspartateAminotransferase':'Aspartate Aminotransferase',                # 21704990
    'FirstGammaGlutamylTransferase':'Gamma Glutamyl Transferase Level',                # 21705790
    'FirstLactateDehydrogenase':'Lactate Dehydrogenase',           # 21705434          
    'FirstHaemoglobin':'Haemoglobin',                            # 23708756   
    'FirstWhiteCellCount':'White Cell Count',                          # 23708746
    'FirstPlateletCount':'Platelet Count',                            # 23708742
    'FirstNeutrophils':'Absolute Neutrophil Count',                               # 21705348
    'FirstDDimer':'D-Dimer',                                   # 21705596
    'FirstCreactiveprotein':'C-Reactive Protein',                # 21704974        
    'FirstTroponinT':'Troponin T Level',                                # 21705122
    'FirstNTproBNP':'NT-pro Brain Natriuretic Peptide',          # 23256967



    'First50pOxygenSaturationVenous':'50% Oxygen Saturation Venous', # 30527181
    'FirstAnionGapVenous':'Anion Gap Venous',
    'FirstBaseExcessVenous': 'Base Excess Venous',
    # 'FirstBicarbonateCalculatedVenous':'Bicarbonate Calculated Venous',
    'FirstBilirubinVenous':'Bilirubin Venous',
    'FirstCarboxyhaemoglobinVenous':'Carboxyhaemoglobin Venous',
    'FirstChlorideDirectVenous':'Chloride Direct Venous',
    'FirstCreatinineVenous':'Creatinine Venous',
    'FirstGlucoseVenous':'Glucose Venous',
    # 'FirstHIonConcentrationVenous':'H Ion Concentration Venous',
    # 'FirstInspiredO2Venous':'Inspired O2 Venous',
    'FirstIonised Calcium Venous':'Ionised Calcium Venous',
    'FirstLactateVenous':'Lactate Venous',
    'FirstMethaemoglobinVenous':'Methaemoglobin Venous',
    'FirstOxygenSaturationVenous':'Oxygen Saturation Venous',
    'FirstOxyhaemoglobinVenous':'Oxyhaemoglobin Venous',
    'FirstpCO2Venous':'pCO2 Venous',
    'FirstpHVenous':'pH Venous',
    'FirstpO2Venous':'pO2 Venous',
    'FirstPotassiumDirectVenous':'Potassium Direct Venous',
    'FirstReducedHaemoglobinVenous':'Reduced Haemoglobin Venous',
    'FirstSodiumDirectVenous':'Sodium Direct Venous',
    'FirstTotalHaemoglobinVenous':'Total Haemoglobin Venous',

    # Res_Of_Interest2 = { 
    'First50pOxygenSaturationArterial':'50% Oxygen Saturation Arterial',
    'FirstAnionGapArterial':'Anion Gap Arterial',
    'FirstBaseExcessArterial':'Base Excess Arterial',
    'FirstBicarbonateCalculatedArterial':'Bicarbonate Calculated Arterial', 
    'FirstBilirubinArterial':'Bilirubin Arterial',
    'FirstCarboxyhaemoglobinArterial':'Carboxyhaemoglobin Arterial',
    'FirstChlorideDirectArterial':'Chloride Direct Arterial',
    'FirstCreatinineArterial':'Creatinine Arterial',
    'FirstGlucoseArterial':'Glucose Arterial',
    # 'FirstHIonConcentrationArterial':'H Ion Concentration Arterial',
    # 'FirstInspiredO2Arterial':'Inspired O2 Arterial',
    'FirstIonised Calcium Arterial':'Ionised Calcium Arterial',
    'FirstLactateArterial':'Lactate Arterial',
    'FirstMethaemoglobinArterial':'Methaemoglobin Arterial',
    'FirstOxygenSaturationArterial':'Oxygen Saturation Arterial',
    'FirstOxyhaemoglobinArterial':'Oxyhaemoglobin Arterial',
    'FirstpCO2Arterial':'pCO2 Arterial',
    'FirstpHArterial':'pH Arterial',
    'FirstpO2Arterial':'pO2 Arterial',
    'FirstPotassiumDirectArterial':'Potassium Direct Arterial',
    'FirstReducedHaemoglobinArterial':'Reduced Haemoglobin Arterial',
    'FirstSodiumDirectArterial':'Sodium Direct Arterial',
    'FirstTotalHaemoglobinArterial':'Total Haemoglobin Arterial',
    }



def linkObservations(df, Facility, engine ):
    """Add associated observations  and report times to GenMed table. 

    Args:
        df (dataframe): GenMed dataframe 
        Facility (str): String representing the hospital 
        engine (sqlalchemy.engine): connection to the database 

    Returns:
        panda.DataFrame: GenMed  Dataframe  with observations added 
    """
    Obs_Of_Interest = getObs_Of_Interest()
    listOfObs =  list(Obs_Of_Interest.keys()) #   ['FirstBloodGlucose', 'FirstBPDiastolic', 'FirstBPSystolic', 'FirstGCSScoreAdult', 'FirstLevelofConsciousness', 'FirstO2Flow', 'FirstPulseRateBPM', 'FirstRespiration', 'FirstSpO2', 'FirstTemperatureDegreesC', 'FirstWeightKg', 'FirstUrinalysisBlood', 'FirstUrinalysisLeukocytes']
    listofObsTimes = listOfObs.copy()
    for i in range(len(listofObsTimes)):
        listofObsTimes[i] = listofObsTimes[i]+"Dtm"


    GenMed_Encounters_withObsAll = pd.concat(
        [df, pd.DataFrame([[None,]*(len(listOfObs)+len(listofObsTimes))],
        index=df.index,
        columns=listOfObs+listofObsTimes)], axis=1)

    length = len(GenMed_Encounters_withObsAll.index)
    numberCheck = re.compile(".*\d.*")

    count=0

    for i in range(0,length):
        if i% 100==0: 
            print(" count {}".format(i))
            #time.sleep(15)
        #if i > 10: break
        visitGUID = GenMed_Encounters_withObsAll.iloc[i].VisitGUID        
        if visitGUID is not None:
            #print(queryObs2.format(visitGUID))
            
            retryFlag = True
            retry_count = 0 
            while retry_count<3 and retryFlag:
                try:
                    with engine.begin() as conn:
                        obs_df = pd.read_sql_query(sqlalchemy.text(queryObs().format(visitGUID)), conn)
                        obs_df = obs_df.dropna(axis=0, subset='ObservationValue')
                        obs_df.sort_values(by='DateEntered', inplace=True)
                        for key in Obs_Of_Interest:
                            #print(key)
                            lenObs = len(obs_df.loc[obs_df.ObservationDesc==Obs_Of_Interest[key]])
                            #print(lenObs)
                            if (lenObs > 0):
                                tmpValue = obs_df.loc[obs_df.ObservationDesc==Obs_Of_Interest[key]].iloc[0].ObservationValue
                                tmpDate= obs_df.loc[obs_df.ObservationDesc==Obs_Of_Interest[key]].iloc[0].DateEntered	
                                #print(tmpValue, tmpDate)
                                GenMed_Encounters_withObsAll.loc[GenMed_Encounters_withObsAll.VisitGUID==visitGUID, key] = tmpValue
                                GenMed_Encounters_withObsAll.loc[GenMed_Encounters_withObsAll.VisitGUID==visitGUID, key+'Dtm'] = tmpDate
                                
                    retryFlag = False 
                                
                except Exception as e:
                    print("Exception")
                    print(e)
                    retry_count+=1 
                    time.sleep(5) 


def getObs_Of_Interest():
    """dictionary linking column names with observation names

    Returns:
        dictionary: dictionary linking column names with observation names
    """
    return {'FirstBloodGlucose':'Blood Glucose', 
                    'FirstBPDiastolic':'BP Diastolic (mm Hg)',
                    'FirstBPSystolic':'BP Systolic (mm Hg)', 
                    'FirstGCSScoreAdult':'GCS Score (Adult)',
                    'FirstLevelofConsciousness':'Level of Consciousness Score', 
                    'FirstO2Flow':'O2 Flow (L/min)',
                    'FirstPulseRateBPM':'Pulse Rate (beats/min)', 
                    'FirstRespiration':'Respiration (breaths/min)', 
                    'FirstSpO2':'SpO2 (%)',
                    'FirstTemperatureDegreesC':'Temperature (degrees C)',
                    'FirstWeightKg':'Weight (kg)',
                    'FirstUrinalysisBlood':'Urinalysis: Blood',
                    'FirstUrinalysisLeukocytes':'Urinalysis: Leukocytes',
                    'FirstPainAssessment':'Pain Assessment',
            }




def replaceNonNUmerical(df):
    """dictionary for swapping non-numeric test reults to numerical values 

    Args:
        df (dataframe): GenMed dataframe with observations and results. 

    Returns:
        _type_: _description_
    """
    replace_nonIntegerValues = {
        'FirstEstimatedGlomerularFiltrationRate': {'&gt;90':'91', '>90':91},
        'FirstCreatinine':{'&lt;5':3,"<5":3},
        'FirstTotalBilirubin': {'&lt;3':2, '<3':2},
        'FirstAlanineAminotransferase': {'&lt;5':2.5, "<5":2.5},        
        'FirstGammaGlutamylTransferase': {'&lt;3':1, "<3":1},
        
        'FirstPlateletCount':{'&lt;1':0,'<1':0} , # , 'Clumped': None, 'Clotted': None}  ,
        'FirstDDimer':{'&lt;0.20':0, '&gt;80':85, '&gt;80.00':85, '&gt;80.0':85, "<0.20":0.0,  ">80.00":85, 'Clotted':None},
        'FirstCreactiveprotein':{'&lt;0.3':0.2, '<0.3':0.2},
        'FirstTroponinT':{'&lt;3':3, '&gt;3':3, '<3':3, '&lt;30':3},
        'FirstNTproBNP':{'&gt;35000': 36000, '&lt;50':25, '>35000':36000, '&gt; 35000':36000, '>34999':36000, "<50":25 },
        'FirstBilirubinVenous': {'<2':2},
        'FirstChlorideDirectVenous':{'<65':60},
        'FirstGlucoseVenous': {'>41.6':42, '<1.1':1},
        'FirstpO2Venous':{'<10':9},
        'FirstAnionGapArterial':{'<1':0},
        'FirstBilirubinArterial':{'<2':1},
        'FirstGlucoseArterial':{'>41.6':42},
        'FirstUrinalysisBlood':{r'(?i).*large.*':4,'l;arge':4, r'(?i).*lge.*':4, r'(?i).*moderate.*':3, r'(?i).*small.*':2,  r'(?i).*sml.*':2,  r'(?i).*trace.*':1, r'(?i).*negative.*':0, r'(?i).*\+\+\+\+.*':4, 'ERY- \+4 ':4,  r'(?i).*intact.*':1, r'(?i).*none.*':0 
            ,'4+':4, '2+':2, 'Ca 80 Ery/uL':None, 'ERY 3+, #Hb 2+':2 , '\+\+\+':3, 'blood':1, 'Nil ':0,'5-10':4,'1+':1, '3+':3, '\+3':3, 'Hb +':1, '\+':1},  #'\+':1,},
        'FirstUrinalysisLeukocytes':{r'(?i).*large*':4,r'(?i).*\+\+\+.*':4, r'(?i).*moderate*':3, r'(?i).*small*':2, r'(?i).*\+\+.*':3, r'(?i).*\+.*':2,  r'(?i).*trace.*':1, r'(?i).*negative.*':0, "nursing home stated leucocytes":None, "NAD":None, "mod":2, "15":1 ,
                                     'Mod':3, 'Mocerate':3, 'urine MCS sent ':None, 'Positive':1},
            }
    GenMed_Entries_ObsRes_corr = df.copy()

    for key in replace_nonIntegerValues:    
        print(key) #,replace_nonIntegerValues[key])
        # if all entries are None get error 
        if len(GenMed_Entries_ObsRes_corr[GenMed_Entries_ObsRes_corr[key].notnull()].index)>0:
            GenMed_Entries_ObsRes_corr[key] = GenMed_Entries_ObsRes_corr[key].replace(replace_nonIntegerValues[key], regex=True)
            # GenMed_Entries_ObsRes_corr[key] = pd.to_numeric(GenMed_Entries_ObsRes_corr[key],errors='coerce')
            #print( GenMed_Entries_ObsRes_corr[key].unique())

    return GenMed_Entries_ObsRes_corr

def plotSettings():
    return {
        #  ( bins, xmin, xmax, log/linear)
        'AGEONADMISSION':(50,20,110,'linear','Age (y)', False, 0,0),
        
        
        'FirstBloodGlucose':(50,0,100,'log','Blood Glucose [mmol/L]', False,0, 0),
        'FirstTemperatureDegreesC':(50,30,45,'log', r"Temperature [$^\circ$C]", True,35.5,38.1),
        'FirstWeightKg':(50,50,150,'log','Weight [kg]', False, 0,0),
        
        'FirstPainAssessment': (11,-0.5,10.5,'log','Pain Assessment', False, 0,0),
        'FirstBPSystolic': (50,50,250,'log', 'BP Systolic [mm Hg]',True, 100,170 ),
        'FirstBPDiastolic': (50,0,200,'log', 'BP Diastolic [mm Hg]', False,0,0),
        'FirstEstimatedGlomerularFiltrationRate': (50,0,100,'log',r"Estimated Glomerular Filtration Rate [mL/min/1.73m$^{2}$]", True, 60, 100),
        'FirstCreatinine': (50,0,800,'log',r"Creatinine - Serum [$\mu$mol/L]", True, 45, 110),
        'FirstAlbumin': (60,0,60,'log','Albumin  Level [g/L]', True, 30, 48),
        'FirstTotalBilirubin': (60,0,100,'log',r"Total Bilirubin Level  [$\mu$mol/L]", True, 2, 24 ),
        'FirstAlkalinePhosphatase': (60,0,800,'log','Alkaline Phosphatase Level [U/L]',True, 30,110),
        'FirstAlanineAminotransferase': (60,0,700,'log','Alanine Aminotransferase Level [U/L]', True,0,55),
        'FirstAspartateAminotransferase': (60,0,700,'log','Aspartate Aminotransferase Level [U/L]', True, 0,45),
        'FirstGammaGlutamylTransferase': (60,0,700,'log','Gamma Glutamyl Transferase Level [U/L]', True, 0, 60),
        'FirstLactateDehydrogenase': (60,0,1200,'log','Lactate Dehydrogenase [U/L]', True, 120, 250),
        'FirstHaemoglobin': (50,10, 220,'log','Haemoglobin [g/L]', True, 115, 175),
        'FirstWhiteCellCount': (50,0, 50,'log',r"White Cell Count [$\times 10^{9}$/L]",True, 4,11),
        'FirstPlateletCount': (50,0, 1000,'log',r"Platelet Count [$\times 10^{9}$/L]",True,150,500),
        'FirstNeutrophils': (50,0, 50,'log',r"Absolute Neutrophil  Count [$\times 10^{9}$/L]",True,1.80,7.50),
        'FirstDDimer': (40,0, 20,'log',r"D-Dimer [mg/L]",True,0,0.79),
        'FirstCreactiveprotein': (50,0, 600,'log',r"C-Reactive Protein [mg/L]",True, 0,8),
        'FirstTroponinT': (50,0, 600,'log',r"Troponin T Level [mg/L]",True,0,16),
        'FirstNTproBNP': (50,0, 40000,'log',r"NT-pro Brain Natriuretic Peptide [mg/L]",True,0,124),
        
        'FirstAnionGapVenous': (50,0, 50,'log',r"Anion Gap Venous [mmol/L]", True, 7, 17),
        'FirstAnionGapArterial': (50,0, 50,'log',r"Anion Gap Arterial [mmol/L]",  True, 7, 17),
        'FirstBaseExcessVenous': (50,-30, 30,'log',r"Base Excess Venous [mmol/L]", True, -3, 3),
        'FirstBaseExcessArterial': (50,-30, 30,'log',r"Base Excess Arterial [mmol/L]", True, -3, 3),
        'FirstBilirubinVenous': (60,0, 60,'log',r"Bilirubin Venous [$\mu$mol/L]", True, 2,24),
        'FirstBilirubinArterial': (60,0, 60,'log',r"Bilirubin Arterial [$\mu$mol/L]", True, 2,24),
        'FirstCarboxyhaemoglobinVenous': (50,0, 20,'log',r"Carboxyhaemoglobin Venous [%]", True, 0.3, 1.8),
        'FirstCarboxyhaemoglobinArterial': (50,0, 20,'log',r"Carboxyhaemoglobin Arterial [%]", True, 0.3, 1.8),
        'FirstChlorideDirectVenous': (50,50, 150,'log',r"Chloride Direct Venous [mmol/L]",False, 100,109),
        'FirstChlorideDirectArterial': (50,50, 150,'log',r"Chloride Direct Arterial [mmol/L]", True, 100,109),
        'FirstCreatinineVenous':(50,0,500,'log',r"Creatinine Venous [$\mu$mol/L]", True, 50, 120),
        'FirstCreatinineArterial':(50,0,500,'log',r"Creatinine Arterial [$\mu$mol/L]", True, 50,120),
        'FirstGlucoseVenous':(50,0,30,'log',r"Glucose  Venous [mmol/L]", False,0,0),
        'FirstGlucoseArterial':(50,0,30,'log',r"Glucose  Arterial [mmol/L]", True,2.6,5.6),
        'FirstIonised Calcium Venous':(50,0,2,'log',r"Ionised Calcium Venous [mmol/L]", True, 1.1, 1.3),
        'FirstIonised Calcium Arterial':(50,0,2,'log',r"Ionised Calcium Arterial [mmol/L]", True, 1.1, 1.3),
        'FirstLactateVenous':(50,0,30,'log',r"Lactate Venous [mmol/L]", True, 0.2, 2.0),
        'FirstLactateArterial':(50,0,30,'log',r"Lactate Arterial [mmol/L]", True, 0.2, 2.0),
        'FirstMethaemoglobinVenous': (20,0, 3,'log',r"Methaemoglobin Venous [%]", True, 0.4, 1.2),
        'FirstMethaemoglobinArterial': (20,0, 3,'log',r"Methaemoglobin Arterial [%]", True, 0.2,0.6),
        'FirstOxygenSaturationVenous': (50,0, 100,'log',r"Oxygen Saturation Venous [%]", False, 0,0),
        'FirstOxygenSaturationArterial': (50,0, 100,'log',r"Oxygen Saturation Arterial [%]", True,95, 99),
        'FirstOxyhaemoglobinVenous': (50,0, 100,'log',r"Oxyhaemoglobin Venous [%]", False, 0,0),
        'FirstOxyhaemoglobinArterial': (50,0, 100,'log',r"Oxyhaemoglobin Arterial [%]", False, 0,0),
        'FirstReducedHaemoglobinVenous': (50,0, 100,'log',r"Reduced Haemoglobin Venous [%]", False, 0,0),
        'FirstReducedHaemoglobinArterial': (50,0, 100,'log',r"Reduced Haemoglobin Arterial [%]", False, 0,0),
        'FirstTotalHaemoglobinVenous': (50,10, 220,'log','Total Haemoglobin Venous [g/L]', True, 115,180),
        'FirstTotalHaemoglobinArterial': (50,10, 220,'log','Total Haemoglobin Arterial [g/L]', True, 115,180), 
        'FirstpCO2Venous': (50,0,150,'log', 'pCO2 Venous [mm Hg]', True,41,51),
        'FirstpCO2Arterial': (50,0,150,'log', 'pCO2 Arterial [mm Hg]', True, 35, 45 ),
        'FirstpO2Venous': (50,0,200,'log', 'pO2 Venous [mm Hg]', True, 25,40),
        'FirstpO2Arterial': (50,0,200,'log', 'pO2 Arterial [mm Hg]', True,67, 108),
        'FirstpHVenous': (50,6.8,7.8,'log', 'pH Venous', True, 7.32,7.42),
        'FirstpHArterial': (50,6.8,7.8,'log', 'pH Arterial', True, 7.36, 7.44),
        'FirstPotassiumDirectVenous':(50,0,10,'log',r"Potassium Direct Venous [mmol/L]", False, 0,0),
        'FirstPotassiumDirectArterial':(50,0,10,'log',r"Potassium Direct Arterial [mmol/L]", True, 3.1, 4.2),
        'FirstSodiumDirectVenous':(50,100,180,'log',r"Sodium Direct Venous [mmol/L]", False, 0,0),
        'FirstSodiumDirectArterial':(50,100,180,'log',r"Sodium Direct Arterial [mmol/L]", True, 137, 145),}


def sql_visit_query():
    return   ''' 
SELECT distinct 
v.ClientGUID, 
v.ChartGUID, 
v.GUID VisitGUID
, JM.JOURNEY_ID
, JM.IRSD_SCORE
,JM.IRSD_DECILE
,DATEDIFF(YEAR, DATE_FROM_PARTS(C.BIRTHYEARNUM,BIRTHMONTHNUM,BIRTHDAYNUM), V.ADMITDTM) AGEONADMISSION
,C.GenderCode
,C.RACECODE AS "IndiginousStatus"
, CLP.LEVELCODE 
, LEFT(v.CurrentLocation, 3) AS HosiptalProxy
, dense_rank() over(partition by v.clientguid order by v.admitdtm) -  dense_rank() over(partition by v.clientguid, v.chartguid order by v.admitdtm) + 1 chartRank
, dense_rank() over(partition by v.clientguid, v.chartguid order by v.admitdtm) visitRank
, v.Active
, v.VisitStatus
, v.InternalVisitStatus
, v.TypeCode
, v.CareLevelCode
, VADD.DiagnosisCode AS PrimaryDiagnosisCode
, DC."diagnosis_code_desc"
, VAPD.ProcedureCode AS PrimaryProcedureCode
, DRG."PropertyValue" AS "DRG"
, DRGCODE."DRGDescription" AS "DRGDescription"
, MDC."PropertyValue" AS "MDC"
, vse.TRIAGE_CATEGORY 
, EDDC.CODE AS EDDiagnosisCode 
, EDDC.DESCRIPTION AS EDDiagnosisCodeDescription
--, OBLP.VALUE AS ED_VISIT_REASON
, v.CurrentLocation
, v.AdmitDtm, v.DischargeDtm 
, datediff(DAY, v.AdmitDtm, v.DischargeDtm  ) LOSNIGHTS
, datediff(HOUR, v.AdmitDtm, v.DischargeDtm  ) LOSHOUR
, v.DischargeDisposition
, v.DischargeLocation
, cvh.tovalue CurrentService
, cvh.fromvalue OldService
, cvh.CREATEDWHEN AS CurrentServiceDtm
, CV3Service.GROUPCODE
, CV3Service.Description AS ServiceDescription
, SXAAMAdmitSource.Code AS AdmitSource
, SXAAMAdmitType.Code AS AdmitType
, EnterpriseVisitCol36 AS EpisodeOfCare          
, EnterpriseVisitCol35 AS SourceOfReferral            
, EnterpriseVisitCol30 AS "Transfer Service"        
, EnterpriseVisitCol26 AS SAH_Diagnosis               
, EnterpriseVisitCol25 AS SAH_Visit_Type
, EnterpriseVisitCol24 AS SAH_Admit_Service       
, EnterpriseVisitCol20 AS "WL Patient Category - Intent"
, EnterpriseVisitCol19 AS "WL Election"
, cud1.value AS CUD_EPISODE_OFCARE 
, cud2.value AS CUD_PATIENT_CATEGORY 
, cud3.value AS CUD_ADMISSION_CATEGORY 
, cud4.value AS CUD_ADMISSION_ELECTION 
FROM PRD_DAP_EMR_DB.dbo.CV3ClientVisit v
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENT  AS C ON C.GUID  = V.CLIENTGUID
LEFT JOIN PRD_DAP_EMR_DB.dbo.SXAAMVisitRegistration ON v.GUID = SXAAMVisitRegistration.ClientVisitGUID
LEFT JOIN PRD_DAP_EMR_DB.dbo.SXAAMAdmitSource ON SXAAMVisitRegistration.AdmitSourceID = SXAAMAdmitSource.AdmitSourceID
LEFT JOIN PRD_DAP_EMR_DB.dbo.SXAAMAdmitType ON SXAAMVisitRegistration.AdmitTypeID = SXAAMAdmitType.AdmitTypeID
LEFT JOIN PRD_DAP_EMR_DB.dbo.SXAAMDischargeCondition ON SXAAMVisitRegistration.DischargeConditionID = SXAAMDischargeCondition.DischargeConditionID
LEFT JOIN PRD_DAP_EMR_DB.dbo.CV3ENTERPRISEVISITDATA  EVD ON EVD.VISITGUID = v.GUID
LEFT JOIN PRD_DAP_EMR_DB.dbo.CV3Service on CV3Service.GUID = v.ServiceGUID
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CL ON V.CURRENTLOCATIONGUID = CL.GUID 
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CLP ON CLP.GUID  = CL.FACILITYGUID 
LEFT JOIN  PRD_DAP_EMR_DB.DBO.SXAAMCLIENTVISITHISTORY AS cvh ON v.guid = cvh.clientvisitguid AND cvh.FIELDTYPE = 4 -- and FROMVALUE != '' and FROMVALUE != TOVALUE
LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMABSTRACTVISITDETAIL  AS VA ON v.GUID = VA.clientvisitguid 
LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMABSTRACTDIAGNOSISDETAIL AS VADD ON va.ABSTRACTVISITDETAILID = VADD.ABSTRACTVISITDETAILID AND VADD.SequenceNumber = 1 
LEFT JOIN DEV_DAP_CAE05_DB.RAW."DIM_Diagnosis_Codes" AS DC ON VADD.ABSTRACTVISITDETAILID AND VADD.SequenceNumber = 1  AND VADD.DiagnosisCode = DC."diagnosis_code"
LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMABSTRACTPROCEDUREDETAIL AS VAPD ON va.ABSTRACTVISITDETAILID = VAPD.ABSTRACTVISITDETAILID AND VAPD.SequenceNumber = 1 
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENTUSERDATA  AS CUD1  ON CUD1.OBJGUID = V.GUID AND CUD1.USERDATACODE = 'VS Episode of Care' 
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENTUSERDATA  AS CUD2  ON CUD2.OBJGUID = V.GUID AND CUD2.USERDATACODE = 'VS Patient Category' 
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENTUSERDATA  AS CUD3  ON CUD3.OBJGUID = V.GUID AND CUD3.USERDATACODE ='VS Admission Category'
LEFT JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENTUSERDATA  AS CUD4  ON CUD4.OBJGUID = V.GUID AND CUD4.USERDATACODE ='VS Admission Election'
LEFT JOIN DEV_DAP_CAE05_DB.RAW."SXARCMAbstractCustomTileData"  AS DRG ON DRG."AbstractVisitDetailID" = VA.ABSTRACTVISITDETAILID and drg."PropertyName" = '3M DRG'
LEFT JOIN DEV_DAP_CAE05_DB.RAW."SXARCMAbstractCustomTileData"  AS MDC ON MDC."AbstractVisitDetailID" = VA.ABSTRACTVISITDETAILID and MDC."PropertyName" = '3M MDC'
LEFT JOIN DEV_DAP_CAE05_DB.RAW.SAH_DRG AS DRGCODE ON DRGCODE."DRGCode"  = DRG."PropertyValue"
LEFT JOIN DEV_DAP_CAE05_DB.RAW.VW_VISIT_SUPPLEMENTAL_EMERGENCY AS VSE ON VSE.VISITGUID = v.GUID  
LEFT JOIN DEV_DAP_CAE05_DB.RAW.VW_EMERGENCY_VISITS_DIAGNOSIS_CODE AS EDDC ON EDDC.VISITGUID = v.GUID
LEFT JOIN DEV_DAP_CAE05_DB.RAW.PATIENT_JOURNEY_MAPPING AS JM  ON JM.VISITGUID = V.GUID 
--LEFT JOIN (PRD_DAP_EMR_DB.DBO.CV3CLIENTDOCUMENT  AS  CD 
--	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSERVATIONDOCUMENT AS OBDP ON CD.GUID = OBDP.OWNERGUID  AND CD.PATCAREDOCGUID   = 137102020 -- AND OBDP.SORTSEQNUM = 1 -- AND OBDP.Active = 1
--	INNER JOIN PRD_DAP_EMR_DB.DBO.SCMOBSFSLISTVALUES AS OBLP ON (CD.CLIENTGUID = OBLP.CLIENTGUID AND OBDP.OBSERVATIONDOCUMENTGUID = OBLP.PARENTGUID  AND OBLP.ACTIVE =1 AND OBLP.SORTSEQNUM = 1)
--	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSCATALOGMASTERITEM AS OCMIP ON (OBDP.OBSMASTERITEMGUID=OCMIP.GUID  AND OCMIP.GUID IN  (3142202890) AND ocmip.NAME= 'ED_ChiefComplaint_' ) -- (17075102890))-- (2759802890) )
--	) ON (V.CLIENTGUID  = CD.CLIENTGUID  AND V.GUID  = CD.CLIENTVISITGUID  )
WHERE
V.VISITSTATUS  = 'DSC'   -- NOT IN ('CAN', 'PRE')
AND V.ADMITDTM BETWEEN '{0}' AND '{1}' --    '2023-02-01'
-- AND (V.DISCHARGEDTM > '2023-01-01' OR V.DISCHARGEDTM IS NULL)
AND  v.TypeCode  not in ('zResult', 'zClerical', 'ZPathology', 'Outpatient', 'zBilling Only') --, 'Emergency') -- = 'Waiting List-IP' --
AND LEFT(v.CurrentLocation, 3)   IN ('LMH', 'MPH', 'RAH', 'QEH', 'FMC', 'NHS')
order by v.clientguid,v.AdmitDtm 
    '''
    
    
def queryDiagnosis():
    return ''' 
SELECT DISTINCT 
   	AbsVisitDetail.ClientVisitGUID AS "VisitGUID"
 	, LISTAGG( AbsDiagDetail.DiagnosisCode,' ') WITHIN GROUP (ORDER BY AbsDiagDetail.SequenceNumber) AS AllDiagnosis
 	--, LISTAGG( AbsDiagDetailHA.DiagnosisCode,',') WITHIN GROUP (ORDER BY AbsDiagDetailHA.SequenceNumber) AS AllDiagnosisHospitalAcquired
FROM PRD_DAP_EMR_DB.DBO.SXARCMAbstractVisitDetail AbsVisitDetail 
LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMAbstractDiagnosisDetail AbsDiagDetail  ON AbsDiagDetail.AbstractVisitDetailID = AbsVisitDetail.AbstractVisitDetailID AND AbsDiagDetail.POACODEDICTIONARYID=2 
--LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMAbstractDiagnosisDetail AbsDiagDetailHA  ON AbsDiagDetailHA.AbstractVisitDetailID = AbsVisitDetail.AbstractVisitDetailID AND AbsDiagDetailHA.POACODEDICTIONARYID=1 
INNER JOIN PRD_DAP_EMR_DB.dbo.CV3ClientVisit v ON V.GUID = AbsVisitDetail.ClientVisitGUID
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CL ON V.CURRENTLOCATIONGUID = CL.GUID 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CLP ON CLP.GUID  = CL.FACILITYGUID 
WHERE 
V.VISITSTATUS  = 'DSC'   -- NOT IN ('CAN', 'PRE')
AND V.ADMITDTM BETWEEN '{0}' AND '{1}' --    '2023-02-01'
-- AND (V.DISCHARGEDTM > '2023-01-01' OR V.DISCHARGEDTM IS NULL)
AND  v.TypeCode  not in ('zResult', 'zClerical', 'ZPathology', 'Outpatient', 'zBilling Only') --, 'Emergency') -- = 'Waiting List-IP' --
AND LEFT(v.CurrentLocation, 3)   IN ('LMH', 'MPH', 'RAH', 'QEH', 'FMC', 'NHS') -- '{0}'
GROUP BY AbsVisitDetail.ClientVisitGUID
'''

def queryDiagnosisHA():
    return ''' 
SELECT DISTINCT 
   	AbsVisitDetail.ClientVisitGUID AS "VisitGUID"
 	, LISTAGG( AbsDiagDetail.DiagnosisCode,' ') WITHIN GROUP (ORDER BY AbsDiagDetail.SequenceNumber) AS AllDiagnosis
 	--, LISTAGG( AbsDiagDetailHA.DiagnosisCode,',') WITHIN GROUP (ORDER BY AbsDiagDetailHA.SequenceNumber) AS AllDiagnosisHospitalAcquired
FROM PRD_DAP_EMR_DB.DBO.SXARCMAbstractVisitDetail AbsVisitDetail 
LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMAbstractDiagnosisDetail AbsDiagDetail  ON AbsDiagDetail.AbstractVisitDetailID = AbsVisitDetail.AbstractVisitDetailID AND AbsDiagDetail.POACODEDICTIONARYID=1 
--LEFT JOIN PRD_DAP_EMR_DB.DBO.SXARCMAbstractDiagnosisDetail AbsDiagDetailHA  ON AbsDiagDetailHA.AbstractVisitDetailID = AbsVisitDetail.AbstractVisitDetailID AND AbsDiagDetailHA.POACODEDICTIONARYID=1 
INNER JOIN PRD_DAP_EMR_DB.dbo.CV3ClientVisit v ON V.GUID = AbsVisitDetail.ClientVisitGUID
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CL ON V.CURRENTLOCATIONGUID = CL.GUID 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CLP ON CLP.GUID  = CL.FACILITYGUID 
WHERE 
V.VISITSTATUS  = 'DSC'   -- NOT IN ('CAN', 'PRE')
AND V.ADMITDTM BETWEEN '{0}' AND '{1}' --    '2023-02-01'
-- AND (V.DISCHARGEDTM > '2023-01-01' OR V.DISCHARGEDTM IS NULL)
AND  v.TypeCode  not in ('zResult', 'zClerical', 'ZPathology', 'Outpatient', 'zBilling Only') --, 'Emergency') -- = 'Waiting List-IP' --
AND LEFT(v.CurrentLocation, 3)   IN ('LMH', 'MPH', 'RAH', 'QEH', 'FMC', 'NHS') -- '{0}'
GROUP BY AbsVisitDetail.ClientVisitGUID
'''


def queryEDVisitReasons():
    return ''' 
SELECT DISTINCT 
V.GUID AS "VISITGUID",
LISTAGG( OBLP.VALUE,' -- ') WITHIN GROUP (ORDER BY OBLP.CREATEDWHEN ) AS ED_VISIT_REASON
FROM PRD_DAP_EMR_DB.DBO.CV3CLIENTDOCUMENT  AS  CD 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSERVATIONDOCUMENT AS OBDP ON CD.GUID = OBDP.OWNERGUID  AND CD.PATCAREDOCGUID   = 137102020 -- AND OBDP.SORTSEQNUM = 1 -- AND OBDP.Active = 1
INNER JOIN PRD_DAP_EMR_DB.DBO.SCMOBSFSLISTVALUES AS OBLP ON (CD.CLIENTGUID = OBLP.CLIENTGUID AND OBDP.OBSERVATIONDOCUMENTGUID = OBLP.PARENTGUID  AND OBLP.ACTIVE =1 AND OBLP.SORTSEQNUM = 1)
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSCATALOGMASTERITEM AS OCMIP ON (OBDP.OBSMASTERITEMGUID=OCMIP.GUID  AND OCMIP.GUID IN  (3142202890) AND ocmip.NAME= 'ED_ChiefComplaint_' ) -- (17075102890))-- (2759802890) )
INNER JOIN PRD_DAP_EMR_DB.dbo.CV3ClientVisit v ON V.CLIENTGUID  = CD.CLIENTGUID  AND V.GUID  = CD.CLIENTVISITGUID 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CL ON V.CURRENTLOCATIONGUID = CL.GUID 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3LOCATION  AS CLP ON CLP.GUID  = CL.FACILITYGUID 
WHERE 
V.VISITSTATUS  = 'DSC'   -- NOT IN ('CAN', 'PRE')
AND V.ADMITDTM BETWEEN '{0}' AND '{1}' --    '2023-02-01'
AND  v.TypeCode = 'Emergency' --   not in ('zResult', 'zClerical', 'ZPathology', 'Outpatient', 'zBilling Only') --, 'Emergency') -- = 'Waiting List-IP' --
AND LEFT(v.CurrentLocation, 3)   IN ('LMH', 'MPH', 'RAH', 'QEH', 'FMC', 'NHS') -- '{0}'
GROUP BY v.GUID
    '''
    
def queryObservations():
    return ''' 
SELECT 
		O.GUID                                       as "ObservationGUID"
        , CV.VisitIDCode
        , CD.ClientVisitGUID
        , CD.ClientGUID
        , O.ObsItemGUID
        , CMI.ModifyFormFilter                         as ObservationDesc
        , min(CD.Entered)                              as DateEntered
        , coalesce(SOLV.Value, left(O.ValueText, 255)) as ObservationValue
        , SOLV.SortSeqNum
--        , SOLV.VALUE 
--        , O.VALUETEXT 
        , O.UnitOfMeasure
FROM PRD_DAP_EMR_DB.DBO.CV3CLIENTDOCUMENT AS CD 
	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3CLIENTVISIT AS CV ON cv.guid = cd.CLIENTVISITGUID 
		AND cv.CLIENTGUID = cd.CLIENTGUID 
		AND cv.CHARTGUID  = cd.CHARTGUID 
	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSERVATIONENTRYITEM AS OEI ON OEI.OWNERGUID  = CD.KTREEROOTGUID 
		AND OEI.ITEMTYPE IN (5,6) -- 5 = [Observation Item],6 = [Observation Set],7 = [Observation Modifier],
		AND OEI.ISMASTERITEM =1 -- A flag that indicates if an item of type Observation Item is a master item. 1 = True; 0 = FALSE
	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSERVATIONDOCUMENT AS OD ON OD.OWNERGUID = CD.GUID 
		AND OD.PARAMETERGUID = OEI.GUID
		AND OD.ARCTYPE = CD.ARCTYPE  -- A foreign key to the ArcType column in the CV3ClientDocumentARC table.
	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSERVATION AS O ON O.GUID = OD.OBSERVATIONGUID 
	INNER JOIN PRD_DAP_EMR_DB.DBO.CV3OBSCATALOGMASTERITEM AS CMI ON CMI.GUID  = OEI.OBSMASTERITEMGUID 
		AND OD.OBSMASTERITEMGUID = CMI.GUID
	LEFT OUTER JOIN PRD_DAP_EMR_DB.DBO.SCMOBSFSLISTVALUES AS SOLV 
		--INNER JOIN PRD_DAP_EMR_DB.DBO.cv3obs
		ON SOLV.PARENTGUID = OD.OBSERVATIONDOCUMENTGUID 
		AND SOLV.CLIENTGUID = CD.CLIENTGUID
WHERE -- cv.guid IN (2733386400270, 2758894600270, 2238906100270)
cv.guid in  {0}
	AND O.ObsItemGUID IN (
			102900, -- BP Diastolic (mm Hg)
			202900, -- BP Systolic (mm Hg)
			303402900, 
			303602900, 
			303502900, 
			57902900, 
			1102900, -- O2 Flow (L/min)
			280502900, 
			59702900, 
			802900,  -- Pulse Rate device (not measurement)
			168402900, -- Pule Rate radial  (not measurement)
			302900,  -- Pulse Rate (beats/min)
			502900,  -- Respiration (breaths/min)
			5102900, -- Level of Consciousness Score
			7202900, -- Sedation Score
			702900,  -- SpO2 (%)
			285802900, 
			168302900, -- Temperature meaurement method
			12102900,  -- Temperature (degrees C)
			258102900, 
			1977602900, -- Weight (kg)
           297802900, -- Blood Glucose
           321502900, -- Urinalysis: Blood
           321002900, -- Urinalysis: Leukocytes
           2454802900, -- Pain Assessment
		   59802900 -- Pain Score
						)
GROUP BY SOLV.VALUE 
        , O.VALUETEXT 
        , O.GUID
        , CV.VisitIDCode
        , CD.ClientVisitGUID
        , CD.ClientGUID
        , O.ObsItemGUID
        , CMI.ModifyFormFilter
        , SOLV.SortSeqNum
        , O.UnitOfMeasure
'''


def queryResults():
    return'''
SELECT 
       --R.result_touchedby, 
       --R.result_touchedwhen, 
       --R.result_createdby, 
       R.CREATEDWHEN  AS  "result_createdwhen",
       R.ACTIVE  AS "result_active", 
       R.GUID AS  "result_observationguid", 
       R.ENTERED as "result_entered", 
       R.STATUS as "result_status",   -- The chart item status. F = Final; I = Pending; P = Prelim; R = NotVerified; S = Partial; C = Corrected; D = Delete
--     R.enterrole, 
--     R.userguid, 
       v.guid AS  CLIENTVISITGUID, 
       R.clientguid,
       R.chartguid, 
       R.itemname, 
       R.value, 
       R.unitofmeasure, 
       R.referencelowerlimit,
       R.referenceupperlimit, 
       R.abnormalitycode, 
       r.HL7ABNORMALITYCODE ,
--     --R.restrictedaccess, 
       R.authorizeddtm, 
       R.clusterid,
       R.typecode,
       R.ishistory, 
       R.istextual,
--     R.hashistory, 
       R.orderguid, 
       R.resultitemguid, 
       R.masterguid, 
       R.arrivaldtm, 
       R.hasmedialink, 
--     --R.isreleasedtopatient, 
       R.observationdtm, 
       R.analysisdtm, 
       R.resultitemcode, 
       R.resultitemcodingstandard, 
       R.obsdatatype,
       r.ObservationDtm, 
       O.requesteddtm AS order_Requesteddtm,
       O.performeddtm AS order_performeddtm,
       O.TYPECODE AS order_typecode,
       o.NAME AS oreder_name,
       o.ORDERSETNAME 
FROM PRD_DAP_EMR_DB.DBO.CV3BASICOBSERVATION AS R 
INNER JOIN PRD_DAP_EMR_DB.DBO.CV3ORDER AS O ON O.GUID = r.ORDERGUID 
INNER JOIN PRD_DAP_EMR_DB.dbo.CV3ClientVisit v ON R.CLIENTVISITGUID = v.guid 
WHERE v.guid IN {0} 
and    o.typecode = 'Diagnostic'
'''


