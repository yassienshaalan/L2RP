from RankingHelper import *
import os
import shutil
from ranking import prepareKFoldForLamdaMart
from ranking import prepareKFoldForSVM
from ranking import backAllPredictionsInOneFileStraight
def runLamdamartLearning(lamda_directory,destCopyDirectory,testing):

    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/jforests-0.5.jar',
        destCopyDirectory)
    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/ranking.properties',
        destCopyDirectory)
    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/mslr-eval-score-mslr.pl',
        destCopyDirectory)

    os.chdir(destCopyDirectory)

    command = "java -jar jforests-0.5.jar --cmd=generate-bin --ranking --folder . --file train.txt --file valid.txt --file test.txt"
    os.system(command)

    command = "java -jar jforests-0.5.jar --cmd=train --ranking --config-file ranking.properties --train-file train.bin --validation-file valid.bin --output-model ensemble.txt"
    os.system(command)

    command = "java -jar jforests-0.5.jar --cmd=predict --ranking --model-file ensemble.txt --tree-type RegressionTree --test-file test.bin --output-file predictions.txt"
    os.system(command)

    command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
    os.system(command)

    predicitonsFile = destCopyDirectory+"predictions.txt"
    testFile = destCopyDirectory+"test.txt"
    categoriesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    destDirectory = destCopyDirectory+"prediction/"



    try:
        os.stat(destDirectory)
    except:
        os.mkdir(destDirectory)

    transformPredictionsToComputed(testing, categoriesDirectory, destDirectory, predicitonsFile)
    return
def runLamdamartLearningOnly(lamda_directory,destCopyDirectory,justTesting):
    if justTesting != 1:

        shutil.copy2(
            lamda_directory+'jforests-0.5.jar',
            destCopyDirectory)
        shutil.copy2(
            lamda_directory+'ranking.properties',
            destCopyDirectory)
        shutil.copy2(
            lamda_directory+'mslr-eval-score-mslr.pl',
            destCopyDirectory)

        os.chdir(destCopyDirectory)



        command = "java -jar jforests-0.5.jar --cmd=generate-bin --ranking --folder . --file train.txt --file valid.txt --file test.txt"
        os.system(command)

        command = "java -jar jforests-0.5.jar --cmd=train --ranking --config-file ranking.properties --train-file train.bin --validation-file valid.bin --output-model ensemble.txt"
        os.system(command)

    os.chdir(destCopyDirectory)

    command = "java -jar jforests-0.5.jar --cmd=predict --ranking --model-file ensemble.txt --tree-type RegressionTree --test-file test.bin --output-file predictions.txt"
    os.system(command)

    command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
    os.system(command)

    return


def runSVMRankOnly(destCopyDirectory, c):
    print("Learning to Rank using SVM")
    os.chdir(destCopyDirectory)
    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/svm_rank_learn.exe',
        destCopyDirectory)
    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/svm_rank_classify.exe',
        destCopyDirectory)
    shutil.copy2(
        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/mslr-eval-score-mslr.pl',
        destCopyDirectory)
    # Svm_Rank Example
    # Training
    command = "svm_rank_learn.exe -c "
    command += str(20)
    command += " train.txt model.dat"
    print(command)
    os.system(command)
    # Prediction
    command = "svm_rank_classify.exe test.txt model.dat predictions.txt"
    os.system(command)

    command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
    os.system(command)
    return


def runSVMRankOnly(learning_lib_directory,destCopyDirectory, ce, gamma, useCGamma=0):
    print("Using SVM Light Regression")
    os.chdir(destCopyDirectory)
    shutil.copy2(
        learning_lib_directory+'svm_learn.exe',
        destCopyDirectory)
    shutil.copy2(
        learning_lib_directory+'svm_classify.exe',
        destCopyDirectory)
    shutil.copy2(
        learning_lib_directory+'mslr-eval-score-mslr.pl',
        destCopyDirectory)
    # Svm_Rank Example
    # Training
    command = "svm_learn.exe -z r "
    if useCGamma == 1:
        command += "-c "
        command += str(ce)
        command += " -g "
        command += str(gamma)

    command += " train.txt model.dat"
    os.system(command)

    # Prediction
    command = "svm_classify.exe test.txt model.dat predictions.txt"
    os.system(command)

    command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
    os.system(command)
    return

