def getProductsWithNumberofReviewsThreshold(categoriesDirectory,productBaseDirectory,destDirectory,experimentDirectory,threshold):
    print("Procedure to Count Number of Reviews for each Product")
    print("Started")
    startFrom = 0
    index = 0
    filehandleProducts = open(experimentDirectory+"DataSet_"+str(threshold)+".txt",'w')
    for filename in os.listdir (categoriesDirectory):
        if index >= startFrom:
            categoryPath = categoriesDirectory +filename
            category = filename
            categoryName = category.split(".txt")
            categoryName = categoryName[0]
            counter = 0
            print("considering "+categoryName)
            filehandleCounts = open(destDirectory+"/"+categoryName+".txt",'w')
            with open(categoryPath, 'r') as fp:
             for line in fp:
                 tuple = line.split('\t')
                 productId = tuple[0]
                 innerCounter = 0
                 fileName = productBaseDirectory+productId+".txt"
                 try:
                      innerCounter = sum(1 for line in open(fileName, 'r'))
                 except IOError as e:
                      pass
                 if innerCounter >= threshold:
                     counter = counter + 1
                     filehandleCounts.write(productId)
                     filehandleCounts.write("\n")
             filehandleCounts.close()
            filehandleProducts.write(str(counter))
            filehandleProducts.write("\n")
    filehandleProducts.close()
    print("Finished")
    return
def getProductsWithNumberofReviewsThresholdFromOther(categoriesOriginalDirectory,biggerThresholdDirectory,destDirectory):
    print("Procedure to record products difference between two datasets")

    for filename in os.listdir (categoriesOriginalDirectory):
        categoryPath = categoriesOriginalDirectory +filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        print("considering "+categoryName)
        prodcutdict = dict()
        filehandleDifferenceProducts = open(destDirectory+categoryName+".txt",'w')
        with open(categoryPath, 'r') as fp:
            for line in fp:
                tuple = line.split('\t')
                productId = tuple[0]
                prodcutdict[productId] = 0
        categoryPath = biggerThresholdDirectory +"/"+categoryName+".txt"
        with open(categoryPath, 'r') as fp:
            for line in fp:
                tuple = line.split('\t')
                productId = tuple[0]
                productId = productId.split('\n')
                productId = productId[0]
                try:
                    ratingValue = prodcutdict[productId]
                    ratingValue = ratingValue + 1
                    prodcutdict[productId] = 1
                except KeyError as e:
                    print("This was not found "+productId)
        for key,value in prodcutdict.items():
            if value == 0:
                filehandleDifferenceProducts.write(key)
                filehandleDifferenceProducts.write("\n")
        filehandleDifferenceProducts.close()
    print("Finished")
    return
def createNewSortedSalesRankListForCertainDataSet(categoriesOriginalDirectory,newDatasetDirectory,destDirectory):
    print("Procedure to create new sorted Sales Rank based on new selected DataSet")

    for filename in os.listdir (categoriesOriginalDirectory):
        categoryPath = categoriesOriginalDirectory +filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        #print("considering "+categoryName)

        prodcutdict = []
        if not os.path.exists(destDirectory):
            os.makedirs(destDirectory)
        filehandleDifferenceProducts = open(destDirectory+"/"+categoryName+".txt",'w')
        counter = 0
        with open(categoryPath, 'r') as fp:
            for line in fp:
                tuple = line.split('\t')
                productId = tuple[0]
                prodcutdict.append((productId,int(tuple[1])))

        categoryPath = newDatasetDirectory +"/"+categoryName+".txt"
        newListProducts = []
        try:
            with open(categoryPath, 'r') as fp:
                for line in fp:
                    tuple = line.split('\t')
                    productId = tuple[0]
                    productId = productId.split('\n')
                    productId = productId[0]
                    newListProducts.append(productId)

        except IOError as e:
            pass
        resultList = []
        for product in newListProducts:
            for productSales in prodcutdict:
                if product == productSales[0]:
                    resultList.append(productSales)
                    break
        quickSort(resultList)
        print(len(resultList))

        for product in resultList:
           filehandleDifferenceProducts.write(str(product[0]))
           filehandleDifferenceProducts.write("\t")
           filehandleDifferenceProducts.write(str(product[1]))
           filehandleDifferenceProducts.write("\n")
        filehandleDifferenceProducts.close()

    print("Finished")
    return
