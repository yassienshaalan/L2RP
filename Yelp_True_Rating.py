#Author: Yassien Shaalan

def computeMajorityVoteForProductCategories(filePath,category,destDirectory):
    print("Procedure to compute the average score for each product under each category")
    print("Considering "+category)
    #product_Id Category sales_rank
    #print("Started")
    start = datetime.now()
    #print(start)
    line = ""
    filehandle = open(destDirectory+category+".txt",'w')
    with open(filePath, 'r') as fp:
      for line in fp:
           row = line.split('\t')
           productId = row[0]
           print(productId)
           fileName = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"+productId+".txt"
           overallRate = 0
           counter = 0
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    review = item.split('\t')
                    overallRate = overallRate + float(review[5])
                    counter = counter + 1
           except IOError as e:
              pass
           #filehandle.write(productId)
           #filehandle.write("\t")
           overallRate = overallRate/counter
           overallRate = round(overallRate,4)
           print("Average Score "+str(overallRate))
           #filehandle.write(str(overallRate))
           #filehandle.write("\n")
           break
    #filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computeDiricheletwithForgettingFactor(path,categoryName,destDirectory):
    print("Procedure to compute product rating based on dirichelet distribution with Forgetting factor")
    print("Considering "+categoryName)
    start = datetime.now()
    line = ""
    filehandle = open(destDirectory+categoryName+".txt",'w')
    with open(path, 'r') as fp:
      for line in fp:
           row = line.split('\t')
           productId = row[0]
           productId = productId.split('\n')
           productId = productId[0]
           #print(productId)
           prior = [1,1,1,1,1]
           lamda = 0.9
           forgettingFactors = generateWeights(lamda)
           print(forgettingFactors)

           #print(forgettingFactors)
           ratingTemproalCategory,ratingHelpfulnessCategory = analyzeProduct(productBaseDirectory,productId)
           #print("------------------------------------------------")
           ratingTemproalCategoryWeighted = []
           ratingHelpfCategoryWeighted = []
           #print(ratingTemproalCategory)
           for i in range(len(ratingTemproalCategory)):
               newCat = dict()
               helpCat = dict()
               #print("------------")
               for item in ratingTemproalCategory[i]:
                   #newCat[item] = int(round(ratingTemproalCategory[i][item]*(forgettingFactors[item-1]+ratingHelpfulnessCategory[i][item]),0))
                   newCat[item] = int(round(ratingTemproalCategory[i][item]*(forgettingFactors[item-1]),0))
                   helpCat[item] = int(round(ratingTemproalCategory[i][item]*(ratingHelpfulnessCategory[i][item]),0))
               #print(newCat)
               ratingTemproalCategoryWeighted.append(newCat)
               ratingHelpfCategoryWeighted.append(helpCat)

           #------------------------------------------------------------------------------------------------------------
           #Preparing Prior on just summing the degree of helpfulness
           newHelpfulnessPrior = aggregateRatingsForAllTimePeriods(ratingHelpfulnessCategory)
           newHelpPriorValuesOld = []
           for help in newHelpfulnessPrior:
               newHelpPriorValuesOld.append(int(round(newHelpfulnessPrior[help],0)))
           #------------------------------------------------------------------------------------------------------------
           #print("OLD newHelpfulnessPrior")
           #print(newHelpPriorValuesOld)
           #------------------------------------------------------------------------------------------------------------
           #Preparing New Prior on just summing the degree of helpfulness*NumVotes
           newHelpPriorValues = aggregateRatingsForAllTimePeriods(ratingHelpfCategoryWeighted)
           newHelpPriorValuesNew = []
           for help in newHelpPriorValues:
               newHelpPriorValuesNew.append(int(round(newHelpPriorValues[help],0)))
           #------------------------------------------------------------------------------------------------------------
           #print("newHelpPriorValues")
           #print(newHelpPriorValuesNew)

           ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategoryWeighted)
           #print(ratings)

           #retValue = dirichlet_mean(ratings,newHelpPriorValuesOld)
           #print("old Ret")
           #print(retValue)
           retValue = dirichlet_mean(ratings,prior)
           #print("New Ret")
           #print(retValue)
           #print(retValue)
           filehandle.write(productId)
           filehandle.write("\t")
           filehandle.write(str((retValue)))
           filehandle.write("\n")

           '''

           print("--------------------------------")
           for cat in ratingTemproalCategoryWeighted:
                print(cat)
           print("--------------------------------")
           oldratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategory)
           print(" old ratings")
           print(oldratings)
           retValue = dirichlet_mean(oldratings,prior)
           print("old dirichlet")
           print(retValue)
           ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategoryWeighted)
           print(" new ratings")
           print(ratings)
           retValue = dirichlet_mean(ratings,prior)
           print("new dirichlet")
           print(retValue)
           '''

    return
