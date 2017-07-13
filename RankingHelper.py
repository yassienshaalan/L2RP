import os
from alogrithms import mergeSort
from dirichlet_True_Rating import measureDistanceBetweenForCategory
import subprocess
from Testing import writeCorrelationRScript
from Testing import runSpearmanExtractScript
from Testing import  runKenallExtractScript
import numpy as np
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
def transformPredictionsToComputedPerCategory_New_Setup(categoryName,categoriesDirectory, destDirectory,predicitonsFile):
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
def Copy_Rank_From_One_Set_To_Other(source_directory,old_directory,dest_directory):
    categories =["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories","Electronics"]
    for category in categories:
        source_cat_path = source_directory+category+".txt"
        ranks = []
        print("Processing "+category)
        with open(source_cat_path, 'r') as fp:
            for line in fp:
                row = line.split(" ")
                ranks.append(row[0])
        print(ranks)
        source_cat_path = old_directory + category + ".txt"
        new_file_path = dest_directory+category+".txt"
        print(new_file_path)
        filehandle = open(new_file_path,'w')
        index = 0
        print("Writing new file")
        with open(source_cat_path, 'r') as fp:
            for line in fp:
                row = line.split(" ")
                filehandle.write(str(ranks[index])+" ")
                for i in range(1,len(row)):
                    if i <len(row)-1:
                        filehandle.write(str(row[i])+" ")
                    else:
                        filehandle.write(str(row[i]))

                index+=1
        filehandle.close()


    return


def Extract_Products_Sub_Categories():
    meta_dat_file_path = "D:/Yassien_PhD/metadata.json/metadata.json"
    import json
    orig_catNames = ["Arts, Crafts & Sewing", "Industrial & Scientific", "Jewelry", "Toys & Games",
                     "Computers & Accessories", "Video Games",
                     "Electronics", "Software", "Cell Phones & Accessories"]
    arts_dict = dict()
    indust_dict = dict()
    jewlery_dict = dict()
    toys_dict = dict()
    computer_dict = dict()
    video_dict = dict()
    electronic_dict = dict()
    software_dict = dict()
    cell_dict = dict()
    num_products = 0
    with open(meta_dat_file_path, 'r') as fp:
        for line in fp:
            # print(line)
            line = line.replace("'", '"')
            # print(line)
            try:
                decoded = json.loads(line)
                try:
                    # print(str(decoded['asin']))
                    cats = str(decoded['categories']).split(",")
                    new_cats = []
                    for cat in cats:
                        # print(cat)
                        cat = cat.replace("[", '')
                        cat = cat.replace("]", '')
                        new_cats.append(cat)
                    cats = new_cats
                    num_products += 1
                    print(num_products)
                    # print(cats)
                    # print(cats[0])
                    if any("Arts" in s for s in cats):
                        print("Found Art")
                        arts_dict[decoded['asin']] = cats
                    if any("Industrial" in s for s in cats):
                        print("Found Industrial")
                        indust_dict[decoded['asin']] = cats
                    if any("Jewelry" in s for s in cats):
                        print("Found Jewelry")
                        jewlery_dict[decoded['asin']] = cats
                    if any("Toys" in s for s in cats):
                        print("Found Toys")
                        toys_dict[decoded['asin']] = cats
                    if any("Computers" in s for s in cats):
                        print("Found Computers")
                        computer_dict[decoded['asin']] = cats
                    if any("Video" in s for s in cats):
                        print("Found Video")
                        video_dict[decoded['asin']] = cats
                    if any("Electronics" in s for s in cats):
                        print("Found Electronics")
                        electronic_dict[decoded['asin']] = cats
                    if any("Software" in s for s in cats):
                        print("Found Sotware")
                        software_dict[decoded['asin']] = cats
                    if any("Cell Phones" in s for s in cats):
                        print("Found Cell")
                        cell_dict[decoded['asin']] = cats
                        # print(str(decoded['asin'])+" "+str(decoded['categories']))
                except KeyError:
                    pass
            except json.decoder.JSONDecodeError:
                # print("Error with "+line)
                pass

    print("Finished Reading the file now will write each file ")
    base_directory = "D:\Yassien_PhD\Product_categories_with_sub_categories/"
    print("Writing Arts, Crafts & Sewing of size " + str(len(arts_dict)))
    filepath = base_directory + "Arts, Crafts & Sewing.txt"
    filehandle = open(filepath, 'w')
    for key, value in arts_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Industrial & Scientific of size " + str(len(indust_dict)))
    filepath = base_directory + "Industrial & Scientific.txt"
    filehandle = open(filepath, 'w')
    for key, value in indust_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Jewelry of size " + str(len(jewlery_dict)))
    filepath = base_directory + "Jewelry.txt"
    filehandle = open(filepath, 'w')
    for key, value in jewlery_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Toys & Games of size " + str(len(toys_dict)))
    filepath = base_directory + "Toys & Games.txt"
    filehandle = open(filepath, 'w')
    for key, value in toys_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Computers & Accessories of size " + str(len(computer_dict)))
    filepath = base_directory + "Computers & Accessories.txt"
    filehandle = open(filepath, 'w')
    for key, value in computer_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Video Games of size " + str(len(video_dict)))
    filepath = base_directory + "Video Games.txt"
    filehandle = open(filepath, 'w')
    for key, value in video_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Electronics of size " + str(len(electronic_dict)))
    filepath = base_directory + "Electronics.txt"
    filehandle = open(filepath, 'w')
    for key, value in electronic_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Software of size " + str(len(software_dict)))
    filepath = base_directory + "Software.txt"
    filehandle = open(filepath, 'w')
    for key, value in software_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Cell Phones & Accessories of size " + str(len(cell_dict)))
    filepath = base_directory + "Cell Phones & Accessories.txt"
    filehandle = open(filepath, 'w')
    for key, value in cell_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    return

