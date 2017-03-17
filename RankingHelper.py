import os
from alogrithms import mergeSort
from dirichlet_True_Rating import measureDistanceBetweenForCategory
import subprocess
from Testing import writeCorrelationRScript
from Testing import runSpearmanExtractScript
from Testing import  runKenallExtractScript

def transformPredictionsToComputedPerCategory(categoryName,categoriesDirectory, destDirectory,predicitonsFile):
    print("Procedure to combine prediction values with Product names for Kendal preparation")
    offset = 0
    predictions = []
    with open(predicitonsFile, 'r') as fp:
        for line in fp:
            row = line.split("\n")
            predictions.append(row[0])
    print("No. Predictions")
    print(len(predictions))
    total = 0
    print(categoryName)
    catPath = categoriesDirectory + categoryName + ".txt"
    products = []
    with open(catPath, 'r') as fp:
        for line in fp:
            row = line.split("\t")
            products.append(row[0])
    numLines = len(products)
    total += numLines
    FilePath = destDirectory + categoryName + ".txt"

    filehandle = open(FilePath, 'w')
    for i in range(len(products)):
        if (i + offset < len(predictions)):
            filehandle.write(products[i])
            filehandle.write("\t")
            filehandle.write(predictions[i + offset])
            filehandle.write("\n")
        else:
            break
    offset += numLines
    print("Total Products")
    print(total)
    return