def analyzeProduct(poductsBaseDirectory,productID):

    productPath = poductsBaseDirectory+productID+".txt"
    productDates = []
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    ratingsDictionary = dict()
    numFeedBackDictionary = dict()
    numHelpFeedDictionary = dict()
    ratingsDateDictionary = dict()#{'1.0':None,'2.0':None,'3.0':None,'4.0':None,'5.0':None}
    average = 0
    sumRatings = 0
    numReviews = 0
    with open(productPath, 'r') as fp:
            for line in fp:
                review = line.split('\t')
                numReviews+=1
                #----------------------------------------------------------------------------
                #Extracting Date
                datesplit = review[2].split(',')
                monthDay = datesplit[0]
                month = ""
                day = ""
                monthDone = 0
                for char in monthDay:
                    if char != " " and monthDone== 0:
                        month = month + char
                    if char == " ":
                        monthDone = 1
                    if monthDone== 1:
                        day = day + char
                if len(datesplit)>1 and datesplit[1]!=' ' and len(datesplit[1])<=5:
                    year = int(datesplit[1])
                    month = int(month)
                    day = int(day)

                    currentDay = datetime(year, month, day)

                    productDates.append((currentDay))
                    if currentDay >maxDate:
                        maxDate = currentDay
                    if currentDay <minDate:
                        minDate = currentDay

                    #----------------------------------------------------------------------------

                    #Extracting Rates
                    rating = float(review[5])
                    sumRatings+=rating
                    try:
                        ratingValue = ratingsDictionary[rating]
                        ratingValue = ratingValue + 1
                        ratingsDictionary[rating] = ratingValue
                    except KeyError as e:
                        ratingsDictionary[rating] = 1
                    #----------------------------------------------------------------------------
                    #Adding Rating Date
                    try:
                        dateList = ratingsDateDictionary[rating]
                        dateList.append(currentDay)
                        ratingsDateDictionary[rating] = dateList
                    except KeyError as e:
                        dateList = []
                        dateList.append(currentDay)
                        ratingsDateDictionary[rating] = dateList

                    #-----------------------------------------------------------------------------
                    #Adding num FeedBack
                    numFeedback = 0
                    if review[3] != "":
                        numFeedback = int(review[3])
                    try:
                        feedList = numFeedBackDictionary[rating]
                        feedList.append((numFeedback,currentDay))
                        numFeedBackDictionary[rating] = feedList
                    except KeyError as e:
                        feedList = []
                        feedList.append((numFeedback,currentDay))
                        numFeedBackDictionary[rating] = feedList
                    #-----------------------------------------------------------------------------
                    #Adding num Helpful FeedBack
                    numHelpfulFeedback = 0
                    if review[4] != "":
                        numHelpfulFeedback = int(review[4])
                    try:
                        feedList = numHelpFeedDictionary[rating]
                        feedList.append((numHelpfulFeedback,currentDay))
                        numHelpFeedDictionary[rating] = feedList
                    except KeyError as e:
                        feedList = []
                        feedList.append((numHelpfulFeedback,currentDay))
                        numHelpFeedDictionary[rating] = feedList
                    #-----------------------------------------------------------------------------
                    #print(currentDay)
                    #print(rating)
                    #print(numHelpfulFeedback)
                    #print(numFeedback)
                    helpfulness = 0
                    if numFeedback !=0:
                        helpfulness = numHelpfulFeedback/numFeedback
                    #print(helpfulness)
    #print(numFeedBackDictionary)
    #print(numHelpFeedDictionary)

    average = sumRatings/len(productDates)
    '''
    for key,value in ratingsDateDictionary.items():
        print(key)
        for val in value:
            print(val)
    '''

    diff = (maxDate-minDate).days
    n = len(productDates)
    ''' larger to smaller
    if diff > 5000:
        n = 40
    elif diff > 4000 and diff<=5000:
        n = 40
    elif diff > 3000 and diff<=4000:
        n = 30
    elif diff > 2000 and diff<=3000:
        n = 25
    elif diff > 1000 and diff<=2000:
        n = 20
    elif diff > 500 and diff<=1000:
        n = 20
    elif diff > 300 and diff<=500:
        n = 15
    else:
        n = 20
    '''

    ''' Smaller to Larger
    if diff > 5000:
        n = 50
    elif diff > 4000 and diff<=5000:
        n = 45
    elif diff > 3000 and diff<=4000:
        n = 40
    elif diff > 2000 and diff<=3000:
        n = 35
    elif diff > 1000 and diff<=2000:
        n = 30
    elif diff > 500 and diff<=1000:
        n = 20
    elif diff > 300 and diff<=500:
        n = 10
    else:
        n = 5
    '''
    #for day in productDates:
     #   print(day)

    '''
     sortedDates = productDates
    n = 10
    quickSortList(sortedDates)
    timeInterval = []
    counter = 0
    numReviews = len(productDates)
    numAllowed = int(numReviews/n)
    index = 0
    for i in range(n):
        if index<len(sortedDates):
            timeInterval.append(sortedDates[index])
            index = index+numAllowed
        else:
            break
    del timeInterval[-1]
    timeInterval.append(maxDate)

    #print(timeInterval)
    '''
    tempDate = minDate
    timeInterval = []
    timeInterval.append(tempDate)
    #numDays = int(diff/n)

    n = 10
    numDays = int(diff/n)
    #print(n)
    #print(diff)
    #print(numDays)
    #print("--")
    for i in range(n):
           tempDate = tempDate + timedelta(days=numDays)
           timeInterval.append(tempDate)


    del timeInterval[-1]
    timeInterval.append(maxDate)
    if len(ratingsDateDictionary) < 5:
        #Just adding missing keys
        if ratingsDateDictionary.get(1) == None:
            ratingsDateDictionary[1] = []
        if ratingsDateDictionary.get(2) == None:
            ratingsDateDictionary[2] = []
        if ratingsDateDictionary.get(3) == None:
            ratingsDateDictionary[3] = []
        if ratingsDateDictionary.get(4) == None:
            ratingsDateDictionary[4] = []
        if ratingsDateDictionary.get(5) == None:
            ratingsDateDictionary[5] = []

    if len(numFeedBackDictionary) < 5:
        # Just adding missing keys
        if numFeedBackDictionary.get(1) == None:
            numFeedBackDictionary[1] = []
        if numFeedBackDictionary.get(2) == None:
            numFeedBackDictionary[2] = []
        if numFeedBackDictionary.get(3) == None:
            numFeedBackDictionary[3] = []
        if numFeedBackDictionary.get(4) == None:
            numFeedBackDictionary[4] = []
        if numFeedBackDictionary.get(5) == None:
            numFeedBackDictionary[5] = []

    if len(numHelpFeedDictionary) < 5:
        # Just adding missing keys
        if numHelpFeedDictionary.get(1) == None:
            numHelpFeedDictionary[1] = []
        if numHelpFeedDictionary.get(2) == None:
            numHelpFeedDictionary[2] = []
        if numHelpFeedDictionary.get(3) == None:
            numHelpFeedDictionary[3] = []
        if numHelpFeedDictionary.get(4) == None:
            numHelpFeedDictionary[4] = []
        if numHelpFeedDictionary.get(5) == None:
            numHelpFeedDictionary[5] = []

    starTimeIntervalRewards = []
    ratingTemproalCategory = []
    for key,value in ratingsDateDictionary.items():
        ratingDates = value
        ratingIntervals = []
        for ratingdate in ratingDates:
            for i in range(len(timeInterval)-1):
                 if (ratingdate >= timeInterval[i] and ratingdate < timeInterval[i+1]) or (ratingdate > timeInterval[i] and ratingdate <= timeInterval[i+1]):
                    ratingIntervals.append((i+1))
                    break

        #print(ratingIntervals)
        intervalDict = dict()
        for item in ratingIntervals:
            try:
                val = intervalDict[item]
                val = val + 1
                intervalDict[item] = val
            except KeyError as e:
                intervalDict[item] = 1

        #print(intervalDict)
        ratingTemproalCategory.append(intervalDict)

    ratingVotes = []
    for key,value in numFeedBackDictionary.items():
        feedbackDates = value
        ratingIntervals = []
        for feedDate in feedbackDates:
            ratingdate = feedDate[1]
            for i in range(len(timeInterval)-1):
                if (ratingdate >= timeInterval[i] and ratingdate < timeInterval[i+1]) or (ratingdate > timeInterval[i] and ratingdate <= timeInterval[i+1]):
                    ratingIntervals.append(((i+1),feedDate[0]))
                    break
        intervalDict = dict()
        for item in ratingIntervals:
            try:
                val = intervalDict[item[0]]
                val = val + item[1]
                intervalDict[item[0]] = val
            except KeyError as e:
                intervalDict[item[0]] = item[1]
        ratingVotes.append(intervalDict)
        #print(intervalDict)

    #print("-----------------------------------------------------")
    ratingHelpfulness = []
    for key,value in numHelpFeedDictionary.items():
        feedbackDates = value
        ratingIntervals = []
        for feedDate in feedbackDates:
            ratingdate = feedDate[1]
            for i in range(len(timeInterval)-1):
                 if (ratingdate >= timeInterval[i] and ratingdate < timeInterval[i+1]) or (ratingdate > timeInterval[i] and ratingdate <= timeInterval[i+1]):
                    ratingIntervals.append(((i+1),feedDate[0]))
                    break
        intervalDict = dict()
        for item in ratingIntervals:
            try:
                val = intervalDict[item[0]]
                val = val + item[1]
                intervalDict[item[0]] = val
            except KeyError as e:
                intervalDict[item[0]] = item[1]

        ratingHelpfulness.append(intervalDict)
    resulTemproalCategoryRating = []
    '''print("ratingTemproalCategory")
    print(len(ratingsDateDictionary))
    print(ratingsDateDictionary)
    print(len(ratingTemproalCategory))
    print(ratingTemproalCategory)
    '''
    if len(ratingTemproalCategory) > 5:
        del ratingTemproalCategory[-1]
    for cat in ratingTemproalCategory:
               timePeriodDict = dict()
               for i in range(n+1):
                   timePeriodDict[i]=0
               #timePeriodDict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
               for item in cat:
                   try:
                        timePeriodDict[item] = cat[item]
                   except KeyError as e:
                        pass
               resulTemproalCategoryRating.append(timePeriodDict)
    resulTemproalVotesDictionary= []
    for cat in ratingVotes:
               #timePeriodDict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
               timePeriodDict = dict()
               for i in range(n+1):
                   timePeriodDict[i]=0
               for item in cat:
                   try:
                        timePeriodDict[item] = cat[item]
                   except KeyError as e:
                        pass
               resulTemproalVotesDictionary.append(timePeriodDict)

    resulTemproalHelpFeedDictionary= []
    for cat in ratingHelpfulness:
               #timePeriodDict = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0}
               timePeriodDict = dict()
               for i in range(n+1):
                   timePeriodDict[i]=0
               for item in cat:
                   try:
                        timePeriodDict[item] = cat[item]
                   except KeyError as e:
                        pass
               resulTemproalHelpFeedDictionary.append(timePeriodDict)

    resulTemproalHelpfulnessWeight = []
    for i in range(len(resulTemproalVotesDictionary)):
        helpfulnessDict = dict()
        for val in resulTemproalVotesDictionary[i]:
            numVotes = resulTemproalVotesDictionary[i][val]
            helpfulVotes = resulTemproalHelpFeedDictionary[i][val]
            helpfulness = 0
            if numVotes != 0:
                helpfulness = helpfulVotes/numVotes
            helpfulnessDict[val] = helpfulness
        resulTemproalHelpfulnessWeight.append(helpfulnessDict)

    return resulTemproalCategoryRating,resulTemproalHelpfulnessWeight,n,average,numReviews,numFeedBackDictionary,numHelpFeedDictionary,ratingsDateDictionary