def computeTrueRateForAllCategoreis(productBaseDirectory,directory,option,destDirectory,startFrom):
    print("Procedure to read Compute all product categories majority vote")
    #print("Started")
    start = datetime.now()
    index = 0
    #endAt = startFrom + 4
    #print(start)
    for filename in os.listdir (directory):
        if index >= startFrom:
            path = directory +filename
            category = filename
            categoryName = category.split(".txt")
            categoryName = categoryName[0]
            if option == 0:#Normal Mean
                computeMajorityVoteForProductCategories(path,categoryName,destDirectory)
            elif option == 1:#Normal Dirichelet
                computeNormalDirichelet(productBaseDirectory,path,categoryName,destDirectory)
            elif option == 2:#Weighted Dirichelet
                computeWeightedDirichelet(path,categoryName,destDirectory)
            elif option == 3:#Average & Dirichelet
                computeAverageAndDirichelet(path,categoryName,destDirectory)
            elif option == 4:#Dirichelet with forgetting factor
                computeDiricheletwithForgettingFactor(path,categoryName,destDirectory)
                break
        #if index == (endAt-1):
         #   break
        index = index + 1

    Finished = datetime.now()
    done = Finished - start
    print("done out")
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def sortRatedCategories(directory,destDirectory,startFrom):
    print("Procedure to sort categories after rating")
    print("Started ")
    start = datetime.now()
    index = 0
    #endAt = startFrom + 4
    print(start)
    for filename in os.listdir (directory):
        if index >= startFrom:
            path = directory +filename
            category = filename
            categoryName = category.split(".txt")
            categoryName = categoryName[0]
            sortRatedCategory(path,categoryName,destDirectory)
            break
        #if index == (endAt-1):
         #   break
        index = index + 1

    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    print("done out")
    return
def sortRatedCategory(filePath,category,destDirectory):
    print("Procedure to read category rated File, get a product from it and read its file and sort it and write to a file for a cetegory file")
    print("Considering "+category)
    #product_Id Category sales_rank
    import sys
    sys.setrecursionlimit(100000)

    #print("Started")
    start = datetime.now()
    #print(start)
    line = ""
    listofProducts = []
    filehandle = open(destDirectory+category+".txt",'w')
    with open(filePath, 'r') as fp:
      for line in fp:
         tuple = line.split('\t')
         listofProducts.append((tuple[0],float(tuple[1])))

    quickSort(listofProducts)
    if len(listofProducts) == 0:
        print("problem with zero lists")
    for item in reversed(listofProducts):
        filehandle.write(item[0])
        filehandle.write("\t")
        filehandle.write(str(item[1]))
        filehandle.write("\n")
    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")

    print("done in")
    return
def measureDistanceBetweenSalesRankandRatedCategories(directorySales,directory_Rated,destDirectory,startFrom):
    print("Procedure to measure differences in sales sorted lists and majority vote sorted lists")
    #print("Started")
    start = datetime.now()
    #print(start)
    index = 0
    #endAt = startFrom + 4
    for filename in os.listdir (directorySales):
        if index >= startFrom:
            path1 = directorySales +filename
            path2 = directory_Rated +filename
            category = filename
            categoryName = category.split(".txt")
            categoryName = categoryName[0]
            measureDistanceBetweenForCategory(path1,path2,categoryName,destDirectory)
            break
        #if index == (endAt-1):
           # break
        index = index + 1


    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")

    print("done out")
    return

    return