def transformPredictionsToComputed(testing_Set, categoriesDirectory, destDirectory,predicitonsFile):
    offset = 0
    predictions = []
    with open(predicitonsFile, 'r') as fp:
        for line in fp:
            row = line.split("\n")
            predictions.append(row[0])
    print("No. Predictions")
    print(len(predictions))
    total = 0
    for category in testing_Set:
        print(category)
        catPath = categoriesDirectory + category + ".txt"
        products = []
        with open(catPath, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                products.append(row[0])
        numLines = len(products)
        total += numLines
        FilePath = destDirectory + category + ".txt"

        filehandle = open(FilePath, 'w')
        for i in range(len(products)):
            if (i + offset <len(predictions)):
                filehandle.write(products[i])
                filehandle.write("\t")
                print()
                filehandle.write(predictions[i + offset])
                filehandle.write("\n")
            else:
                break
        offset += numLines
    print("Total Products")
    print(total)
    return

def divideAllPredictionsFileIntoChunks(destDirectory,sortedSalesRankDirectory,categoryName,dataset_type):

    salesrank=[]
    data = []
    predictionsFilePath = destDirectory+categoryName+".txt"
    with open(predictionsFilePath, 'r') as fp:
        for line in fp:
            data.append(line)
    print("Num All Predictions "+str(len(data)) )

    salesRankFilePath = sortedSalesRankDirectory + categoryName + ".txt"
    with open(salesRankFilePath, 'r') as fp:
        for line in fp:
            if dataset_type=="amazon":
                salesrank.append(line)
            elif dataset_type == "yelp":
                newLine = line.split('\t')
                newLine = newLine[0]+"\t"+newLine[2]
                salesrank.append(newLine)
    print("Num SalesRank " + str(len(salesrank)))
    index = 0
    numSets = 0
    newPredicitonDirectory = destDirectory + "Predictions"
    print("newPredicitonDirectory")
    print(newPredicitonDirectory)
    try:
        os.stat(newPredicitonDirectory)
        os.chmod(newPredicitonDirectory, 0o777)
    except:
        os.mkdir(newPredicitonDirectory)
        os.chmod(newPredicitonDirectory, 0o777)
    newSalesDirectory = destDirectory + "SalesRank"
    try:
        os.stat(newSalesDirectory)
    except:
        os.mkdir(newSalesDirectory)
    writtenPredictions = 0
    writtenSales = 0
    for folder in os.listdir(destDirectory):
        setFilePath = destDirectory + folder
        if os.path.isdir(setFilePath):
            for files in os.listdir(setFilePath):
                if files == "predictions.txt":
                    filePath = setFilePath + "/"+files
                    counter = 0
                    with open(filePath, 'r') as fp:
                        for line in fp:
                            counter+=1
                    print("Chuck size is " + str(counter))
                    categoryName = "Part"
                    filePathToWrite = newPredicitonDirectory + "/" + categoryName + "_" + str(numSets + 1) + ".txt"
                    filehandle = open(filePathToWrite, 'w')
                    #print("Writing Predictions of Chunk "+str(numSets))
                    for j in range(counter):
                        if index+j >=len(data):
                            break
                        else:
                            filehandle.write(data[index+j])
                            writtenPredictions+=1
                    filehandle.close()
                    filePathToWrite = newSalesDirectory + "/" + categoryName + "_" + str(numSets + 1) + ".txt"
                    filehandle = open(filePathToWrite, 'w')
                    #print("Writing SalesRank of Chunk " + str(numSets))
                    for j in range(counter):
                        if index + j >= len(data):
                            break
                        else:
                            filehandle.write(salesrank[index + j])
                            writtenSales+=1
                    filehandle.close()
                    index+=counter
                    numSets+=1
    print("Written "+str(writtenPredictions)+" prediction records")
    print("Written " + str(writtenSales) + " sales rank records")
    return
def sortRankedProductDirectory(inputDirectory,destDirectory,reverse):
    #print("Procedure to read category rated File, get a product from it and read its file and sort it and write to a file for a cetegory file")
    #product_Id Category sales_rank
    import sys
    sys.setrecursionlimit(10000000)
    for filename in os.listdir(inputDirectory):
        line = ""
        listofProducts = []
        filePath = inputDirectory+filename
        print(filePath)
        print("Sorting "+filename)
        with open(filePath, 'r') as fp:
          for line in fp:
             tuple = line.split('\t')
             listofProducts.append((tuple[0],float(tuple[1])))
        mergeSort(listofProducts)
        if len(listofProducts) == 0:
            print("problem with zero lists")

        basedir = os.path.dirname(destDirectory)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        newFilePath = destDirectory+ filename

        filehandle = open(newFilePath, 'w')

        if reverse == 1:
            for item in reversed(listofProducts):
                filehandle.write(item[0])
                filehandle.write("\t")
                filehandle.write(str(item[1]))
                filehandle.write("\n")
        else:
            for item in (listofProducts):
                filehandle.write(item[0])
                filehandle.write("\t")
                filehandle.write(str(item[1]))
                filehandle.write("\n")
        filehandle.close()

    print("Finished Sorting")
    return
from natsort import natsorted

def createSortedRankAndRunR(categoryMainDirectory,lib,categoryName,orig_CatName,dataset_type,salesRankDirectory,R_path):
    print("categoryMainDirectory")
    print(categoryMainDirectory)
    '''if dataset_type =="amazon":
        salesRankDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    elif dataset_type=="yelp":
        salesRankDirectory ="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Resturants_Categories/"'''
    correlationFilePath = categoryMainDirectory+"correlation_"+lib+".txt"

    correlationFileHandle = open(correlationFilePath, 'w')
    correlationFileHandle.write("Kendal Tau")
    correlationFileHandle.write("\t")
    correlationFileHandle.write("Spearman Rho")
    correlationFileHandle.write("\n")

    corList = []
    lst = os.listdir(categoryMainDirectory)
    lst = natsorted(lst)


    for folder in lst:
        setFilePath = categoryMainDirectory + folder
        print("Processing "+str(folder))
        if os.path.isdir(setFilePath):
                cutoff = folder.split('_')
                cutoff = int(cutoff[1])
                destDirectory=setFilePath+"/"
                divideAllPredictionsFileIntoChunks(destDirectory,salesRankDirectory,orig_CatName,dataset_type)

                sortedSalesRankDirectory = destDirectory + "Sorted_Sales_Rank"
                try:
                    os.stat(sortedSalesRankDirectory)
                except:
                    os.mkdir(sortedSalesRankDirectory)

                sourceDirectory = destDirectory+"SalesRank/"
                sortedSalesRankDirectory+="/"
                sortRankedProductDirectory(sourceDirectory, sortedSalesRankDirectory,0)

                sortedPredictionDirectory = destDirectory + "Sorted_Predictions"
                try:
                    os.stat(sortedPredictionDirectory)
                except:
                    os.mkdir(sortedPredictionDirectory)

                sourceDirectory = destDirectory + "Predictions/"
                sortedPredictionDirectory += "/"
                sortRankedProductDirectory(sourceDirectory, sortedPredictionDirectory, 1)
                files = []
                for file in os.listdir(sourceDirectory):
                    #file = file.split(".")
                    files.append(file)
                rDirectory = destDirectory + "R_Difference"
                try:
                    os.stat(rDirectory)
                except:
                    os.mkdir(rDirectory)
                rDirectory += "/"
                for file in files:
                    path1 = sortedSalesRankDirectory+file
                    path2 = sortedPredictionDirectory+file
                    measureDistanceBetweenForCategory(path1, path2, file, rDirectory)


                destDirectory = destDirectory.replace('/', "//")
                destDirectory = destDirectory.replace('\\', "////")
                correlationFn = 1
                rScriptFilePath = writeCorrelationRScript(destDirectory, correlationFn)
                kendall = runKenallExtractScript(rScriptFilePath,R_path)
                correlationFn = 2
                rScriptFilePath = writeCorrelationRScript(destDirectory, correlationFn)
                spearman = runSpearmanExtractScript(rScriptFilePath,R_path)
                kendalAverage = 0
                spearmanAverage = 0
                writtenData = ""
                if len(kendall) == len(spearman) and len(spearman)!=0 and len(kendall)!=0:
                    for i in range(len(kendall)):
                        writtenData+=folder
                        correlationFileHandle.write(folder)
                        writtenData += "\t"
                        correlationFileHandle.write("\t")
                        writtenData += str(i+1)
                        correlationFileHandle.write(str(i+1))
                        writtenData += "\t"
                        correlationFileHandle.write("\t")
                        kendalAverage+=kendall[i]
                        writtenData += str(kendall[i])
                        correlationFileHandle.write(str(kendall[i]))
                        writtenData += "\t"
                        correlationFileHandle.write("\t")
                        spearmanAverage += spearman[i]
                        writtenData += str(spearman[i])
                        correlationFileHandle.write(str(spearman[i]))
                        writtenData += "\n"
                        correlationFileHandle.write("\n")
                writtenData += "Average\t"
                correlationFileHandle.write("Average ")
                writtenData += "\t"
                correlationFileHandle.write("\t")

                if len(kendall) >0:
                    writtenData += str(round(kendalAverage/len(kendall),3))
                    correlationFileHandle.write(str(round(kendalAverage/len(kendall),3)))
                    print("Average Kendall "+str(round(kendalAverage/len(kendall),3)))
                else:
                    writtenData += "0"
                    correlationFileHandle.write("0")
                writtenData += "\t"
                correlationFileHandle.write("\t")
                if len(kendall)>0:
                    writtenData += str(round(spearmanAverage / len(kendall), 3))
                    correlationFileHandle.write(str(round(spearmanAverage / len(kendall), 3)))
                else:
                    writtenData += "0"
                    correlationFileHandle.write("0")
                writtenData += "\n\n"
                correlationFileHandle.write("\n\n")
                corList.append(writtenData)
    #Here i will write every thing once time so that it be sorted
    '''print(corList)
    for cut in corList:
        correlationFileHandle.write(cut)
    '''
    #correlationFileHandle.close()
    return
def computeCategoryStatistics(categoryMainDirectory):
    for folder in os.listdir(categoryMainDirectory):
        setFilePath = categoryMainDirectory + folder
        if os.path.isdir(setFilePath):

            numSets = 0
            for folder1 in os.listdir(setFilePath):
                setFilePath1 = setFilePath + "/"+folder1
                if os.path.isdir(setFilePath1):
                    folderNames = folder1.split('_')
                    if "Set" in folderNames:
                        numSets+=1
                    if folder1 == "Set_1":
                        qidLastTest = ""
                        setFilePath2 = setFilePath1 + "/" + "test.txt"
                        with open(setFilePath2, 'r') as fp:
                            for line in fp:
                                row = line.split(" ")
                                qidLastTest = row[1]

                        qidLastTest = qidLastTest.split(':')
                        qidLastTest = qidLastTest[1]
                        qidLastTest = int(qidLastTest)
                        qidLastTest+=1
                        qidLastTrain = ""
                        setFilePath2 = setFilePath1 + "/" + "train.txt"
                        with open(setFilePath2, 'r') as fp:
                            for line in fp:
                                row = line.split(" ")
                                qidLastTrain = row[1]
                        qidLastTrain = qidLastTrain.split(':')
                        qidLastTrain = qidLastTrain[1]
                        qidLastTrain = int(qidLastTrain)
                        qidLastTrain+=1

            print(folder+" " +str(qidLastTrain-qidLastTest)+" " +str(qidLastTest)+" " +str(qidLastTrain)+" " +str(numSets))

    return

'''
#categoriesList = ["Industrial","Jewelry","Toys","Arts","Video Games","Computers","Software","Cell Phones","Electronics"]
#orig_catNames = ["Industrial & Scientific","Jewelry","Toys & Games","Arts, Crafts & Sewing","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
categoriesList = ["Toys"]
orig_catNames = ["Toys & Games"]
for i in range(len(categoriesList)):
#categoryName="Electronics"
    categoryName=categoriesList[i]
    orig_CatName = orig_catNames[i]
    categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
    #createSortedRankAndRunR(categoryMainDirectory,"Lamda_mart",categoryName,orig_CatName)

    categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
    #createSortedRankAndRunR(categoryMainDirectory,"SVM",categoryName)

    categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Light/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
    createSortedRankAndRunR(categoryMainDirectory,"SVM Light",categoryName,orig_CatName)


    #categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
    #computeCategoryStatistics(categoryMainDirectory)
#'''
#SVM Regression code
#"Industrial & Scientific","Arts, Crafts & Sewing","Computers & Accessories","Cell Phones & Accessories",
#categoriesList = ["Industrial","Jewelry","Toys","Arts","Video Games","Computers","Software","Cell Phones","Electronics"]
#orig_catNames = ["Industrial & Scientific","Jewelry","Toys & Games","Arts, Crafts & Sewing","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
categoriesList = ["Jewelry"]
orig_catNames = ["Jewelry"]
'''
for i in range(len(categoriesList)):
    categoryName=categoriesList[i]
    orig_CatName = orig_catNames[i]
    categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_mixed_lamda/"+categoryName+"/"
    createSortedRankAndRunR(categoryMainDirectory,"Lamda",categoryName,orig_CatName)

#'''
'''
from dirichlet_True_Rating import computeNDCG
destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2\TQ_correlation_as_L2R_Evaluation\Video Games\Cutoff_3\R_Difference/"
meanNDCG = 0
for i in range(1,11):
    meanNDCG+=computeNDCG(destDirectory,i)
meanNDCG= meanNDCG/10
print("meanNDCG "+str(meanNDCG))
'''
#computeNDCG(destDirectory,10)


'''
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
import numpy as np
X = []
y = []
predicitonsFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_mixed_lamda/Arts\Cutoff_10\Set_1/train.txt"
with open(predicitonsFile, 'r') as fp:
    for line in fp:
        row = line.split(" ")
        y.append(int(row[0]))
        x =[]
        for i in range(2,len(row)):
            feature = row[i].split(':')
            x.append(float(feature[1]))
        X.append(x)


y = np.asarray(y)
X = np.asarray(X)


# feature extraction
test = SelectKBest(score_func=chi2, k=4)
fit = test.fit(X, y)
# summarize scores
np.set_printoptions(precision=3)
print(fit.scores_)
features = fit.transform(X)
print("features")
print(features.shape)
print(type(features))
print(features[0])
'''