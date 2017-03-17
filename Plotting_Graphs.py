import pylab as plt


def readProductsLifeTimeData(filePath):
    numDays = []
    with open(filePath, 'r') as fp:
        for line in fp:
            row = line.split('\n')
            numDays.append(int(row[0]))
    return numDays
def computeRangesfromProductsNumDays(numDays):
    numProducts = len(numDays)
    maxLength = max(numDays)
    numperiods = int(maxLength / 180)

    periods = []
    months = []
    for i in range(numperiods):
        periods.append(i * 180)
        months.append(int(periods[i] / 30))

    if periods[len(periods) - 1] < maxLength:
        periods.append(maxLength)
        months.append(int(maxLength / 30))

    periodsDict = dict()
    for i in range(len(periods) - 1):
        periodsDict[(periods[i], periods[i + 1])] = 0

    for days in numDays:
        for key, value in periodsDict.items():
            start = key[0]
            end = key[1]
            if days > start and days <= end:
                newVal = value + 1
                periodsDict[key] = newVal

    x = []
    y = []

    numProducts = 0
    for per in periods:
        for key, value in periodsDict.items():
            if key[0] == per:
                numProducts += value
                x.append(key)
                y.append(value)
                break

    lastMonth = months[-1]
    x = months
    if len(x)>len(y):
        del x[-1]
        x[len(x)-1] = lastMonth
    return x,y,numProducts
def plotHistogram(x,y,title,xLable,yLabel,catName,show):
    plt.title(title)
    plt.xlabel(xLable)
    plt.ylabel(yLabel)
    plt.hist(x, len(x),weights=y)
    plt.show()
    return plt
def computeAndPlotPorductCategoryLifeSpanData(catName,show):
    filePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Categories_Lifetime/" + catName + ".txt"
    numDays = readProductsLifeTimeData(filePath)
    x, y,numProducts = computeRangesfromProductsNumDays(numDays)
    title =  catName+" Products LifeSpan Distributions("+str(numProducts)+")"
    xlabel = "Number of Months "
    ylabel = "Number of Products"
    plotHistogram(x, y, title, xlabel, ylabel)
    return
def computeAndPlotPorductCategoryLifeSpanDataForCombination(catName,xs,ys):
    filePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Categories_Lifetime/" + catName + ".txt"
    numDays = readProductsLifeTimeData(filePath)
    x, y,numProducts = computeRangesfromProductsNumDays(numDays)
    xs.append(x)
    ys.append(y)
    return xs,ys

''''
catName = "Video Games"
categoryNameList = ["Arts, Crafts & Sewing","Cell Phones & Accessories","Computers & Accessories","Electronics","Industrial & Scientific","Jewelry","Software","Toys & Games","Video Games"]
xs = []
ys = []
for cat in categoryNameList:
    xs,ys=computeAndPlotPorductCategoryLifeSpanDataForCombination(cat,xs,ys)

for i in range(len(xs)):
    plt.hist(xs[i], len(xs[i]),alpha=0.5, weights=ys[i],label=categoryNameList[i])
plt.legend(loc='upper right')
plt.title("Products LifeSpan Distributions")
plt.xlabel("Number of Months")
plt.ylabel("Number of Products")
plt.show()
'''

from temp_Function import analyzeProduct
from datetime import timedelta
productBaseDirectory= "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
productId = "B001HDOQHM"
ratingTemproalCategory, ratingHelpfulnessCategory, n, average,numReviews,numFeedBackPerDayDictionary,numHelpFeedPerDayDictionary,ratingsDateDictionary = analyzeProduct(productBaseDirectory,productId)
print("Actual Num Reviews")
print(numReviews)
#print(ratingTemproalCategory)
#print("ratingsDateDictionary")
#print(ratingsDateDictionary)
datesrating = []
for key,value in ratingsDateDictionary.items():
    for val in value:
        datesrating.append((val,key))
datesrating=sorted(datesrating)
#for daterate in datesrating:
  #  print(daterate[0])
proportionalPeriods = []
numRviewsCutoff = int(numReviews/10)
index= 0
proportionalPeriods.append(datesrating[0][0])
for daterate in datesrating:
    #print(daterate[1])
    if index == numRviewsCutoff :
        proportionalPeriods.append(daterate[0])
        index=0
    else:
        index+=1
if index!=0:
    proportionalPeriods.append(datesrating[len(datesrating)-1][0])
print("numRviewsCutoff")
print(numRviewsCutoff)
print("proportionalPeriods")
print(len(proportionalPeriods))
print(proportionalPeriods)
for i in range(len(proportionalPeriods)-1):
    print((proportionalPeriods[i+1]-proportionalPeriods[i]).days)

numDaysDiff = (datesrating[len(datesrating)-1][0]-datesrating[0][0]).days
print("numDaysDiff")
print(numDaysDiff)
print("numMonths")
numMonths = int(numDaysDiff/30)
print(numMonths)
print("numYears")
print(int(numMonths/12))
pace = int(numDaysDiff/10)
print("pace")
print(pace)

periods = []
current = datesrating[0][0]
periods.append(current)
for i in range(10):
    current = current + timedelta(days=pace)
    periods.append(current)

if periods[len(periods)-1]<datesrating[len(datesrating)-1][0]:
    del periods[-1]
    periods.append(datesrating[len(datesrating)-1][0])
#print("Periods")
#print(len(periods))
#print(periods)
numReviewsPerPeriod = dict()
totalNumReviews = 0
for daterate in datesrating:
    date = daterate[0]
    rate = daterate[1]
    periodID = 0
    for i in range(len(periods)-1):
        if date >=periods[i]and date<=periods[i+1]:
            periodID = i
            try:
                numReviews = numReviewsPerPeriod[i]+1
                numReviewsPerPeriod[i]=numReviews
                totalNumReviews+=1
            except KeyError:
                numReviewsPerPeriod[i] = 1
                totalNumReviews += 1

print("numReviewsPerPeriod")
print(numReviewsPerPeriod)
for key,value in numReviewsPerPeriod.items():
    print(str(key+1)+" "+str(value))
print("totalNumReviews read")
print(totalNumReviews)




