import os
from RankingHelper import *
from ranking import prepareKFoldForSVM
import shutil
from ranking import backAllPredictionsInOneFileStraight
print("will start Java SVM Rank ")
AllTrainingSets = []
AllTestingSets = []
AllTrainingSets, AllTestingSets = prepareKFoldForSVM()

def runSVMRankOnly(destCopyDirectory,c):
        print("Learning to Rank using SVM")
        os.chdir(destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/svm_rank_learn.exe', destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/svm_rank_classify.exe',destCopyDirectory)
        shutil.copy2('C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/mslr-eval-score-mslr.pl',destCopyDirectory)
        #Svm_Rank Example
        #Training
        command = "svm_rank_learn.exe -c "
        command+=str(20)
        command+=" train.txt model.dat"
        print(command)
        os.system(command)
        #Prediction
        command = "svm_rank_classify.exe test.txt model.dat predictions.txt"
        os.system(command)

        command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
        os.system(command)
        return
        '''

        predicitonsFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/Set_"+str(i+1)+"/predictions.txt"
        testFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/Set_"+str(i+1)+"/test.txt"
        categoriesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
        destDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/K_Fold/Set_"+str(i+1)+"/prediction/"
        try:
            os.stat(destDirectory)
        except:
            os.mkdir(destDirectory)

        transformPredictionsToComputed(AllTestingSets[i],categoriesDirectory,destDirectory,predicitonsFile)
        #'''
#'''
#cutoffs = [3, 5, 10, 20, 30, 40]
#cutoffs = [50,60,70,100,120,150]
#cutoffs = [160,180,200,220,250]
#cutoffs = [3, 5, 10, 20, 30, 40,50,60,70,100,120,150,160,180,200,220]
#cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220,250,280,300,350,400]
#cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220, 250, 280, 300, 350, 400,500,600]
#cutoffs = [280, 300, 350, 400,500,600]
cutoffs = [50,100,150,200,250,300,400]
#category = "Toys & Games", ""
categoryList = ["Cell Phones & Accessories", "Electronics"]
#'''
for category in categoryList:

        for i in range(len(cutoffs)):
                numSets = 0
                cutoff = "Cutoff_" + str(cutoffs[i])#str((i + 1) * 10)
                print("Preparing data for "+str(cutoff))
                directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/SVM_Light/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25/"+category+"/"+cutoff+"/"
                try:
                        os.stat(directory)
                except:
                        os.mkdir(directory)

                for folder in os.listdir(directory):
                    setFilePath = directory + folder
                    if os.path.isdir(setFilePath):
                        numSets+=1
                print("Num Sets "+str(numSets))
                for j in range(numSets):
                    print("Training Fold_" + str(j + 1))
                    destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/SVM_Light/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25/"+category+"/"+cutoff+"/Set_"+str(j+1)+"/"
                    runSVMRankOnly(destCopyDirectory,cutoffs[i])

                destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/SVM_Light/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25/"+category+"/"+cutoff+"/"
                backAllPredictionsInOneFileStraight(destCopyDirectory)
                predicitonsFile = destCopyDirectory+"AllPredictions.txt"
                categoriesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
                destDirectory = destCopyDirectory
                transformPredictionsToComputedPerCategory(category,categoriesDirectory, destDirectory, predicitonsFile)
#'''

print("done")