def measureDistanceBetweenForCategory(path1,path2,category,destDirectory):
    print("Procedure to compare two categories")
    print("Considering "+category)
    #product_Id Category sales_rank
    import sys
    sys.setrecursionlimit(100000)
    #print("Started")
    start = datetime.now()
    #print(start)
    line = ""
    salesRankList = []
    majorityVoateList = []
    filehandle = open(destDirectory+category+".txt",'w')

    with open(path1, 'r') as fp:
      for line in fp:
         tuple = line.split('\t')
         salesRankList.append(tuple[0])

    with open(path2, 'r') as fp:
      for line in fp:
         tuple = line.split('\t')
         majorityVoateList.append(tuple[0])

    salesRankIndices = []
    salesRankProduct = []
    majorityIndices = []
    majorityProduct = []
    if len(salesRankList) != len(majorityVoateList):
       print("Error UnEven Lists")
       return
    else:
        salesIndex = 1
        for sales in (salesRankList):
            salesRankIndices.append(salesIndex)
            salesRankProduct.append(sales)
            majorIndex = 1
            for majority in (majorityVoateList):
                if sales == majority:
                    difference = salesIndex - majorIndex
                    majorityProduct.append(majority)
                    majorityIndices.append(majorIndex)
                    #filehandle.write(sales)
                    #filehandle.write("\t")
                    #filehandle.write(str(difference))
                    #filehandle.write("\n")
                    break
                majorIndex = majorIndex + 1
            salesIndex = salesIndex + 1
    #filehandle.close()



    for i in range(len(salesRankIndices)):
        filehandle.write(str(salesRankIndices[i]))
        filehandle.write("\t")
        #filehandle.write(str(salesRankProduct[i]))
        #filehandle.write("\t")
        #filehandle.write(str(majorityProduct[i]))
        #filehandle.write("\t")
        filehandle.write(str(majorityIndices[i]))
        filehandle.write("\n")

    filehandle.close()

    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")

    print("done in")
    return
def MAE(predicitonList,trueList):
        n = len(trueList)
        if n > 0:
            summation = 0
            for i in range(n):
                summation = summation + ((predicitonList[i] - trueList[i]) ** 2)
            mse = summation/n
        else:
            mse = -1
        return mse
def RMSE(mse):
        rmse = math.sqrt(mse)
        return rmse
def computeMAEForLists(sourceDirectory,destDirectory,fileName):

    print("Procedure to read MAE for two lists")
    start = datetime.now()
    filehandle = open(destDirectory+fileName+".txt",'w')
    print("considering"+fileName)
    for filename in os.listdir (sourceDirectory):
        path = sourceDirectory +filename

        meanList = []
        dirichletList = []
        with open(path, 'r') as fp:
          for line in fp:
             row = line.split('\t')
             meanList.append(float(row[1]))
             dirichletList.append(float(row[2]))

        mae = MAE(dirichletList,meanList)
        filehandle.write(str(mae))
        filehandle.write("\n")
    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return

def convertJsonReviesToProducts(sourcefilePath,destFilePath):

    rData = open(sourcefilePath)
    print("Started")
    print("Loading JSON")
    #reviews_parsed = json.loads(rData.read())
    reviews_parsed = []
    counter = 0
    with rData as myfile:
        for line in myfile:
            reviews_parsed.append(json.loads(line))
            #print(counter)
            counter = counter + 1
            #if counter == 200:
             #  break
    print("finished preparing")
    print("reviews_parsed")
    #reviews_parsed = json.loads(input)
    print("Loading Done")
    review_data = reviews_parsed

    #rev_data = open(destFilePath, 'w')
    # create the csv writer object
    print("Starting to collect product reviews")
    # open a file for writing
    productReviews = dict()

    for review in review_data:
        counter = 0
        indexes = []
        keys = []
        for key in review.keys():
            if key == "type":
                indexes.append(counter)
            else:
                keys.append(key)
            counter += 1
        counter = 0
        keyIndex = 0
        line = ""
        prodKey = ""
        for val in review.values():
            if counter != indexes[0]:
                line += keys[keyIndex]
                line += "\t"
                line += "::"
                line += "\t"
                if keys[keyIndex] == "business_id":
                    prodKey = val
                if keys[keyIndex] == "text":
                    try :
                        val
                        new = str(val).split("\n")
                        for sent in new:
                            line = line + sent +"\t"
                    except UnicodeEncodeError as err:
                        pass
                else:
                    line += str(val)
                line += "\t"
                line += "::"
                keyIndex += 1
            counter += 1
        #filehandle.write("\n")
        line += "\n"

        try:
                reviewsLine = productReviews[prodKey]
                reviewsLine = reviewsLine + line
                productReviews[prodKey] = reviewsLine
        except KeyError as e:
                productReviews[prodKey] = line

    print("Finished Collecting product reviews")
    print("Starting to Write")
    for key,value in productReviews.items():
        filePath = destFilePath+key+".txt"
        filehandle = open(filePath,'w')
        print("writing file "+key)
        newLine = value

        '''
        newLine.replace('\u2103',' ')
        newLine.replace('\u016b',' ')
        newLine.replace('\u014d',' ')
        newLine.replace('\u016f',' ')
        newLine.replace('\uff01',' ')

        for char in value:
            try :
                char
                if char !='\u2103' and char !='\u016b' and char !='\u014d' and char !='\u016f'and char !='\uff01':
                    newLine = newLine + char
            except UnicodeEncodeError as err:
                print("found one bad character")
                pass
        '''
        try:
            filehandle.write(newLine)
        except UnicodeEncodeError as err:
                print("found one bad character not writing")
                pass

        filehandle.close()
    print("Finished Writing")
    return
