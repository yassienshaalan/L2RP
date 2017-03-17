__author__ = 's3525116'
from user_data import *
#from reviews import *
from helper_Functions import *
import csv
#-----------------------------------------------------------------------------------------------------------------------
def createReviewFromRecord(record):
    numFields = len(record)
    review = ""
    if numFields == 7:
       review = Review(record[0],record[1],record[2],record[3],record[4],record[5],record[6])
    return review
#-----------------------------------------------------------------------------------------------------------------------
def retrieveNumberofReviewsAboveNumInFile(threshold):
    #File numProductReviews.txt Structure
    #PorductId \t NumReviews
    print("Procedure to Count Number of Products with Number of Reviews Above",threshold)
    print("Started")
    newFileName = "C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary/Product_Queries/"+"Products_With_More_Than_"+str(threshold-1)+"_views.txt"
    newFileHandle = open(newFileName,'w')
    data_initial = open("C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary/numProductReviews.txt", "rU")
    counter = 0
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    for row in reader:
        temp = [i.split('\t') for i in row]
        temp = list(temp[0])
        if int(temp[1]) >= threshold:
            counter = counter + 1
            newFileHandle.write(temp[0])
            newFileHandle.write("\n")
    newFileHandle.close()
    print("Number of products",counter)
    print("Finished")
    return