def getProductAllLiefCycle(productidPath):
    productDates = []
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    with open(productidPath, 'r') as fp:
        for line in fp:
            review = line.split('\t')
            #----------------------------------------------------------------------------
            #Extracting Date
            datesplit = review[2].split(',')
            monthDay = datesplit[0]
            month = ""
            day = ""
            monthDone = 0
            for char in monthDay:
                if char != " " and monthDone== 0:
                    month = month + char
                if char == " ":
                    monthDone = 1
                if monthDone== 1:
                    day = day + char
            if len(datesplit)>1 and datesplit[1]!=' ' and len(datesplit[1])<=5:
                year = int(datesplit[1])
                month = int(month)
                day = int(day)

                currentDay = datetime(year, month, day)
                productDates.append((currentDay))
                if currentDay >maxDate:
                    maxDate = currentDay
                if currentDay <minDate:
                    minDate = currentDay
    diff = (maxDate-minDate).days
    return diff,len(productDates)
def getProductAllLiefCycleTest(productidPath):
    productDates = []
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    with open(productidPath, 'r') as fp:
        for line in fp:
            review = line.split('\t')
            #----------------------------------------------------------------------------
            #Extracting Date
            datesplit = review[2].split(',')
            monthDay = datesplit[0]
            month = ""
            day = ""
            monthDone = 0
            for char in monthDay:
                if char != " " and monthDone== 0:
                    month = month + char
                if char == " ":
                    monthDone = 1
                if monthDone== 1:
                    day = day + char
            if len(datesplit)>1 and datesplit[1]!=' ' and len(datesplit[1])<=5:
                year = int(datesplit[1])
                month = int(month)
                day = int(day)

                currentDay = datetime(year, month, day)
                productDates.append((currentDay))
                if currentDay >maxDate:
                    maxDate = currentDay
                if currentDay <minDate:
                    minDate = currentDay
    diff = (maxDate-minDate).days
    #for day in productDates:
     #   print(day)
    print("num Reviews")
    numReviews = len(productDates)
    print(numReviews)
    print("Num Periods")
    n = 20
    print(n)
    print("--------------------")
    sortedDates = productDates

    quickSortList(sortedDates)
    timeInterval = []
    counter = 0
    numAllowed = int(numReviews/n)
    print("numAllowed")
    print(numAllowed)
    index = 0
    for i in range(n):
        if index<len(sortedDates):
            timeInterval.append(sortedDates[index])
            index = index+numAllowed
        else:
            break
    del timeInterval[-1]
    timeInterval.append(maxDate)
    print("timeInterval")
    print(timeInterval)
    print(len(timeInterval))
    for day in timeInterval:
        print(day)
    print("minDate")
    print(minDate)
    print("MaxDate")
    print(maxDate)
    ratingInervals = dict()
    for day in productDates:
     for i in range(len(timeInterval)-1):
                if day >= timeInterval[i] and day < timeInterval[i+1]:
                    try:
                         days = ratingInervals[timeInterval[i]]
                         days.append(day)
                         ratingInervals[timeInterval[i]] = days
                    except KeyError as e:
                        days = []
                        days.append(day)
                        ratingInervals[timeInterval[i]] = days
                    break

    counter = 0
    for key,value in ratingInervals.items():
        print(len(value))
        for item in value:
            counter+=1
    print("num")
    print(counter)
    return diff,len(productDates)
