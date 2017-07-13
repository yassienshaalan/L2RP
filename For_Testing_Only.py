from Extract_Polarties import extract_Weighted_Product_Polarities

#extract_Weighted_Product_Polarities()
#Airline Data Example
#Calculating Skewness Statistic For Flight Time Using Python
#You can download dataset from http://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236

import pandas as pd
import matplotlib.pylab as plt
from sklearn import preprocessing
from scipy.stats import skew
from scipy.stats import boxcox
import numpy as np

#First we import the data
#data = pd.read_csv('C:/Users/Yassien\Downloads/On_Time_On_Time_Performance_2015_1/On_Time_On_Time_Performance_2015_1.csv')

#Replace Missing Values with zero
#data['AirTime'].fillna(0,inplace=True)
'''
#The next line uses scale method from scikit-learn to transform the distribution
#This will not impact Skewness Statistic calculation
#We have included this for sake of completion
#Note that we changed the following line to process the square roots instead of actuals
print(type(data['AirTime']))
AirTime = preprocessing.scale(np.sqrt(data['AirTime']))
print(type(AirTime))
#Note that we shift the values by 1 to get rid of zeros
AirTimeBoxCox = preprocessing.scale(boxcox(data['AirTime']+1)[0])
AirTimeOrig = preprocessing.scale(data['AirTime'])

#Next We calculate Skewness using skew in spicy.stats
skness = skew(AirTime)
print("sqrt sk "+str(skness))
sknessBoxCox = skew(AirTimeBoxCox)
print("boxcox sk "+str(sknessBoxCox))
sknessOrig = skew(AirTimeOrig)
print("orig sk "+str(sknessOrig))
#We draw the histograms
figure = plt.figure()
figure.add_subplot(131)
plt.hist(AirTime,facecolor='red',alpha=0.75)
plt.xlabel("AirTime - Transformed(Using Sqrt)")
plt.title("Transformed AirTime Histogram")
plt.text(2,100000,"Skewness: {0:.2f}".format(skness))

figure.add_subplot(132)
plt.hist(AirTimeBoxCox,facecolor='blue',alpha=0.75)
plt.xlabel("AirTime - Using BoxCox Transformation")
plt.title("AirTime Histogram - Un-Skewed(BoxCox)")
plt.text(2,100000,"Skewness: {0:.2f}".format(sknessBoxCox))

figure.add_subplot(133)
plt.hist(AirTimeOrig,facecolor='green',alpha=0.75)
plt.xlabel("AirTime - Based on Original Flight Times")
plt.title("AirTime Histogram - Right Skewed")
plt.text(2,100000,"Skewness: {0:.2f}".format(sknessOrig))

plt.show()
'''
from Resolve_Skewness import resolve_Skewness_For_Feature
#resolve_Skewness_For_Feature(data['AirTime'],"AirTime")
import  math
import numpy as np
orig_feature= [1000000,100000000,100100000000]
val = np.sqrt(orig_feature)
print(val)