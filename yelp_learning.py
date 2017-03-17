import json
'''
sourcefilePath="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json"
rData = open(sourcefilePath, 'r', encoding='utf-8')
print("Started")
print("Loading JSON")
# reviews_parsed = json.loads(rData.read())
num_busnesses = 0
num_resturants = 0
rest_sub_cat_dict = dict()
bus_sub_cat_dict= dict()
with rData as myfile:
    for line in myfile:
        jsonLine = json.loads(line)
        categories = jsonLine['categories']
        is_rest = 0
        for cat in categories:
            if cat =="Restaurants":
                num_resturants+=1
                is_rest=1
                break
        for cat in categories:
            if is_rest==1:
                try:
                    rest_sub_cat_dict[cat]+=1
                except KeyError:
                    rest_sub_cat_dict[cat]=1
            if is_rest == 1:
                try:
                    busineses=bus_sub_cat_dict[cat]
                    busineses.append((jsonLine['business_id'],jsonLine['review_count']))
                    bus_sub_cat_dict[cat]=busineses
                except KeyError:
                    busineses= []
                    pair = (jsonLine['business_id'],jsonLine['review_count'])
                    busineses.append(pair)
                    bus_sub_cat_dict[cat] = busineses
        num_busnesses += 1


print("Num Resturants is "+str(num_resturants))
print("Num Businesses is "+str(num_busnesses))
num_sub_cats = 0
for key,valule in rest_sub_cat_dict.items():
    if valule>=1000:
        print(key+" "+str(valule))
    num_sub_cats+=1
print("Num sub cats of resturants is "+str(num_sub_cats))


for key,value in bus_sub_cat_dict.items():
    if key == "Italian"or key =="American (New)"or key =="American (Traditional)"or key =="Thai"or key =="Chinese"or key =="Mexican"or key =="Japanese"or key =="Cafes" or key=="Bars":
        filehandle = open("C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews\yelp_dataset_challenge_academic_dataset/Resturants_Categories/" + key + ".txt",'w')
        print(key+" "+str(len(value)))
        for pair in value:
            business = pair[0]
            rev_count = pair[1]
            filehandle.write(business+"\t"+str(rev_count)+"\n")
        #print(value)




import  os
sourceDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/Resturants_Categories/"
for file in os.listdir(sourceDirectory):
    file_path = sourceDirectory+file
    num_gt_100=0
    avg_rev_count = 0
    num_business = 0
    with open(file_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            if int(row[1])>=100:
                num_gt_100+=1
            avg_rev_count+=int(row[1])
            num_business+=1
    avg_rev_count=round(avg_rev_count/num_business,0)
    print(file+" num_business "+str(num_business)+" avg_rev_count "+str(avg_rev_count)+" num_gt_100 "+str(num_gt_100))

'''
from datetime import datetime
import  os
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
def compute_yelp_usefulness(category_baseDirectory,productBaseDirectory,dataset_type):
    for filename in os.listdir(category_baseDirectory):
        category_file_path = category_baseDirectory + filename
        funny = 0
        useful = 0
        cool = 0
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                product_file_path = productBaseDirectory + row[0] + ".txt"

                try:
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            row2 = line2.split("\t")
                            if dataset_type == "yelp":
                                for item in row2:
                                    votes = str(row2[2]).split(',')
                                    funny+= int(votes[0].split(':')[1])
                                    useful+= int(votes[1].split(':')[1])
                                    cool+= int(votes[2].split(':')[1].split('}')[0])
                except FileNotFoundError:
                    pass
        print(filename +"U "+str(useful)+" C "+str(cool)+" F "+str(funny))
    return