def createVerifiedProducts(verifiedSourceDirectory,productBaseCategory,destDirectory,startFrom):
    index = 0
    for directory in os.listdir (verifiedSourceDirectory):
        if index >= startFrom:
            categoryPath = verifiedSourceDirectory +directory
            print("Considering "+directory)
            for filename in os.listdir (categoryPath):
                verifiedProductPath = categoryPath+"/"+filename
                baseProductPath = productBaseCategory+filename
                verifiedList = dict()
                verCount = 0
                allCount = 0
                if not os.path.exists(destDirectory+directory):
                    os.makedirs(destDirectory+directory)
                newVerProductRevewsFile = destDirectory+directory+"/"+filename
                print(filename)
                filehandle = open(newVerProductRevewsFile,'w')
                with open(verifiedProductPath, 'r') as fp:
                    for line in fp:
                        record = line.split("\t")
                        #print(record)
                        verf = int(record[len(record)-1])
                        record = line.split(" ")
                        user = record[0]
                        if verf == 1:
                            verifiedList[user] = 1
                            verCount+=1
                        allCount+=1
                with open(baseProductPath, 'r') as fp:
                    for line in fp:
                        review = line.split("\t")
                        try:
                            verUser = verifiedList[review[0]]
                            filehandle.write(line)
                        except KeyError as e:
                            pass
                filehandle.close()

        index+=1
    return
