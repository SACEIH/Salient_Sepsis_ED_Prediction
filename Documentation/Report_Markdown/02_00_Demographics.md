\newpage

# Demographics and Validation Metrics

The performance of the ML model will evaluated in comparison with current
scoring systems in terms of sensitivity/specificity and against the proposed
adult sepsis pathway. The two scoring systems used are qSOFA and the SIRS
criteria. In addition the fraction of patients who require ICU usage and patient
mortality will also be examined. 

## qSOFSA 

The quick Sequential Organ Failure Assessment (qSOFA) [@10.1001/jama.2016.0288]
is used to identify high-risk patients for in-hospital mortality with suspected
infection outside the ICU. Two or more of the following  criteria need to be met
for a positive qSOFA: 

- Glasgow Coma Scale < 15,
- Respiratory rate $\ge$ 22,
- Systolic Blood Pressure $\le$ 100 mmHg.

##  Systemic Inflammatory Response Syndrome (SIRS) 

There are multiple levels to the SIRS schema [@BONE19921644;@Evans2021] relating
to the severity of the response. The first is the basic SIRS criteria which
requires at least two of the following conditions: 

- T $<$ 36 \textdegree C or T $>$ 38 \textdegree C,
- Heart rate $>$ 90,
- Respiratory rate $>$ 20,
- White Blood Count $>$ 12

The second level is the Sepsis Criteria (SIRS + Source of Infection) which has
not yet been implemented in this study as it requires searching the free text
progress notes. 

The third level is Severe Sepsis Criteria (Organ Dysfunction, Hypotension, or
Hypoperfusion) which requires at least one of the following to be satisfied (we
have excluded the drop in blood pressure as the patients being reviewed have
just presented to the ED and usually only have one set of vital signs): 

- Lactate Blood Gas $>$ 4,
- Systolic Blood Pressure $\le$ 90.


## Adult Sepsis Pathway 

There are two pathways for flagging a patient as being at risk of Sepsis and
requiring either review by a Senior Medical Officer or a Medical Emergency
response. The Purple pathway is triggered if any of the patient’s observations
in the Rapid Detection and Response (RDR) are in the purple zone (Table
-@tbl:table1). The Red pathway is triggered if there are two or more red zone
observations.

## ICU Usage 

A stay in the ICU is identified by matching the patient’s location to the ICU
wards in the first episode of care (EoC) after inpatient admission. .

## Mortality 

Mortality is measured using the patients date of death and the date/time of the
presentation at the ED. The mortality is calculated for death as an inpatient
and at after admission are.

## Triage Category 

We categorise the patients based on the the triage category assigned on
presentation at the emergency department.  Patients with Sepsis, especially this
in triage category 3, 4 or 5 can have there triage classification changed if
they deteriorate while waiting to be seen. 

## Waiting Times 

In order to understand the clinical workflow the various time stamps recorded in
the ED status board will be analysed in order to measure the time waiting to be
seen ('WTB'), the decision to admit, when ready for ward transfer. 

## Sepsis Patients 

The demographics for the 2023 training sample are given in Table -@tbl:demo_2023
amd for the 2024 validation data set in Table -@tbl:demo_2024
The metrics for the 2023 training sample are given in Table -@tbl:Metrics_2023
and for the 2024 validation sample Table -@tbl:Metrics_2024. 
The outcomes for
the 2023 training sample are give in Table -@tbl:Outcomes_2023 and for the 2024
validation sample Table -@tbl:Outcomes_2024.




| Triage Category   |   EoC |   Average Age |   Indigenous |   Female |   Indeterminate |   Unknown |
|:------------------|------:|--------------:|-------------:|---------:|----------------:|----------:|
| 1                 |   239 |          74.2 |            6 |      111 |               0 |         0 |
| 2                 |  1235 |          71.9 |           41 |      552 |               0 |         0 |
| 3                 |   945 |          70.7 |           41 |      451 |               0 |         0 |
| 4                 |   133 |          66.2 |            5 |       68 |               0 |         0 |
| 5                 |     5 |          42.4 |            2 |        2 |               0 |         0 |
| Total/Mean        |  2557 |         325   |           95 |     1184 |               0 |         0 |
 
