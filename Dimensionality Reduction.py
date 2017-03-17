#Import Library
# #Assumed you have training and test data set as train and test
from sklearn import decomposition
#  Create PCA obeject
n_features = 250

sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\SVM_Light\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25\Arts\Cutoff_10\Set_1/"

X = []  # list of samples each with list of features
trainFilePath = sourceDirectory+"train.txt"
with open(trainFilePath, 'r') as fp:
    for line in fp:
        vector = []
        row = line.split(" ")
        for i in range(2,len(row)):
            feature = row[i]
            feature = feature.split(':')
            vector.append(float(feature[1]))
        X.append(vector)

print("X")
#print(X)
n_sample = len(X)
##''''
print(n_sample)
k =min(n_sample, n_features)
pca= decomposition.PCA(n_components=k)
# #default value of
#  For Factor analysis #
fa= decomposition.FactorAnalysis()
# Reduced the dimension of training dataset using PCA

#Reduced the dimension of test dataset
train = X
train_reduced = pca.fit_transform(train)
print(type(train_reduced))
print("train_reduced")
print(train_reduced)
import numpy as np
np.set_printoptions(suppress=True)

#print(X)
test = X
test_reduced = pca.transform(test)
#'''
