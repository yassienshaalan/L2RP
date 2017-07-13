import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier

def plot_feature_importance1(features,importances,indices,feature_names):
    plt.figure()
    print(features.shape[1])
    plt.title("Feature importances")
    plt.bar(range(features.shape[1]), importances[indices], color="r", yerr=std[indices], align="center")
    #plt.xticks(range(features.shape[1]), indices)
    plt.xticks(range(features.shape[1]), feature_names)
    plt.xlim([-1, features.shape[1]])
    plt.show()
    return
def plot_feature_importance2(features,importances,indices,feature_names, category_name,num_max_features):
    f, ax = plt.subplots(figsize=(11, 9))
    plt.title("Feature ranking for "+category_name, fontsize=20)
    print("range(features.shape[1]) "+str(range(features.shape[1])))
    #plt.bar(features.shape[1], importances[indices], color="b", align="center")
    plt.bar(range(num_max_features), importances[indices[range(num_max_features)]], color="b", align="center")
    #feature_names = df.columns  # e.g. ['A', 'B', 'C', 'D', 'E']

    plt.xticks(range(num_max_features), feature_names,rotation='vertical')# plot features by names
    #plt.xticks(range(features.shape[1]), indices) plot feature by indices
    #plt.xlim([-1, features.shape[1]])
    plt.xlim([-1, num_max_features])
    plt.ylabel("importance", fontsize=18)
    plt.xlabel("index of the feature", fontsize=18)
    plt.show()
    return


def Extract_Features_From_File(file_path):
    ranks = []
    features_vectors = []
    with open(file_path, 'r') as filep:
        for item in filep:
            row = item.split(' ')
            rank = row[0]
            ranks.append(int(rank))
            vector = []
            for i in range(2, len(row)):
                feat = row[i].split(':')
                if len(feat)>1:
                    vector.append(float(feat[1]))
            features_vectors.append(vector)

    return features_vectors,ranks

def Feature_Selection_Using_UniVariate(X,Y):
    # feature extraction using Univariate Selection
    print("Feature extraction using Univariate Selection")
    test = SelectKBest(score_func=chi2, k=4)
    fit = test.fit(X, Y)
    # summarize scores
    np.set_printoptions(precision=3)
    print(fit.scores_)
    features = fit.transform(X)
    print(features.shape)
    # summarize selected features
    print(features[0:5, :])

    return

def Feature_Selection_Using_Recursive_Feature_Elimination(X,Y):
    # Feature Extraction with RFE
    print("Feature Extraction with RFE")
    model = LogisticRegression()
    num_requested_features = int(X.shape[1]/2)
    print("num_requested_features "+str(num_requested_features))
    rfe = RFE(model, 3)
    print("Fitting")
    fit = rfe.fit(X, Y)
    print("Num Features: " + str(fit.n_features_))
    print("Selected Features " + str(fit.support_))
    print("Feature Ranking: " + str(fit.ranking_))
    return

def Feature_Selection_Using_Principal_Component_Analysis(X,Y):
    # feature extraction
    print("Principal Component Analysis")
    pca = PCA(n_components=3)
    fit = pca.fit(X)
    # summarize components
    print("Explained Variance: "+str(fit.explained_variance_ratio_))
    print(fit.components_)
    return
def get_feature_names(num_time_periods):
    feature_names = []
    for i in range(num_time_periods):
        feature_names.append("#Rating_1_P"+str(i+1))
        feature_names.append("#Rating_2_P" + str(i + 1))
        feature_names.append("#Rating_3_P" + str(i + 1))
        feature_names.append("#Rating_4_P" + str(i + 1))
        feature_names.append("#Rating_5_P" + str(i + 1))

    for i in range(num_time_periods):
        feature_names.append("#Helpful_1_P" + str(i + 1))
        feature_names.append("#Helpful_2_P" + str(i + 1))
        feature_names.append("#Helpful_3_P" + str(i + 1))
        feature_names.append("#Helpful_4_P" + str(i + 1))
        feature_names.append("#Helpful_5_P" + str(i + 1))

    for i in range(num_time_periods):
        feature_names.append("#Non_Helpful_1_P" + str(i + 1))
        feature_names.append("#Non_Helpful_2_P" + str(i + 1))
        feature_names.append("#Non_Helpful_3_P" + str(i + 1))
        feature_names.append("#Non_Helpful_4_P" + str(i + 1))
        feature_names.append("#Non_Helpful_5_P" + str(i + 1))

    for i in range(num_time_periods):
        feature_names.append("#Sent_+ve_1_P" + str(i + 1))
        feature_names.append("#Sent_-ve_1_P" + str(i + 1))
        feature_names.append("#Sent_+ve_2_P" + str(i + 1))
        feature_names.append("#Sent_-ve_2_P" + str(i + 1))
        feature_names.append("#Sent_+ve_3_P" + str(i + 1))
        feature_names.append("#Sent_-ve_3_P" + str(i + 1))
        feature_names.append("#Sent_+ve_4_P" + str(i + 1))
        feature_names.append("#Sent_-ve_4_P" + str(i + 1))
        feature_names.append("#Sent_+ve_5_P" + str(i + 1))
        feature_names.append("#Sent_-ve_5_P" + str(i + 1))

    #for i in range(X.shape[1]):
      #  feature_names.append("feature_" + str(i + 1))

    return feature_names
def Feature_Selection_Using_Feature_Importance(X,Y,category_name,feature_names,num_max_features):
    # feature extraction
    print("Feature Importance Feature selection")
    model = ExtraTreesClassifier(class_weight='balanced',n_jobs=1)
    model.fit(X, Y)
    #print(model.feature_importances_)
    #print(type(model.feature_importances_))
    feat_imp = model.feature_importances_
    indices = np.argsort(feat_imp)[::-1]
    #print(indices)
    print("len feature names "+str(len(feature_names)))
    selected_feature_names =[]
    for f in range(X.shape[1]):
        print("%d. feature %d (%f) %s" % (f + 1, indices[f], feat_imp[indices[f]],feature_names[indices[f]]))
        if f <num_max_features:
            selected_feature_names.append(feature_names[indices[f]])
    #print(feature_names)
    print (selected_feature_names)
    plot_feature_importance2(X, feat_imp, indices,selected_feature_names,category_name,num_max_features) #feature_names,category_name,num_max_features)
    return
file_path = "D:\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/train.txt"
features_vectors,ranks = Extract_Features_From_File(file_path)
X = np.array(features_vectors)
Y = np.array(ranks)
print(X.shape)
print(Y.shape)
timeperiods=1
num_max_features = 11
#feature_names = get_feature_names(timeperiods)
feature_names = []
feature_names.append("1-Star")
feature_names.append("2-Star")
feature_names.append("3-Star")
feature_names.append("4-Star")
feature_names.append("5-Star")

feature_names.append("Avg_Star")
feature_names.append("Min LS")
feature_names.append("Max LS")
feature_names.append("Median LS")
feature_names.append("Median # Revs")
feature_names.append("Median Active")



Feature_Selection_Using_Feature_Importance(X,Y,"Jewelry",feature_names,num_max_features)
#Feature_Selection_Using_UniVariate(X,Y)
#Feature_Selection_Using_Recursive_Feature_Elimination(X,Y)
#Feature_Selection_Using_Principal_Component_Analysis(X,Y)