print("will start Lamdamart Learning to Rank")
#'''
AllTrainingSets = []
AllTestingSets = []
#AllTrainingSets, AllValidating, AllTestingSets = prepareKFoldForLamdaMart()

'''#AllTrainingSets, AllTestingSets = prepareKFoldForSVM()
for i in range(5):
    print("Training Fold_" + str(i + 1))
    destCopyDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold/Set_" + str(i + 1) + "/"
    runLamdamartLearning(destCopyDirectory,AllTestingSets[i])
'''
#AllTrainingSets.append(['Appliances', 'Arts, Crafts & Sewing', 'Camera &amp; Photo', 'Electronics', 'Home Improvement', 'Jewelry', 'Office Products', 'Watches'])
#AllTestingSets.append(['Appliances', 'Arts, Crafts & Sewing', 'Camera &amp; Photo', 'Electronics', 'Home Improvement', 'Jewelry', 'Office Products', 'Watches'])
#runLamdamartLearning(destCopyDirectory,AllTestingSets[0])
#'''


#'''
#cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220, 250, 280, 300, 350, 400,500,600]
from RankingHelper import createSortedRankAndRunR
cutoffs = [10]

def runLamadaMart_All_Categories_Old_Experiment_Setup(categoryList,base_learning_directory,learning_lib_directory,exp_type):

    for category in categoryList:
        for i in range(len(cutoffs)):
            cutoff = "Cutoff_" + str(cutoffs[i])  # str((i + 1) * 10)
            # cutoff = str(cutoffs[i])
            print("Preparing data for " + str(cutoff))
            numSets = 0
            directory = destCopyDirectory = base_learning_directory + category + "/" + cutoff + "/"
            for folder in os.listdir(directory):
                setFilePath = directory + folder
                if os.path.isdir(setFilePath):
                    numSets += 1
            print("numSets " + str(numSets))
            for i in range(numSets):
                destCopyDirectory = base_learning_directory + category + "/" + cutoff + "/" + "Set_" + str(i + 1) + "/"
                if exp_type == "svm":
                    runSVMRankOnly(learning_lib_directory, destCopyDirectory, 20, 0, 0)
                elif exp_type == "lamda":
                    runLamdamartLearningOnly(learning_lib_directory, destCopyDirectory, 0)
                elif exp_type == "regression":
                    runSVMRankOnly(destCopyDirectory, 0, 0, 0)

            destCopyDirectory = base_learning_directory + category + "/" + cutoff + "/"
            backAllPredictionsInOneFileStraight(destCopyDirectory)
            predicitonsFile = destCopyDirectory + "AllPredictions.txt"
            destDirectory = destCopyDirectory
            transformPredictionsToComputedPerCategory(category, categoriesDirectory, destDirectory, predicitonsFile)
    return
def runLamadaMart_All_Categories_New_Experiment_Setup(base_learning_directory,learning_lib_directory,exp_type):
    for category in categoryList:
        print("Processing "+category)
        for i in range(len(cutoffs)):
            cutoff = "Cutoff_" + str(cutoffs[i])
            try:
                os.stat(base_learning_directory + category + "/")
            except:
                os.mkdir(base_learning_directory + category + "/")
            destCopyDirectory = base_learning_directory + category + "/" + cutoff + "/"
            try:
                os.stat(destCopyDirectory)
            except:
                os.mkdir(destCopyDirectory)
            if exp_type == "svm":
                runSVMRankOnly(learning_lib_directory, destCopyDirectory, 20, 0, 0)
            elif exp_type == "lamda":
                runLamdamartLearningOnly(learning_lib_directory, destCopyDirectory, 0)
            elif exp_type == "regression":
                runSVMRankOnly(destCopyDirectory, 0, 0, 0)

    return
