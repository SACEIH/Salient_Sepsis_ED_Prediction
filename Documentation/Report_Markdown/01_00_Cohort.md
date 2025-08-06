\newpage
# Cohort 

The data for this study was sourced from the South Australian Electronic Medical
Record system (EMR). The data set is composed of Emergency Department (ED)
presentations by an adult (age of at least 16 years) followed by an inpatient (IP) admission with sepsis diagnosis
identified by the ICD-10 codes, Table -@tbl:tableicd-10 [^1] (based on a journey,
see appendix -@sec:Journey). 

Specifically we only include the first ED presentation in a journey. The ED
presentation must also be the first EoC in the journey. This excludes
presentations that are part of the admission process when the patient is
transferred from one hospital to another. It also excludes complex journeys such
as a patient who is admitted via day procedure in hospital (e.g. Extracorporeal
dialysis) We also require that at least three of the following vital signs are
recorded in the EMR during the presentation: respiration, O~2~ Saturation,
systolic blood pressure, pulse rate and temperature[^2] (Table -@tbl:table1).  

The IP admission is required to be the first episode of care (EoC) after any ED
presentations [^3]. IP admissions where the patient does not leave the ED are
excluded (these are identified by an IP discharge date/time within 60 minutes of
the discharge date/time of the ED presentation and a location that includes the
string "ED-Admin".) 


The training data set includes all presentations to Emergency Departments at
metropolitan hospitals in the calendar year 2023 in which at least three
observations of vital signs of interest have been made (see Table -@tbl:table1).
There are 260,596 ED presentations with at least three vital signs recorded
which included 2,557 presentations that resulted in an inpatient admission which
includes at least one ICD-10 code matching a Sepsis diagnosis (of these 920 have
sepsis as the primary, or first-listed, diagnosis). Note, 52,233 (16.7%) out of
a total 312,829  ED presentations do not have at least three  observations of
vital signs recorded in the EMR and have been excluded from the analysis.

The first verification data set is created from all ED presentations at
metropolitan hospitals in the calendar year 2024  in which at least three
observations of vital signs of interest have been made. There are 263,594   ED
presentations with at least three vital signs recorded which included 2,446
presentations that resulted in an inpatient admission which includes at least
one ICD-10 code matching a Sepsis diagnosis (of these 912 have sepsis as the
primary, or first-listed, diagnosis). Note, 46,250 (14.9%) out of a total
309,844 ED presentations do not have at least three  observations of vital signs
recorded in the EMR and have been excluded from the analysis.

The fraction of Sepsis cases that are not identified, ICD-10 A41.9, i.e. where
pathology tests have not identified the infection agent, is 66.9% in the 2023
training data set and 69.4% in the 2024 verification data set (see Tables
-@tbl:table-verification_2023-icd10 & -@tbl:table-verification_2024-icd10). 

[^1]: We have removed infant Sepsis ICD-10 codes from the previous work. 

[^2]: O~2~ Flow and the sedation score are not included as these are not usually
    filled out if the patient is not receiving oxygen or is awake and aware. 

[^3]: Note to self, need to look at joining transfers. See CAP and COPD analyses. 