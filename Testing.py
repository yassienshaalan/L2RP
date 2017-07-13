import os
from datetime import datetime
#print("Using the LETOR Testing Script ")
#os.chdir("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/MSLR-WEB10K\Fold1/")

##command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-score-mslr.pl test.txt predictions.txt results.txt 1"
#command = "C:\Strawberry\perl/bin/perl.exe Eval-Score-3.0.pl test.txt predictions.txt results.txt 1"
command = "C:\Strawberry\perl/bin/perl.exe mslr-eval-ttest-mslr.pl results.txt results.txt sig_results.txt"

'''
os.chdir("C:\Strawberry\perl/bin/")
command = "C:\Strawberry\perl/bin/perl.exe ppm.pl install Statistics::DependantTTest"

#'''
def extractProductPrice():
    FilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_prices.txt"
    filehandle = open(FilePath, 'w')
    file = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/metadata.json/MetaDataSet.txt"
    counter = 0
    with open(file, 'r') as fp:
        for line in fp:
            productId = ""
            asin = line.split("asin")
            if len(asin) > 1:
                product = asin[1].split(",")
                if len(product) > 1:
                    product = product[0].split(":")
                    start = 0
                    if len(product) > 1:
                        for c in product[1]:
                            if c == "'" and start == 0:
                                start = 1
                                continue
                            elif c == "'" and start == 1:
                                break
                            if start == 1:
                                productId += c
            productPrice = -1
            price = line.split("'price':")
            if len(price) > 1:
                price = price[1].split(",")
                if len(price) > 1:
                    price = price[0]
                    if len(price) > 1:
                        productPrice = ""
                        for c in price:
                            if c != ' ':
                                productPrice += c
                        productPrice = float(productPrice)

            print(productId + " " + str(productPrice))
            counter += 1
            # if productPrice == -1:
            #  print(line)
            filehandle.write(productId)
            filehandle.write("\t")
            filehandle.write(str(productPrice))
            filehandle.write("\n")
    print("Found " + str(counter) + " Product Prices")
    return
def splitParagraphIntoSentences(paragraph):
    ''' break a paragraph into sentences
        and return a list '''
    import re
    # to split by multile characters

    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[.!?]')
    if len(paragraph) >0 and paragraph !=" ":
        try :
            sentenceList = sentenceEnders.split(paragraph)
        except TypeError:
            sentenceList = []
            pass
    else:
        sentenceList = []
    return sentenceList

def writePolarityLine(filehandle1,productid,commentPolarityTotal,totalPostive,totalNegative,numSentences):
    try:
        filehandle1.write(productid)
        filehandle1.write("\t")
        filehandle1.write(str(commentPolarityTotal))
        filehandle1.write("\t")
        filehandle1.write(str(totalPostive))
        filehandle1.write("\t")
        filehandle1.write(str(totalNegative))
        filehandle1.write("\t")
        filehandle1.write(str(numSentences))
        filehandle1.write("\n")
    except IOError as e:
        print("error writing for  " + productid)
        pass
    return
def writePolarityLineNew(filehandle1,commentPolarityTotal,totalPostive,totalNegative,numSentences,newLine):
    try:
        filehandle1.write(str(commentPolarityTotal))
        filehandle1.write("\t")
        filehandle1.write(str(totalPostive))
        filehandle1.write("\t")
        filehandle1.write(str(totalNegative))
        filehandle1.write("\t")
        filehandle1.write(str(numSentences))
        filehandle1.write("\t")
        if newLine == 1:
            filehandle1.write("\n")
    except IOError as e:
        print("error writing")
        pass
    return
def writePolarityLineInString(filehandle1,value,newLine):
    try:
        filehandle1.write(value)
        if newLine == 1:
            filehandle1.write("\n")
    except IOError as e:
        print("error writing")
        pass
    return
