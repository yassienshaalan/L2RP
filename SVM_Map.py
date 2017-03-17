import os
from RankingHelper import *
from ranking import prepareKFoldForSVM
import shutil
from ranking import backAllPredictionsInOneFileStraight
print("will start Java SVM Map ")
AllTrainingSets = []
AllTestingSets = []
AllTrainingSets, AllTestingSets = prepareKFoldForSVM()

def runSVMRankOnly(destCopyDirectory):
        print("Learning to Rank using SVM Map")
        os.chdir(destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/svm-map-win/svm_map_learn.exe', destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/svm-map-win/svm_map_classify.exe',destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/mslr-eval-score-mslr.pl',destCopyDirectory)
        #Svm_Rank Example
        #Training
        command = "svm_map_learn.exe -c 0.1 train.txt model.dat"
        os.system(command)

        #Prediction
        command = "svm_map_classify.exe test.txt model.dat predictions.txt"
        os.system(command)

        command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
        os.system(command)
        return
#'''
#cutoffs = [3, 5, 10, 20, 30, 40]
#cutoffs = [50,60,70,100,120,150]
#cutoffs = [160,180,200,220,250]
#cutoffs = [3, 5, 10, 20, 30, 40,50,60,70,100,120,150,160,180,200,220]
#cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220,250,280,300,350,400]
cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220, 250, 280, 300, 350, 400,500,600]
category = "Arts, Crafts & Sewing"
'''
for i in range(len(cutoffs)):
        numSets = 0
        cutoff = "Cutoff_" + str(cutoffs[i])#str((i + 1) * 10)
        print("Preparing data for "+str(cutoff))
        directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Map/K_Fold_PerCategory_Basic/"+category+"/"+cutoff+"/"
        try:
                os.stat(directory)
        except:
                os.mkdir(directory)

        for folder in os.listdir(directory):
            setFilePath = directory + folder
            if os.path.isdir(setFilePath):
                numSets+=1
        print("Num Sets "+str(numSets))
        for i in range(numSets):
            print("Training Fold_" + str(i + 1))
            destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Map/K_Fold_PerCategory_Basic/"+category+"/"+cutoff+"/Set_"+str(i+1)+"/"
            runSVMRankOnly(destCopyDirectory)


        destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Map/K_Fold_PerCategory_Basic/"+category+"/"+cutoff+"/"
        backAllPredictionsInOneFileStraight(destCopyDirectory)
        predicitonsFile = destCopyDirectory+"AllPredictions.txt"
        categoriesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
        destDirectory = destCopyDirectory
        transformPredictionsToComputedPerCategory(category,categoriesDirectory, destDirectory, predicitonsFile)
#'''
destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Map/K_Fold_PerCategory_Basic/Arts, Crafts & Sewing\Cutoff_3\Set_1/"
runSVMRankOnly(destCopyDirectory)
print("done")