def convertJsonBusinessToProductCategories(sourcefilePath,destFilePath):

    rData = open(sourcefilePath,'r',encoding='utf-8')
    print("Started")
    print("Loading JSON")
    #reviews_parsed = json.loads(rData.read())
    reviews_parsed = []
    counter = 0
    with rData as myfile:
        for line in myfile:
            reviews_parsed.append(json.loads(line))
            #print(counter)
            counter = counter + 1


    print("finished preparing")
    print("reviews_parsed")
    #reviews_parsed = json.loads(input)
    print("Loading Done")
    review_data = reviews_parsed

    #rev_data = open(destFilePath, 'w')
    # create the csv writer object
    print("Starting to collect product reviews")
    # open a file for writing
    productReviews = dict()
    allCatList = []
    for review in review_data:
        counter = 0
        indexes = []
        keys = []
        #print(review.values())

        for key in review.keys():
            if key == "latitude" or key == "longitude" or key == "full_address" or key == "type"or key == "open"or key == "hours" or key == "attributes":
                indexes.append(counter)
            else:
                keys.append(key)
            counter += 1
        counter = 0
        keyIndex = 0
        line = ""
        prodKey = ""
        for val in review.values():
            if counter != indexes[0] and counter != indexes[1]and counter != indexes[2]and counter != indexes[3]and counter != indexes[4]and counter != indexes[5]and counter != indexes[6]:
                line = line + keys[keyIndex]
                line = line + "\t"
                line = line + "::"
                line = line + "\t"
                line = line +str(val)
                line = line +"\t"
                line = line + "::"
                if keys[keyIndex] == "categories":
                    prodKey = val
                keyIndex += 1
            counter += 1
        line = line + "\n"
        #---------------------------------------------------------------------------------------------------------------
        newLine = ""
        for char in line:
            try :
                char
                if char !='\u2103' and char !='\u016b' and char !='\u014d' and char !='\u016f':
                    newLine = newLine + char
            except UnicodeEncodeError as err:
                print("found one bad character")
                pass

        #---------------------------------------------------------------------------------------------------------------
        allCatList.append(prodKey)
        productKey = ""
        for cat in prodKey:
            productKey = productKey +"_"+cat
        try:
                reviewsLine = productReviews[productKey]
                reviewsLine = reviewsLine + newLine
                productReviews[productKey] = reviewsLine
        except KeyError as e:
                foundKey = ""
                for key,value in productReviews.items():
                    counter = 0
                    for cat in prodKey:
                        if cat in key:
                            #print(cat +" in " + key)
                            if counter == 0:
                                #print("will take this key "+key)
                                foundKey = key
                                break
                            counter += 1

                if foundKey != "":
                    reviewsLine = productReviews[foundKey]
                    reviewsLine = reviewsLine + newLine
                    productReviews[foundKey] = reviewsLine
                else:
                    productReviews[productKey] = newLine
        #---------------------------------------------------------------------------------------------------------------
    print("Finished Collecting product reviews")
    print("Starting to Write")
    for key,value in productReviews.items():
        tempCat = key
        tempCat = tempCat.split("/")
        newKey = key
        if len(tempCat)>1:
            newKey = tempCat[0]+"_"+tempCat[1]
        newKey = str(newKey)
        try:
            filePath = destFilePath+newKey+".txt"
            filehandle = open(filePath,'w')
            filehandle.write(value)
        except UnicodeEncodeError:
            print("Error with file "+str(key))
            pass

        filehandle.close()
    print(len(productReviews))
    print("Finished Writing")
    return