import math
def compute_TQ_for_Yelp(category_baseDirectory,productBaseDirectory,dest_category,categoriesList):
    print("Computing TQ Rank score for Yelp Dataset")
    for category in categoriesList:
        print("Considering "+str(category))
        predictions_file_path = dest_category+category+"/Cutoff_10/Set_1/predictions.txt"
        all_predictions_file_path = dest_category+category+"/Cutoff_10/"+category+".txt"
        filehandle = open(predictions_file_path, 'w')
        filehandle2 = open(all_predictions_file_path,'w')
        category_file_path = category_baseDirectory + category+".txt"
        num_products =0
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                productid = row[0]
                product_file_path = productBaseDirectory + productid + ".txt"
                productDates = []
                helpfulness = []
                ratings =[]
                minDate = datetime(2050, 12, 31)
                maxDate = datetime(1950, 1, 1)
                try:
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            row2 = line2.split("\t")
                            #print(row2)
                            votes = str(row2[2]).split(',')
                            funny = int(votes[0].split(':')[1])
                            useful = int(votes[1].split(':')[1])
                            cool = int(votes[2].split(':')[1].split('}')[0])
                            helpfulness.append((int(useful),int(cool),int(funny)))
                            found_date=0
                            star_rating=0
                            found_rating=0
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
                                    productDates.append((currentDay))
                                    if currentDay > maxDate:
                                        maxDate = currentDay
                                    if currentDay < minDate:
                                        minDate = currentDay
                                    #print(currentDay)
                                    found_date = 0
                                if item == "::stars":
                                    found_rating = 1
                                    continue
                                if item == "::":
                                    continue
                                if found_rating == 1:
                                    star_rating = int(item)
                                    ratings.append(int(star_rating))
                                    found_rating = 0
                            #here i have all data stars, helpfulness and time
                            date_len = len(productDates)
                            help_len= len(helpfulness)
                            rating_len = len(ratings)
                    if help_len!=rating_len or rating_len!=date_len or date_len!=help_len:
                        print(date_len)
                        print(help_len)
                        print(rating_len)
                        print("probleeeeeeeeeeeeeeeeeeem")


                except FileNotFoundError:
                    print("File Not Found")
                    pass
                maxDiff = (maxDate - minDate).days
                # print("maxDiff " + str(maxDiff))
                tq_rating = 0
                for i in range(rating_len):
                    timeDiff = (productDates[i] - minDate).days
                    # print("time diff " +str(timeDiff))
                    if maxDiff == 0:
                        time_score = 0
                    else:
                        time_score = timeDiff / maxDiff
                    # print("time_score " + str(time_score))
                    votes = helpfulness[i]
                    # print("votes ")
                    # print(votes)
                    # print("time_score " + str(time_score))
                    if (votes[0] + votes[1] + votes[2]) == 0:
                        helpfulness_score = 0
                    else:
                        helpfulness_score = (votes[0] + votes[1]) / (votes[0] + votes[1] + votes[2])
                        # print("helpfulness_score " + str(helpfulness_score))
                    current_rating = ratings[i]
                    # print("current_rating " + str(current_rating))
                    beta = 10
                    numerator = beta * (time_score + helpfulness_score)
                    # print("numerator " + str(numerator))
                    exp_weight = (math.e ** numerator)
                    # print("exp_weight " + str(exp_weight))
                    tq_rating += (exp_weight * current_rating)
                    # print("tq_rating " + str(exp_weight*current_rating))
                tq_rating /= rating_len
                print("Num_products " + str(num_products))
                num_products += 1
                filehandle.write((str(tq_rating) + "\n"))
                filehandle2.write(str(productid)+"\t"+str(tq_rating)+"\n")
    return
def compute_AVG_for_Yelp(category_baseDirectory,productBaseDirectory,dest_category,categoriesList):
    print("Computing AVG Rank score for Yelp Dataset")
    for category in categoriesList:
        print("Considering "+str(category))
        predictions_file_path = dest_category+category+"/Cutoff_10/Set_1/predictions.txt"
        all_predictions_file_path = dest_category+category+"/Cutoff_10/"+category+".txt"
        filehandle = open(predictions_file_path, 'w')
        filehandle2 = open(all_predictions_file_path,'w')
        category_file_path = category_baseDirectory + category+".txt"
        num_products =0
        with open(category_file_path, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                productid = row[0]
                product_file_path = productBaseDirectory + productid + ".txt"
                avg_rating = 0
                num_reviews = 1
                try:
                    with open(product_file_path, 'r') as fp1:
                        for line2 in fp1:
                            row2 = line2.split("\t")
                            star_rating=0
                            found_rating=0
                            for item in row2:
                                if item == "::date":
                                    found_date = 1
                                    continue
                                if item == "::":
                                    continue

                                if item == "::stars":
                                    found_rating = 1
                                    continue
                                if item == "::":
                                    continue
                                if found_rating == 1:
                                    star_rating = int(item)
                                    avg_rating+=star_rating
                                    break
                            num_reviews+=1
                except FileNotFoundError:
                    print("File Not Found")
                    pass

                    avg_rating /= num_reviews
                print("Num_products " + str(num_products))
                num_products += 1
                filehandle.write((str(avg_rating) + "\n"))
                filehandle2.write(str(productid)+"\t"+str(avg_rating)+"\n")
    return
dataset_type = "amazon"
#category_baseDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/amazon_exp_categories/"
#productBaseDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
dataset_type="yelp"
category_baseDirectory="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Resturants_Categories/"
productBaseDirectory="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\ProductReviews_New/"
#compute_yelp_stats(category_baseDirectory,productBaseDirectory,dataset_type)
#compute_yelp_usefulness(category_baseDirectory,productBaseDirectory,dataset_type)
dest_category = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\AVG_Predictions/"
categoriesList = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
compute_AVG_for_Yelp(category_baseDirectory,productBaseDirectory,dest_category,categoriesList)