def compute_Kendall_Old_Experiment_Setup(categoriesList,orig_catNames,base_learning_directory,dataset_type,rename):
    for i in range(len(categoriesList)):

        categoryName = categoriesList[i]
        orig_CatName = orig_catNames[i]

        original_directory = base_learning_directory + orig_CatName + "/"
        new_directory = base_learning_directory + categoryName + "/"
        if dataset_type == "amazon" and rename == 1:
            print("Will Rename folder")
            os.chmod(original_directory, 0o777)
            os.rename(original_directory, new_directory)
            print("Renamed the folder")
        categoryMainDirectory = base_learning_directory + categoryName + "/"
        salesRankDirectory = "f:\Yassien_PhD\Experiment_4\categories_sales_rank/"
        R_path = "C:\Program Files\R\R-3.2.2/bin/Rscript.exe"  # RMIT
        # R_path ="C:\Program Files\R\R-3.3.2/bin/Rscript.exe" #Laptop
        createSortedRankAndRunR(categoryMainDirectory, "Lamda", categoryName, orig_CatName, dataset_type,salesRankDirectory, R_path)
        if dataset_type == "amazon" and rename == 1:
            os.chmod(new_directory, 0o777)
            os.rename(new_directory, original_directory)
        print("Returned the folder back to original name")
    return
from Data_Preparation_For_Learning import  compute_Kendall_New_Experiment_Setup
#*******************************Yelp Dataset
#categoryList = ["Mexican", "Cafes", "Chinese", "Thai", "American (Traditional)", "Italian", "American (New)", "Japanese", "Bars"]
#base_learning_directory ="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\AVG_Predictions/"
#categoriesDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Resturants_Categories/"
#*******************************Amazon Dataset
#Prepare the data for the new experiemnt setup
drive = "f:/"

from Data_Preparation_For_Learning import Prepare_Training_Testing_Data_New_Experiment_Setup
Prepare_Training_Testing_Data_New_Experiment_Setup(5,drive)
###########

categoryList = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
base_learning_directory = drive+"Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target/" #"f:\Yassien_PhD\Experiment_4\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_samp/"
categoriesDirectory = drive+"Yassien_PhD\Experiment_4\categories_sales_rank/"
learning_lib_directory =drive+"Yassien_PhD\Experiment 2\Lamda_Java/"#"Yassien_PhD\Experiment 2\SVM_Light\svm_light_windows64/"
exp_type ="lamda"
#'''
#runLamadaMart_All_Categories_Old_Experiment_Setup(categoryList,base_learning_directory,learning_lib_directory,exp_type)
runLamadaMart_All_Categories_New_Experiment_Setup(base_learning_directory,learning_lib_directory,exp_type)
#'''


#'''
#*******************************Yelp Dataset
#categoriesList = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
#orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
#*******************************Amazon Dataset
categories_sales_rank=drive+"Yassien_PhD\Experiment_5\Categories_Ranked_by_Sales_Rank/"
categories_with_testing_indices=drive+"Yassien_PhD\Experiment_5\Categories/"
categoriesList = ["Arts","Industrial", "Jewelry", "Toys", "Computers", "Video Games", "Electronics","Software", "Cell Phones"]
orig_catNames  = ["Arts, Crafts & Sewing","Industrial & Scientific", "Jewelry",  "Toys & Games","Computers & Accessories", "Video Games", "Electronics", "Software", "Cell Phones & Accessories"]
dataset_type="amazon"
rename=1
#query_size = 100
R_path = "C:\Program Files\R\R-3.2.2/bin/Rscript.exe"  # RMIT
#R_path ="C:\Program Files\R\R-3.3.2/bin/Rscript.exe" #Laptop
#compute_Kendall_Old_Experiment_Setup(categoriesList,orig_catNames,base_learning_directory,dataset_type,rename)
compute_Kendall_New_Experiment_Setup(base_learning_directory,categories_sales_rank,categories_with_testing_indices,"LamdaMart",R_path)
#'''
print("done")