def Extract_Products_Sub_Categories_Yelp():
    meta_dat_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
    import json
    orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    cafes_dict = dict()
    chinese_dict = dict()
    mexican_dict = dict()
    italian_dict = dict()
    american_trad_dict = dict()
    thai_dict = dict()
    bars_dict = dict()
    japansese_dict = dict()
    american_new_dict = dict()
    num_products = 0
    with open(meta_dat_file_path, 'r') as fp:
        for line in fp:
            # print(line)
            line = line.replace("'", '"')
            # print(line)
            try:
                decoded = json.loads(line)
                try:
                    #print(decoded['business_id'])
                    # print(str(decoded['asin']))
                    cats = str(decoded['categories']).split(",")
                    new_cats = []
                    for cat in cats:
                        # print(cat)
                        cat = cat.replace("[", '')
                        cat = cat.replace("]", '')
                        new_cats.append(cat)
                    cats = new_cats
                    num_products += 1
                    print(num_products)
                    # print(cats)
                    # print(cats[0]) "", "", "", ""]
                    if any("Cafes" in s for s in cats):
                        print("Found Cafes")
                        cafes_dict[decoded['business_id']] = cats
                    if any("Chinese" in s for s in cats):
                        print("Found Chinese")
                        chinese_dict[decoded['business_id']] = cats
                    if any("Mexican" in s for s in cats):
                        print("Found Mexican")
                        mexican_dict[decoded['business_id']] = cats
                    if any("Italian" in s for s in cats):
                        print("Found Italian")
                        italian_dict[decoded['business_id']] = cats
                    if any("American (Traditional)" in s for s in cats):
                        print("Found American (Traditional)")
                        american_trad_dict[decoded['business_id']] = cats
                    if any("Thai" in s for s in cats):
                        print("Found Thai")
                        thai_dict[decoded['business_id']] = cats
                    if any("Bars" in s for s in cats):
                        print("Found Bars")
                        bars_dict[decoded['business_id']] = cats
                    if any("Japanese" in s for s in cats):
                        print("Found Japanese")
                        japansese_dict[decoded['business_id']] = cats
                    if any("American (New)" in s for s in cats):
                        print("Found American (New)")
                        american_new_dict[decoded['business_id']] = cats
                        # print(str(decoded['asin'])+" "+str(decoded['categories']))
                except KeyError:
                    pass
            except json.decoder.JSONDecodeError:
                # print("Error with "+line)
                pass

    print("Finished Reading the file now will write each file ")
    #'''
    base_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Product_categories_with_sub_categories/"
    print("Writing Cafes of size " + str(len(cafes_dict)))
    filepath = base_directory + "Cafes.txt"
    filehandle = open(filepath, 'w')
    for key, value in cafes_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Chinese of size " + str(len(chinese_dict)))
    filepath = base_directory + "Chinese.txt"
    filehandle = open(filepath, 'w')
    for key, value in chinese_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    print("Writing Mexican of size " + str(len(mexican_dict)))
    filepath = base_directory + "Mexican.txt"
    filehandle = open(filepath, 'w')
    for key, value in mexican_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Italian of size " + str(len(italian_dict)))
    filepath = base_directory + "Italian.txt"
    filehandle = open(filepath, 'w')
    for key, value in   italian_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing American (Traditional) of size " + str(len(american_trad_dict)))
    filepath = base_directory + "American (Traditional).txt"
    filehandle = open(filepath, 'w')
    for key, value in american_trad_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Thai of size " + str(len(thai_dict)))
    filepath = base_directory + "Thai.txt"
    filehandle = open(filepath, 'w')
    for key, value in thai_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Bars of size " + str(len(bars_dict)))
    filepath = base_directory + "Bars.txt"
    filehandle = open(filepath, 'w')
    for key, value in bars_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing Japanese of size " + str(len(japansese_dict)))
    filepath = base_directory + "Japanese.txt"
    filehandle = open(filepath, 'w')
    for key, value in japansese_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()

    print("Writing American (New) of size " + str(len(american_new_dict)))
    filepath = base_directory + "American (New).txt"
    filehandle = open(filepath, 'w')
    for key, value in american_new_dict.items():
        filehandle.write(key + "\t")
        for cat in value:
            filehandle.write(cat + "\t")
        filehandle.write("\n")
    filehandle.close()
    #'''
    return

