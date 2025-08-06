---
title: "SALIENT: ED Machine Learning Sepsis Prediction"
author: "Iain A Bertram,"
date: "11 July 2025"
bibliography: report.bib 
csl: cell-numeric.csl    
toc-own-page: true
titlepage: true
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "360049"
titlepage-rule-height: 0
titlepage-background: "Word_document_template_back.png"
header-left: "\\hspace{1cm}"
header-center: "OFFICIAL: Sensitive"
header-right: "Page \\thepage"
footer-right: "\\hspace{1cm}"
footer-left: "\\hspace{1cm}"
footer-center: "OFFICIAL: Sensitive "
geometry: "left=1cm,right=1cm,top=2.6cm,bottom=3.25cm"
page-background: "headers.pdf"
page-background-opacity: 0.5
code-block-font-size: "\\scriptsize"
listings: True
# abstract-title: "Abstract"
# abstract: |
#    This is an example document to test stuff with Pandoc. In this case the goal
#    is to understand when or why is the Abstract title portrayed.
# classoption:
# - abstract
---

# About this document
This technical document has been developed as part of the ‘Gen Med Project’ by the Commission on Excellence and Innovation in Health (CEIH). The project forms part of a program of work that is funded through the Acute Models of Care Grant 2022 by the Medical Research Future Fund (MRFF). The project’s primary goal is to reduce unwarranted clinical variation in general medicine, using a data analytics and machine learning approach.

Sepsis was identified as a focus area from early analysis that looked at high bed day consumption and high opportunity Diagnosis Related Groups (DRGs) that included shortness of breath as a symptom.


# Document Revisions 

|     No.    |     Date        |     Description    |     Person          |
|------------|-----------------|--------------------|--------------------|
|     0.1    |     30/10/24    |     First Draft <br> Document describing the ED Sepsis Presentation ML model, <br> and the various verification requirements for the model. |     Iain Bertram    |
|            |                 |                                                                           |                     |
|            |                 |                                                                           |                     |


\pagebreak

# Introduction 

A new adult sepsis pathway has been proposed for use with public hospitals within South
Australia. This pathway is intended to identify patients who are at risk of developing 
Sepsis and initiating a standardised treatment programme. The patients are identified 
using Rapid Detection and Response (RDR) Observation Charts as implemented within the 
public hospital Electronic Medical Record (EMR) using the Sunrise Deteriorating Patient 
Reference Guide  [@RDR]. 

There are two pathways for flagging a patient as being at risk of Sepsis and
requiring either review by a Senior Medical Officer or a Medical Emergency
response. The Purple pathway is triggered if any of the patient’s observations
in the Rapid Detection and Response (RDR) are in the purple zone (Table
-@tbl:table1). The Red pathway is triggered if there are two or more red zone
observations. 

This report describes the development of a Machine Learning (ML) model that can be used 
in place of these pathways. I.e. to develop machine learning models that identify people 
who will be admitted to hospital and will have a sepsis diagnosis (based on ICD-10 
codes) on inpatient discharge based on measurement of the patient’s vital signs.

|     Measure                            |     Purple    |     Red    |     Yellow    |     Yellow    |     Red     |     Purple    |
|----------------------------------------|:-------------:|:----------:|:-------------:|:-------------:|:-----------:|:-------------:|
|                                        |               |     Low    |               |               |    High     |               |
|     Respiration (breaths/min)          |     7         |            |     10        |     21        |     26      |     31        |
|     O~2~ Saturation (%)                  |     88        |     91     |     94        |     NA        |     NA      |     NA        |
|     O~2~ Flow (L/min)                    |     NA        |     NA     |     NA        |     5         |     7       |     8         |
|     Blood Pressure Systolic (mm Hg)    |     89        |     99     |     NA        |     170       |     180     |     200       |
|     Pulse Rate (beats/min)             |     39        |     49     |     59        |     100       |     120     |     140       |
|     Temperature (ºC)                   |               |     35     |     35.5      |     38.1      |     38.6    |               |
|     Level of Consciousness             |     NA        |     NA     |     NA        |               |     2       |     3         |

Table: Rapid Detection and Response (RDR) Alert Triggers {#tbl:table1}