def extractProductPolarties():
    print("Extracting Polarities for all products in Amazon Dataset")
    FilePath1 = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties.txt"
    filehandle1 = open(FilePath1, 'w')
    filehandle1.write("ProductID  TotalPolarity  NumPositive  NumNegative  NumSentences\n")

    directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    counter = 0
    for filename in os.listdir(directory):
        productFile = directory + filename
        productid = filename.split(".")
        productid = productid[0]
        #print(productid)
        numSentences = 0
        computed = 1
        inputFile = "C:\SentiTemp_2/test.txt"
        try:
            filehandle = open(inputFile, 'w')
        except IOError as e:
            print("error writing in file "+inputFile)
            inputFile = "C:\SentiTemp_2/test1.txt"
            try:
                filehandle = open(inputFile, 'w')
            except IOError as e:
                print("error writing in file " + inputFile)
                print("failed")
                computed = 0
                pass
            pass
        with open(productFile, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                text = ""
                if len(row)>8:
                    text+=row[6]+"\t"
                    text += row[7]
                #print(text)

                sentences = splitParagraphIntoSentences(text)
                for sent in sentences:
                    if len(sent)>1:
                        #print(sent)
                        numSentences+=1
                        filehandle.write(sent)
                        filehandle.write("\n")

                filehandle.write("---")
                filehandle.write("\n")
                #print("------------------------------")

        filehandle.close()
        if computed == 1:
            os.chdir("C:\SentiTemp_2/")
            command = "java -jar SentiStrengthCom.jar sentidata C:\SentiTemp_2/ input " + inputFile
            os.system(command)
            fileToRead = "C:\SentiTemp_2/test0_out.txt"

            commentPolarityTotal = 0
            commentPolarity = 0
            totalPostive = 0
            totalNegative = 0
            try:
                with open(fileToRead, 'r') as sentiStrfp:
                    bIgnoreFirst = 0
                    for senti in sentiStrfp:
                        if bIgnoreFirst == 0:
                            bIgnoreFirst = 1
                            continue
                        sentSplit = senti.split('\t')
                        if sentSplit[2] == "\n":
                            continue

                        if sentSplit[2] == "---\n":
                            commentPolarityTotal += commentPolarity
                            commentPolarity = 0
                        else:
                            numPostive = int(sentSplit[0])
                            numNegative = int(sentSplit[1])
                            sentPolarity = numPostive + numNegative
                            if sentPolarity >= 0:
                                commentPolarity+=1
                                totalPostive+=1
                            else:
                                commentPolarity-=1
                                totalNegative += 1



                os.remove(inputFile)
                os.remove(fileToRead)
            except IOError as e:
                print("error writing in file " + fileToRead)
                writePolarityLine(filehandle1, productid, 0, 0, 0, 0)
                pass
            writePolarityLine(filehandle1, productid, commentPolarityTotal, totalPostive, totalNegative, numSentences)
        else:
            writePolarityLine(filehandle1, productid, 0, 0, 0, 0)

        counter += 1
        print(counter)
    filehandle1.close()
    print("Found " + str(counter) + " Product Polarities")
    return
def extractProductPolartiesPerRatingLevel():
    print("Extracting Polarities for all products in Amazon Dataset Per each rating level")
    FilePath1 = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties_Per_RatingLevel.txt"
    filehandle1 = open(FilePath1, 'a')
    #filehandle1.write("ProductID  TotalPolarity1 NumPositive1  NumNegative1  NumSentences1 TotalPolarity2 1NumPositive2  NumNegative2  NumSentences2 TotalPolarity3 NumPositive3  NumNegative3  NumSentences3 TotalPolarity4 NumPositive4  NumNegative4  NumSentences4 TotalPolarity5 NumPositive5  NumNegative5  NumSentences5\n")
    writtenProductsDict = dict()
    firstLine = 0
    with open(FilePath1, 'r') as fp:
        for line in fp:
            if firstLine == 0:
                firstLine = 1
                continue
            else:
                row = line.split("\t")
                writtenProductsDict[row[0]] = 1

    directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    #directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews_Verified\Automotive/"
    counter = 0
    for filename in os.listdir(directory):
        productFile = directory + filename
        productid = filename.split(".")
        productid = productid[0]
        print(productid)
        try:
            result = writtenProductsDict[productid]
            counter += 1
            print(counter)
            continue
        except KeyError:
            pass

        ratingsDictionary = dict()

        computed = 1


        with open(productFile, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                if len(row)>5:
                    rating = float(row[5])
                    text = ""
                    if len(row)>8:
                        text+=row[6]+"\t"
                        text += row[7]
                    sentences = splitParagraphIntoSentences(text)

                    try:
                        ratingSentences = ratingsDictionary[rating]
                        ratingSentences.append(sentences)
                        ratingsDictionary[rating] = ratingSentences
                    except KeyError as e:
                        ratingSentences = sentences
                        ratingsDictionary[rating] = ratingSentences
        #Fix it for missing ratings
        if len(ratingsDictionary) < 5:
            if ratingsDictionary.get(1) == None:
                ratingsDictionary[1] = []
            if ratingsDictionary.get(2) == None:
                ratingsDictionary[2] = []
            if ratingsDictionary.get(3) == None:
                ratingsDictionary[3] = []
            if ratingsDictionary.get(4) == None:
                ratingsDictionary[4] = []
            if ratingsDictionary.get(5) == None:
                ratingsDictionary[5] = []

        filehandle1.write(productid)
        filehandle1.write("\t")
        #keyIndex = 0
        writingDict = dict()
        inputFile = "C:\SentiTemp_2/test.txt"
        try:
            filehandle = open(inputFile, 'w')
            computed = 1
        except IOError as e:
            print("error writing in file " + inputFile)
            inputFile = "C:\SentiTemp_2/test1.txt"
            try:
                filehandle = open(inputFile, 'w')
            except IOError as e:
                print("error writing in file " + inputFile+" again")
                print("failed")
                computed = 0
                pass
            pass

        for key, value in ratingsDictionary.items():
            if value == []:
                '''if keyIndex == len(ratingsDictionary)-1:
                    result = " 0    0   0   0 \n"
                    #writePolarityLineNew(filehandle1,0,0,0,0,1)
                else:
                    #writePolarityLineNew(filehandle1, 0, 0, 0, 0, 0)
                    result = " 0    0   0   0   "
                '''
                result = "0    0   0   0   "
                writingDict[key] = result
            else:

                numSentences = 0
                for comment in value:
                    sentences = splitParagraphIntoSentences(comment)
                    for sent in sentences:
                        if len(sent) > 1:
                            numSentences += 1
                            filehandle.write(sent)
                            filehandle.write("\n")

                filehandle.write("rating"+str(key))
                filehandle.write("\n")
                # print("------------------------------")
                #filehandle.close()
                #keyIndex += 1
        filehandle.close()
        if computed == 1:
            os.chdir("C:\SentiTemp_2/")
            command = "java -jar SentiStrengthCom.jar sentidata C:\SentiTemp_2/ input " + inputFile
            os.system(command)
            fileToRead = "C:\SentiTemp_2/test0_out.txt"

            commentPolarityTotal = 0
            commentPolarity = 0
            totalPostive = 0
            totalNegative = 0
            numSentences = 0
            try:
                with open(fileToRead, 'r') as sentiStrfp:
                    bIgnoreFirst = 0
                    for senti in sentiStrfp:
                        if bIgnoreFirst == 0:
                            bIgnoreFirst = 1
                            continue
                        sentSplit = senti.split('\t')
                        if sentSplit[2] == "\n":
                            continue

                        if sentSplit[2] == "rating1.0\n":
                            commentPolarityTotal += commentPolarity
                            numSentences += 1
                            result = str(commentPolarityTotal)+"\t" +str(totalPostive)+"\t" +str(totalNegative)+"\t" +str(numSentences)+"\t"
                            writingDict[1] = result
                            commentPolarityTotal = 0
                            commentPolarity = 0
                            totalPostive = 0
                            totalNegative = 0
                            numSentences = 0
                        elif sentSplit[2] == "rating2.0\n":
                            commentPolarityTotal += commentPolarity
                            numSentences += 1
                            result = str(commentPolarityTotal) + "\t" + str(totalPostive) + "\t" + str(totalNegative) + "\t" + str(numSentences) + "\t"
                            writingDict[2] = result
                            commentPolarityTotal = 0
                            commentPolarity = 0
                            totalPostive = 0
                            totalNegative = 0
                            numSentences = 0
                        elif sentSplit[2] == "rating3.0\n":
                            commentPolarityTotal += commentPolarity
                            numSentences += 1
                            result = str(commentPolarityTotal) + "\t" + str(totalPostive) + "\t" + str(totalNegative) + "\t" + str(numSentences) + "\t"
                            writingDict[3] = result
                            commentPolarityTotal = 0
                            commentPolarity = 0
                            totalPostive = 0
                            totalNegative = 0
                            numSentences = 0
                        elif sentSplit[2] == "rating4.0\n":
                            commentPolarityTotal += commentPolarity
                            numSentences += 1
                            result = str(commentPolarityTotal) + "\t" + str(totalPostive) + "\t" + str(totalNegative) + "\t" + str(numSentences) + "\t"
                            writingDict[4] = result
                            commentPolarityTotal = 0
                            commentPolarity = 0
                            totalPostive = 0
                            totalNegative = 0
                            numSentences = 0
                        elif sentSplit[2] == "rating5.0\n":
                            commentPolarityTotal += commentPolarity
                            numSentences += 1
                            result = str(commentPolarityTotal) + "\t" + str(totalPostive) + "\t" + str(totalNegative) + "\t" + str(numSentences) + "\t"
                            writingDict[5] = result
                            commentPolarityTotal = 0
                            commentPolarity = 0
                            totalPostive = 0
                            totalNegative = 0
                            numSentences = 0
                        else:
                            numPostive = int(sentSplit[0])
                            numNegative = int(sentSplit[1])
                            sentPolarity = numPostive + numNegative
                            numSentences += 1
                            if sentPolarity >= 0:
                                commentPolarity += 1
                                totalPostive += 1
                            else:
                                commentPolarity -= 1
                                totalNegative += 1
            except IOError as e:
                print("error writing in file " + fileToRead)
                '''if keyIndex == len(ratingsDictionary) - 1:
                    writePolarityLineNew(filehandle1, 0, 0, 0, 0, 1)
                else:
                    writePolarityLineNew(filehandle1, 0, 0, 0, 0, 0)
                pass
            # writePolarityLine(filehandle1, productid, commentPolarityTotal, totalPostive, totalNegative, numSentences)
            if keyIndex == len(ratingsDictionary) - 1:
                writePolarityLineNew(filehandle1, commentPolarityTotal, totalPostive, totalNegative, numSentences,
                                     1)
            else:
                writePolarityLineNew(filehandle1, commentPolarityTotal, totalPostive, totalNegative, numSentences,
                                     0)
                                     '''

            for key, value in writingDict.items():
                writePolarityLineInString(filehandle1, writingDict[key], 0)



        else:
            print("Problem encountered")
            '''if keyIndex == len(ratingsDictionary) - 1:
                writePolarityLineNew(filehandle1, 0, 0, 0, 0, 1)
            else:
                writePolarityLineNew(filehandle1, 0, 0, 0, 0, 0)
                    '''

        os.remove(inputFile)
        os.remove(fileToRead)
        filehandle1.write("\n")
        counter += 1
        print(counter)
    filehandle1.close()
    print("Found " + str(counter) + " Product Polarities")
    return


from datetime import timedelta
def divideReviewsByRatingLevelByTimePeriods(productFilePath,nPeriods,data_set_type):
    productDates = []
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    AllReviews = []
    reviewRatingLevelTimeDict = dict()
    try:
        with open(productFilePath, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                AllReviews.append(row)
                datesplit=[]
                if data_set_type=="amazon":
                    # Extracting Date
                    datesplit = row[2].split(',')
                    monthDay = datesplit[0]
                    month = ""
                    day = ""
                    monthDone = 0
                    for char in monthDay:
                        if char != " " and monthDone == 0:
                            month = month + char
                        if char == " ":
                            monthDone = 1
                        if monthDone == 1:
                            day = day + char
                    if len(datesplit) > 1 and datesplit[1] != ' ' and len(datesplit[1]) <= 5:
                        year = int(datesplit[1])
                        month = int(month)
                        day = int(day)

                elif data_set_type=="yelp":
                    found_date =0
                    for item in row:
                        if item == "::date":
                            found_date = 1
                            continue
                        if item == "::":
                            continue
                        if found_date == 1:
                            datesplit = item.split('-')
                            if len(datesplit)==0:
                                continue
                            #print(item)
                            month=int(datesplit[1])
                            day=int(datesplit[2])
                            year=int(datesplit[0])
                            break

                currentDay = datetime(year, month, day)

                productDates.append((currentDay))
                if currentDay > maxDate:
                    maxDate = currentDay
                if currentDay < minDate:
                    minDate = currentDay

        diff = (maxDate - minDate).days
        numDaysPerPeriod = int(diff / nPeriods)
        timeInterval = []
        timeInterval.append(minDate)
        tempDate = minDate
        for i in range(nPeriods):
            tempDate = tempDate + timedelta(days=numDaysPerPeriod)
            timeInterval.append(tempDate)

        if timeInterval[len(timeInterval)-1]<maxDate:
            del timeInterval[-1]
            timeInterval.append(maxDate)

        reviewTimeDict = dict()
        numActualReviews = len(AllReviews)
        for i in range(len(productDates)):
            for j in range(len(timeInterval)-1):
                if timeInterval[j]<= productDates[i] and productDates[i]<=timeInterval[j+1]:
                    try:
                        reviews = reviewTimeDict[j]
                        reviews.append(AllReviews[i])
                        reviewTimeDict[j] = reviews
                    except KeyError:
                        list=[]
                        list.append(AllReviews[i])
                        reviewTimeDict[j]=list
                    break
        #Fix Missing periods
        if len(reviewTimeDict) < nPeriods:
            # Just adding missing keys
            for i in range(nPeriods):
                if reviewTimeDict.get(i) == None:
                    reviewTimeDict[i] = []

        for i in range(nPeriods):
            if reviewRatingLevelTimeDict.get(i) == None:
                reviewRatingLevelTimeDict[i] = []
        newCountReviews = 0
        for key,value in reviewTimeDict.items():
            newCountReviews+=len(value)

            reviewRatingDict = dict()
            for i in range(1,6):
                if reviewRatingDict.get(i) == None:
                    reviewRatingDict[i] = []

            for val in value:
                rating=0
                if data_set_type=="amazon":
                    rating = int(float(val[5]))
                elif data_set_type=="yelp":
                    found_rating = 0
                    for item in val:
                        if item == "::stars":
                            found_rating = 1
                            continue
                        if item == "::":
                            continue
                        if found_rating == 1:
                            rating = int(item)
                            break
                try:
                    reviews= reviewRatingDict[rating]
                    reviews.append(val)
                    reviewRatingDict[rating] = reviews
                except KeyError:
                    list = []
                    list.append(val)
                    reviewRatingDict[rating]=list
            reviewRatingLevelTimeDict[key]=reviewRatingDict

        if numActualReviews != newCountReviews:
            print("Original Count of review is "+str(numActualReviews)+" ,however after setting the periods became "+str(newCountReviews))
    except FileNotFoundError:
        print("Skipping file "+productFilePath)
    #print("extracted periods for product Successfully")
    return reviewRatingLevelTimeDict


def extractProductPolartiesPerRatingLevelPerTimePeriod(categorieList,polartiesFilePath,productBaseDirectory,category_base_directory,dataset_type,timeperiods):

    print("Extracting Polarities for all products in "+dataset_type+" Dataset Per each rating level per Time Period")
    #polartiesFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties_Per_RatingLevelPerTimePeriod.txt"
    filehandle1 = open(polartiesFilePath, 'w')
    #productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    count = 0
    for cat in categorieList:
        #catFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"+cat+".txt"
        catFilePath =category_base_directory+cat+".txt"
        print("Considering "+cat)
        with open(catFilePath, 'r') as fp:
            for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                count+=1
                #productId="UL3OMN_c-NXHlyb97pDifA"
                productFilePath = productBaseDirectory+productId+".txt"
                print(productId)
                reviewRatingLevelTimeDict = divideReviewsByRatingLevelByTimePeriods(productFilePath, timeperiods,dataset_type)
                if len(reviewRatingLevelTimeDict)==0:
                    continue
                filehandle1.write(productId+"\t")
                inputFile = "C:\SentiTemp_2/test.txt"
                try:
                    filehandle = open(inputFile, 'w')
                    computed = 1
                except IOError as e:
                    print("error writing in file " + inputFile)
                    inputFile = "C:\SentiTemp_2/test1.txt"
                    try:
                        filehandle = open(inputFile, 'w')
                    except IOError as e:
                        print("error writing in file " + inputFile + " again")
                        print("failed")
                        computed = 0
                        pass
                    pass

                for key,value in reviewRatingLevelTimeDict.items():
                    filehandle.write("Period" + str(key)+"\n")
                    ratingsDictionary = dict()
                    ratingsDictionary = value
                    for key2, value2 in ratingsDictionary.items():
                        if len(value2) != 0:#a rating with actual comments
                            reviews = value2
                            for review in reviews:
                                    text = ""
                                    if dataset_type=="amazon":
                                        if len(review) > 8:
                                            text += review[6] + "\t"
                                            text += review[7]
                                    elif dataset_type=="yelp":
                                        found_text = 0
                                        for item in review:
                                            if item == "::text":
                                                found_text = 1
                                                continue
                                            if item == "::":
                                                continue
                                            if found_text == 1:
                                                text = item
                                                break

                                    sentences = splitParagraphIntoSentences(text)
                                    numSentences = 0
                                    for sent in sentences:
                                        if len(sent) > 1:
                                            numSentences += 1
                                            filehandle.write(sent)
                                            filehandle.write("\n")
                                    filehandle.write("rating"+str(key2)+"\n")

                filehandle.close()
                #if computed == 1:
                os.chdir("C:\SentiTemp_2/")
                command = "java -jar SentiStrengthCom.jar sentidata C:\SentiTemp_2/ input " + inputFile
                os.system(command)
                fileToRead = "C:\SentiTemp_2/test0_out.txt"
                totalPostive = 0
                totalNegative = 0
                periods = []
                start = 0
                end = 0
                writingDict = dict()
                try:
                    with open(fileToRead, 'r') as sentiStrfp:
                        bIgnoreFirst = 0
                        for senti in sentiStrfp:
                            if bIgnoreFirst == 0:
                                bIgnoreFirst = 1
                                continue
                            sentSplit = senti.split('\t')
                            if sentSplit[2] == "\n":
                                continue

                            if sentSplit[2].find("Period")!=-1:
                                if end == 0 and start == 1:
                                    end = 1
                                    start = 0
                                    if len(writingDict)<5:
                                        for i in range(1,6):
                                            if writingDict.get(i) == None:
                                                writingDict[i] = "0\t0\t"
                                    periods.append(writingDict)
                                if start == 0:
                                    start = 1
                                    end = 0
                                    writingDict = dict()

                            if sentSplit[2] == "rating1\n":
                                result = str(totalPostive) + "\t" + str(totalNegative) + "\t"
                                writingDict[1] = result
                                totalPostive = 0
                                totalNegative = 0
                            elif sentSplit[2] == "rating2\n":
                                result = str(totalPostive) + "\t" + str(totalNegative) + "\t"
                                writingDict[2] = result
                                totalPostive = 0
                                totalNegative = 0
                            elif sentSplit[2] == "rating3\n":
                                result = str(totalPostive) + "\t" + str(totalNegative) + "\t"
                                writingDict[3] = result
                                totalPostive = 0
                                totalNegative = 0
                            elif sentSplit[2] == "rating4\n":
                                result = str(totalPostive) + "\t" + str(totalNegative) + "\t"
                                writingDict[4] = result
                                totalPostive = 0
                                totalNegative = 0
                            elif sentSplit[2] == "rating5\n":
                                result =  str(totalPostive) + "\t" + str(totalNegative) + "\t"
                                writingDict[5] = result
                                totalPostive = 0
                                totalNegative = 0
                            else:
                                numPostive = int(sentSplit[0])
                                numNegative = int(sentSplit[1])
                                sentPolarity = numPostive + numNegative
                                numSentences += 1
                                if sentPolarity >= 0:
                                    totalPostive += 1
                                else:
                                    totalNegative += 1
                        if end == 0 and start == 1:
                            if len(writingDict) < 5:
                                for i in range(1, 6):
                                    if writingDict.get(i) == None:
                                        writingDict[i] = "0\t0\t"
                            periods.append(writingDict)
                        for period in periods:
                            for rateKey,ratevalue in period.items():
                                filehandle1.write(ratevalue)

                except IOError:
                    pass

                os.remove(inputFile)
                os.remove(fileToRead)
                filehandle1.write("\n")
                print("Num Products " + str(count))
                #if count == 50:
                #break
    filehandle1.close()

    print("Num Products "+str(count))
    print("Num Categories "+str(len(categorieList)))
    return
def extractTraininTestingCategoriesForSVM():
    fileToRead = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/temp.txt"
    training = []
    testing = []
    with open(fileToRead, 'r') as fp:
      for line in fp:
          line = str(line.strip('\n'))
          line = line.strip("(")
          category = ""
          for c in line:
              if c =="(":
                  break
              else:
                  category+=c
          if len(training)==24:
                testing.append(category)
          else:
                training.append(category)
    print("Training")
    print(len(training))
    print(training)
    print("Testing")
    print(len(testing))
    print(testing)
    return
def extractTraininTestingCategoriesForLamdamart():
    fileToRead = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/temp.txt"
    training = []
    validating = []
    testing = []
    with open(fileToRead, 'r') as fp:
      for line in fp:
          line = str(line.strip('\n'))
          line = line.strip("(")
          category = ""
          for c in line:
              if c =="(":
                  break
              else:
                  category+=c
          if len(training)!=8:
              training.append(category)
          elif len(validating) != 11:
              validating.append(category)
          else:
              testing.append(category)
    print("Training")
    print(len(training))
    print(training)
    print("Validating")
    print(len(validating))
    print(validating)
    print("Testing")
    print(len(testing))
    print(testing)

    return
#output = os.system(command)
#print(output)
print("Start")
#extractProductPolarties()
#extractTraininTestingCategoriesForLamdamart()
import subprocess
def runSpearmanExtractScript(scriptFile,R_path):
    print("Running Spearman R Script")
    numbers = []
    try:
        out = subprocess.check_output([R_path, scriptFile])
        print("Command Called now Extracting numbers")
        out = out.strip()
        out = str(out)
        out = out.split('n')
        index = 0
        size = len(out)
        for item in out:
            number = item.split('\\')
            number = number[0].split(']')
            number = number[1]
            number = number.lstrip()
            if index == size-1:
                number = number.split("'")
                numbers.append(float(number[0]))
            else:
                numbers.append(float(number))
            index+=1
        print(numbers)
    except:
        pass
    return numbers
def runKenallExtractScript(scriptFile,R_path):
    print("Running Kendal R Script")
    numbers = []
    try:
        out = subprocess.check_output([R_path, scriptFile])
        print("Command Called now Extracting numbers")
        out = out.strip()
        print(out)
        out = str(out)
        out = out.split("tau")
        print(out)
        for part in out:
            number = part.split(",")
            number = number[0].split('=')
            if len(number) > 1:
                number = number[1].lstrip()
                numbers.append(float(number))
        print(numbers)
    except:
        pass
    return numbers
def runKenallExtractFromNewScript(scriptFile,R_path):
    print("Running Kendal R Script")
    numbers = []
    try:
        out = subprocess.check_output([R_path, scriptFile])
        print("Command Called now Extracting numbers")
        out = out.strip()
        out = str(out)
        #print(out)
        out = out.split("[1]")
        #print(len(out))
        #print(out)
        #text = str(out[1].split(' ')[1]).split("'")[0]
        #print(text)
        #kendall = float(text)
        #print(kendall)
        #numbers.append(kendall)

        #print(numbers)
        for i in range(1,len(out),2):
            query_name = out[i].split('.txt')[0].rstrip().split('"')[1]
            #print(query_name)
            tau = out[i+1].lstrip().rstrip().split("'")[0]#(out[i+1].split(' ')[1]).split("'")[0].split('\n')[0]
            tau = tau.replace('\r\n', '')
            new_tau = ""
            for c in tau:
                if c =='\\':
                    break
                else:
                    new_tau+=c
            tau = new_tau
            #print(tau)
            try:
                tau=float(tau)
            except:
                print("couldn't convert")
                print(type(tau))
            #print("ktau")
            #print(tau)
            numbers.append((int(query_name),tau))
            '''number = part.split(",")
            number = number[0].split('=')
            if len(number) > 1:
                number = number[1].lstrip()
                numbers.append(float(number))'''

    except:
        pass
    return numbers
def writeCorrelationRScript(destDirectory,correlationFn):
    #correlationFn 1 means Kendall tau and 2 means Spearman Correlation
    if correlationFn == 1:
        #print("Writing Kendall tau R Script File")
        rScriptFilePath = destDirectory + "R_Kendall_Script.r"
    else:
        #print("Writing Spearman Correlation R Script File")
        rScriptFilePath = destDirectory + "R_Spearman_Script.r"

    rScriptFileHandle = open(rScriptFilePath, 'w')
    if correlationFn == 1:
        rScriptFileHandle.write("library(Kendall)\n")

    directParts = destDirectory.split('//')
    print("destDirectory ")
    print(destDirectory)
    newDistDirect = ""
    index = 0
    for part in directParts:

        if index == len(directParts)-1:
            continue
        elif index == len(directParts)-2:
            newDistDirect += part+"/"
        else:
            newDistDirect += part
            newDistDirect+= '/'
        index+=1

    #newDistDirect = newDistDirect.replace('//', "\\\\")

    rScriptFileHandle.write("files <-list.files(")
    rScriptFileHandle.write('"')
    differenceDirectory = newDistDirect + "R_Difference"
    rScriptFileHandle.write(differenceDirectory)
    rScriptFileHandle.write('")')
    rScriptFileHandle.write("\n")
    rScriptFileHandle.write("size<- length(files)\n")
    rScriptFileHandle.write("for (i in 1: size)\n")
    rScriptFileHandle.write("{\n")
    rScriptFileHandle.write("mydodo<-read.table(file.path(")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(differenceDirectory+"////")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(",files[i]))\n")
    if correlationFn == 1:
        rScriptFileHandle.write("print(Kendall(mydodo$V1,mydodo$V2))\n")
    else:
        rScriptFileHandle.write("print(cor(mydodo$V1,mydodo$V2))\n")
    rScriptFileHandle.write("}\n")
    rScriptFileHandle.close()
    print("Finished Writing")
    return rScriptFilePath

def writeCorrelationRScriptNew(destDirectory,correlationFn):
    #correlationFn 1 means Kendall tau and 2 means Spearman Correlation
    if correlationFn == 1:
        #print("Writing Kendall tau R Script File")
        rScriptFilePath = destDirectory + "R_Kendall_Script.r"
    else:
        #print("Writing Spearman Correlation R Script File")
        rScriptFilePath = destDirectory + "R_Spearman_Script.r"

    rScriptFileHandle = open(rScriptFilePath, 'w')
    if correlationFn == 1:
        rScriptFileHandle.write("library(Kendall)\n")

    directParts = destDirectory.split('/')

    newDistDirect = ""
    index = 0
    for part in directParts:

        if index == len(directParts)-1:
            continue
        elif index == len(directParts)-2:
            newDistDirect += part+"//"
        else:
            newDistDirect += part
            newDistDirect+= '//'
        index+=1

    newDistDirect = newDistDirect.replace('\\', "\\\\")

    rScriptFileHandle.write("files <-list.files(")
    rScriptFileHandle.write('"')
    differenceDirectory = newDistDirect + "R_Difference"
    rScriptFileHandle.write(differenceDirectory)
    rScriptFileHandle.write('")')
    rScriptFileHandle.write("\n")
    rScriptFileHandle.write("size<- length(files)\n")
    rScriptFileHandle.write("for (i in 1: size)\n")
    rScriptFileHandle.write("{\nprint(files[i])\n")
    rScriptFileHandle.write("mydodo<-read.table(file.path(")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(differenceDirectory+"////")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(",files[i]))\n")
    if correlationFn == 1:
        rScriptFileHandle.write("print(Kendall(mydodo$V1,mydodo$V2))\n")
    else:
        rScriptFileHandle.write("print(cor(mydodo$V1,mydodo$V2))\n")
    rScriptFileHandle.write("}\n")
    rScriptFileHandle.close()
    print("Finished Writing")
    return rScriptFilePath

def writeCorrelationRScriptNew_Method(destDirectory,correlationFn):
    #correlationFn 1 means Kendall tau and 2 means Spearman Correlation
    if correlationFn == 1:
        #print("Writing Kendall tau R Script File")
        rScriptFilePath = destDirectory + "R_Kendall_Script.r"
    else:
        #print("Writing Spearman Correlation R Script File")
        rScriptFilePath = destDirectory + "R_Spearman_Script.r"

    rScriptFileHandle = open(rScriptFilePath, 'w')
    if correlationFn == 1:
        rScriptFileHandle.write("library(Kendall)\n")

    directParts = destDirectory.split('/')

    newDistDirect = ""
    index = 0
    for part in directParts:

        if index == len(directParts)-1:
            continue
        elif index == len(directParts)-2:
            newDistDirect += part+"//"
        else:
            newDistDirect += part
            newDistDirect+= '//'
        index+=1

    newDistDirect = newDistDirect.replace('\\', "\\\\")

    rScriptFileHandle.write("files <-list.files(")
    rScriptFileHandle.write('"')
    differenceDirectory = newDistDirect + "R_Difference"
    rScriptFileHandle.write(differenceDirectory)
    rScriptFileHandle.write('")')
    rScriptFileHandle.write("\n")
    rScriptFileHandle.write("size<- length(files)\n")
    rScriptFileHandle.write("for (i in 1: size)\n")
    rScriptFileHandle.write("{\nprint(files[i])\n")
    rScriptFileHandle.write("mydodo<-read.table(file.path(")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(differenceDirectory+"////")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(",files[i]))\n")
    if correlationFn == 1:
        rScriptFileHandle.write("print(cor(mydodo$V1,mydodo$V2,method="+'"'+"kendall"+'"'+"))\n")
    else:
        rScriptFileHandle.write("print(cor(mydodo$V1,mydodo$V2))\n")
    rScriptFileHandle.write("}\n")
    rScriptFileHandle.close()
    print("Finished Writing")
    return rScriptFilePath
def writeCorrelationRScriptOneFile(file_path,correlationFn,destDirectory):
    #correlationFn 1 means Kendall tau and 2 means Spearman Correlation
    if correlationFn == 1:
        #p
        rScriptFilePath = destDirectory + "R_Kendall_Script.r"
    else:
        rScriptFilePath = destDirectory + "R_Spearman_Script.r"

    file_path = file_path.replace('/', "\\\\")
    file_path = file_path.replace('\\', "\\\\")
    rScriptFileHandle = open(rScriptFilePath, 'w')
    if correlationFn == 1:
        rScriptFileHandle.write("library(Kendall)\n")


    rScriptFileHandle.write("mydodo<-read.table(file.path(")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write(file_path+"")
    rScriptFileHandle.write('"')
    rScriptFileHandle.write("))\n")
    if correlationFn == 1:
        rScriptFileHandle.write("print(Kendall(mydodo$V1,mydodo$V2))\n")
    else:
        rScriptFileHandle.write("print(cor(mydodo$V1,mydodo$V2))\n")

    rScriptFileHandle.close()
    print("Finished Writing")
    return rScriptFilePath
#from RankingHelper import runRScript

#runSpearmanExtractScript(rFile)
#runKenallExtractScript(rFile)

def computeLifeTimeForProductCategory(categoryPath,baseProductDirectory,categoryName,destinationDirectory):
    fileTorWritePath = destinationDirectory+categoryName+".txt"
    filehandle = open(fileTorWritePath, 'w')
    with open(categoryPath, 'r') as fp:
        for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                productPath = baseProductDirectory+productId+".txt"
                minDate = datetime(2050, 12, 31)
                maxDate = datetime(1950, 1, 1)
                with open(productPath, 'r') as fp2:
                    for line2 in fp2:
                        review = line2.split('\t')
                        datesplit = review[2].split(',')
                        monthDay = datesplit[0]
                        month = ""
                        day = ""
                        monthDone = 0
                        for char in monthDay:
                            if char != " " and monthDone == 0:
                                month = month + char
                            if char == " ":
                                monthDone = 1
                            if monthDone == 1:
                                day = day + char
                        if len(datesplit) > 1 and datesplit[1] != ' ' and len(datesplit[1]) <= 5:
                            year = int(datesplit[1])
                            month = int(month)
                            day = int(day)

                            currentDay = datetime(year, month, day)
                            if currentDay > maxDate:
                                maxDate = currentDay
                            if currentDay < minDate:
                                minDate = currentDay
                filehandle.write(str((maxDate-minDate).days))
                filehandle.write("\n")
    filehandle.close()
    return
def computeLifeTimeForProductCategoryList(categoryList,baseCategoryPath,baseProductDirectory,destinationDirectory):
    print("Procedure to compute life time of products for a list of categories ")
    print(categoryList)
    for categoryName in categoryList:
        print("Considerting "+categoryName)
        categoryFilePath = baseCategoryPath+categoryName+".txt"
        computeLifeTimeForProductCategory(categoryFilePath,baseProductDirectory,categoryName,destinationDirectory)
        
    return
from alogrithms import  mergeSort
def RankGivenAverageTargetForLearningPreparation(averageTargetCatPath,destCatPath):
    productsAverage=[]
    index = 0
    originalLines = []
    with open(averageTargetCatPath, 'r') as fp2:
        for line2 in fp2:
            productVector = line2.split(' ')
            productsAverage.append((index,float(productVector[0])))
            originalLines.append(productVector)
            index+=1

    #print(productsAverage)
    total = len(productsAverage)
    mergeSort(productsAverage)
    #print(productsAverage)
    productDict = dict()
    currentIndex = 0
    for item in reversed(productsAverage):
        try:
            found = productDict[item[0]]
        except KeyError:
            productDict[item[0]]=total-currentIndex
        currentIndex+=1
    #print(productDict)
    #'''
    filehandle = open(destCatPath, 'w')
    currentIndex = 0
    for key,value in productDict.items():
        filehandle.write(str(value)+" ")
        for i in range(1,len(originalLines[currentIndex])):
            filehandle.write(originalLines[currentIndex][i])
            if i != len(originalLines[currentIndex])-1:
                filehandle.write(" ")
        currentIndex+=1
    filehandle.close()
    #'''
    return
def copyLablelFromLearningDataToOther(category,sourceDirectoryOfLabel,sourceDirectoryofFeatures,destDirectory):
    print("Procedure to change the label to from One similar data to other")
    catLabelFilePath = sourceDirectoryOfLabel + category + ".txt"
    catFeatureFilePath = sourceDirectoryofFeatures + category + ".txt"
    destCatPath = destDirectory+ category + ".txt"
    labels = []
    with open(catLabelFilePath, 'r') as fp2:
        for line in fp2:
            featureVector = line.split(" ")
            labels.append((featureVector[0]))
    index = 0
    filehandle = open(destCatPath, 'w')
    with open(catFeatureFilePath, 'r') as fp2:
        for line in fp2:
            featureVector = line.split(" ")
            filehandle.write(labels[index])
            filehandle.write(" ")
            for i in range(1,len(featureVector)):
                filehandle.write(featureVector[i])
                if i !=len(featureVector)-1:
                    filehandle.write(" ")
            index+=1

    filehandle.close()
    return
def prepareAggregateFnForEvaluation(regressionSourceDirectory,destDirectory,baseCategoryDirectory):

    for category in os.listdir(regressionSourceDirectory):
        print(category)
        origCatName = ""

        if category == "Arts":
            origCatName = "Arts, Crafts & Sewing"
        elif category == "Industrial":
            origCatName= "Industrial & Scientific"
        elif category == "Toys":
            origCatName = "Toys & Games"
        elif category == "Computers":
            origCatName= "Computers & Accessories"
        elif category == "Cell Phones":
            origCatName = "Cell Phones & Accessories"
        else:
            origCatName = category

        AllProducts = []
        originalCatFile = baseCategoryDirectory+origCatName+".txt"
        with open(originalCatFile, 'r') as fp2:
            for line in fp2:
                row = line.split("\t")
                AllProducts.append(row[0])

        index = 0
        newDirectory = destDirectory + category
        try:
            os.stat(newDirectory)
        except:
            os.mkdir(newDirectory)

        catPath = regressionSourceDirectory+category+"/cutoff_3/"

        newCutoff = newDirectory+"/cutoff_3"
        try:
            os.stat(newCutoff)
        except:
            os.mkdir(newCutoff)

        AllpredicitonsFile = newCutoff + "/" + "AllPredictions.txt"
        produccAllpredicitonsFile = newCutoff + "/" + origCatName+".txt"
        filehandleAll = open(AllpredicitonsFile, 'w')
        filehandleAllProduct = open(produccAllpredicitonsFile, 'w')
        for i in range(1,6):
            set = "Set_"+str(i)+"/"
            newSetPath =newCutoff+"/"+set
            try:
                os.stat(newSetPath)
            except:
                os.mkdir(newSetPath)
            predicitonsFile = newSetPath+"/"+"predictions.txt"

            testPath = catPath+set+"test.txt"
            filehandle = open(predicitonsFile, 'w')
            with open(testPath, 'r') as fp2:
                for line in fp2:
                    row = line.split(" ")
                    filehandle.write(row[0])
                    filehandle.write("\n")
                    filehandleAll.write(row[0])
                    filehandleAll.write("\n")
                    filehandleAllProduct.write(AllProducts[index])
                    filehandleAllProduct.write("\t")
                    filehandleAllProduct.write(row[0])
                    filehandleAllProduct.write("\n")
                    index+=1
            filehandle.close()
    return
def fix_yelp_review_files(productBaseDirectory,fixed_product_base_directory):

    for filename in os.listdir(productBaseDirectory):
        product_file_path = productBaseDirectory + filename
        new_product_file_path = fixed_product_base_directory+filename
        lines=[]
        previous_row=""
        rewrite=0
        with open(product_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                if row[0]!="votes":
                    previous_row+=line
                    rewrite=1
                else:
                    if len(previous_row)!=0:
                        temp_row=previous_row.split('\n')
                        previous_row=""
                        for i in range(len(temp_row)-1):
                            previous_row+=temp_row[i]
                        previous_row+="\n"
                        pr_row=lines.pop()
                        temp_row=str(pr_row).split('\n')
                        pr_row=""
                        for i in range(len(temp_row) - 1):
                            pr_row+=temp_row[i]
                        pr_row+=previous_row
                        lines.append(pr_row)
                    previous_row=""
                    lines.append(line)
        if rewrite ==1:
            print("Rewriting "+filename)
            filehandle = open(new_product_file_path, 'w')
            for line in lines:
                filehandle.write(line)
            filehandle.close()
    return
def fix_yelp_review_categories(category_baseDirectory,fixed_product_base_directory,product_base_directory):
    for filename in os.listdir(category_baseDirectory):
        category_file_path = category_baseDirectory + filename
        new_file_category_path = fixed_product_base_directory+filename
        filehandle = open(new_file_category_path, 'w')
        print("Considering "+filename)
        num_products=0
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                product_file_path = product_base_directory+row[0]+".txt"
                num_products+=1
                try:
                    counter = 0
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            counter+=1
                    filehandle.write(row[0]+"\t"+str(counter)+"\n")
                except FileNotFoundError:
                    pass
                print(num_products)
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
    # print("votes")
    # print(votes)
    posterior = map(sum, zip(votes, prior))
    temp = list(map(sum, zip(votes, prior)))
    to = list(enumerate(temp))
    # print("posterior")
    # print(temp)
    # print("enum posterior")
    # print(to)
    N = sum(posterior)
    # print("Sum Posterior")
    # print(N)
    weights = list(map(lambda i: (i[0] + 1) * i[1], to))
    # print(weights)
    newlist = []
    for item in weights:
        item = item / sum(weights)
        newlist.append(item)
    # print(newlist)
    # print(sum(weights))
    retValue = float(float(sum(weights)) / N)
    # print(retValue)
    return retValue
def add_dirichlet_to_review_categories_yelp(category_baseDirectory,fixed_product_base_directory,productBaseDirectory):

    for filename in os.listdir(category_baseDirectory):
        category_file_path = category_baseDirectory + filename
        new_file_category_path = fixed_product_base_directory + filename
        filehandle = open(new_file_category_path, 'w')
        print("Considering " + filename)
        num_products = 0
        prior = [1, 1, 1, 1, 1]
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                product_file_path = productBaseDirectory + row[0] + ".txt"
                num_products += 1
                ratingsDictionary = {0:0,1:0,2:0,3:0,4:0,5:0}
                try:
                    counter = 0
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            row2 = line2.split("\t")
                            found_rating = 0
                            for item in row2:
                                if item == "::stars":
                                    found_rating = 1
                                    continue
                                if item == "::":
                                    continue
                                if found_rating == 1:
                                    rating = int(item)
                                    ratingsDictionary[rating]+=1
                                    break
                            counter += 1
                    dirichlet_value = dirichlet_mean(ratingsDictionary,prior)
                    #print(ratingsDictionary)
                    #print(dirichlet_value)
                    filehandle.write(row[0] + "\t" + str(counter) + "\t"+str(dirichlet_value)+"\n")
                except FileNotFoundError:
                    pass
                print(num_products)
        filehandle.close()
    return
def check_man_gt_100_in_testing(predictions_dirct,category_baseDirectory,Categories_Indices_for_testing):
    for filename in os.listdir(category_baseDirectory):
        category_file_path = category_baseDirectory + filename
        category_name =filename.split('.')[0]
        new_file_category_path = fixed_product_base_directory + filename
        print("Considering " + filename)
        new_file_category_path=Categories_Indices_for_testing+filename
        filehandle = open(new_file_category_path, 'w')
        product_dict = dict()
        cat_dict = dict()
        cat_indices=[]
        current_index = 0
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                if int(row[1])>=100:
                    cat_indices.append(current_index)
                    filehandle.write(str(current_index)+"\n")
                    try:
                        product_dict[row[0]]
                    except KeyError:
                        product_dict[row[0]]=1
                current_index+=1
        print(cat_indices)
        filehandle.close()
        cat_dict[category_name]=cat_indices
        predict_folder = predictions_dirct+category_name+"/Cutoff_10\Predictions/"
        for filename2 in os.listdir(predict_folder):
            predict_file_path = predict_folder + filename2
            num_gt_100=0
            with open(predict_file_path, 'r') as fp:
                for line in fp:
                    row = line.split("\t")
                    try:
                        product_dict[row[0]]
                        num_gt_100+=1
                    except KeyError:
                        pass
            print("found in "+filename2+" "+str(num_gt_100))
    return
def compute_yelp_stats(category_baseDirectory,productBaseDirectory,dataset_type):
    all_rev = 0
    for filename in os.listdir(category_baseDirectory):
        category_file_path = category_baseDirectory + filename
        total_num_rev = 0
        product_lives = []
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                total_num_rev+=int(row[1])

                product_file_path = productBaseDirectory + row[0] + ".txt"
                try:
                    minDate = datetime(2050, 12, 31)
                    maxDate = datetime(1950, 1, 1)
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            row2 = line2.split("\t")
                            if dataset_type == "yelp":
                                found_date = 0
                                for item in row2:
                                    if item == "::date":
                                        found_date = 1
                                        continue
                                    if item == "::":
                                        continue
                                    if found_date == 1:
                                        datesplit = item.split('-')
                                        if len(datesplit) == 0:
                                            continue
                                        # print(item)
                                        month = int(datesplit[1])
                                        day = int(datesplit[2])
                                        year = int(datesplit[0])
                                        currentDay = datetime(year, month, day)
                                        if currentDay > maxDate:
                                            maxDate = currentDay
                                        if currentDay < minDate:
                                            minDate = currentDay
                                        break
                            elif dataset_type =="amazon":
                                datesplit = row2[2].split(',')
                                monthDay = datesplit[0]
                                month = ""
                                day = ""
                                monthDone = 0
                                for char in monthDay:
                                    if char != " " and monthDone == 0:
                                        month = month + char
                                    if char == " ":
                                        monthDone = 1
                                    if monthDone == 1:
                                        day = day + char
                                if len(datesplit) > 1 and datesplit[1] != ' ' and len(datesplit[1]) <= 5:
                                    year = int(datesplit[1])
                                    month = int(month)
                                    day = int(day)

                                    currentDay = datetime(year, month, day)
                                    if currentDay > maxDate:
                                        maxDate = currentDay
                                    if currentDay < minDate:
                                        minDate = currentDay

                    product_life = (maxDate - minDate).days
                    #print(product_life)
                    product_lives.append(product_life)
                except IOError:
                    pass
        avg_life = 0
        for pro_life in product_lives:
            avg_life+=pro_life
        #print("avg_life "+str(avg_life))
        #print("len "+str(len(product_lives)))
        avg_life=int(avg_life/len(product_lives))
        print(filename + " " + str(avg_life))
        all_rev+=total_num_rev
    #print("all rev "+str(all_rev))
    return
'''
destDirectoryForRFileCreation = "C://Yassien_RMIT PhD//Datasets//TruthDiscovery_Datasets//Web data Amazon reviews//Unique_Products_Stanford_three//Experiment 2//Svm_Test//K_Fold_PerCategory//Industrial & Scientific//Cutoff_3//"
correlationFn = 1
rScriptFilePath = writeCorrelationRScript(destDirectoryForRFileCreation,correlationFn)
runKenallExtractScript(rScriptFilePath)
correlationFn = 2
rScriptFilePath = writeCorrelationRScript(destDirectoryForRFileCreation,correlationFn)
runSpearmanExtractScript(rScriptFilePath)
print("Finished")
'''
#extractProductPolartiesPerRatingLevel()
'''
categorybaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
baseProductDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
destinationDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Categories_Lifetime/"
categoryList = ["Industrial & Scientific","Jewelry","Arts, Crafts & Sewing","Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
computeLifeTimeForProductCategoryList(categoryList,categorybaseDirectory,baseProductDirectory,destinationDirectory)
'''

#*******************************Yelp Dataset polarties extraction configuration**************************************************************************************
categoriesList = ["American (New)","American (Traditional)","Bars","Cafes","Chinese","Italian","Japanese","Mexican","Thai"]
polartiesFilePath="f:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/product_polarties_Per_RatingLevelPer_1_TimePeriod.txt"
productBaseDirectory="f:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/ProductReviews_New/"
catFilePath="f:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/Resturants_Categories/"
dataset_type="yelp"
timeperiods = 1
#********************************************************************************************************************************************************************
#*******************************Amazon Dataset polarties extraction configuration**************************************************************************************
#categoriesList = ["Industrial & Scientific","Jewelry","Toys & Games","Arts, Crafts & Sewing","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
#polartiesFilePath="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 3/product_polarties_Per_RatingLevelPer_15_TimePeriod.txt"
#productBaseDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
#catFilePath="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
#dataset_type="amazon"
#timeperiods = 15
#extractProductPolartiesPerRatingLevelPerTimePeriod(categoriesList,polartiesFilePath,productBaseDirectory,catFilePath,dataset_type,timeperiods)

'''
categoryList = ["Industrial & Scientific","Jewelry","Arts, Crafts & Sewing","Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
#categoryList = ["Computers & Accessories"]
for cat in categoryList:
    print("Considering "+cat)
    averageTargetCatPath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_Average_Target/"+cat+".txt"
    destCatPath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_Average_Target_For_Ranking/"+cat+".txt"
    RankGivenAverageTargetForLearningPreparation(averageTargetCatPath,destCatPath)
#'''

'''
categoryList = ["Industrial & Scientific","Jewelry","Arts, Crafts & Sewing","Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
for cat in categoryList:
    print("Considering "+cat)
    sourceDirectoryOfLabel = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_TQ_Target_For_Ranking/"
    sourceDirectoryofFeatures = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_10_Time_Interval_TQ_Target_For_Ranking/"
    copyLablelFromLearningDataToOther(cat,sourceDirectoryOfLabel, sourceDirectoryofFeatures, destDirectory)

print("Done")
#'''
baseCategoryDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/amazon_exp_categories/"
regressionSourceDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Regression\K_Fold_PerCategory_Basic__With_TQ_Target_25/"
destDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/TQ_correlation_as_L2R_Evaluation/"
#prepareAggregateFnForEvaluation(regressionSourceDirectory,destDirectory,baseCategoryDirectory)
category_baseDirectory="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/Resturants_Categories/"
fixed_product_base_directory="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/ProductReviews_Fixed/"
productBaseDirectory="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/ProductReviews_New/"
#fix_yelp_review_files(productBaseDirectory,fixed_product_base_directory)
#fix_yelp_review_categories(category_baseDirectory,fixed_product_base_directory,productBaseDirectory)
#add_dirichlet_to_review_categories_yelp(category_baseDirectory,fixed_product_base_directory,productBaseDirectory)
predictions_dirct = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda/"
Categories_Indices_for_testing="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Indices_for_testing/"
#check_man_gt_100_in_testing(predictions_dirct,category_baseDirectory,Categories_Indices_for_testing)
dataset_type = "amazon"
category_baseDirectory=baseCategoryDirectory
productBaseDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
#compute_yelp_stats(category_baseDirectory,productBaseDirectory,dataset_type)

#Get Unique products within from queries of one product category
'''
main_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
test_file = "D:\Yassien_PhD\Experiment_6\Randomized_Queryset/testing.txt"
product_dict = dict()
with open(test_file, 'r') as fp:
    for line in fp:
        row = line.split('\t')
        query_file_path = main_dirc+row[0]+".txt"
        with open(query_file_path, 'r') as fp2:
            for line2 in fp2:
                row2 = line2.split('\t')
                try:
                    product_dict[row2[0]]
                except KeyError:
                    product_dict[row2[0]]=1

print("Num Unique Products "+str(len(product_dict)))
'''
#import math
#print(math.e ** 700)