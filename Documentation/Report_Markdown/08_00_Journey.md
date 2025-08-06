\newpage
# Appendices

## Patient Journey  {#sec:Journey}

Descriptions and variable names listed below are based on the SA Health EMR.
Episodes of Care are joined into a journey if they meet the following criteria. If the value is set to zero, the EoC is part of the same journey. 

1.	Check if the previous CHARTGUID entry (for the same     
    CLIENTGUID order by discharge datetime) is the same as the current CHARTGUID.  
    If yes, set the value to 0.
2.	Check if the time difference between the previous discharge datetime (for the same) and 
    current admission datetime is within 6 hours (either before or after).  
    If yes, set the value to 0.
3.	Check if the time difference between the previous discharge datetime (for the same CLIENTGUID) and 
    current admission datetime is within 24 hours (either before or after) and the ‘previous_discharge_disposition’ 
    (for the same CLIENTGUID order by admission datetime) is in this list ('IP Other hosp - Down', 'IP Other hosp - Up', 
    'IP Other Hospital - DOWN','IP Other Hospital - UP').  
    If yes, set the value to 0.
4.	Check if the previous discharge datetime (for the same CLIENTGUID order by discharge
    datetime) is before the current admission datetime and the previous admission datetime
    (for the same CLIENTGUID order by admission datetime) date is after the current admission datetime.  
    If yes, set the value to 0.
5.	Check if the time difference between the previous discharge datetime (for the same
    CLIENTGUID order by admission datetime) and current admission datetime is within 24 
    hours (either before or after) and the previous episode_of_care(for the same 
    CLIENTGUID order by admission datetime) is 'Rehabilitation' and the current 
    episode_of_care is 'Hospital at Home - Rehab at Home'.  
    If yes, set the value to 0.
6.	Check if the time difference between the previous admission datetime (for the same
    CLIENTGUID order by admission datetime) and current admission datetime is within 24 
    hours (either before or after) and the previous TYPECODE (for the same CLIENTGUID 
    order by admitdate asc) is 'Emergency' and the current source_of_referral is 'IP 
    Casualty-Emergency' and the current TYPECODE is 'Inpatient'.  
    If yes, set the value to 0.

If none of the above conditions are met start a new journey.