def countProductsByCategory(destDirectory):
    for directory in os.listdir (destDirectory):
        categoryPath = destDirectory +directory
        productCount = 0
        numReviews = 0
        for filename in os.listdir (categoryPath):
            verifiedProductPath = categoryPath+"/"+filename
            #print(verifiedProductPath)
            with open(verifiedProductPath, 'r') as fp:
                    for line in fp:
                        numReviews+=1
            if numReviews >= 1000:
                productCount+=1
        #print("Considering "+directory+"\t\t\t\t\t\t\t"+str(productCount))
        print(str(productCount))
    return
def writeProductsByCategorywithThresholdVerified(sourceDirectory,destDirectory,threshold):
    for directory in os.listdir (sourceDirectory):
        categoryPath = sourceDirectory +directory
        numReviews = 0
        print("Considering "+categoryPath)
        newDirectory = "Dataset_L_"+str(threshold)
        if not os.path.exists(destDirectory+newDirectory):
            os.makedirs(destDirectory+newDirectory)
        categoryFilePathToWrite = destDirectory+newDirectory+"/"+directory+".txt"
        filehandle = open(categoryFilePathToWrite,'w')
        for filename in os.listdir (categoryPath):
            productName = filename.split(".")
            productName = productName[0]
            verifiedProductPath = categoryPath+"/"+filename
            numReviews = 0
            with open(verifiedProductPath, 'r') as fp:
                    for line in fp:
                        numReviews+=1
            if numReviews < threshold and numReviews !=0:
                filehandle.write(productName)
                filehandle.write("\n")
        filehandle.close()
    return
