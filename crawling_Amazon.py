
def extractVerifiedFromUrl(url,productUserVerification,browser):

    '''from fake_useragent import UserAgent
    ua = UserAgent()
    ua.ie
    '''
    import time
    import random
    import urllib.request
    from bs4 import BeautifulSoup
    print(url)
    proxy_handler = urllib.request.ProxyHandler({"http": "http://bproxy.rmit.edu.au:8080"})
    proxy_auth_handler = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    opener.addheaders = [('User-agent', browser)]
    result = 0
    #url = "https://www.amazon.com/dp/0000031852"
    try:
        x = opener.open(url)
        try:
            soup=BeautifulSoup(x.read(),"html5lib")
            authorID = ""
            name = ""
            r1=soup.find_all("div",{"class":"a-section review"})
            if len(r1)==0 :
                print("Could not load")
                result = -1
                time.sleep(5+(random.random()-0.5)*5)
                return productUserVerification, result
            for x in range(0,len(r1)):
                verified = "Not Verified Purchase"
                r2=r1[x].find_all("span",{"class":"a-size-mini a-color-state a-text-bold"})
                for y in r2:
                    verified = y.text.strip()
                r3=r1[x].find_all("a",{"class":"a-size-base a-link-normal author"})
                for y in r3:
                    res = str(y).split("profile")
                    res = res[1].split(">")
                    res = res[0].split("/")
                    res = res[1].split('"')
                    authorID =res[0]
                    name = y.text.strip()

                if authorID != "":
                    try:
                        availableString = productUserVerification[authorID+" "+name]
                        productUserVerification[authorID+" "+name] = verified
                    except KeyError as e:
                        productUserVerification[authorID+" "+name] = verified
        except urllib.error.HTTPError as e:
                print("Service Unavailable")
                print("Sleeping")
                result = -1
                time.sleep(50)
                return productUserVerification, result


    except urllib.error.URLError as e1:
        print("Connection refused")
        print("Sleeping")
        result = -1
        time.sleep(20+(random.random()-0.5)*5)
    return productUserVerification, result
def getProductVerifiedPurchase(url,productId):
    '''
    proxy_handler = urllib.request.ProxyHandler({"http": "http://bproxy.rmit.edu.au:8080"})
    proxy_auth_handler = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    productUserVerification = dict()
    print("AMAZON...product verified Purchases")
    result = 0
    try:
        x = opener.open(url)
        soup=BeautifulSoup(x.read(),"html5lib")
        authorID = ""
        name = ""
        r1=soup.find_all("div",{"class":"a-section celwidget"})
        for x in range(0,len(r1)):
            verified = "Not Verified Purchase"
            r2=r1[x].find_all("span",{"class":"a-size-mini a-color-state a-text-bold"})
            for y in r2:
                res = str(y).split("\n")

                verified = res[1]
            r3=r1[x].find_all("a",{"class":"noTextDecoration"})
            for y in r3:
                res = str(y).split("profile")
                res = res[1].split(">")
                res = res[0].split("/")
                res = res[1].split('"')
                authorID =res[0]
                name = y.text.strip()

            if authorID != "":
                try:
                    availableString = productUserVerification[authorID+" "+name]
                    productUserVerification[authorID+" "+name] = verified
                except KeyError as e:
                    productUserVerification[authorID+" "+name] = verified
        '''
    import urllib.request
    from bs4 import BeautifulSoup
    productUserVerification = dict()
    result = -1
    previousCount = 0
    numRepition = 0
    externalRepition = 0
    for i in range(500):
        result = -1
        newUrl="http://www.amazon.com/product-reviews/"
        newUrl = newUrl + productId +"?pageNumber="+str(i)
        #newUrl="http://www.amazon.com/product-reviews/0001473123?pageNumber=2"
        numServiceUnAval = 0
        browserIndex = 0
        numRepition = 0
        browsers = ['Mozilla/5.0','Opera/9.80','Safari/537.36','Chrome/47.0.2526.111','AppleWebKit/537.36','Trident/7.0']
        while result == -1:
            if browserIndex > 5:
                browserIndex = 0
            productUserVerification, result = extractVerifiedFromUrl(newUrl,productUserVerification,browsers[browserIndex])
            if result == -1:
                numServiceUnAval = numServiceUnAval + 1
                browserIndex = browserIndex + 1
            if previousCount == len(productUserVerification):
                numRepition = numRepition + 1
            if previousCount != len(productUserVerification):
                previousCount = len(productUserVerification)
            if numRepition == 3:
                break

        if numRepition == 3:
            break
    return productUserVerification, result
def crawlPorductVerification(productId,destDirectory):

    productUrl = "http://www.amazon.com/dp/"+productId
    print(productId)
    import urllib.request
    from bs4 import BeautifulSoup
    productUserVerification,result = getProductVerifiedPurchase(productUrl,productId)
    print(len(productUserVerification))
    if len(productUserVerification)>0:
        filePath = destDirectory+"/"+productId+".txt"
        filehandle = open(filePath,'w')
        for key,value in productUserVerification.items():
            try:
                string = str(key)+" "+str(value)+"\t"
                filehandle.write(string)
                if value == "Verified Purchase":
                    filehandle.write("1")
                else:
                    filehandle.write("0")
                filehandle.write("\n")
            except UnicodeEncodeError as e:
                pass
        filehandle.close();
    return
def crawlDataForCategories(directory,startFrom,endAt):
    import os
    print("AMAZON...product verified Purchases")
    index = 0
    twohundredCounter = 0
    import time
    import urllib.request
    from bs4 import BeautifulSoup
    for filename in os.listdir (directory):
        categoryName = filename
        categoryName = categoryName.split(".txt")
        categoryName = categoryName[0]
        print("Considering "+categoryName)
        filePath = directory+filename
        destinationCat = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories_verified/"+categoryName
        if index >= startFrom:
            innnedIndex = 0
            with open(filePath, 'r') as fp:
                for line in fp:
                   if innnedIndex >= 3000:
                       productId = line.split("\t")
                       productId = productId[0]
                       crawlPorductVerification(productId,destinationCat)
                       if innnedIndex == endAt:
                             break
                       if twohundredCounter == 100:
                           print("Sleeping")
                           time.sleep(200)
                           twohundredCounter = 0
                       twohundredCounter = twohundredCounter + 1

                   innnedIndex = innnedIndex + 1
        index = index + 1


    print("......Done")

#crawlDataForCategories("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/",31,30000)
productUrl = "https://www.amazon.com/dp/0000031852"
productId = "0000031852"
getProductVerifiedPurchase(productUrl,productId)