Table: Demographics of the patients diagnosed with sepsis in 2023 training sample  {#tbl:demo_2023}

| Triage Category   |   EoC |   Average Age |   Indigenous |   Female |   Indeterminate |   Unknown |
|:------------------|------:|--------------:|-------------:|---------:|----------------:|----------:|
| 1                 |   241 |          75.3 |            2 |      101 |               0 |         0 |
| 2                 |  1210 |          71.9 |           44 |      451 |               0 |         0 |
| 3                 |   838 |          70.1 |           32 |      344 |               0 |         0 |
| 4                 |   157 |          69.8 |           11 |       61 |               0 |         0 |
| Total/Mean        |  2446 |          71.5 |           89 |      957 |               0 |         0 |

Table: Demographics of the patients diagnosed with sepsis in 2024 validation sample  {#tbl:demo_2024}

| Triage Category   |   EoC |   Average Age |   >2 vital signs available |   qSOFA Flag |   SIRS Flag |   SIRS Severe |   Purple >0 Flag |   Red >1 Flag |
|:------------------|------:|--------------:|---------------------------:|-------------:|------------:|--------------:|-----------------:|--------------:|
| 1                 |   239 |          74.2 |                        239 |          142 |         132 |            45 |               80 |            34 |
| 2                 |  1235 |          71.9 |                       1235 |          458 |         711 |           163 |              246 |           162 |
| 3                 |   945 |          70.7 |                        945 |          171 |         484 |            52 |               74 |            52 |
| 4                 |   133 |          66.2 |                        133 |           12 |          57 |             1 |               10 |             6 |
| 5                 |     5 |          42.4 |                          5 |            0 |           1 |             0 |                0 |             0 |
| Total/Mean        |  2557 |          71.3 |                       2557 |          783 |        1385 |           261 |              410 |           254 |

Table:  Metrics for the for patients diagnosed with sepsis in 2023 training sample  {#tbl:Metrics_2023}


| Triage Category   |   EoC |   Average Age |   >2 vital signs available |   qSOFA Flag |   SIRS Flag |   SIRS Severe |   Purple >0 Flag |   Red >1 Flag |
|:------------------|------:|--------------:|---------------------------:|-------------:|------------:|--------------:|-----------------:|--------------:|
| 1                 |   241 |          75.3 |                        241 |          107 |         150 |            70 |              126 |            41 |
| 2                 |  1210 |          71.9 |                       1210 |          324 |         722 |           157 |              324 |           207 |
| 3                 |   838 |          70.1 |                        838 |           93 |         407 |            62 |              109 |            61 |
| 4                 |   157 |          69.8 |                        157 |           17 |          79 |            15 |               20 |             9 |
| Total/Mean        |  2446 |          71.5 |                       2446 |          541 |        1358 |           304 |              579 |           318 |

Table:Metrics for the for patients diagnosed with sepsis in 2024 validation sample  {#tbl:Metrics_2024}

| Triage Category   |   EoC |   Average Age |   ICU Stay |   Died as IP |   Died 30 days after admission |
|:------------------|------:|--------------:|-----------:|-------------:|-------------------------------:|
| 1                 |   239 |          74.2 |         89 |           81 |                            109 |
| 2                 |  1235 |          71.9 |        400 |          208 |                            292 |
| 3                 |   945 |          70.7 |        247 |          135 |                            176 |
| 4                 |   133 |          66.2 |         39 |           23 |                             26 |
| 5                 |     5 |          42.4 |          2 |            0 |                              0 |
| Total/Mean        |  2557 |          71.3 |        777 |          447 |                            603 |

Table:  Outcomes for the for patients diagnosed with sepsis in 2023 training sample  {#tbl:Outcomes_2023}

| Triage Category   |   EoC |   Average Age |   ICU Stay |   Died as IP |   Died 30 days after admission |
|:------------------|------:|--------------:|-----------:|-------------:|-------------------------------:|
| 1                 |   241 |          75.3 |         75 |           87 |                            102 |
| 2                 |  1210 |          71.9 |        344 |          206 |                            232 |
| 3                 |   838 |          70.1 |        227 |          126 |                            135 |
| 4                 |   157 |          69.8 |         39 |           15 |                             21 |
| Total/Mean        |  2446 |          71.5 |        685 |          434 |                            490 |

Table:  Outcomes for the for patients diagnosed with sepsis in 2024 validation sample  {#tbl:Outcomes_2024}

| Triage Category   |   FMC |   LMH |   MPH |   NHS |   QEH |   RAH |   Row Total |
|:------------------|------:|------:|------:|------:|------:|------:|------------:|
| 1                 |    75 |    79 |    10 |     1 |    44 |    30 |         239 |
| 2                 |   251 |   301 |    59 |    10 |   206 |   408 |        1235 |
| 3                 |   151 |   216 |   116 |    27 |   179 |   256 |         945 |
| 4                 |    21 |    32 |    14 |     5 |    29 |    32 |         133 |
| 5                 |     1 |     3 |     0 |     0 |     1 |     0 |           5 |
| Total             |   499 |   631 |   199 |    43 |   459 |   726 |        2557 |

Table:  ED presentations for patients diagnosed with sepsis in 2023 training sample  {#tbl:hospitals_2023}

| Triage Category   |   FMC |   LMH |   MPH |   NHS |   QEH |   RAH |   Row Total |
|:------------------|------:|------:|------:|------:|------:|------:|------------:|
| 1                 |    93 |    41 |    10 |     3 |    60 |    34 |         241 |
| 2                 |   263 |   283 |    78 |    20 |   225 |   341 |        1210 |
| 3                 |   122 |   205 |   123 |    29 |   159 |   200 |         838 |
| 4                 |    12 |    39 |    23 |     6 |    43 |    34 |         157 |
| Total             |   490 |   568 |   234 |    58 |   487 |   609 |        2446 |

Table:  ED presentations for patients diagnosed with sepsis in 2024 validation sample  {#tbl:hospitals_2024}




\newpage
### Discharge Disposition of Sepsis Patients 

The discharge disposition from the ED of the patients diagnosed with Sepsis are
listed in Tables -@tbl:Discharge_2023 & -@tbl:Discharge_2024. This shows the
number of patients who are admitted directly as inpatients, who are admitted to
the EECU and are transferred to another hospital, and those that died in the ED.

In addition there is a small cohort of patients who were not admitted included
as patients "admitted" with Sepsis (12 in 2023 and 16 in 2024). This is caused
by our journey definition. We have required the ED presentation to be the first
in in a set of connected EoC.  In this case the patient has represented at an ED
within 6 hours of discharge and been admitted with Sepsis. We have used this
journey definition so as not to double count patients who are transferred
between hospitals.

If we examine timelines of the patient journeys for patients who were not
admitted from the ED (Fig. -@fig:non_admitted_timelines_2023) we we find four of
the 12 patients were admitted (three of which were hospital transfers). A
similar analysis of the 2024 validation sample finds at least five of the 16
patients were admitted. 


*Add patient timelines for some of these to the appendix*.


| Triage Category   |   EoC |   Average Age |   Admit as Inpatient |   Admit to EECU |   Transfer to Other Hospital |   Not admitted as inpatients |   Died in the ED |   Row Total |
|:------------------|------:|--------------:|---------------------:|----------------:|-----------------------------:|-----------------------------:|-----------------:|------------:|
| 1                 |   239 |          74.2 |                  230 |               5 |                            4 |                            0 |                0 |         239 |
| 2                 |  1235 |          71.9 |                 1152 |              37 |                           40 |                            6 |                0 |        1235 |
| 3                 |   945 |          70.7 |                  798 |              69 |                           74 |                            4 |                0 |         945 |
| 4                 |   133 |          66.2 |                  107 |              17 |                            7 |                            2 |                0 |         133 |
| 5                 |     5 |          42.4 |                    5 |               0 |                            0 |                            0 |                0 |           5 |
| Total/Mean        |  2557 |          71.3 |                 2292 |             128 |                          125 |                           12 |                0 |        2557 |

Table:  Discharge Disposition for the for patients diagnosed with sepsis in 2023 training sample  {#tbl:Discharge_2023}


| Triage Category   |   EoC |   Average Age |   Admit as Inpatient |   Admit to EECU |   Transfer to Other Hospital |   Not admitted as inpatients |   Died in the ED |   Row Total |
|:------------------|------:|--------------:|---------------------:|----------------:|-----------------------------:|-----------------------------:|-----------------:|------------:|
| 1                 |   241 |          75.3 |                  229 |               7 |                            5 |                            0 |                0 |         241 |
| 2                 |  1210 |          71.9 |                 1111 |              39 |                           53 |                            7 |                0 |        1210 |
| 3                 |   838 |          70.1 |                  681 |              79 |                           70 |                            8 |                0 |         838 |
| 4                 |   157 |          69.8 |                  122 |              21 |                           13 |                            1 |                0 |         157 |
| Total/Mean        |  2446 |          71.5 |                 2143 |             146 |                          141 |                           16 |                0 |        2446 |

Table:  Discharge Disposition for the for patients diagnosed with sepsis in 2024 validation sample  {#tbl:Discharge_2024}


![Journeys for patients diagnosed with sepsis with an ED discharge
disposition consistent with not bing admitted in the 2023 training sample.](./figures/section_02/patient_timelines_not_admitted_2023.png){#fig:non_admitted_timelines_2023}
 



\newpage
## Patients without Sepsis 

| Triage Category   |    EoC |   Average Age |   Indigenous |   Female |   Indeterminate |   Unknown |
|:------------------|-------:|--------------:|-------------:|---------:|----------------:|----------:|
| 1                 |   3901 |          58   |          262 |     1796 |               0 |         2 |
| 2                 |  54363 |          57.7 |         2573 |    26586 |               5 |         5 |
| 3                 | 126945 |          54.9 |         6370 |    69688 |              23 |         6 |
| 4                 |  64936 |          49   |         3726 |    35166 |              13 |         7 |
| 5                 |   7894 |          43.8 |          600 |     3733 |               0 |         1 |
| Total/Mean        | 258039 |         263   |        13531 |   136969 |              41 |        21 |

Table: Demographics of the patients diagnosed with sepsis in 2023 training sample  {#tbl:demo_no_sepsis_2023}

| Triage Category   |    EoC |   Average Age |   Indigenous |   Female |   Indeterminate |   Unknown |
|:------------------|-------:|--------------:|-------------:|---------:|----------------:|----------:|
| 1                 |   3745 |          57.1 |          242 |     1332 |               0 |         3 |
| 2                 |  53951 |          57.6 |         2401 |    21084 |               2 |         3 |
| 3                 | 126441 |          55   |         5606 |    54120 |              17 |         4 |
| 4                 |  68531 |          49.4 |         3434 |    27502 |               6 |         3 |
| 5                 |   8480 |          43.9 |          593 |     2993 |               1 |         1 |
| Total/Mean        | 261148 |          53.7 |        12276 |   107031 |              26 |        14 |

Table: Demographics of the patients diagnosed with sepsis in 2024 validation sample  {#tbl:demo_no_sepsis_2024}



| Triage Category   |    EoC |   Average Age |   >2 vital signs available |   qSOFA Flag |   SIRS Flag |   SIRS Severe |   Purple >0 Flag |   Red >1 Flag |
|:------------------|-------:|--------------:|---------------------------:|-------------:|------------:|--------------:|-----------------:|--------------:|
| 1                 |   3901 |          58   |                       3901 |          687 |        1458 |           219 |              653 |           200 |
| 2                 |  54363 |          57.7 |                      54363 |         3185 |       15895 |           615 |             2799 |          1059 |
| 3                 | 126945 |          54.9 |                     126945 |         2653 |       29872 |           420 |             1997 |           725 |
| 4                 |  64936 |          49   |                      64936 |          422 |       11597 |            82 |              545 |           127 |
| 5                 |   7894 |          43.8 |                       7894 |           16 |        1347 |             2 |               43 |            10 |
| Total/Mean        | 258039 |          53.7 |                     258039 |         6963 |       60169 |          1338 |             6037 |          2121 |

Table:  Metrics for the for patients diagnosed with sepsis in 2023 training sample  {#tbl:Metrics_no_sepsis_2023}

| Triage Category   |    EoC |   Average Age |   >2 vital signs available |   qSOFA Flag |   SIRS Flag |   SIRS Severe |   Purple >0 Flag |   Red >1 Flag |
|:------------------|-------:|--------------:|---------------------------:|-------------:|------------:|--------------:|-----------------:|--------------:|
| 1                 |   3745 |          57.1 |                       3745 |          399 |        1451 |           201 |              923 |           273 |
| 2                 |  53951 |          57.6 |                      53951 |         2058 |       15911 |           656 |             4093 |          1626 |
| 3                 | 126441 |          55   |                     126441 |         1571 |       29467 |           483 |             2355 |           874 |
| 4                 |  68531 |          49.4 |                      68531 |          285 |       12338 |            86 |              545 |           185 |
| 5                 |   8480 |          43.9 |                       8480 |            6 |        1476 |             4 |               35 |            16 |
| Total/Mean        | 261148 |          53.7 |                     261148 |         4319 |       60643 |          1430 |             7951 |          2974 |

Table:  Metrics for the for patients diagnosed with sepsis in 2024 validation sample  {#tbl:Metrics_no_sepsis_2024}


| Triage Category   |    EoC |   Average Age |   ICU Stay |   Died as IP |   Died 30 days after admission |
|:------------------|-------:|--------------:|-----------:|-------------:|-------------------------------:|
| 1                 |   3901 |          58   |        422 |          183 |                            394 |
| 2                 |  54363 |          57.7 |       1106 |          726 |                           1849 |
| 3                 | 126945 |          54.9 |        851 |          633 |                           2148 |
| 4                 |  64936 |          49   |        142 |           95 |                            387 |
| 5                 |   7894 |          43.8 |          6 |            0 |                             11 |
| Total/Mean        | 258039 |          53.7 |       2527 |         1637 |                           4789 |

Table:  Outcomes for the for patients not diagnosed with sepsis in 2023 training sample  {#tbl:Outcomes_no_sepsis_2023}

| Triage Category   |    EoC |   Average Age |   ICU Stay |   Died as IP |   Died 30 days after admission |
|:------------------|-------:|--------------:|-----------:|-------------:|-------------------------------:|
| 1                 |   3745 |          57.1 |        312 |          198 |                            304 |
| 2                 |  53951 |          57.6 |       1060 |          690 |                           1469 |
| 3                 | 126441 |          55   |        800 |          641 |                           1785 |
| 4                 |  68531 |          49.4 |        123 |           93 |                            379 |
| 5                 |   8480 |          43.9 |          4 |            3 |                             14 |
| Total/Mean        | 261148 |          53.7 |       2299 |         1625 |                           3951 |

Table:  Outcomes for the for patients not diagnosed with sepsis in 2024 validation sample  {#tbl:Outcomes_no_sepsis_2024}


| Triage Category   |   FMC |   LMH |   MPH |   NHS |   QEH |   RAH |   Row Total |
|:------------------|------:|------:|------:|------:|------:|------:|------------:|
| 1                 |  1216 |   910 |   136 |    56 |   418 |  1165 |        3901 |
| 2                 | 13323 | 11041 |  4277 |  3991 |  5536 | 16195 |       54363 |
| 3                 | 25718 | 21568 | 14875 | 13752 | 19051 | 31981 |      126945 |
| 4                 | 10627 | 12288 |  6281 |  9984 | 11947 | 13809 |       64936 |
| 5                 |  1210 |  2836 |   502 |  1092 |   555 |  1699 |        7894 |
| Total             | 52094 | 48643 | 26071 | 28875 | 37507 | 64849 |      258039 |

Table:  ED presentations for patients not diagnosed with sepsis in 2023 training sample  {#tbl:hospitals_no_sepsis_2023}

| Triage Category   |   FMC |   LMH |   MPH |   NHS |   QEH |   RAH |   Row Total |
|:------------------|------:|------:|------:|------:|------:|------:|------------:|
| 1                 |  1104 |   645 |   141 |   129 |   558 |  1168 |        3745 |
| 2                 | 14287 | 10055 |  4313 |  3836 |  5613 | 15847 |       53951 |
| 3                 | 24700 | 20873 | 17377 | 13302 | 19625 | 30564 |      126441 |
| 4                 |  9911 | 14281 |  7913 | 10058 | 14007 | 12361 |       68531 |
| 5                 |  1049 |  3212 |   890 |  1384 |   689 |  1256 |        8480 |
| Total             | 51051 | 49066 | 30634 | 28709 | 40492 | 61196 |      261148 |

Table:  ED presentations for patients not diagnosed with sepsis in 2024 validation sample  {#tbl:hospitals_no_sepsis_2024}


\newpage
### Discharge Disposition of  Patients  without Sepsis 

| Triage Category   |    EoC |   Average Age |   Admit as Inpatient |   Admit to EECU |   Transfer to Other Hospital |   Not admitted as inpatients |   Died in the ED |   Row Total |
|:------------------|-------:|--------------:|---------------------:|----------------:|-----------------------------:|-----------------------------:|-----------------:|------------:|
| 1                 |   3901 |          58   |                 2471 |             400 |                           52 |                          960 |               15 |        3898 |
| 2                 |  54363 |          57.7 |                21150 |            8340 |                         1399 |                        23271 |               38 |       54198 |
| 3                 | 126945 |          54.9 |                33495 |           19663 |                         2607 |                        70100 |               18 |      125883 |
| 4                 |  64936 |          49   |                 8943 |            6863 |                          712 |                        46164 |                1 |       62683 |
| 5                 |   7894 |          43.8 |                  565 |             371 |                           38 |                         6320 |                0 |        7294 |
| Total/Mean        | 258039 |          53.7 |                66624 |           35637 |                         4808 |                       146815 |               72 |      253956 |

Table:  Discharge Disposition for the for patients not diagnosed with sepsis in 2023 training sample  {#tbl:Discharge_not_sepsis_2023}

| Triage Category   |    EoC |   Average Age |   Admit as Inpatient |   Admit to EECU |   Transfer to Other Hospital |   Not admitted as inpatients |   Died in the ED |   Row Total |
|:------------------|-------:|--------------:|---------------------:|----------------:|-----------------------------:|-----------------------------:|-----------------:|------------:|
| 1                 |   3745 |          57.1 |                 2223 |             543 |                           93 |                          859 |               18 |        3736 |
| 2                 |  53951 |          57.6 |                21128 |           10441 |                         1486 |                        20722 |               28 |       53805 |
| 3                 | 126441 |          55   |                31544 |           23671 |                         2897 |                        66744 |               25 |      124881 |
| 4                 |  68531 |          49.4 |                 8902 |            8787 |                          907 |                        46915 |                1 |       65512 |
| 5                 |   8480 |          43.9 |                  511 |             488 |                           48 |                         6744 |                0 |        7791 |
| Total/Mean        | 261148 |          53.7 |                64308 |           43930 |                         5431 |                       141984 |               72 |      255725 |

Table:  Discharge Disposition for the for patients not diagnosed with sepsis in 2024 validation sample  {#tbl:Discharge_not_sepsis_2024}

\newpage

## Variable Distributions 




![Distributions of the various observations used in the Machine Learning models. The
data for patients with a Sepsis admission (light blue) and without Sepsis
(yellow). The rectangles outlined in black contain normal results as taken from
the Deteriorating Patient Reference Guide
[@RDR].](./figures/section_02/variable_distributions.png){#fig:variable_distributions}