def computeMajorityVoteForProductCategories(filePath,category,productBaseDirectory,destDirectory):
    print("Procedure to compute the average score for each product under each category")
    print("Considering "+category)
    #product_Id Category sales_rank
    #print("Started")
    start = datetime.now()
    #print(start)
    line = ""
    #filehandle = open(destDirectory+category+".txt",'w')
    with open(filePath, 'r') as fp:
      for line in fp:
           row = line.split('::')
           productId = ""
           for item in row:
               if productId == 1:
                   productId = item
                   productId = productId.split('\t')
                   productId = productId[1]
               if "business_id" in item:
                   productId = 1
           productId = "AX8x7z1B5jYaEg9g9LaC3g"
           fileName = productBaseDirectory+productId+".txt"
           print(fileName)
           overallRate = 0
           counter = 0
           productrates = []
           productdates = []
           minDate = datetime(2050, 12, 31)
           maxDate = datetime(1950, 1, 1)
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    row = item.split('::')
                    ratingFlag = 0
                    dateFlag = 0
                    currentdate = ""
                    rating = 0

                    for attr in row:
                        field = attr.split('\t')
                        #print(field)
                        if len(field) == 3 and ratingFlag == 1:
                            rating = float(field[1])
                            productrates.append(rating)
                            print(rating)
                            ratingFlag = 0
                        if len(field) == 3 and dateFlag == 1:
                            currentdate = field[1]
                            currentdate = currentdate.split('-')
                            year = int(currentdate[0])
                            month = int(currentdate[1])
                            day = int(currentdate[2])
                            currentdate = datetime(year, month, day)
                            productdates.append(currentdate)
                            print(currentdate)
                            if currentdate >maxDate:
                                maxDate = currentdate
                            if currentdate <minDate:
                                minDate = currentdate
                            dateFlag = 0
                        if len(field) == 2 and field[0] == "stars":
                            ratingFlag = 1
                        if len(field) == 2 and field[0] == "date":
                            dateFlag = 1
                    overallRate = overallRate + rating
                    counter = counter + 1
           except IOError as e:
              pass
           #filehandle.write(productId)
           #filehandle.write("\t")
           print("num ratings")
           print(counter)
           overallRate = overallRate/counter
           print("overallRate")
           print(overallRate)
           print("minDate")
           print(minDate)
           print("maxDate")
           print(maxDate)
           #overallRate = round(overallRate,4)
           #print("Average Score "+str(overallRate))
           #filehandle.write(str(overallRate))
           #filehandle.write("\n")
           break
    #filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computeTrueRateForAllCategoreis(productBaseDirectory,directory,option,destDirectory):
    for filename in os.listdir (directory):
        filePath = directory +filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        if categoryName != "UnCategoriezed":
            if option == 0:
                computeMajorityVoteForProductCategories(filePath,categoryName,productBaseDirectory,destDirectory)
                break

    return
def compute_dataset_statistics(product_categories,productBaseDirectory):
    for filename in os.listdir(product_categories):
        filePath = product_categories + filename
        print(filePath)
        count = 0
        with open(filePath, 'r') as fp:
            for line in fp:
                line=line.split('\t')
                num_reviews = int(line[1])
                if num_reviews >=100:
                    count+=1
                '''product_file_path = productBaseDirectory+line[0]+".txt"
                count=0
                with open(product_file_path, 'r') as fp2:
                    for line2 in fp2:
                        count+=1
                print(count)
                print("---------------------")'''
        print(count)
    return
#------------------------------------Program Start----------------------------------------------------------------------
import sys
import os
from datetime import datetime
from datetime import timedelta
import math
from temp_Function import  *
from alogrithms import *
import json
import csv
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    '''
    x = str(sys.argv[1])
    y = str(sys.argv[2])
    z = str(sys.argv[3])
    sys.stdout.write(str(createNewVerifiedDataset(x,y,z)))
    '''
    print("Hello This is Yelp Dataset")
    #------------------------Building the Yelp Dataset like Amazon in terms of product Categories-----------------------
    filePath = "/research/remote/petabyte/users/yassien/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review.json"
    destFile= "/research/remote/petabyte/users/yassien/yelp_dataset_challenge_academic_dataset/Product_Reviews/"
    #convertJsonReviesToProducts(filePath,destFile)
    #filePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
    #destFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset\Product_Categories/"
    #convertJsonBusinessToProductCategories(filePath,destFile)
    #-------------------------------------------------------------------------------------------------------------------

    '''
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/ProductReviews_New/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset\Product_Categories\Cagegories_1_Keyword/"
    option = 0
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset\Experiment 1\Computed_Rating\categories_average_rating/"
    computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory)
    '''
    product_categories = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/Cat_Stats/"
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/ProductReviews_New/"
    compute_dataset_statistics(product_categories,productBaseDirectory)