def writeProductsByCategorywithThresholdNonVerified(sourceDirectory,complementDataset,destDirectory,threshold):

    for directory in os.listdir(sourceDirectory):
        categoryPath = sourceDirectory + directory
        print("Considering " + directory)
        newDirectory = "Dataset_L_" + str(threshold)
        if not os.path.exists(destDirectory + newDirectory):
            os.makedirs(destDirectory + newDirectory)
        originalProducts = dict()
        with open(categoryPath, 'r') as fp:
            for line in fp:
                product = line.split("\t")
                product = product[0]
                originalProducts[product] = 0

        categoryPath = complementDataset + directory

        complentList = []
        with open(categoryPath, 'r') as fp:
            for line in fp:
                product = line.split("\t")
                product = product[0].split("\n")
                product = product[0]

                complentList.append(product)

        for product in complentList:
            originalProducts[product] = 1

        categoryFilePathToWrite = destDirectory + newDirectory + "/" + directory
        filehandle = open(categoryFilePathToWrite, 'w')

        for key, value in originalProducts.items():
            if value == 0:
                filehandle.write(key)
                filehandle.write("\n")
        filehandle.close()


    return
#----------------------------------Programs Start here ---------------------------------------------------------------------------------
import sys
import os
from alogrithms import *
from datetime import datetime
from datetime import timedelta
'''
#----------------------------------Get Number of products of category with certain threshold--------------- -------------------------------------------------------------
#categories_path = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/categories/"
#productBaseDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Product_Reviews/"
categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
threshold = 1000#int(raw_input("Input Threshold "))
destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/"
newDirectory = destDirectory+"Dataset_"+str(threshold)
if not os.path.exists(newDirectory):
    os.makedirs(newDirectory)
getProductsWithNumberofReviewsThreshold(categories_path,productBaseDirectory,newDirectory,destDirectory,threshold)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

'''
#----------------------------------Take all categories and subset products and give the difference products -------------------------------------------------------------
categoriesOriginalDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
biggerThresholdDirectory= "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/Dataset_50"
destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/Dataset_less_50/"
getProductsWithNumberofReviewsThresholdFromOther(categoriesOriginalDirectory,biggerThresholdDirectory,destDirectory)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''
'''
#--------------------------------------------------------------Create Sales rank based on sub group or product category--------------------------------------------------
categoriesOriginalDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_sales_rank/"
newDatasetDirectory= "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/Dataset_L_100/"
destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_non_verified/categores_sorted_sales_rank_dataset_less_100/"
createNewSortedSalesRankListForCertainDataSet(categoriesOriginalDirectory,newDatasetDirectory,destDirectory)
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

#productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
#productId = "B000LXHJDM"
#analyzeProduct(productBaseDirectory,productId)
#productIDPath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/B0000CBK1L.txt"
#getProductAllLiefCycleTest(productIDPath)
#verifiedSourceDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories_verified/"
#productBaseCategory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
#destDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Product_Reviews_Verified/"
#createVerifiedProducts(verifiedSourceDirectory,productBaseCategory,destDirectory,27)
#------------------------------Creating Dataset for certain number of reviews-----------------------------------------------------------------------
'''
#sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Product_Reviews_verfified/"
sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
complementDataset = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/Dataset_100/"
destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/"
threshold = 100
#writeProductsByCategorywithThresholdVerified(sourceDirectory,destDirectory,threshold)
writeProductsByCategorywithThresholdNonVerified(sourceDirectory,complementDataset,destDirectory,threshold)
'''
#--------------------Counting number of reviews for each product category
'''directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets_Verified/Dataset_30/"
for filename in os.listdir (directory):
        verifiedProductPath = directory+"/"+filename
        numReviews = 0
        #print(filename)
        with open(verifiedProductPath, 'r') as fp:
                for line in fp:
                    numReviews+=1
        print(numReviews)

