
#from exp17 import product_details
from bs4 import BeautifulSoup
import urllib.request

def product_details(url,productId):
    proxy_handler = urllib.request.ProxyHandler({"http": "http://bproxy.rmit.edu.au:8080"})
    proxy_auth_handler = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    product={}
    try:
        x = opener.open(url)

        print("AMAZON...product details")

        #-----------------------------------------------------------------------------
        soup=BeautifulSoup(x.read(),"html5lib")
        counter = 0
        for a in soup.find_all('a', href=True):
            extractedUrl = a['href']
            if productId in extractedUrl and "product-reviews" in extractedUrl:
                #print ("Found the URL:", a['href'])
                counter = counter + 1
        r1= soup.find(id="price")
        #print("counter")
        #print(counter)
        #-----------------------------------------------------------------------------
        mrp = None
        if r1 !=None:
            r2= r1.table.find_all("tr")
            mrp= r2[0].find_all("td")[1].text.strip()

        r3= soup.find(id="averageCustomerReviews")
        if(r3.find(id="acrPopover")):
            rating= r3.find(id="acrPopover")['title'].strip()[0]
        else:
            rating="0"
        if(r3.find(id="acrCustomerReviewText")):
            reviews= r3.find(id="acrCustomerReviewText").text.strip()[:-17]
        elif(r3.find(id="acrCustomerWriteReviewText")):
            reviews="0"
        else:
            reviews="not available"
        if(soup.find(id="altImages")):
            images=len(soup.find(id="altImages").find_all("li",{"class":"a-spacing-small item"}))
        else:
            images=0
        if(soup.find(id="productDescription")):
            description=soup.find(id="productDescription").find("div",{"class":"productDescriptionWrapper"}).text.strip()
        else:
            description="Not Available"
        product['mrp']=mrp
        product['reviews']=reviews
        product['images']=images
        product['rating']=rating
        product['description']=description

        numberVerified = 0
        numberID = 0
        numCommon = 0
        authorID = ""
        name = ""
        r1=soup.find_all("div",{"class":"a-row"})
        for x in range(0,len(r1)):
            r2=r1[x].find("span",{"class":"a-size-mini a-color-state a-text-bold"})
            r3=r1[x].find("a",{"class":"noTextDecoration"})
            verified = "Not Verified Purchase"
            if r2 != None:
                verified = r2.text.strip()
                numberVerified = numberVerified + 1
            if r3 != None:
                 idLink = r3['href']
                 parts = idLink.split("/")
                 authorID = parts[len(parts)-1]
                 name = r3.text.strip()
                 numberID = numberID + 1
            if r2 != None and r3 != None:
                numCommon = numCommon +1
            if authorID!="" and name !="":
                print(authorID +" "+name +" "+verified)
        print("Num Common")
        print(numCommon)
        print("Num Verified")
        print(numberVerified)
        print("Num ID")
        print(numberID)
    except urllib.error.HTTPError as e:
        print("Service Unavailable")
    print("....Done")
    return product
def clear_learning_directories(catNames,basic_directory):
    #catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    for cat in catNames:
        dest_directory = basic_directory + cat + "/"
        working_directory = dest_directory + "Cutoff_10/"
        import os
        import shutil
        lst = os.listdir(working_directory)
        for folder in lst:
            setFilePath = working_directory + folder
            print("Processing " + str(setFilePath))
            if os.path.isdir(setFilePath):
                setFilePath = working_directory + folder + "/"
                if "Set" in folder:
                    lst2 = os.listdir(setFilePath)
                    for file in lst2:
                        if "test.txt" != file:
                            file_path = setFilePath + file
                            print("To Delete " + file_path)
                        try:
                            os.remove(file_path)
                        except FileNotFoundError:
                            print("pass")

                    shutil.copy2(
                        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\Mixed_Queries_For_Training/train.txt',
                        setFilePath)
                    shutil.copy2(
                        'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\Mixed_Queries_For_Training/valid.txt',
                        setFilePath)
                    continue
                else:
                    os.chmod(setFilePath, 0o644)
                    shutil.rmtree(setFilePath)
                    # os.remove(setFilePath)
            else:
                os.remove(setFilePath)
    return
print("Hi")
url = "https://www.amazon.com/dp/0000031852"
productId = "0000031852"
#product= product_details(url,productId)
#print("product")
catNames = ["Arts, Crafts & Sewing", "Video Games","Cell Phones & Accessories"]

basic_directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/"
#clear_learning_directories(catNames,basic_directory)


'''import os
import  shutil
des = "F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_with_var_train/"
lst = os.listdir(des)
for folder in lst:
    setFilePath = des + folder+"/"
    lst2 = os.listdir(setFilePath)
    for folder2 in lst2:
        setFilePath2 = setFilePath + folder2 + "/"
        lst3 = os.listdir(setFilePath2)
        for folder3 in lst3:
            setFilePath3 = setFilePath2 + folder3 + "/"
            if os.path.isdir(setFilePath3):
                shutil.copy2(
                    setFilePath3+'train.txt',
                    setFilePath3 + 'valid.txt')'''

import requests

jwt_end_point = "https://insites-api.gd/v2/company/{20765463}"
pay_load={"password":"admin",
          "rememberMe":"true",
          "username":"admin"}
jwt_end_response = requests.post(jwt_end_point,json=pay_load)
print("hi")
print(jwt_end_response.json())