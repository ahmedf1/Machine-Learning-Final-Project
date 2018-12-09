'''
Redwanul Mutee 
Farhad Ahmed
ML Project: Data Formatting
'''

import pandas as pd

#DF(1) regents scores
df = pd.read_csv("raw_regents_scores_2015.csv", na_values='s')                                                      #Read from regents Scores CSV
                                                                                                                    #Drop Columns that are not needed
df.drop( ['School Name', 'School Type', 'Demographic Variable', 'Total Tested',
 'Number Scoring Below 65', 'Percent Scoring Below 65', 'Number Scoring 65 or Above', 
 'Percent Scoring 65 or Above', 'Number Scoring 80 or Above', 'Percent Scoring 80 or Above', 
 'Number Scoring CR', 'Percent Scoring CR'], axis=1, inplace= True )
                                                                                                                    #View dataframe columns using print(list(df))
df = df.dropna()                                                                                                    ##Drop rows with N/A values and Keep only rows where
df = df[df["School Level"] == "High school"]                                                                        #                    School level is high school, 
df = df[df["Year"] == 2015]                                                                                         #                    Year is 2015, 
df = df[df["Demographic Category"] == "All Students"]                                                               #                    Demographic category is all students

df.drop( ['School Level','Year','Demographic Category'], axis=1, inplace= True )                                    #Can now drop columns: School Level, Year and Demographic Category Column --> they are same for all rows                                                                                                  
df.rename(columns={'Regents Exam': 'Entry Number'}, inplace=True)
df = pd.pivot_table(df, values = 'Mean Score', index=['School DBN'], columns = 'Entry Number').reset_index()        #Pivot dataframe so that the regents exams (switched to entry numbers) are columns with values mean score, index is still unique school dbn


df.drop( ['Common Core English', 'Common Core Geometry', 
        'U.S. History and Government', 'Common Core Algebra',
        'Physical Settings/Earth Science'], axis=1, inplace= True )                                                 #Unfortunately had to drop some regents to get more complete rows :(
df = df.dropna()                                                                                                    #Drop NA values so we only have rows of schools where all regents have mean scores (nothing is NA)
#print(df.head(1))                                                                                                  #Check dataframe first row



#DF2 is sat scores
df2 = pd.read_csv("raw_sat_scores_2015.csv")                                                                        #Read from Sat scores CSV
df2.drop( ['School Name', 'Borough', 'Building Code', 'Street Address', 'City',                                     #Drop Columns that are not needed
    'State', 'Zip Code','Latitude',	'Longitude', 'Phone Number', 'Start Time', 
    'End Time', 'Student Enrollment', 'Percent White', 'Percent Black',
    'Percent Hispanic', 'Percent Asian', 'Percent Tested'], axis=1, inplace= True )
df2 = df2.dropna()                                                                                                  #Drop rows with N/A values
df2.rename(columns={'School ID': 'School DBN'}, inplace=True)                                                       #Rename School Id so that it matches column School DBN in regents csv. we do this so we can merge on this column

df2['Average SAT Score (Total)'] =  df2[['Average Score (SAT Math)', 
                                        'Average Score (SAT Reading)',
                                        'Average Score (SAT Writing)']].sum(axis=1)                                 #Create new column that calculates avg sat score from avg sat section scores
#print(df2.head(1))



#DF3 Merging df1 and df2
df3 = pd.merge(df, df2, on='School DBN', how='outer')                                                               #Merge the dat on school dbn
df3 = df3.dropna()                                                                                                  #Drop rows with N/A values
#print(df3.head(2))

df3.to_csv("HS_Regents_Sat_Scores_2015.csv")                                                                        #Export df as csv