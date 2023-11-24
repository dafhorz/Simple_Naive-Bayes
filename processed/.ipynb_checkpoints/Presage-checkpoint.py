#Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
sns.set(color_codes=True)

# to display all columns
pd.set_option('display.max_columns', None)
pd.options.display.max_rows = 400


#Leer datos
df = pd.read_csv('./raw/adult_data.csv')

for i in list(df.columns):
    if df[i].dtype!='int64':
        df[i]=df[i].str.replace(' ','')
        
        
#Crear bins
df['age-bins'] = pd.qcut(df['age'], q = 5)
df['hours-per-week-bins'] = pd.cut(df['hours-per-week'], bins=5)


#Cálculo de pesos
def scoreIndividualComputation(df, totalRows, var, val, Ccol, Cval):
    NC = len(df[ df[Ccol]==Cval ])
    NCcomplement = totalRows - NC
    NxiC = len(   df[ (df[var]==val) & (df[Ccol]==Cval)  ]   )
    NxiCcomplement = len(   df[ (df[var]==val) & (df[Ccol]!=Cval)  ]   )
    
    return np.log10( (NxiC/NC)/(NxiCcomplement/NCcomplement)   )



#Assumes that income is the target variable. 
def score(df):
    totalRows=len(df)
    
    score = pd.DataFrame(columns = ['Variable', 'Valor', 'Score'])
    
    for var in list(df.columns):
        if df[var].dtype!='int64' and var!='income':
            for val in list(df[var].unique()):
                #newrow = pd.DataFrame({'Variable':var, 'Valor':val, 'Score': scoreIndividualComputation(df, totalRows, var, val, 'income', '>50K')            })
                #score=pd.concat([score, newrow ]).reset_index(drop=True)
                score=score.append( {'Variable':var, 'Valor':val, 'Score': scoreIndividualComputation(df, totalRows, var, val, 'income', '>50K')            }, ignore_index=True)
    
    return score


score=score(df)
score.to_csv('./processed/scores.csv', index=False)