#-----------------------------------------------------------------------------------------------------------------------
#import statistics
def calculateProductRating(filePath):
    '''
    The product file line syntax
    <member id> \t <product id> \t <date> \t <number of helpful feedbacks> \t <number of feedbacks> \t <rating> \t <title> \t <body>
    :param filePath:
    :return:
    '''
    '''
    :param filePath:
    :return:
    '''
    print("Procedure to Calculate product rating from file")
    print("Started")
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    allweightedRating = []
    allzscores = []
    allsuspectZscores = []
    allsuspectIndex = []
    allsuspectValues  = []
    productnames = []
    allsuspectReview = []
    allsuspectReviewObjects = []
    for row in reader:
        extractString = str(row)
        productname = ""
        for char in extractString:
            if char !='[' and char != ']' and char != "'":
                productname = productname + char
        newFilePath = "C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary\Products/"+productname
        new_data_initial = open(newFilePath, "rU")
        newreader = csv.reader((line.replace('\0','') for line in new_data_initial), delimiter='\n')
        productnames.append(productname)
        allReviews = []
        weightedRating = []
        zscores = []
        suspectZscores = []
        suspectIndex = []
        suspectValues  = []
        suspectReview = []
        suspectReviewObjects = []

        for newrow in newreader:
         temp = [i.split('\t') for i in newrow]
         temp = list(temp[0])
         allReviews.append(temp)

        #Intially set all memeber weight to 1 all honest and equal
        memberWeight = dict([(record[0], 1) for record in allReviews])
        #Adjust review rating to be weighted rating

        for rev in allReviews:
            memIdWeight = memberWeight.get(rev[0])
            convertedtoNum = float(rev[5])
            if memIdWeight != None:
                newRate = convertedtoNum*memIdWeight
                weightedRating.append(newRate)
            else:
                newRate = convertedtoNum
                weightedRating.append(newRate)

        numReviews = len(weightedRating)
        mean = statistics.mean(weightedRating)
        std = statistics.stdev(weightedRating)
        pstdev = statistics.pstdev(weightedRating)
        pvariance = statistics.pvariance(weightedRating)
        median_low = statistics.median_low(weightedRating)
        median_high = statistics.median_high(weightedRating)

        index = 0
        for rate in weightedRating:
            if (rate-mean)== 0:
                tempval = 0
            else:
                tempval = (rate-mean)/std
            zscores.append(round(tempval,3))
            if tempval < 0:
                tempval = tempval * -1
            if tempval > 1.1:
                suspectZscores.append(round(tempval,3))
                suspectValues.append(rate)
                suspectIndex.append(index)
                suspectReview.append(allReviews[index])
                reviewtest = createReviewFromRecord(allReviews[index])
                suspectReviewObjects.append(reviewtest)
                #printReview(reviewtest)
            index = index + 1


        zscore = mean - 4
        if std== 0:
            zscore = 0
        else:
            zscore = zscore/std
        coffVariance = std/mean
        pAgree = 0
        pNAgree = 0
        for rate in weightedRating:
            if rate == 4 or rate == 5:
                pAgree = pAgree + 1
            elif rate == 1 or rate == 2 or rate == 3:
                pNAgree = pNAgree + 1

        pAgree = pAgree/numReviews
        pAgree = round(pAgree*100)
        pNAgree = pNAgree/numReviews
        pNAgree = round(pNAgree*100)

        '''
        print("Statistics")
        print("----------------------------------------------------------------------------------------------------")
        text = "Mean = "+str(round(mean,3))
        print(text)
        text = "Std = "+str(round(std,3))
        print(text)
        text = "Pvariance = "+str(round(pvariance,3))
        print(text)
        text = "Pstdev = "+str(round(pstdev,3))
        print(text)
        text = "ZScore_General = "+str(round(zscore,3))
        print(text)
        text = "coffVariance = "+str(round(coffVariance*100,3))+"%"
        print(text)
        text = "pAgree = "+str(pAgree)+"%"
        print(text)
        text = "pNAgree = "+str(pNAgree)+"%"
        print(text)
        text = "median_low = "+str(median_low)
        print(text)
        text = "median_high = "+str(median_high)
        print(text)
        print("----------------------------------------------------------------------------------------------------")
        print("numReviews")
        print(numReviews)
        print(weightedRating)
        print("zscores")
        print(zscores)
        print("suspectZscores")
        print(suspectZscores)
        print("suspectValues")
        print(suspectValues)
        print("suspectIndex")
        print(suspectIndex)
        print("suspectReview")
        for rev in suspectReview:
            print(rev)
        print("----------------------------------------------------------------------------------------------------")
        '''

        #Creating Z Table
        '''print("Creating ZTable")
        from tabulate import tabulate
        table = [[0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09],[0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09], [0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09],[0.00,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09]]
        print(tabulate(table))'''
        #writing in Excel File
        allweightedRating.append(weightedRating)
        allzscores.append(zscores)
        allsuspectIndex.append(suspectIndex)
        allsuspectZscores.append(suspectZscores)
        allsuspectValues.append(suspectValues)
        allsuspectReview.append(suspectReview)
        allsuspectReviewObjects.append(suspectReviewObjects)

        counter = counter + 1
        #if counter == 1:
         #  break
    #writeAnalysisExcelFile("C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary/analysis.xls","sheet_1",productnames,allweightedRating,"weightedRating",allzscores,"zscores",allsuspectZscores,"suspectZscores",allsuspectValues,"suspectValues",allsuspectIndex,"suspectIndex",)
    writeAnalysisTextFile("C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary/analysis/analysis.txt",productnames,allweightedRating,"weightedRating",allzscores,"zscores",allsuspectZscores,"suspectZscores",allsuspectValues,"suspectValues",allsuspectIndex,"suspectIndex")
    writeSuspectReviews("C:\Yassien_RMIT PhD\Datasets\Liu_Amazon_Dataset\Primary/analysis/suspect_reviews.txt",productnames,allsuspectReview)
    print("Finished")
    return
#-----------------------------------------------------------------------------------------------------------------------
def writeReviewToFile(fileHandle,review):
     print(review)
     print(type(review))
     nSize = len(review)
     for i in range(nSize):
         fileHandle.write(review[i])
         if i < nSize-1:
            fileHandle.write("\t")
     return
