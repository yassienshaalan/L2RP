import pandas as pd
import matplotlib.pylab as plt
from sklearn import preprocessing
from scipy.stats import skew
from scipy.stats import boxcox
import numpy as np

def resolve_Skewness_For_Feature(orig_feature,feature_name,plot):

    #The next line uses scale method from scikit-learn to transform the distribution
    #This will not impact Skewness Statistic calculation
    #We have included this for sake of completion
    #Note that we changed the following line to process the square roots instead of actuals
    orig_feature.fillna(0, inplace=True)
    try:
        sqrt_scaled_feature = preprocessing.scale(np.sqrt(orig_feature))
    except ValueError:
        #orig_feature[orig_feature >10000] = 1000
        #print("feature name "+feature_name)
        print("Failed sqrt")
        sqrt_scaled_feature = np.zeros(shape=(len(orig_feature), 1))


    #Note that we shift the values by 1 to get rid of zeros
    try:
        boxCox_scaled = preprocessing.scale(boxcox(orig_feature+1)[0])
    except ValueError:
        #orig_feature = orig_feature.where(orig_feature < 0, 0.1)
        orig_feature[orig_feature < 0] = 0.1
        boxCox_scaled = preprocessing.scale(boxcox(orig_feature + 100)[0])
        #plot = 1
    orig_scaled_feat = preprocessing.scale(orig_feature)

    #Next We calculate Skewness using skew in spicy.stats
    skness = skew(sqrt_scaled_feature)
    sknessBoxCox = skew(boxCox_scaled)
    sknessOrig = skew(orig_scaled_feat)

    #print("orig skewness "+str(sknessOrig[0])+" sqt skewness "+str(skness[0])+" boxcox skewness "+str(sknessBoxCox[0]))
    print("orig skewness " + str(sknessOrig[0]) + " boxcox skewness " + str(sknessBoxCox[0]))
    #print(orig_scaled_feat)
    #We draw the histograms
    if plot == 1:
        figure = plt.figure()
        figure.add_subplot(131)
        plt.hist(sqrt_scaled_feature,facecolor='red',alpha=0.75)
        plt.xlabel(feature_name+" - Transformed(Using Sqrt)")
        plt.title("Transformed "+feature_name+" Histogram")
        plt.text(0,350,"Skewness: {0:.2f}".format(skness[0]))
        #print("box")
        #print(boxCox_scaled)
        figure.add_subplot(132)
        plt.hist(boxCox_scaled,facecolor='blue',alpha=0.75)
        plt.xlabel(feature_name+" - Using BoxCox Transformation")
        plt.title(feature_name+" Histogram - Un-Skewed(BoxCox)")
        plt.text(0,350,"Skewness: {0:.2f}".format(sknessBoxCox[0]))

        figure.add_subplot(133)
        plt.hist(orig_scaled_feat,facecolor='green',alpha=0.75)
        plt.xlabel(feature_name+" - Based on Original Flight Times")
        plt.title(feature_name+" Histogram - Right Skewed")
        plt.text(0,350,"Skewness: {0:.2f}".format(sknessOrig[0]))

        plt.show()

    normalized_box = boxCox_scaled
    min_max_scaler = preprocessing.MinMaxScaler()
    normalized_box  = min_max_scaler.fit_transform(boxCox_scaled)

    return normalized_box

def Normalize_Input(input_vec):
    min_max_scaler = preprocessing.MinMaxScaler()
    normalized_output = min_max_scaler.fit_transform(input_vec)
    return normalized_output