def Filter_Product_Sub_Categories_With_Current():
    orig_catNames = ["Arts, Crafts & Sewing", "Industrial & Scientific", "Jewelry", "Toys & Games",
                     "Computers & Accessories", "Video Games",
                     "Electronics", "Software", "Cell Phones & Accessories"]
    all_subcategories_base_directory = "D:\Yassien_PhD\Product_categories_with_sub_categories/"
    our_currrent_categories_base_directory = "D:/Yassien_PhD\categories/"
    new_filtered_sub_cats = "D:/Yassien_PhD\Product_categories_with_sub_categories_filtered/"
    for category in orig_catNames:
        print("Considering "+category)
        file_path = our_currrent_categories_base_directory+category+".txt"
        products_dict = dict()
        with open(file_path, 'r') as fp:
            for line in fp:
                products_dict[line.split('\t')[0]]=1
        file_path = all_subcategories_base_directory + category + ".txt"
        file_to_write = new_filtered_sub_cats+category+".txt"
        filehandle= open(file_to_write,'w')
        with open(file_path, 'r') as fp:
            for line in fp:
                try:
                    products_dict[line.split('\t')[0]]
                    filehandle.write(line)
                except:
                    pass
        filehandle.close()

    return

def Filter_Product_Sub_Categories_With_Current_Yelp():
    orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    all_subcategories_base_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Product_categories_with_sub_categories/"
    our_currrent_categories_base_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Resturants_Categories/"
    new_filtered_sub_cats = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Product_categories_with_sub_categories_filtered/"
    for category in orig_catNames:
        print("Considering "+category)
        file_path = our_currrent_categories_base_directory+category+".txt"
        products_dict = dict()
        with open(file_path, 'r') as fp:
            for line in fp:
                products_dict[line.split('\t')[0]]=1
        file_path = all_subcategories_base_directory + category + ".txt"
        file_to_write = new_filtered_sub_cats+category+".txt"
        filehandle= open(file_to_write,'w')
        with open(file_path, 'r') as fp:
            for line in fp:
                try:
                    products_dict[line.split('\t')[0]]
                    filehandle.write(line)
                except:
                    pass
        filehandle.close()

    return
def Count_Sub_Categories():
    orig_catNames = ["Arts, Crafts & Sewing", "Industrial & Scientific", "Jewelry", "Toys & Games",
                     "Computers & Accessories", "Video Games",
                     "Electronics", "Software", "Cell Phones & Accessories"]
    all_subcategories_base_directory = "D:/Yassien_PhD\Product_categories_with_sub_categories_filtered/"
    for category in orig_catNames:
        file_path = all_subcategories_base_directory+category+".txt"
        sub_cats_dict = dict()
        with open(file_path, 'r') as fp:
            for line in fp:
                subs = line.split('\t')
                for i in range(1,len(subs)):
                    try:
                        sub_cats_dict[subs[i]]
                    except KeyError:
                        sub_cats_dict[subs[i]]=1

        print("Category "+category)
        print("Num sub categores "+str(len(sub_cats_dict)))
        for key,value in sub_cats_dict.items():
            print(key)
        print("**********************************************************************************************")

    return