'''

'''
productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
productId = "B001HDOQHM"
#analyzeProduct(productBaseDirectory,productId)



filePath = "//ntapprdfs01n01.rmit.internal\sl6\s3525116\Configuration\Desktop/test.txt"

with open(filePath, 'r') as fp:
     ratings = []
     total = []
     helpful = []
     for line in fp:
         row = line.split("\t")
         ratings.append(float(row[0]))
         helpful.append(int(row[1]))
         total.append(int(row[2]))
     sum = len(ratings)
     index = 0
     average = 0
     sumHelp = 0
     sumTotal = 0
     num = int(sum/10)
     overall = 0
     lastAverage = 0
     lastHelpful = 0
     lastTotal = 0
     bShowAverage = 1
     bShowHelpful = 0
     bShowTotal = 0
     for i in range(sum):
         average+=ratings[i]
         #print(ratings[i])
         overall+=ratings[i]
         sumHelp+=helpful[i]
         sumTotal+=total[i]
         if index == num-1:
             #print("avg")
             lastAverage = round(average/num,3)
             lastHelpful = sumHelp
             lastTotal = sumTotal
             if sum-i > num:
                if bShowAverage:
                    print(lastAverage)
                if bShowHelpful:
                    print(lastHelpful)
                if bShowTotal:
                    print(lastTotal)
             average = 0
             sumHelp = 0
             sumTotal = 0
             index = 0
         else:
             index = index + 1

     if index >0:
         avg = round(average/index,6)
         lastAverage = round((lastAverage+avg)/2,3)
         if bShowAverage:
            print(lastAverage)
         if bShowHelpful:
            print(lastHelpful)
         if bShowTotal:
            print(lastTotal)

     overall = round(overall/sum,3)
     print("------")
     print(overall)

'''
