import os
from RankingHelper import transformPredictionsToComputedPerCategory
from ranking import prepareKFoldForSVM
import shutil
from ranking import backAllPredictionsInOneFileStraight
print("will start Java SVM Light Regression")

def runSVMRankOnly(destCopyDirectory,ce,gamma,useCGamma=0):
        print("Using SVM Light Regression")
        os.chdir(destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Learning_Libraries/svm_light_windows64/svm_learn.exe', destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Learning_Libraries/svm_light_windows64/svm_classify.exe',destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/mslr-eval-score-mslr.pl',destCopyDirectory)
        #Svm_Rank Example
        #Training
        command = "svm_learn.exe -z r "
        if useCGamma == 1:
            command += "-c "
            command+=str(ce)
            command+=" -g "
            command+=str(gamma)

        command+=" train.txt model.dat"
        os.system(command)

        #Prediction
        command = "svm_classify.exe test.txt model.dat predictions.txt"
        os.system(command)

        command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
        os.system(command)
        return

c = [2**-5,2**-3,2**1,2**2,2**3,2**5]
gamma = [2**-15,2**-10,2**-5,2**1,2**2,2**3]
#categoriesList = ["Jewelry","Toys & Games","Arts, Crafts & Sewing","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
categoriesList = ["Mexican", "Cafes", "Chinese", "Thai", "American (Traditional)", "Italian", "American (New)", "Japanese", "Bars"]
#categoriesList = ["Industrial & Scientific"]
for category in categoriesList:
#category = "Industrial & Scientific"
#for i in range(6):
    numSets = 0
    #category+="_"+str((i+1))
    #print(category+"_"+str((i+1)))
    directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Regression\K_Fold_PerCategory_Basic__With_TQ_Target_25/" + category + "/"
    for folder in os.listdir(directory):
        setFilePath = directory + folder
        if os.path.isdir(setFilePath):
            numSets+=1
    print("Num Sets "+str(numSets))
    for j in range(numSets):
        print("Training Fold_" + str(j + 1))
        destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Regression\K_Fold_PerCategory_Basic__With_TQ_Target_25/"+ category +"/Set_"+str(j+1)+"/"
        runSVMRankOnly(destCopyDirectory,c[0],gamma[0],0)


    destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Regression\K_Fold_PerCategory_Basic__With_TQ_Target_25/"+ category + "/"
    backAllPredictionsInOneFileStraight(destCopyDirectory)
    predicitonsFile = destCopyDirectory+"AllPredictions.txt"
    categoriesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    destDirectory = destCopyDirectory
    transformPredictionsToComputedPerCategory(category,categoriesDirectory, destDirectory, predicitonsFile)
    #'''

print("done")