def Determine_Sub_Categories_For_Product_List(product_file_path,filtered_subs_directory_path,category_name):
    print("Considering "+category_name)
    product_list = []
    with open(product_file_path, 'r') as fp:
        for line in fp:
            product_list.append(line.split('\t')[0])

    print("Total num products "+str(len(product_list)))
    num_found = 0
    with open(filtered_subs_directory_path, 'r') as fp:
        for line in fp:
            productid = line.split('\t')[0]
            if productid in product_list:
                num_found+=1
    print("Num found "+str(num_found))
    print("**********************************************************************************************************")
    return
def Create_Queries_For_Product_Category(filtered_cat_path,new_cat_directory,category_name):
    print ("This procedure creates queries for each sub category and collect all products within this category")
    #First run is to determine all sub categories
    print("Considering "+category_name)
    sub_cats_dict = dict()
    print("Determining All sub categories")
    with open(filtered_cat_path, 'r') as fp:
        for line in fp:
            subs = line.split('\t')
            for i in range(1, len(subs)):
                subs[i] = subs[i].replace("'", '')
                subs[i] = subs[i].lstrip()
                try:
                    sub_cats_dict[subs[i]]
                except KeyError:
                    sub_cats_dict[subs[i]] = new_cat_directory+"/"+subs[i]+".txt"

    print("Collecting products for each subcategory")
    #Now we will put each product in the designated query
    with open(filtered_cat_path, 'r') as fp:
        for line in fp:
            subs = line.split('\t')
            productid = subs[0]
            for i in range(1, len(subs)):
                subs[i] = subs[i].replace("'", '')
                subs[i] = subs[i].lstrip()
                file_path = sub_cats_dict[subs[i]]
                try:
                    filehandle = open(file_path,'a')
                    filehandle.write(productid+"\n")
                    filehandle.close()
                except FileNotFoundError:
                    print("File Not found: "+file_path)
                    pass
    print("Finished writing queries ")
    print("***********************************************************************************************************")

    return
def Count_Queries_With_Given_Num_Products(category_folder,desired_num_products):

    total_num_queries = 0
    num_queries_desired = 0
    max_num_products=-100
    max_num_prod_query = ""
    for file in os.listdir(category_folder):
        num_products = 0
        query_file_path = category_folder+file
        with open(query_file_path, 'r') as fp:
            for line in fp:
                num_products+=1
        if num_products>max_num_products:
            max_num_products = num_products
            max_num_prod_query = query_file_path
        if num_products>=desired_num_products:
            num_queries_desired+=1

        total_num_queries+=1
    #print("Total # Queries is "+str(total_num_queries))
    print("#Queries with num products "+str(desired_num_products)+" is "+str(num_queries_desired))
    #print("**************************************************************************************")
    #print(str(num_queries_desired))
    #print("max_num_products "+str(max_num_products)+" "+max_num_prod_query)
    return
import shutil
def Collect_Queries_With_Given_Num_Products(category_folder,desired_num_products,dest_directory):

    total_num_queries = 0
    num_queries_desired = 0
    for file in os.listdir(category_folder):
        num_products = 0
        query_file_path = category_folder+file
        with open(query_file_path, 'r') as fp:
            for line in fp:
                num_products+=1
        if num_products>=desired_num_products:
            shutil.copy2(query_file_path,dest_directory)
            num_queries_desired+=1

        total_num_queries+=1
    #print("Total # Queries is "+str(total_num_queries))
    print("#Queries with num products "+str(desired_num_products)+" is "+str(num_queries_desired))
    print("**************************************************************************************")
    #print(str(num_queries_desired))
    return
def Create_All_Queries_For_Categories_Based_on_Subs():

    orig_catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
    base_filtered_category = "D:\Yassien_PhD\Product_categories_with_sub_categories_filtered/"
    base_destenation_directory = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category/"
    for cat in orig_catNames:
        filtered_cat_path = base_filtered_category+cat+".txt"
        new_cat_directory = base_destenation_directory+cat
        try:
            os.stat(new_cat_directory)
        except:
            os.mkdir(new_cat_directory)

        Create_Queries_For_Product_Category(filtered_cat_path,new_cat_directory,cat)
    return