def writeSuspectReviews(filename,productnames,allsuspectReview):
    print("Writing suspect revies txt file")
    print(filename)
    suspectReviews = open(filename,'w')
    index = 0
    suspectReviews.write("#<member id> \t <product id> \t <date> \t <number of helpful feedbacks> \t <number of feedbacks> \t <rating> \t <title> \t <body>\n")
    for item in productnames:
        suspectReviews.write("ProductId")
        suspectReviews.write("\t")
        suspectReviews.write(productnames[index])
        suspectReviews.write("\n")
        for interitem in allsuspectReview[index]:
            #suspectReviews.write(str(interitem))
            writeReviewToFile(suspectReviews,interitem)
            suspectReviews.write("\n")
        index = index + 1
        suspectReviews.write("\n")
    return
def writeAnalysisTextFile(filename,productnames, list1,title1,list2,title2,list3,title3,list4,title4,list5,title5):
    print("Writing Analysis txt file")
    print(filename)
    analysisFile = open(filename,'w')
    row = 0
    column = 0
    index = 0
    for item in list1:
        analysisFile.write("ProductId")
        analysisFile.write("\t")
        analysisFile.write(productnames[index])
        analysisFile.write("\n")

        analysisFile.write(title1)
        analysisFile.write("\t")
        for interitem in list1[index]:
            analysisFile.write(str(interitem))
            analysisFile.write("\t")

        analysisFile.write("\n")
        analysisFile.write(title2)
        analysisFile.write("\t")
        analysisFile.write("\t")
        for interitem in list2[index]:
            analysisFile.write(str(interitem))
            analysisFile.write("\t")

        analysisFile.write("\n")
        analysisFile.write(title3)
        analysisFile.write("\t")
        for interitem in list3[index]:
            analysisFile.write(str(interitem))
            analysisFile.write("\t")

        analysisFile.write("\n")
        analysisFile.write(title4)
        analysisFile.write("\t")
        for interitem in list4[index]:
            analysisFile.write(str(interitem))
            analysisFile.write("\t")

        analysisFile.write("\n")
        analysisFile.write(title5)
        analysisFile.write("\t")
        for interitem in list5[index]:
            analysisFile.write(str(interitem))
            analysisFile.write("\t")

        analysisFile.write("\n")
        index = index + 1

    analysisFile.close()

    print("Finished Analysis text file")
    return
'''
import xlwt
def writeAnalysisExcelFile(filename, sheetname,productnames, list1,title1,list2,title2,list3,title3,list4,title4,list5,title5):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheetname)
    print("Writing Analysis Excel file")
    print(filename)
    row = 0
    column = 0
    index = 0
    print("len"+str(len(list1)))
    for item in list1:
        column = 0
        sh.write(row, column, "ProductId")
        sh.write(row, column+1, productnames[index])
        sh.write(row+1, column, title1)
        sh.write(row+2, column, title2)
        sh.write(row+3, column, title3)
        sh.write(row+4, column, title4)
        sh.write(row+5, column, title5)
        column = 1
        print("product name")
        print(productnames[index])
        print(len(list1[index]))
        print(list1[index])
        for interitem in list1[index]:
            sh.write(row+1, column, interitem)
            column = column + 1

        column = 1

        for interitem in list2[index]:
            sh.write(row+2, column, interitem)
            column = column + 1

        column = 1

        for interitem in list3[index]:
            sh.write(row+3, column, interitem)
            column = column + 1

        column = 1

        for interitem in list4[index]:
            sh.write(row+4, column, interitem)
            column = column + 1
        column = 1

        for interitem in list5[index]:
            sh.write(row+5, column, interitem)
            column = column + 1

        row = row +6
        index = index + 1

    book.save(filename)

    print("Finished Analysis file")
    return
'''
def extractReviewFromList(list):

    return Review(list[0],list[1],list[2],list[3],list[4],list[5],list[6])
