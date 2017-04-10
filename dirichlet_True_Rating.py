#Author: Yassien Shaalan

def computeMajorityVoteForProductCategories(productBaseDirectory,filePath,category,destDirectory):
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
           productId = productId.split('\n')
           productId = productId[0]
           #fileName = productBaseDirectory+category+"/"+productId+".txt"
           fileName = productBaseDirectory + productId + ".txt"
           overallRate = 0
           counter = 0
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    review = item.split('\t')
                    print
                    overallRate = overallRate + float(review[5])
                    counter = counter + 1
           except IOError as e:
              print("error opening file "+fileName)
              pass
           filehandle.write(productId)
           #print(productId)
           filehandle.write("\t")
           overallRate = overallRate/counter
           #print(overallRate)
           #overallRate = round(overallRate,4)
           #print("Average Score "+str(overallRate))
           filehandle.write(str(overallRate))
           filehandle.write("\n")
    #filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computeNumberOfReviewsForProductCategories(productBaseDirectory,filePath,category,destDirectory):
    print("Procedure to compute of reviews for each product under each category")
    print("Considering " + category)
    # product_Id Category sales_rank
    # print("Started")
    start = datetime.now()
    # print(start)
    line = ""
    filehandle = open(destDirectory + category + ".txt", 'w')
    with open(filePath, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            productId = row[0]
            productId = productId.split('\n')
            productId = productId[0]
            fileName = productBaseDirectory + productId + ".txt"
            counter = 0
            try:
                with open(fileName, 'r') as filep:
                    for item in filep:
                        counter = counter + 1
            except IOError as e:
                print("error opening file " + fileName)
                pass
            filehandle.write(productId)
            filehandle.write("\t")
            filehandle.write(str(counter))
            filehandle.write("\n")
    # filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in " + str(round(done.total_seconds() / 60, 3)) + " minutes")
    return
#from ranking import computeExponentialScore
def computExponentialModel(productBaseDirectory,filePath,category,destDirectory):
    print("Procedure to compute of Exponential Model for each product under each category")
    print("Considering " + category)
    # product_Id Category sales_rank
    # print("Started")
    start = datetime.now()
    # print(start)
    line = ""
    filePathExpertiese = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/UserHelpfulVotesPerCategoryNew/" + category+".txt"
    userExpert = dict()
    with open(filePathExpertiese, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            userExpert[row[0]] = float(row[3])
    filehandle = open(destDirectory + category + ".txt", 'w')
    with open(filePath, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            productId = row[0]
            productId = productId.split('\n')
            productId = productId[0]
            fileName = productBaseDirectory + productId + ".txt"
            retValue = computeExponentialScore(fileName, userExpert)
            filehandle.write(productId)
            filehandle.write("\t")
            filehandle.write(str(retValue))
            filehandle.write("\n")
    # filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in " + str(round(done.total_seconds() / 60, 3)) + " minutes")
    return
def computeExponentialScore(productFileName,userExpert):

    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    productDates = []
    weights = []
    rates = []
    reviewHelpfulWeight = []
    extrweights = []
    with open(productFileName, 'r') as filep:
        # get the most recent date and oldest date
        for item in filep:
            review = item.split('\t')
            maxVotes = 0
            try:
                maxVotes = userExpert[review[0]]

            except KeyError as e:
                maxVotes = 0

            numHelpful = int(review[4])
            numtotalVotes = 0
            if review[3] != "":
                numtotalVotes = int(review[3])

            weightMaxHelpVotes = 0
            extraWei = 0
            if maxVotes > 0:
                weightMaxHelpVotes = float(float(numHelpful) / float(maxVotes))
            if numtotalVotes > 0:
                extraWei = float(float(numHelpful) / float(numtotalVotes))

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

                productDates.append((currentDay))
                if currentDay > maxDate:
                    maxDate = currentDay
                if currentDay < minDate:
                    minDate = currentDay

                # reviewHelpfulWeight.append(weightMaxHelpVotes)
                reviewHelpfulWeight.append(userExpert[review[0]])
                rates.append(float(review[5]))

                extrweights.append(extraWei)

        newweights = []
        index = 0
        # print("-------------------------------------------------")
        dayweights = []
        credweights = []

        for revweighthelp in reviewHelpfulWeight:
            timeDiff = (productDates[index] - minDate).days
            beta = 0.01
            part2 = revweighthelp
            part1 = beta * timeDiff
            # print("--------------")
            part1 = part1 / 2
            part2 = part2 + part1 / 2

            # dayweights.append(part1)
            # credweights.append(part2)
            # print(productDates[index])
            # print(part1)
            # print(revweighthelp)
            # print(part2)
            part3 = part1 + part2
            # print(part3)
            expValue = (math.e ** part3)
            # print(expValue)
            newweights.append(expValue)
            index = index + 1

        index = 0
        minVal = 100000000
        maxVal = -10000000

        index = 0
        for item in newweights:
            if item > maxVal:
                maxVal = item
            if item < minVal:
                minVal = item
        newFinalRate = 0

        for item in newweights:
            newWeight = float((float((item - minVal)) / float((maxVal - minVal))))
            newRate = newWeight * rates[index]
            # print("new Weight")
            # print(newRate)
            newFinalRate = newFinalRate + newRate
            index = index + 1

    return newFinalRate
def computeNormalDirichelet(productBaseDirectory,path,categoryName,destDirectory):
    print("Procedure to compute product rating based on normal dirichelet distribution")
    print("Considering "+categoryName)
    #product_Id Category sales_rank
    #print("Started")
    #start = datetime.now()
    #print(start)
    line = ""
    filehandle = open(destDirectory+categoryName+".txt",'w')
    with open(path, 'r') as fp:
      for line in fp:
           row = line.split('\t')
           productId = row[0]
           productId = productId.split('\n')
           productId = productId[0]
           ratingsDictionary = dict()
           #fileName = productBaseDirectory+categoryName+"/"+productId+".txt"
           fileName = productBaseDirectory + productId + ".txt"
           opened = 0
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    review = item.split('\t')
                    rating = float(review[5])
                    opened = 1
                    try:
                        ratingValue = ratingsDictionary[rating]
                        ratingValue = ratingValue + 1
                        ratingsDictionary[rating] = ratingValue
                    except KeyError as e:
                        ratingsDictionary[rating] = 1

           except IOError as e:
              print("problem opening the file")
              pass
           prior = [1,1, 1,1,1]
           #if len(ratingsDictionary)>0:
           retValue = dirichlet_mean(ratingsDictionary,prior)
           filehandle.write(productId)
           filehandle.write("\t")
           filehandle.write(str(retValue))
           filehandle.write("\n")

    filehandle.close()
    #Finished = datetime.now()
    #done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def dirichlet_mean(ratingsDictionary, prior):
        """
        Computes the Dirichlet mean with a prior.
        """
        #print("-----------------------------")
        #print("prior")
        #print(prior)
        votes = []
        for key,value in ratingsDictionary.items():
            votes.append(value)
        #print("votes")
        #print(votes)
        posterior = map(sum, zip(votes, prior))
        temp = list(map(sum, zip(votes, prior)))
        to = list(enumerate(temp))
        #print("posterior")
        #print(temp)
        #print("enum posterior")
        #print(to)
        N = sum(posterior)
        #print("Sum Posterior")
        #print(N)
        weights   = list(map(lambda i: (i[0]+1)*i[1], to))
        #print(weights)
        newlist = []
        for item in weights:
            item = item/sum(weights)
            newlist.append(item)
        #print(newlist)
        #print(sum(weights))
        retValue =  float(float(sum(weights)) / N)
        #print(retValue)
        return retValue
def computeWeightedDirichelet(path,categoryName,destDirectory):
    print("Procedure to compute product rating based on weighted dirichelet distribution")
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
           ratingsDictionary = dict()
           ratingsDateDictionary = dict()#{'1.0':None,'2.0':None,'3.0':None,'4.0':None,'5.0':None}
           timeIntervalReward = [-5,-4,-3,-2,0,6,20,100,256,512]
           prior = [1,1,1,1,1]
           productDates = []
           minDate = datetime(2050, 12, 31)
           maxDate = datetime(1950, 1, 1)
           fileName = productBaseDirectory+productId+".txt"
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    review = item.split('\t')
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
           except IOError as e:
              pass

           #print(productDates)
           #print(minDate)
           #print(maxDate)
           diff = (maxDate-minDate).days
           tempDate = minDate
           timeInterval = []
           timeInterval.append(tempDate)
           for i in range(10):
               numDays = int(diff/10)
               tempDate = tempDate + timedelta(days=numDays)
               timeInterval.append(tempDate)

           del timeInterval[-1]
           timeInterval.append(maxDate)
           missing = 0
           if len(ratingsDateDictionary)<5:
            temp = 0
            for key,value in ratingsDateDictionary.items():
                temp = temp + key
            missing = 15- temp

           starTimeIntervalRewards = []
           for key,value in ratingsDateDictionary.items():
            ratingDates = value
            ratingIntervals = []
            ratingPrior = []

            for ratingdate in ratingDates:
                finalVal = 0
                for i in range(len(timeInterval)-1):
                    if ratingdate >= timeInterval[i] and ratingdate <= timeInterval[i+1]:
                        #ratingIntervals.append(timeIntervalReward[i])
                        ratingIntervals.append((i+1))
                        break
                #ratingIntervals.append(finalVal)


            starTimeIntervalRewards.append(ratingIntervals)


           for item in starTimeIntervalRewards:
               tempVal = 0
               finalVal = 0

               for interval in item:
                   tempVal = tempVal + interval
                   '''


                  if interval>5:
                   tempVal = tempVal +1
                  else:
                   tempVal = tempVal - 1
                '''
               tempVal = int(tempVal/len(item))
               #tempVal = int(tempVal/10)
               ratingPrior.append(tempVal)
               #ratingPrior.append(finalVal)
           #print(productId)
           #print(starTimeIntervalRewards)

           filehandle.write(productId)
           filehandle.write("\t")
           #print("old prior")
           #print(prior)

           oldretValue = dirichlet_mean(ratingsDictionary,prior)
           if len(ratingsDateDictionary)<5:
               if missing != 0:
                   ratingPrior.insert(int(missing-1),0)

           prior = ratingPrior
           retValue = dirichlet_mean(ratingsDictionary,prior)

           if len(ratingPrior) > 15:
               print(productId)
               print(ratingsDictionary)
               print(starTimeIntervalRewards)
               print("Old retValue ")
               print(oldretValue)
               print("new Prior")
               print(ratingPrior)
               print("new retValue ")
               print(retValue)

           filehandle.write(str(retValue))
           filehandle.write("\n")
           

    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def generateWeights(lamda,n):
     forgettingFactors = []
     for i in range(1,n+1):
       #forgettingFactors.append(math.pow(lamda,math.exp((10-i))))
        #print((10-i))
        forgettingFactors.append(math.exp(lamda*(i-n)))
        #forgettingFactors.append(math.exp(i))
     return forgettingFactors

def generateHelpfulnessWeight(help,i):
     return help*math.exp(i)

def aggregateRatingsForAllTimePeriods(ratingTemproalCategory):
    ratingDict = {1:0,2:0,3:0,4:0,5:0}
    rating = 1
    for cat in ratingTemproalCategory:
        sum = 0
        for item in cat:
            sum = sum + cat[item]
        ratingDict[rating] = sum
        rating = rating + 1

    return ratingDict
from ranking import buildFeatureListForCategoryRetDict
from sklearn.externals import joblib
def computeRatingFromLearning(productBaseDirectory,path,categoryName,destDirectory):
    print("Considering " + categoryName)

    learningDirectory ="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Learning_Models/GThan100/LassRegression/"
    learningFile = learningDirectory+categoryName+'.pkl'
    if not os.path.exists(learningFile):
        return
    X,y = buildFeatureListForCategoryRetDict(path,productBaseDirectory)
    ridge= joblib.load(learningFile)
    print("learningFile")
    print(learningFile)
    print("ridge")
    print(ridge)
    predictions = ridge.predict(X)
    filehandle = open(destDirectory + categoryName + ".txt", 'w')
    index = 0
    for product in y:
        filehandle.write(product)
        filehandle.write("\t")
        filehandle.write(str((predictions[index])))
        filehandle.write("\n")
        index+=1
    filehandle.close()
    print("Done")
    return
def computeDiricheletwithTimeWindow(productBaseDirectory,path,categoryName,destDirectory):
    #print("Procedure to compute product rating based on dirichelet distribution with Forgetting factor")
    print("Considering "+categoryName)
    start = datetime.now()
    line = ""
    filehandle = open(destDirectory+categoryName+".txt",'w')
    productBaseDirectory = productBaseDirectory+categoryName+"/"
    with open(path, 'r') as fp:
      for line in fp:
           row = line.split('\t')
           productId = row[0]
           productId = productId.split('\n')
           productId = productId[0]
           #print(productId)
           prior = [2,2,2,2,2]
           lamda = 0.9
           #n = 35
           #print(forgettingFactors)
           #print("original")
           ratingTemproalCategory,ratingHelpfulnessCategory,n = analyzeProduct(productBaseDirectory,productId)
           #print(ratingTemproalCategory)
           forgettingFactors = generateWeights(lamda,n)
           #for i in range(len(ratingTemproalCategory)):
            #    print(ratingTemproalCategory[i])
           #print("------------------------------------------------")
           ratingTemproalCategoryWeighted = []
           ratingHelpfCategoryWeighted = []
           #print(ratingTemproalCategory)
           #print("forgettingFactors")
           #print(forgettingFactors)
           for i in range(len(ratingTemproalCategory)):
               newCat = dict()
               helpCat = dict()
               #print("------------")
               counta = 1
               for item in ratingTemproalCategory[i]:
                   newhelp = ratingHelpfulnessCategory[i][item]
                   #print("old help")
                   #print(ratingHelpfulnessCategory[i][item])
                   #newhelp = generateHelpfulnessWeight(ratingHelpfulnessCategory[i][item],counta)
                   #print("newhelp")
                   #Old Rating
                   #newCat[item] = round((ratingTemproalCategory[i][item])*(forgettingFactors[item-1]+((forgettingFactors[item-1]+(forgettingFactors[item-1]*ratingHelpfulnessCategory[i][item])))),3)
                   '''print("help")
                   print(ratingHelpfulnessCategory[i][item])
                   print("time weight")
                   print(counta/n)
                   print("sum*100")
                   print(math.exp((100*((counta/n)+ratingHelpfulnessCategory[i][item]))))
                   print("votes weight")
                   '''
                   newCat[item] = ratingTemproalCategory[i][item]*(math.exp((10*((counta/n)+ratingHelpfulnessCategory[i][item]))))
                   #print(newCat[item])
                   #helpCat[item] = round(newhelp,3)
                   counta+=1
               #print(newCat)
               ratingTemproalCategoryWeighted.append(newCat)
               ratingHelpfCategoryWeighted.append(helpCat)
           #------------------------------------------------------------------------------------------------------------
           '''
           #Preparing Prior on just summing the degree of helpfulness
           newHelpfulnessPrior = aggregateRatingsForAllTimePeriods(ratingHelpfulnessCategory)
           newHelpPriorValuesOld = []
           for help in newHelpfulnessPrior:
               newHelpPriorValuesOld.append((round(newHelpfulnessPrior[help],3)))
           #------------------------------------------------------------------------------------------------------------
           #print("OLD newHelpfulnessPrior")

           #------------------------------------------------------------------------------------------------------------
           #Preparing New Prior on just summing the degree of helpfulness*NumVotes
           #print(ratingHelpfCategoryWeighted)
           newHelpPriorValues = aggregateRatingsForAllTimePeriods(ratingHelpfCategoryWeighted)

           newHelpPriorValuesNew = []
           #print("OLD HelpPriorValues")
           #print(newHelpPriorValues)
           for help in newHelpPriorValues:
               newHelpPriorValuesNew.append(round(newHelpPriorValues[help]/n,3))
           #------------------------------------------------------------------------------------------------------------
           #print("helpfulness")
           #print(newHelpPriorValuesNew)
           #prior = newHelpPriorValuesNew
           #for i in range(5):
            #   prior[i] = prior[i]+newHelpPriorValuesNew[i]
           #print("New Prior")
           #print(prior)

           #print(ratings)
           '''
           ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategoryWeighted)
           #print(ratings)
           '''
           count = 0
           for key,value in ratings.items():
               prior[count] = int(value*2)
               count+=1
           print("prior")
           print(prior)
           '''
           retValue = dirichlet_mean(ratings,prior)
           filehandle.write(productId)
           filehandle.write("\t")
           filehandle.write(str((retValue)))
           filehandle.write("\n")
           #break
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
def computeAverageAndDirichelet(path,categoryName,destDirectory):
    print("Procedure to compute product rating based on weighted dirichelet distribution")
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
           ratingsDictionary = dict()
           prior = [1,1,1,1,1]
           fileName = productBaseDirectory+productId+".txt"

           counter = 0
           overallRate = 0
           try:
              with open(fileName, 'r') as filep:
                for item in filep:
                    review = item.split('\t')
                    overallRate = overallRate + float(review[5])
                    counter = counter + 1
                    #Extracting Rates
                    rating = float(review[5])
                    try:
                        ratingValue = ratingsDictionary[rating]
                        ratingValue = ratingValue + 1
                        ratingsDictionary[rating] = ratingValue
                    except KeyError as e:
                        ratingsDictionary[rating] = 1
                    #-----------------------------------------------------------------------------
           except IOError as e:
              pass
           filehandle.write(productId)
           filehandle.write("\t")
           overallRate = overallRate/counter
           filehandle.write(str((overallRate)))
           filehandle.write("\t")
           retValue = dirichlet_mean(ratingsDictionary,prior)
           filehandle.write(str((retValue)))
           filehandle.write("\n")


    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computeTrueRateForAllCategoreis(productBaseDirectory,directory,option,destDirectory,startFrom):
    print("Procedure to read Compute all product categories Rating ")
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
                computeMajorityVoteForProductCategories(productBaseDirectory,path,categoryName,destDirectory)
            elif option == 1:#Normal Dirichelet
                computeNormalDirichelet(productBaseDirectory,path,categoryName,destDirectory)
            elif option == 2:#Weighted Dirichelet
                computeWeightedDirichelet(path,categoryName,destDirectory)
            elif option == 3:#Average & Dirichelet
                computeAverageAndDirichelet(path,categoryName,destDirectory)
            elif option == 4:#Dirichelet with forgetting factor
                computeDiricheletwithForgettingFactor(path,categoryName,destDirectory)
            elif option == 5:
                computeDiricheletwithTimeWindow(productBaseDirectory,path,categoryName,destDirectory)
            elif option == 6:
                computeRatingFromLearning(productBaseDirectory, path, categoryName, destDirectory)
            elif option == 7:
                computeNumberOfReviewsForProductCategories(productBaseDirectory, path, categoryName, destDirectory)
            elif option == 8:
                computExponentialModel(productBaseDirectory, path, categoryName, destDirectory)
                #break
            if categoryName == "Baby":
                break
        #if index == 1:
        #  break
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

        #if index == (endAt-1):
         #   break
        #if index == 1:
         # break
        index = index + 1

    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    print("done out")
    return

from alogrithms import *
def sortRatedCategory(filePath,category,destDirectory):
    print("Procedure to read category rated File, get a product from it and read its file and sort it and write to a file for a cetegory file")
    print("Considering "+category)
    #product_Id Category sales_rank
    import sys
    sys.setrecursionlimit(10000000)

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
    #quickSort(listofProducts)
    '''listofProducts.clear()
    listofProducts.append(("A",15))
    listofProducts.append(("A",20))
    listofProducts.append(("A",50))
    listofProducts.append(("A",30))
    listofProducts.append(("A",25))
    listofProducts.append(("A",10))'''
    #merge_sort(listofProducts)
    mergeSort(listofProducts)
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
            #break
        #if index == (endAt-1):
           # break
        #if index == 1:
        #  break
        index = index + 1


    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")

    print("done out")
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
    print(path1)
    print(path2)
    try:
        with open(path1, 'r') as fp:
          for line in fp:
             tuple = line.split('\t')
             salesRankList.append(tuple[0])
    except IOError as e:
        print("error opening file " + path1)
        return
    try:
        with open(path2, 'r') as fp:
          for line in fp:
             tuple = line.split('\t')
             majorityVoateList.append(tuple[0])
    except IOError as e:
        print("error opening file " + path1)
        return

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
            found = 0
            for majority in (majorityVoateList):
                #print("sales "+str(sales))
                #print("majority "+str(majority))
                if sales == majority:
                    difference = salesIndex - majorIndex
                    majorityProduct.append(majority)
                    majorityIndices.append(majorIndex)
                    #filehandle.write(sales)
                    #filehandle.write("\t")
                    #filehandle.write(str(difference))
                    #filehandle.write("\n")
                    found = 1
                    break
                majorIndex = majorIndex + 1
            salesIndex = salesIndex + 1
            if found == 0:
                print("Didn't find "+sales)
    #filehandle.close()
    print("majorityIndices")
    print(len(majorityIndices))
    print("salesRankIndices")
    print(len(salesRankIndices))
    print("majorityVoateList")
    print(len(majorityVoateList))
    if len(salesRankIndices)>0:
        filePath = destDirectory + category + ".txt"
        filehandle = open(filePath, 'w')

    for i in range(len(salesRankIndices)):
        filehandle.write(str(salesRankIndices[i]))
        filehandle.write("\t")
        #filehandle.write(str(salesRankProduct[i]))
        #filehandle.write("\t")
        #filehandle.write(str(majorityProduct[i]))
        #filehandle.write("\t")
        filehandle.write(str(majorityIndices[i]))
        filehandle.write("\n")

    if len(salesRankIndices) > 0:
        filehandle.close()

    Finished = datetime.now()
    done = Finished - start
    #print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")

    print("done in")
    return
def computeKendalTau(directory):
    print("Procedure to Kendall Tau between computed rating and sales rank")
    for filename in os.listdir (directory):
        category = filename
        filename = directory+filename
        salesRank = []
        predicted = []
        with open(filename, 'r') as fp:
            for line in fp:
                row = line.split("\n")
                row = row[0].split("\t")
                salesRank.append(row[0])
                predicted.append(row[1])
        tau, _ = stats.kendalltau(salesRank, predicted)
        tau = round(tau, 3)
        print(category +' '+str(tau))

    return
from ranking_metrics import *
def computeNDCG(directory,k):
    print("Procedure to NDCG between computed rating and sales rank")
    num = 0
    sumNDCG = 0
    for filename in os.listdir(directory):
        category = filename
        filename = directory + filename
        r = []
        with open(filename, 'r') as fp:
            for line in fp:
                row = line.split("\n")
                row = row[0].split("\t")
                r.append(int(row[0])-int(row[1]))

        for i in range(len(r)):
            r[i]+=len(r)

        ndcg = ndcg_at_k(r,k,0)

        ndcg = round(ndcg, 4)
        print(category + ' ' + str(ndcg))
        sumNDCG+=ndcg
        num+=1
    AvgNDCG = sumNDCG/num
    AvgNDCG = round(AvgNDCG,4)
    print("Average NDCG @ " +str(k) +" ="+str(AvgNDCG))
    return AvgNDCG
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
def getProductsLifeCycle(sourceCategory,productBaseDirectory,destFilePath):
    filehandle = open(destFilePath,'w')
    for filename in os.listdir (sourceCategory):
        filehandle.write(filename)
        filehandle.write("\n")
        with open(sourceCategory+filename, 'r') as fp:
          for line in fp:
               row = line.split('\t')
               productId = row[0]
               productId = productId.split('\n')
               productId = productId[0]
               productPath = productBaseDirectory+productId+".txt"
               lifecyle,n = getProductAllLiefCycle(productPath)
               filehandle.write(str(lifecyle))
               filehandle.write("\t")
               filehandle.write(str(n))
               filehandle.write("\n")
        print(filename)
        filehandle.write("\n")
    filehandle.close()
    return
#------------------------------------Program Start----------------------------------------------------------------------
import sys
import os
from datetime import datetime
from datetime import timedelta
import math
from temp_Function import  *
from scipy import stats
#-----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    '''
    x = str(sys.argv[1])
    y = str(sys.argv[2])
    z = str(sys.argv[3])
    sys.stdout.write(str(createNewVerifiedDataset(x,y,z)))
    '''

    '''
    To do dirichlet Rating
    print("Please Enter Input Directory Option Destination ")
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
    option = 1
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_normal_dirichelet_rating/"
    startFrom = 0
    computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory,startFrom)
    '''
    '''
    Sorting Categories
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_normal_dirichelet_rating/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_dirichlet_sorted/"
    sortRatedCategories(sourceDirectory,destDirectory,0)
    '''
    '''
    Measuring Difference between sales rank and computed ranking
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_average_sorted/"
    destDirectory =   "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_average_R/"
    salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/categories_sorted_sales_rank/"
    measureDistanceBetweenSalesRankandRatedCategories(salesDirectory,sourceDirectory,destDirectory,0)
    '''

    ##-----------------------------------------------Testing-------------------------------------------------------------------------------------------------------------------------
    '''
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
    option = 2
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    startFrom = 0
    computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory,startFrom)

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    sortRatedCategories(sourceDirectory,destDirectory,0)

    salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_sales_rank/"
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    destDirectory =   "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/R_Difference/test/"
    measureDistanceBetweenSalesRankandRatedCategories(salesDirectory,sourceDirectory,destDirectory,0)
    '''

    '''
    ##--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
    option = 2
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    startFrom = 0
    computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory,startFrom)

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    sortRatedCategories(sourceDirectory,destDirectory,0)

    salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_sales_rank/"
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    destDirectory =   "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/R_Difference/test/"
    measureDistanceBetweenSalesRankandRatedCategories(salesDirectory,sourceDirectory,destDirectory,0)

    '''
    '''
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets/Dataset_50/"
    option = 3
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/Datasets/Dataset_50/"
    startFrom = 0
    computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory,startFrom)
    '''

    #Computing MAE for Mean and Simple Dirichlet
    '''
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_50/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/MAE_Datasets/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_50_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_100/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_100_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_200/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_200_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_300/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_300_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_400/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_400_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_500/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_500_MAE")

    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/computed_mean_dirichlet_different_datasets/Dataset_1000/"
    computeMAEForLists(sourceDirectory,destDirectory,"Dataset_1000_MAE")

    '''


    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    #productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Product_Reviews_Verified/"
    #productBaseDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Product_Reviews/"
    #categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\Datasets\Dataset_100/"
    #categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\Datasets\Dataset_L_100/"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    #categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Datasets_Verified/Dataset_100/"
    #categories_path = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Datasets/Dataset_400/"
    #categories_path = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/categories/"
    option = 8
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    #destDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Computed_Rating/test/"
    startFrom = 0
    #computeTrueRateForAllCategoreis(productBaseDirectory,categories_path,option,destDirectory,startFrom)


    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Computed_Rating/test/"
    destDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    #sourceDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Computed_Rating/test/"
    #destDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Sorted_Categories/test/"
    #sortRatedCategories(sourceDirectory,destDirectory,0)

    #salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categores_sorted_sales_rank_dataset_more_1000/"
    salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_sales_rank/"
    #salesDirectory =  "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_verified/categores_sorted_sales_rank_dataset_more_100/"
    #salesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_non_verified/categores_sorted_sales_rank_dataset_more_100/"
    #salesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_non_verified/categores_sorted_sales_rank_dataset_less_100/"
    #salesDirectory =  "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Sorted_Categories/categores_sorted_sales_rank_dataset_more_400/"
    #salesDirectory =  "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Sorted_Categories/categories_sorted_sales_rank/"
    sourceDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/test/"
    #sourceDirectory = "/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/Sorted_Categories/test/"
    destDirectory ="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/R_Difference/test/"
    #destDirectory ="/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/R_Difference/test/"
    #measureDistanceBetweenSalesRankandRatedCategories(salesDirectory,sourceDirectory,destDirectory,0)

    #computeKendalTau(destDirectory) Compute Kendall
    #computeNDCG(destDirectory)

    #destFilePath="/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/LifeCycleAnalysis/Cat_400.txt"
    #destFilePath="/research/remote/petabyte/users/yassien/Unique_Products_Stanford_three/Experiment_2/LifeCycleAnalysis/Cat_400.txt"
    #getProductsLifeCycle(categories_path,productBaseDirectory,destFilePath)
    #productIDPath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/B0002KHBS2.txt"
    #getProductAllLiefCycleTest(productIDPath)