def Create_All_Queries_For_Categories_Based_on_Subs_Yelp():

    orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    base_filtered_category = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Product_categories_with_sub_categories_filtered/"
    base_destenation_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Queries_Per_Product_Category/"
    for cat in orig_catNames:
        filtered_cat_path = base_filtered_category+cat+".txt"
        new_cat_directory = base_destenation_directory+cat
        try:
            os.stat(new_cat_directory)
        except:
            os.mkdir(new_cat_directory)

        Create_Queries_For_Product_Category(filtered_cat_path,new_cat_directory,cat)
    return

def Create_All_Products_Indices_Yelp():
    orig_catNames = ["Cafes", "Chinese", "Mexican", "Italian", "American (Traditional)", "Thai", "Bars", "Japanese",
                     "American (New)"]

    main_all_indices_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\All_Products_Per_Cat_Indices/"
    tq_rank_dest_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Ranked_by_TQ_Rank/"
    sales_rank_dest_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Ranked_by_Sales_Rank/"

    for category in orig_catNames:
        print("Considering "+category)
        cat_sales_rank_path = sales_rank_dest_main_dirc+category+".txt"
        cat_tq_rank_path=tq_rank_dest_main_dirc+category+".txt"
        all_indices_path=main_all_indices_dirc+category+".txt"
        Create_All_Products_Indices_Per_Category(cat_sales_rank_path, cat_tq_rank_path, all_indices_path)
    return