#-----------------------------------------------------------------------------------------------------------------------
def readSuspectedReviews(filePath):
    '''
    Parsing file suspectedReviews.txt
    Comment At the begining #<member id> 	 <product id> 	 <date> 	 <number of helpful feedbacks> 	 <number of feedbacks> 	 <rating> 	 <title> 	 <body>
    ProductId	value
    reviews
    ProductId	value
    reviews
    '''
    #This function return a dictonary of members with the key of member id
    print("Procedure to Parse suspectedReviews' Data")
    print("Started")
    allMembers = []
    counter = 0
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    bFirst = 0
    counter = 0
    listReviews = []
    priductId = ""
    suspectReviewDict = dict()
    for row in reader:
       if bFirst == 0:
           bFirst = 1   #ignoring the comment line at the begining
           continue
       if row != []:
           tempStr = [i.split('\t') for i in row]
           temp=list(tempStr[0])
           nSize = len(temp)
           if nSize == 2:
               if len(listReviews) > 0:
                   suspectReviewDict[priductId] = listReviews
               else:
                   listReviews = []
               priductId = temp[1]
           elif nSize == 7:
               review = extractReviewFromList(temp)
               listReviews.append(review)


    if len(listReviews) > 0:
       suspectReviewDict[priductId] = listReviews
    counter = counter + 1

    print("suspectReviewDict")
    #print(suspectReviewDict)
    print(len(suspectReviewDict))
    print("Finished")
    return suspectReviewDict
#-----------------------------------------------------------------------------------------------------------------------
def countNumberofVotes(filePath):
    '''
    The product file line syntax
    <member id> \t <product id> \t <date> \t <number of helpful feedbacks> \t <number of feedbacks> \t <rating> \t <title> \t <body>
    :param filePath:
    '''
    print("Procedure to Calculate number of votes from file")
    print("Started")
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    numReviews = 0
    numValidReviews = 0
    votesFile = open("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Liu_Amazon_Dataset\Primary/Review_Dates.txt",'w')
    productnames = []
    for row in reader:
        extractString = str(row)
        productname = ""
        for char in extractString:
            if char !='[' and char != ']' and char != "'":
                productname = productname + char
        newFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Liu_Amazon_Dataset\Primary\Products_Unique/"+productname
        new_data_initial = open(newFilePath, "rU")
        newreader = csv.reader((line.replace('\0','') for line in new_data_initial), delimiter='\n')
        productnames.append(productname)
        allReviews = []
        counter = counter + 1
        for newrow in newreader:
         temp = [i.split('\t') for i in newrow]
         temp = list(temp[0])
         allReviews.append(temp)

        for rev in allReviews:
            toko = str(rev[2])
            toko = toko.split(",")
            if len(toko) > 1:
                votesFile.write(toko[1])
                votesFile.write("\n")
                numValidReviews = numValidReviews + 1
            numReviews = numReviews + 1

    votesFile.close()
    print("Number of Products")
    print(counter)
    print("Number of Reviews for all products")
    print(numReviews)
    print("Number of valid Reviews")
    print(numValidReviews)
    print("Finished")
    return
