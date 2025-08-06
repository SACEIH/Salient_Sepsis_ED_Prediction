\newpage
# Machine Learning 

The data described in the earlier section is used to train and validate
diagnosis classifier models Sepsis. The data is prepared by setting any missing
measurement from in the data set with the defaults listed in Table
-@tbl:defaults. Numerical variables are transformed on to the range $[0,1]$.
Categorical values are passed through the One Hot Encoder algorithm
[@OneHotEncoder,@scikit-learn] to turn them into a complete set of logical
variables. 

The data set is split into training and validation sets using an
80:20% split. An XG Boost  model [@DBLP:journals/corr/ChenG16] is optimised by
randomly scanning through the possible model settings and minimising the false
positive rate for a true positive rate of 85%. The optimized model is then
tested on the validation samples.

|     Property or Result                 |     Default     |
|----------------------------------------|-----------------:|
|     Age                                |     NA          |
|     Sex                                |     NA          |
|     Respiration (breaths/min)          |     15          |
|     O2 Saturation (%)                  |     98          |
|     Blood Pressure Systolic (mm Hg)    |     120         |
|     Pulse Rate (beats/min)             |     80          |
|     Temperature (ºC)                   |     37.5        |
|     Level of Consciousness             |     0           |

Table: Data used in the ML models. If no result has been recorded the default
value is assigned. If the default is NA (not applicable) then there is no
default value.  {#tbl:defaults}

## ML Metrics 

Standard machine learning quality metrics are  calculated where $N$ is the size
of the cohort, $\text{TP}$ is the number of true positives,  $\text{TN}$ is the
number if true negatives, $\text{FP}$ is the number of false positives,
$\text{TN}$ is the number if false negatives, $N_{\text{sepsis}}$ is the number
of patients with a sepsis diagnosis and $N_{\text{not sepsis}} =
N-N_{\text{sepsis}}$ is the number of patients who do not have sepsis:

$$\text{Accuracy} = A = \frac{\text{TP} +\text{TN}}{N}$$ {#eq:accuracy}
$$\text{Precision} = P = \frac{\text{TP}}{\text{TP} + \text{FP}}$$ {#eq:precision}
$$\text{Recall} = R = \frac{\text{TP}}{\text{TP} + \text{FN}}$$ {#eq:recall}
$$F_{1} = \frac{2 P R}{P+R}$$ {#eq:f1} 
$$\text{Sensitivity}  = \frac{\text{TP}}{N_{\text{sepsis}}}$$ {#eq:sensitivity}
$$\text{Specificity}  = \frac{\text{TN}}{N_{\text{not sepsis}}}$$ {#eq:specificity}

## Variation Across Subgroups 

The performance of the ML model for different subgroups of the patient cohort
will be verified for
- the patient’s gender, 
- indigenous status, 
- the hospital,
- age groups, 
- triage categories, 
- arrival mode. 

The true positive and true negative rates will be compared across these subgroups.

## Optimisation 

Several strategies for optimising the ML model will be explored. 

The first will be the cohort composition and will compare patients with a
minimum of three of the following vital signs are recorded in the EMR during the
presentation: respiration, O~2~ Saturation, systolic blood pressure, pulse rate
and temperature and patients where all five are recorded. 

The second will look at variations in the data included in the model. For
example is the patients age included, do we use the O~2~ flow to create a
categorical true false value etc.

The third variation will be the variable used in fitting the model. The  variables to be optimized are: 
- minimising the false positive rate for a true positive rate of 85%, 
- maximising the sensitivity for a specificity of 95%. 