def Create_All_Products_Indices_Per_Category(cat_sales_rank_path,cat_tq_rank_path,all_indices_path):

    index=0
    product_dict=dict()
    sales_rank_dict = dict()
    tq_rank_dict = dict()
    with open(cat_sales_rank_path, 'r') as fp:
        for line in fp:
            row=line.split('\t')
            productid = row[0]
            sales_rank = row[1].split("\n")[0]
            product_dict[productid]=index
            sales_rank_dict[productid]=sales_rank
            index+=1
    #print(sales_rank_dict)
    with open(cat_tq_rank_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            productid = row[0]
            tq_rank = row[1].split("\n")[0]
            tq_rank_dict[productid] = tq_rank
    #print(tq_rank_dict)
    #print("********************************")
    filehandle=open(all_indices_path,'w')
    filehandle.write("ProductId\tIndex\tSales_Rank\tTQ_Rank\n")
    for key,value in product_dict.items():
        filehandle.write(key+"\t"+str(value)+"\t"+str(sales_rank_dict[key])+"\t"+str(tq_rank_dict[key])+"\n")
    filehandle.close()

    return

def Create_Coded_Queries_Repository(cat_query_directory,base_dest,coded_query_map_path,categoryname,start_from,filehandle):

    for file in os.listdir(cat_query_directory):
        sub_cat_file_name = file.split('.')[0]
        file_path = cat_query_directory+file
        query_name = str(start_from)#"qid_"+str(start_from)
        query_file_name = query_name+".txt"
        query_file_path = base_dest+query_file_name
        shutil.copy2(file_path, query_file_path)
        filehandle.write(query_name+"\t"+categoryname+"\t"+sub_cat_file_name+"\n")
        start_from+=1
    #filehandle.close()
    return start_from


def Check_Product_Duplicates_In_Sub_Cat():
    base_sub_cats_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/"
    new_base_sub_cats_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_new/"
    query_map_file_path = base_sub_cats_dirc+"query_code_map.txt"
    ignore_first = 0
    with open(query_map_file_path, 'r') as filep:
        for item in filep:
            if ignore_first == 0:
                ignore_first=1
                continue
            line = item.split('\t')
            qid = line[0]
            category = line[1]
            sub_category = line[2].split('\n')[0]
            sub_cat_file_path = base_sub_cats_dirc+category+"/"+sub_category+".txt"
            products_per_sub_cat = dict()
            num_duplicates=0
            print(sub_cat_file_path)
            with open(sub_cat_file_path, 'r') as filep:
                for item in filep:
                    line = item.split('\n')
                    try:
                        products_per_sub_cat[line[0]]
                        print(line[0] + " duplicate in " + category+" "+sub_category)
                        num_duplicates+=1
                    except KeyError:
                        products_per_sub_cat[line[0]]=1
            '''if num_duplicates>0:
                filhandle = open(sub_cat_file_path,'w')
                for key,value in products_per_sub_cat.items():
                    filhandle.write(key+"\n")
                filhandle.close()'''
            print("Num Dups per query "+str(num_duplicates))
            print("***************************************************************************************************")

    return

def Check_Product_Duplicates_In_Sub_Cat_Codes():
    base_sub_cats_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    new_base_cat_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded_new/"
    base_sub_cats_dirc = new_base_cat_dirc
    for file_name in os.listdir(base_sub_cats_dirc):
        query_file_path = base_sub_cats_dirc+file_name
        num_duplicates = 0
        products_per_sub_cat = dict()
        with open(query_file_path, 'r') as filep:
            for item in filep:
                line = item.split('\n')
                try:
                    products_per_sub_cat[line[0]]
                    print(line[0] + " duplicate in " + file_name)
                    num_duplicates+=1
                except KeyError:
                    products_per_sub_cat[line[0]]=1

        '''new_file_path = new_base_cat_dirc+file_name
        filhandle = open(new_file_path,'w')
        for key,value in products_per_sub_cat.items():
            filhandle.write(key+"\n")
        filhandle.close()'''
        print("Num Dups per query "+file_name+"\t"+str(num_duplicates))
        print("***************************************************************************************************")

    return

def Count_Product_Duplicates_In_Sub_Cat_Codes():
    base_sub_cats_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    for file_name in os.listdir(base_sub_cats_dirc):
        query_file_path = base_sub_cats_dirc + file_name
        num_prods = 0
        with open(query_file_path, 'r') as filep:
            for item in filep:
                num_prods+=1


        print("Num prods per query " + file_name + "\t" + str(num_prods))
        #print("***************************************************************************************************")
    return
def Count_Reviews_per_product_Sub_cat():
    base_num_revs_dirc = "D:\Yassien_PhD/Number_of_reviews_per_product/"
    base_sub_cats_dirc = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/"
    query_map_file_path = base_sub_cats_dirc+"query_code_map.txt"
    ignore_first = 0
    medians = []
    medina_dict = dict()
    with open(query_map_file_path, 'r') as filep:
        for item in filep:
            if ignore_first == 0:
                ignore_first=1
                continue
            line = item.split('\t')
            qid = line[0]
            category = line[1]
            sub_category = line[2].split('\n')[0]
            num_revs_file_path = base_num_revs_dirc+category+".txt"
            sub_cat_file_path = base_sub_cats_dirc+category+"/"+sub_category+".txt"
            #print(num_revs_file_path)
            #print(sub_cat_file_path)
            m = Count_Reviews_Per_Product_Set(sub_cat_file_path,num_revs_file_path)
            medians.append(m)

            try:
                med_res=medina_dict[category]
                med_res.append(m)
                medina_dict[category] = med_res
            except KeyError:
                med_res = []
                med_res.append(m)
                medina_dict[category]=med_res
    print("MEdian")
    medians.sort()
    print(medians)
    a = np.array(medians)
    m = np.median(a)
    print("Median of Medians "+str(m))
    for key,value in medina_dict.items():
        num_less = 0
        num_more = 0
        for item in value:
            if item<40:
                num_less+=1
            else:
                num_more+=1
        print(key +"\t"+str(len(value))+"\t"+str(num_less)+"\t"+str(num_more))
    return


def Count_Reviews_Per_Product_Set(cat_prods_path,cat_num_revs_path):
    products_num_revs_dict = dict()
    with open(cat_num_revs_path, 'r') as filep:
        for line in filep:
            line = line.split('\t')
            products_num_revs_dict[line[0]] = int(line[1])
    num_prods = 0
    total_num_revs = 0
    num_prods_gt= 0
    counts = []
    with open(cat_prods_path, 'r') as filep:
        for item in filep:
            line = item.split('\n')
            count = products_num_revs_dict[line[0]]
            #print(count)
            counts.append(count)
            if count>=100:
                num_prods_gt+=1
            total_num_revs+=count
            num_prods+=1
    #print(num_prods_gt)
    #print("Total Num Prods "+str(num_prods))
    #print("Total Num Revs "+str(total_num_revs))
    avg_num_revs = int(total_num_revs/num_prods)
    #print("Avg Num Revs " + str(avg_num_revs))
    #print(counts)
    counts.sort()
    #print(counts)

    a = np.array(counts)
    p = np.percentile(a, 75)
    m=np.median(a)
    #print(p)
    print(str(num_prods)+"\t"+str(avg_num_revs)+"\t"+str(m)+"\t"+str(counts))
    #print("***********************************************************************************************************")

    return m
def Get_Max_Num_Of_Products_Per_Category_Queries(dataset):
    if dataset == "amazon":
        cat_query_directory = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/"
        max_num_prods_cat_file_path ="D:\Yassien_PhD\Experiment_5\Randomized_Queryset/max_num_prodc_per_cat.txt"
    else:
        cat_query_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/"
        max_num_prods_cat_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/max_num_prodc_per_cat.txt"
    filehandle = open(max_num_prods_cat_file_path,'w')
    for folder in os.listdir(cat_query_directory):
        folder_path = cat_query_directory+folder+"/"
        if os.path.isdir(folder_path):
            print("Considering " + folder)
            max_num_prods = -100
            for files in os.listdir(folder_path):
                file_path = folder_path+files
                num_prods = 0
                with open(file_path, 'r') as fp:
                    for line in fp:
                        num_prods+=1
                if max_num_prods<num_prods:
                    max_num_prods = num_prods

            print("Max Num prods "+str(max_num_prods))
            filehandle.write(folder+"\t"+str(max_num_prods)+"\n")

    filehandle.close()
    return

def Trace_Back_Queries_to_Cats_In_Testing_or_Training_Set(dataset,type):
    if dataset == "amazon":
        query_code_map_file_poath = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
        if type == "test":
            testing_queries_file_path = "D:\Yassien_PhD\Experiment_6\Randomized_Queryset/testing.txt"
            query_cat_map_file_path = "D:\Yassien_PhD\Experiment_6\Randomized_Queryset/query_cat_map_test.txt"
        else:
            testing_queries_file_path = "D:\Yassien_PhD\Experiment_6\Randomized_Queryset/training.txt"
            query_cat_map_file_path = "D:\Yassien_PhD\Experiment_6\Randomized_Queryset/query_cat_map_train.txt"
    else:
        query_code_map_file_poath = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
        if type == "test":
            testing_queries_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/testing.txt"
            query_cat_map_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map_test.txt"
        else:
            testing_queries_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/training.txt"
            query_cat_map_file_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map_train.txt"
    query_id_map_dict = dict()
    ignore_first_line=0
    with open(query_code_map_file_poath, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_map_dict[int(row[0])]=row[1]

    cats_dict = dict()
    with open(testing_queries_file_path, 'r') as fp:
        for line in fp:
            qid = int(line.split('\n')[0])
            try:
                result = cats_dict[query_id_map_dict[qid]]
                result.append(qid)
                cats_dict[query_id_map_dict[qid]]=result
            except KeyError:
                queries = []
                queries.append(qid)
                cats_dict[query_id_map_dict[qid]]=queries
    filehandle = open(query_cat_map_file_path,'w')
    for key,value in cats_dict.items():
        print(key+" Total "+str(len(value)))
        filehandle.write(key+"\t")
        for i in range(len(value)):
            if i == len(value)-1:
                filehandle.write(str(value[i])+"\n")
            else:
                filehandle.write(str(value[i]) + "\t")
            print(qid)
        print("*************************************************")
    filehandle.close()

    return

def Create_All_TQ_Ranks_Folder_Yelp():
    categories_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Resturants_Categories/"
    feature_vect_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Different_time_feature_vectors\All_Categories_Data_25_Basic_Features_With_1_Time_Intervals/"
    tq_rank_dest_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Ranked_by_TQ_Rank/"
    sales_rank_dest_main_dirc = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Ranked_by_Sales_Rank/"
    orig_catNames = ["Cafes", "Chinese", "Mexican", "Italian", "American (Traditional)", "Thai", "Bars", "Japanese","American (New)"]
    for category in orig_catNames:
        print(category)
        cat_file_path = categories_main_dirc+category+".txt"
        feature_file_path = feature_vect_main_dirc+category+".txt"
        product_list = []
        tq_rank_list = []
        sales_rank_list = []
        index = 0
        with open(cat_file_path, 'r') as fp:
            for line in fp:
                row = line.split('\t')
                product_list.append(row[0])
                sales_rank_list.append((index,float(row[2].split('\n')[0])))
                index+=1
        with open(feature_file_path, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                tq_rank_list.append(row[0])
        #print(product_list)
        #print(tq_rank_list)
        #print(sales_rank_list)
        mergeSort(sales_rank_list)
        sales_rank_list.reverse()
        #print(sales_rank_list)
        #print(len(product_list))
        #print(len(tq_rank_list))
        sum = len(sales_rank_list)
        new_sales_rank = []
        for i in range(len(sales_rank_list)):
            sum = len(sales_rank_list)-1
            for item in sales_rank_list:
                if item[0]==i:
                    new_rank = sum
                    new_sales_rank.append(new_rank)
                    break
                sum-=1
        #print(new_sales_rank)
        cat_tq_file_path = tq_rank_dest_main_dirc+category+".txt"
        filehandle = open(cat_tq_file_path,'w')
        for i in range(len(product_list)):
            filehandle.write(product_list[i]+"\t"+tq_rank_list[i]+"\n")
        filehandle.close()

        cat_tq_file_path = sales_rank_dest_main_dirc + category + ".txt"
        filehandle = open(cat_tq_file_path, 'w')
        for i in range(len(product_list)):
            filehandle.write(product_list[i] + "\t" + str(new_sales_rank[i]) + "\n")
        filehandle.close()

    return

def dirichlet_mean(ratingsDictionary, prior):
        """
        Computes the Dirichlet mean with a prior.
        """
        # print("-----------------------------")
        # print("prior")
        # print(prior)
        votes = []
        for key, value in ratingsDictionary.items():
            votes.append(value)
        print("votes")
        print(votes)
        posterior = map(sum, zip(votes, prior))
        temp = list(map(sum, zip(votes, prior)))
        to = list(enumerate(temp))
        print("posterior")
        print(posterior)
        print("enum posterior")
        print(to)
        N = sum(posterior)
        print("Sum Posterior")
        print(N)
        weights = list(map(lambda i: (i[0] + 1) * i[1], to))
        print("weights ")
        print(weights)
        newlist = []
        for item in weights:
            item = item / sum(weights)
            newlist.append(item)
        print("newlist")
        print(newlist)
        print("sumWeights")
        print(sum(weights))
        retValue = float(float(sum(weights)) / N)
        print("retValue")
        print(retValue)
        return retValue


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
''
#Copy_Rank_From_One_Set_To_Other("f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/","f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_1_Time_Intervals_old/","f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_1_Time_Intervals/")
#orig_catNames = ["Industrial & Scientific","Jewelry","Arts, Crafts & Sewing","Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
base_filtered_products_directory = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Product_categories_with_sub_categories_filtered/"
#base_num_reviews_directory = "D:/Yassien_PhD/Number_of_reviews_per_product/"
'''
for category_name in orig_catNames:
    cat_prods_path = base_filtered_products_directory+category_name+".txt"
    #cat_num_revs_path = base_num_reviews_directory+category_name+".txt"
    #print("Considering "+category_name)
    #Count_Reviews_Per_Product_Set(cat_prods_path,cat_num_revs_path)
    base_cat_paath = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Queries_Per_Product_Category/"
    category_folder=base_cat_paath+category_name+"/"
    Count_Queries_With_Given_Num_Products(category_folder,10)
    '''

#These lines extract all subcategories, then filter for only products previously extracted and finally extract those subcategories involved as queries
#Extract_Products_Sub_Categories_Yelp()
#Filter_Product_Sub_Categories_With_Current_Yelp()
#Create_All_Queries_For_Categories_Based_on_Subs_Yelp()
#Create_All_TQ_Ranks_Folder_Yelp()
#Create_All_Products_Indices_Yelp()
#Trace_Back_Queries_to_Cats_In_Testing_or_Training_Set("amazon","test")
#Get_Max_Num_Of_Products_Per_Category_Queries("yelp")


base_num_reviews_directory = "D:/Yassien_PhD/Number_of_reviews_per_product/Arts, Crafts & Sewing.txt"
product_sub_cat = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8\Arts, Crafts & Sewing/Airbrush Materials.txt"
#Count_Reviews_Per_Product_Set(product_sub_cat,base_num_reviews_directory)
#Count_Reviews_per_product_Sub_cat()
#counts = [21, 24, 86, 99, 2215, 2215, 7531]
#import numpy as np
#a = np.array(counts)
#p = np.percentile(a, 75)
#print(p)
#Check_Product_Duplicates_In_Sub_Cat_Codes()
#Count_Product_Duplicates_In_Sub_Cat_Codes()
#Check_Product_Duplicates_In_Sub_Cat()