#import statistics
def countDatesofReviewsPerProduct(filePath):
    '''
    The product file line syntax
    <member id> \t <product id> \t <date> \t <number of helpful feedbacks> \t <number of feedbacks> \t <rating> \t <title> \t <body>
    :param filePath:
    '''
    print("Procedure to Calculate number of votes from file")
    print("Started")
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    numReviews = 0
    numValidReviews = 0
    #votesFile = open("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Liu_Amazon_Dataset\Primary/Review_Dates_Per_Product.txt",'w')
    analysisFile = open("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Liu_Amazon_Dataset\Primary/tempo.txt",'w')
    productnames = []
    '''
    analysisFile.write("Cof-Var")
    analysisFile.write("\t")
    analysisFile.write("Min")
    analysisFile.write("\t\t")
    analysisFile.write("Max")
    analysisFile.write("\t\t")
    analysisFile.write("Mean")
    analysisFile.write("\t\t")
    analysisFile.write("Std")
    analysisFile.write("\n")
    '''
    for row in reader:
        extractString = str(row)
        productname = ""
        for char in extractString:
            if char !='[' and char != ']' and char != "'":
                productname = productname + char
        newFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Liu_Amazon_Dataset\Primary\Products_Unique/"+productname
        new_data_initial = open(newFilePath, "rU")
        newreader = csv.reader((line.replace('\0','') for line in new_data_initial), delimiter='\n')
        productnames.append(productname)
        allReviews = []
        counter = counter + 1
        for newrow in newreader:
         temp = [i.split('\t') for i in newrow]
         temp = list(temp[0])
         allReviews.append(temp)
        dates = []
        min = 10000000
        max = 0
        for rev in allReviews:
            toko = str(rev[2])
            toko = toko.split(",")
            if len(toko) > 1:
                #votesFile.write(toko[1])
                year = int(toko[1])
                if year > max:
                    max = year
                if year < min:
                    min = year
                dates.append(year)
                #votesFile.write("\t")
                numValidReviews = numValidReviews + 1
            numReviews = numReviews + 1

        mean = statistics.mean(dates)
        std = statistics.stdev(dates)

        #analysisFile.write(str(round(mean,3)))
        #analysisFile.write("\t")
        analysisFile.write(str(round((std/mean)*100,3)))
        '''
        analysisFile.write("\t")
        analysisFile.write(str(min))
        analysisFile.write("\t")
        analysisFile.write(str(max))
        analysisFile.write("\t")
        analysisFile.write(str(round(mean,3)))
        analysisFile.write("\t")
        analysisFile.write(str(round(std,3)))
        analysisFile.write("\t")

        '''
        analysisFile.write("\n")
        #if counter == 10:
         #   break
        #votesFile.write("\n")

    #votesFile.close()
    analysisFile.close()

    print("Number of Products")
    print(counter)
    print("Number of Reviews for all products")
    print(numReviews)
    print("Number of valid Reviews")
    print(numValidReviews)
    print("Finished")
    return
def countNumberofVotesFromFolder(directory):
    '''
    The product file line syntax
    <member id> \t <product id> \t <date> \t <number of helpful feedbacks> \t <number of feedbacks> \t <rating> \t <title> \t <body>
    :param filePath:
    '''
    print("Procedure to Calculate number of votes from Folder")
    print("Started")
    votesFile = open("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/num_Votes.txt",'w')
    counter = 0
    numReviews = 0
    numValidReviews = 0
    productnames = []
    for filename in os.listdir (directory):
        filename = directory + "/"+filename
        new_data_initial = open(filename, "rU")
        newreader = csv.reader((line.replace('\0','') for line in new_data_initial), delimiter='\n')
        productnames.append(filename)
        allReviews = []
        counter = counter + 1
        for newrow in newreader:
         temp = [i.split('\t') for i in newrow]
         temp = list(temp[0])
         allReviews.append(temp)

        for rev in allReviews:
            votesFile.write(rev[3])
            votesFile.write("\n")
            numValidReviews = numValidReviews + 1
            numReviews = numReviews + 1
        #if counter == 1:
         #   break
    votesFile.close()
    print("Number of Products")
    print(counter)
    print("Number of Reviews for all products")
    print(numReviews)
    print("Number of valid Reviews")
    print(numValidReviews)
    print("Finished")
    return
def getProductsWithNumberofReviewsThreshold(directory,filePathOfResult,threshold):
    print("Procedure to Count Number of Reviews for each Product")
    print("Started")
    numProductReviews = open(filePathOfResult,'w')
    for filename in os.listdir (directory):
        productID = filename
        filename = directory + "/"+filename
        data_initial = open(filename, "rU")
        counter = 0
        reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
        for row in reader:
            counter = counter + 1
        if counter >= threshold:
            print(counter)
            numProductReviews.write(str(productID))
            numProductReviews.write("\t")
            numProductReviews.write(str(counter))
            numProductReviews.write("\n")
    numProductReviews.close()
    print("Finished")
    return