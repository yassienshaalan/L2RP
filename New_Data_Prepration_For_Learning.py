from ranking import computeExponentialScore
from dirichlet_True_Rating import computeTQMinus,computeTQMinus_New
from alogrithms import mergeSort
import shutil
from datetime import datetime
import numpy as np
from ranking import readSentencePolaritiesPerRating
from random import randint
import  math
from Extract_Polarties import extractWeightedPolartiesPerProduct

def Get_User_Helpfulness_Per_Group_of_Products(product_list,product_base_directory):
    user_votes_dict = dict()
    for product in product_list:
        product_file_path = product_base_directory+product+".txt"
        with open(product_file_path, 'r') as filep:
            for line in filep:
                row = line.split('\t')
                #print(row)
                all_feed_bak=0
                if len(row)>3:
                    try:
                        all_feed_bak = int(row[3])
                    except ValueError:
                        pass
                helpful=0
                if len(row)>4:
                    helpful = int(row[4])
                non_help =  all_feed_bak-helpful
                try:
                    result = user_votes_dict[row[0]]
                    helpful+=result[0]
                    non_help+=result[1]
                    user_votes_dict[row[0]] = (helpful,non_help)
                except KeyError:
                    user_votes_dict[row[0]]=(helpful,non_help)

    user_helpfulness_dict=dict()
    for key,value in user_votes_dict.items():
        helpful = value[0]
        non_help = value[1]
        helfpfulness = 0
        if (non_help+helpful)!=0:
            helfpfulness=helpful/(non_help+helpful)
        user_helpfulness_dict[key]= helfpfulness
        #print(str(helpful)+" "+str(non_help)+" "+str(helfpfulness))

    return user_helpfulness_dict

def dirichlet_probability(ratingsDictionary):

    prior=[2,2,2,2,2]
    """
    Computes the Dirichlet expected priority per rating level with a prior.
    """
    votes = []
    for key, value in ratingsDictionary.items():
        votes.append(value)
    #print("votes")
    #print(votes)
    posterior = map(sum, zip(votes, prior))
    temp = list(map(sum, zip(votes, prior)))
    to = list(enumerate(temp))
    #print("posterior")
    #print(posterior)
    #print("enum posterior")
    #print(to)
    N = sum(posterior)
    #print("Sum Posterior")
    #print(N)
    weights = list(map(lambda i: (i[0] + 1) * i[1], to))
    #print("weights ")
    #print(weights)
    newlist = []
    for item in weights:
        item = item / sum(weights)
        newlist.append(item)
    #print("newlist")
    #print(newlist)
    #print("sumWeights")
    #print(sum(weights))
    #retValue = float(float(sum(weights)) / N)
    #print("retValue")
    #print(retValue)
    return newlist



def Get_Product_Rating_Level_Dict(product_file_path):
    ratingsDictionary = dict()
    ratingsDictionary[1] = 0
    ratingsDictionary[2] = 0
    ratingsDictionary[3] = 0
    ratingsDictionary[4] = 0
    ratingsDictionary[5] = 0
    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
            rating = float(review[5])
            try:
                ratingValue = ratingsDictionary[rating]
                ratingValue = ratingValue + 1
                ratingsDictionary[rating] = ratingValue
            except KeyError as e:
                ratingsDictionary[rating] = 1
    return ratingsDictionary

def Get_Product_Weighted_Rating_Level_Dict(product_file_path):
    ratingsDictionary = dict()
    ratingsDictionary[1] = 0
    ratingsDictionary[2] = 0
    ratingsDictionary[3] = 0
    ratingsDictionary[4] = 0
    ratingsDictionary[5] = 0
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)

    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
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

    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
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

            weight = ((currentDay - minDate).days)/(maxDate-minDate).days
            rating = float(review[5])
            expValue = (math.e ** weight*rating)

            try:
                ratingValue = ratingsDictionary[rating]
                ratingValue = ratingValue + expValue
                ratingsDictionary[rating] = ratingValue
            except KeyError as e:
                ratingsDictionary[rating] = expValue

    return ratingsDictionary


def Get_Product_Weighted_Helpful_Votes(product_file_path,bhelp):
    #print(product_file_path)
    weighted_helpful_votes = 0
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    min_helpful = 10000000
    max_helpful = -10
    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
            datesplit = review[2].split(',')
            if len(review)>=5:
                helpful=int(review[4])
                if helpful>max_helpful:
                    max_helpful = helpful
                if helpful<min_helpful:
                    min_helpful = helpful
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
    num_revs = 0
    with open(product_file_path, 'r') as filep:
        for item in filep:
            num_revs+=1
            review = item.split('\t')
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

            weight = ((currentDay - minDate).days)/(maxDate-minDate).days
            helpful = 0
            non_helpful = 0
            if len(review)>=5:
                helpful=int(review[4])
                if review[3]!='':
                    all_feed = int(review[3])
                else:
                    all_feed = helpful
                non_helpful = all_feed-helpful
            rating = 0
            if len(review)>=6:
                rating=float(review[5])
            '''
            if max_helpful-min_helpful>0:
                helpful = (helpful-min_helpful)/(max_helpful-min_helpful)
            else:
                helpful = 0
            #'''

            #print(str(weight) + " " + str(helpful) + " " + str(rating))
            if all_feed > 0:
                if bhelp == 1:
                    weight = weight*(helpful/all_feed)*rating
                else:
                    weight = weight * ((helpful-non_helpful )/ all_feed) * rating
            else:
                weight = 0
            #if weight>700:
             #   weight = 700;
            #print(weight)
            expValue = (math.e ** weight)
            weighted_helpful_votes+=expValue

    if num_revs >0:
        weighted_helpful_votes/=num_revs

    return weighted_helpful_votes

def Get_Product_Weighted_Helpful_Votes_Per_RatingLevel(product_file_path,bhelp):
    #print(product_file_path)

    ratingsDictionary = dict()
    ratingsDictionary[1] = 0
    ratingsDictionary[2] = 0
    ratingsDictionary[3] = 0
    ratingsDictionary[4] = 0
    ratingsDictionary[5] = 0

    #weighted_helpful_votes = 0
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    min_helpful = 10000000
    max_helpful = -10
    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
            datesplit = review[2].split(',')
            if len(review)>=5:
                helpful=int(review[4])
                if helpful>max_helpful:
                    max_helpful = helpful
                if helpful<min_helpful:
                    min_helpful = helpful
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
    num_revs = 0
    with open(product_file_path, 'r') as filep:
        for item in filep:
            num_revs+=1
            review = item.split('\t')
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

            weight = ((currentDay - minDate).days)/(maxDate-minDate).days
            helpful = 0
            non_helpful = 0
            if len(review)>=5:
                helpful=int(review[4])
                if review[3]!='':
                    all_feed = int(review[3])
                else:
                    all_feed = helpful
                non_helpful = all_feed-helpful
            rating = 0
            if len(review)>=6:
                rating=float(review[5])
            '''
            if max_helpful-min_helpful>0:
                helpful = (helpful-min_helpful)/(max_helpful-min_helpful)
            else:
                helpful = 0
            #'''

            #print(str(weight) + " " + str(helpful) + " " + str(rating))
            if all_feed > 0:
                if bhelp == 1:
                    weight = weight*(helpful/all_feed)*rating
                else:
                    weight = weight * ((helpful-non_helpful )/ all_feed) * rating
            else:
                weight = 0
            #if weight>700:
             #   weight = 700;
            #print(weight)
            expValue = (math.e ** weight)
            #weighted_helpful_votes+=expValue

            try:
                ratingValue = ratingsDictionary[rating]
                ratingValue = ratingValue + expValue
                ratingsDictionary[rating] = ratingValue
            except KeyError as e:
                ratingsDictionary[rating] = expValue

    #if num_revs >0:
     #   weighted_helpful_votes/=num_revs

    return ratingsDictionary
def Extract_Features_For_Training_Testing(randomized_queries_dest,queries_directory,training_testing_dest_directory,product_review_base_dirc,ProductPolarities,Producthelpfulness):
    print("Extracting features for testing set")
    queries_file_path = randomized_queries_dest+"testing.txt"
    queries_set = []
    with open(queries_file_path, 'r') as filep:
        for line in filep:
            queries_set.append(line.split('\t')[0])
    queries_feature_file_path = training_testing_dest_directory+"test.txt"
    filehandle = open(queries_feature_file_path,'w')
    Extract_Features_For_Query_List(queries_set,queries_directory, product_review_base_dirc, filehandle,ProductPolarities,Producthelpfulness,"ts")
    #******************************************************************************************************************
    '''

    queries_file_path = randomized_queries_dest + "training.txt"
    queries_set=[]

    with open(queries_file_path, 'r') as filep:
        for line in filep:
            queries_set.append(line.split('\t')[0])

    num_valid = int(len(queries_set)*0.2)
    num_training = len(queries_set)-num_valid
    training_queries = []
    validation_queries = []
    print("Total "+str(len(queries_set)))
    print("Num Valid "+str(num_valid))
    print("Num Train "+str(num_training))

    index = 0
    for i in range(num_valid):
        validation_queries.append(queries_set[index])
        index+=1

    for i in range(num_training):
        training_queries.append(queries_set[index])
        index+=1

    print("Num Actual valid "+str(len(validation_queries)))
    print("Num Actual tain " + str(len(training_queries)))

    print("Extracting features for validation set")
    queries_feature_file_path = training_testing_dest_directory + "valid.txt"
    filehandle = open(queries_feature_file_path, 'w')
    Extract_Features_For_Query_List(validation_queries, queries_directory, product_review_base_dirc, filehandle, ProductPolarities,Producthelpfulness,"v")

    print("Extracting features for training set")
    queries_feature_file_path = training_testing_dest_directory + "train.txt"
    filehandle = open(queries_feature_file_path, 'w')
    Extract_Features_For_Query_List(training_queries, queries_directory, product_review_base_dirc, filehandle,ProductPolarities,Producthelpfulness,"tr")
    #shutil.copy2(queries_feature_file_path,training_testing_dest_directory+"valid.txt")

    #'''
    return

def Aggregate_Rating_Dicts(all_products_rating_dict,product_rating_dict):
    for key,value in all_products_rating_dict.items():
        new_val = product_rating_dict[key]+value
        all_products_rating_dict[key]=new_val
    return all_products_rating_dict

def Transform_To_LogScale(value):
    ret_result = 0
    if value<0:
        value*=-1
    elif value == 0:
        value = 0.01
    ret_result = math.log10(value)
    return ret_result
def Extract_Features_For_Query_List(queries,queries_directory,product_review_base_dirc,filehandle,ProductPolarities,Producthelpfulness,type):
    all_features = []


    min_lifespan, max_life_span, median_lifespan, min_num_revs, max_num_revs, num_rev_median, min_activness, max_activness, activness_median, num_reviewers=0,0,0,0,0,0,0,0,0,0
    product_dict = dict()
    for query in queries:
        print("Processing query id "+str(query))
        query_file_path = queries_directory+query+".txt"
        product_list = []
        with open(query_file_path, 'r') as filep:
            for line in filep:
                product_list.append(line.split('\n')[0])

        print("Num products "+str(len(product_list)))
        #if len(product_list)>100 and type!="ts":
         #   print("We are passing list size is "+str(len(product_list)))
          #  continue
        print("Extracting Features ")

        #'''
        #This part where we compute the life span features of a product list or a query
        min_lifespan,max_life_span,median_lifespan,min_num_revs,max_num_revs,num_rev_median,min_activness,max_activness,activness_median,num_reviewers=Compute_Products_Life_Span(product_list,product_review_base_dirc)

        user_helpfulness_dict = Get_User_Helpfulness_Per_Group_of_Products(product_list,product_review_base_dirc)
        tot_num_revs = 0
        product_TQ_score = dict()
        product_exp_dirichelet = dict()
        all_product_rating_dict=dict()
        all_product_rating_dict[1] = 0
        all_product_rating_dict[2] = 0
        all_product_rating_dict[3] = 0
        all_product_rating_dict[4] = 0
        all_product_rating_dict[5] = 0
        index = 0
        pro_indx_list = []
        product_score_dict = dict()
        prev_zero_count = 0
        for product in product_list:
            product_file_path = product_review_base_dirc+product+".txt"
            tq_score,average_star = computeExponentialScore(product_file_path,user_helpfulness_dict)
            tq_minus_score, average_star = computeTQMinus_New(product_file_path)
            num_revo,life_spano,activo=Compute_Product_LifeSpan_and_Revs(product_file_path)
            tot_num_revs+=num_revo
            #tq_minus_score, average_star = computeTQMinus(product_file_path)
            if tq_score == 0:
                tq_score+=prev_zero_count*0.01
                prev_zero_count+=1
            product_TQ_score[tq_score]=product#Replacing TQ as label with average
            product_score_dict[product]=tq_score
            #print(str(product)+" "+str(tq_score))
            #**********Calculating 5 Dirichlet features for product level
            #product_rating_old_dict=Get_Product_Rating_Level_Dict(product_file_path)
            #print(product_rating_old_dict)
            product_rating_dict = Get_Product_Weighted_Rating_Level_Dict(product_file_path)#Get_Product_Rating_Level_Dict(product_file_path)
            #print(product_rating_dict)
            help = Get_Product_Weighted_Helpful_Votes(product_file_path,1)
            helpfulness_rating_dict = Get_Product_Weighted_Helpful_Votes_Per_RatingLevel(product_file_path, 1)
            #print(helpfulness_rating_dict)
            #print("***************************")
            #total_postive,total_neg,total_polarity = extractWeightedPolartiesPerProduct(product_file_path)
            #print("here is the total "+str(total_postive) + " " + str(total_neg))
            #print(help)
            #print(product_rating_dict)
            #print(product_rating_dict)
            #all_product_rating_dict=Aggregate_Rating_Dicts(all_product_rating_dict,product_rating_dict)

            #product_expected_props = dirichlet_probability(product_rating_dict)
             #print(product_expected_props)
            test_dri = []
            test_dri.append(product_rating_dict[1])
            test_dri.append(product_rating_dict[2])
            test_dri.append(product_rating_dict[3])
            test_dri.append(product_rating_dict[4])
            test_dri.append(product_rating_dict[5])

            product_plarties = ProductPolarities[product]#+ve -ve polarity per star rating level
            product_helpfulenss = Producthelpfulness[product] #Num Helpful and non Helpful per product
            test_dri = []
            product_exp_dirichelet[product]=test_dri#product_expected_props#test_dri#
            pro_indx_list.append((index,tq_score))#tq_score))#Replacing TQ as Label with Average Star
            index+=1
            print(index)

            #pos = product_plarties[0]+product_plarties[2]+product_plarties[4]+product_plarties[6]+product_plarties[8]
            #neg = product_plarties[1] + product_plarties[3] + product_plarties[5] + product_plarties[7] + product_plarties[9]
            #Old Simple Aggregation results of setiments and helpfulness
            '''
            pos = product_plarties[0]
            neg = -product_plarties[1]
            help = product_helpfulenss[0]
            non_help = product_helpfulenss[1]
            '''
            #print(product_plarties)
            try:
                found_score = product_dict[product]
                #print("Found previous score to "+str(product)+" with "+str(found_score)+" current score "+str(tq_score))
            except KeyError:
                '''
                ones.append(tq_minus_score)
                twoes.append(help)
                three.append(product_plarties[0])
                four.append(product_plarties[1])
                five.append(product_plarties[2])
                '''
                product_dict[product]=average_star
            #for polarity in product_plarties:
             #   product_exp_dirichelet[product].append(polarity)

            product_exp_dirichelet[product].append(tq_minus_score)
            #product_exp_dirichelet[product].append(helpfulness_rating_dict[1])
            #product_exp_dirichelet[product].append(helpfulness_rating_dict[2])
            #product_exp_dirichelet[product].append(helpfulness_rating_dict[3])
            #product_exp_dirichelet[product].append(helpfulness_rating_dict[4])
            #product_exp_dirichelet[product].append(helpfulness_rating_dict[5])
            product_exp_dirichelet[product].append(help)
            #product_exp_dirichelet[product].append(product_plarties[0])
            #product_exp_dirichelet[product].append(product_plarties[1])
            product_exp_dirichelet[product].append(product_plarties[2])
            product_exp_dirichelet[product].append(num_revo)
            product_exp_dirichelet[product].append(life_spano)
            product_exp_dirichelet[product].append(activo)
            #product_exp_dirichelet[product].append(total_postive)
            #product_exp_dirichelet[product].append(non_help)

        '''
        all_product_expected_props = dirichlet_probability(all_product_rating_dict)
        all_product_expected_props=[]
        all_product_expected_props.append(all_product_rating_dict[1])
        all_product_expected_props.append(all_product_rating_dict[2])
        all_product_expected_props.append(all_product_rating_dict[3])
        all_product_expected_props.append(all_product_rating_dict[4])
        all_product_expected_props.append(all_product_rating_dict[5])
        #print(all_product_expected_props)
        for product in product_list:#Adding the 5 list level dirichelt features
            for item in all_product_expected_props:
                product_exp_dirichelet[product].append(item)
            #print(product_exp_dirichelet[product])
        #print(all_product_expected_props)

        '''
        #'''
        for product in product_list:  # Adding the list level features life span, median num revs and activness
            product_exp_dirichelet[product].append(min_lifespan+int(query))
            product_exp_dirichelet[product].append(max_life_span+int(query))
            #product_exp_dirichelet[product].append(median_lifespan+int(query))
            #product_exp_dirichelet[product].append(num_reviewers)
            product_exp_dirichelet[product].append(min_num_revs+int(query))
            product_exp_dirichelet[product].append(max_num_revs+int(query))
            #product_exp_dirichelet[product].append(num_rev_median+int(query))
            product_exp_dirichelet[product].append(min_activness+(int(query)/700))
            product_exp_dirichelet[product].append(max_activness+(int(query)/700))
            #product_exp_dirichelet[product].append(activness_median+(int(query)))
            #product_exp_dirichelet[product].append(tot_num_revs)
            #product_exp_dirichelet[product].append(len(product_dict)+int(query))


        #'''
        #'''
        mergeSort(pro_indx_list)
        rank = 0
        product_id_rank = dict()

        for val in pro_indx_list:
            product_id = product_TQ_score[val[1]]
            score = val[1]

            product_id_rank[product_id] = rank#score#rank#tq_score#rank#randint(0,5)#rank
            rank+=1

        for product in product_list:
            feature_vec = []
            rank = product_id_rank[product]
            #rank = product_score_dict[product]#Replaceing TQ old Labeling
            product_level_dirichlet_features = product_exp_dirichelet[product]
            #filehandle.write(str(rank)+" "+"qid:"+str(query)+" ")
            feature_vec.append(rank)
            feature_vec.append(query)
            for item in product_level_dirichlet_features:#These are the first 5 product level dirichelt features
                #filehandle.write(str(index)+":"+str(item)+" ")
                feature_vec.append(item)
            #print(feature_vec)
            #filehandle.write("\n")
            all_features.append(feature_vec)

    #'''

    print("Num unique products in is "+str(len(product_dict)))
    num_features = len(all_features[0])-2
    print("num_features "+str(num_features))
    all_feat_vecs = []
    all_fixed_feat_vecs = []
    for i in range(num_features):
        all_feat_vecs.append([])
        all_fixed_feat_vecs.append([])

    min_values = []
    max_values = []

    print("Fixing Skewness & Normalizing Features")
    #Old Normalization
    '''
    for i in range(num_features):
        max_values.append(-1000)
        min_values.append(10000000)

    for features in all_features:
        #print(features[6])
        #print("Num fet vec "+str(len(features)))
        #print(features)
        for j in range(2,len(features)):
            #print(j)
            if features[j] > max_values[j-2]:
                max_values[j-2] = features[j]
            if features[j] < min_values[j-2]:
                min_values[j-2] = features[j]
    '''

    from Resolve_Skewness import resolve_Skewness_For_Feature
    feature_one = []
    feature_two = []
    feature_three = []
    findex = 0
    feature_names = []
    feature_names.append("TQ_minus")
    feature_names.append("Helpfulness")
    feature_names.append("Total Polarity")
    feature_names.append("Num Revs")
    feature_names.append("LifeSpan")
    feature_names.append("Activness")
    #feature_names.append("Min Num Revs")
    #feature_names.append("Median Num Revs")
    #feature_names.append("Max Num Revs")
    #feature_names.append("min LifeSpan")
    #feature_names.append("Max LifeSpan")
    #feature_names.append("Median LifeSpan")
    #feature_names.append("Min Activness")
    #feature_names.append("Max Activness")
    #feature_names.append("Median Activness")
    #feature_names.append("Max num revs")
    #feature_names.append("Tot_Num_Revs")
    #feature_names.append("Num_prods")
    for features in all_features:
        for j in range(2,len(features)):
            all_feat_vecs[j-2].append(features[j])

    import pandas as pd
    for i in range(num_features):
        all_feat_vecs[i] = pd.DataFrame(all_feat_vecs[i])
        all_fixed_feat_vecs[i]=resolve_Skewness_For_Feature(all_feat_vecs[i], "",0)

    #feature_two = pd.DataFrame(feature_two)
    #feature_two=resolve_Skewness_For_Feature(feature_two, "help",0)
    # feature_three = pd.DataFrame(feature_three)
    # resolve_Skewness_For_Feature(feature_three, "Median")
    findex = 0
    print("Writing Features")
    for features in all_features:
        filehandle.write(str(features[0]) + " " + "qid:" + str(features[1]) + " ")
        index =1
        for j in range(2,len(features)):
            #value = (features[j]-min_values[j-2])/(max_values[j-2]-min_values[j-2])#Normalization Step
            value = all_fixed_feat_vecs[j-2][findex][0]
            filehandle.write(str(index)+":"+str(value)+" ")
            index+=1
        filehandle.write("\n")
        findex += 1
    filehandle.close()


    '''
    import matplotlib.pyplot as plt


    fig = plt.figure
    plt.subplot2grid(shape=(2,6), loc=(0,0), colspan=2)
    plt.hist(ones)
    plt.title("Industrial & Scientific ")
    plt.xlabel("tq_minus")
    plt.ylabel("Frequency")

    print(ones)


    plt.subplot2grid((2,6), (0,2), colspan=2)
    plt.hist(twoes)
    #plt.title("Testing Category Arts & Crafts")
    plt.xlabel("help")
    plt.ylabel("Frequency")

    twoes.sort()
    print(twoes)

    plt.subplot2grid((2,6), (0,4), colspan=2)
    plt.hist(three)
    plt.xlabel("postive")
    plt.ylabel("Frequency")


    plt.subplot2grid((2,6), (1,1), colspan=2)
    plt.hist(four)
    # plt.title("Testing Category Arts & Crafts")
    plt.xlabel("negative")
    plt.ylabel("Frequency")
    #print(four)

    plt.subplot2grid((2,6), (1,3), colspan=2)
    plt.hist(five)
    # plt.title("Testing Category Arts & Crafts")
    plt.xlabel("tot_polarity")
    plt.ylabel("Frequency")
    #print(five)
    plt.show()
    #'''
    return
def Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon(drive):
    print("This procedure performs the preparation of the training and testing from queries based on sub categories for all cagegories at once Amazon Dataset")
    categories = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games",
                     "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]

    queries_directory = drive+"Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    query_map_code_file_path = drive+"Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    queries_cat_sub_cat_dict = dict()
    ignore_first = 0
    with open(query_map_code_file_path, 'r') as filep:
        for line in filep:
            if ignore_first == 0:
                ignore_first = 1
                continue
            line = line.split('\t')
            queries_cat_sub_cat_dict[line[0]]=(line[1],line[2].split('\n')[0])

    training_testing_dest_directory = drive+"Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/"
    randomized_queries_dest = drive+"Yassien_PhD\Experiment_6\Randomized_Queryset/"
    product_review_base_dirc = drive+"Yassien_PhD\Product_Reviews/"
    #ProductPolaritiesPerRating = SummarizeSentencePolaritiesPerRatingPerPeriod_To_1("D:\Yassien_PhD\Experiment_5/product_polarties_Per_RatingLevelPer_5_TimePeriod.txt",5)
    ProductPolarities = Read_Product_Polarties(drive+"\Yassien_PhD\Experiment_6/weighted_product_polarties_t.txt")
    Producthelpfulness = Read_Product_Helpfulness(drive+"\Yassien_PhD\Experiment_6/product_Helpfluness.txt")
    Extract_Features_For_Training_Testing(randomized_queries_dest,queries_directory,training_testing_dest_directory,product_review_base_dirc,ProductPolarities,Producthelpfulness)

    return
def Compute_Product_LifeSpan_and_Revs(product_file_path):
    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    num_rev = 0
    with open(product_file_path, 'r') as filep:
        for line in filep:
            num_rev += 1
            review = line.split('\t')
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
    life_span = (maxDate - minDate).days
    active = num_rev / life_span
    return num_rev,life_span,active
def Compute_Products_Life_Span(product_list,product_base_directory):
    #print("Computing product life spans")
    #print(product_list)
    min_life_span = 100000000000000000
    max_life_span = -100
    life_spans = []
    num_revs = []
    min_num_revs = 10000000000000000000
    max_num_revs = 0
    tot_num_revs = 0
    min_activness = 100000000000000000
    max_activness = -100
    num_reviewers = 0
    activness = []
    reviewers_dict = dict()
    for product in product_list:
        product_path = product_base_directory+product+".txt"
        minDate = datetime(2050, 12, 31)
        maxDate = datetime(1950, 1, 1)
        num_rev = 0
        with open(product_path, 'r') as filep:
            for line in filep:
                num_rev+=1
                review = line.split('\t')
                datesplit = review[2].split(',')
                monthDay = datesplit[0]
                try:
                    result = reviewers_dict[review[0]]
                except KeyError:
                    reviewers_dict[review[0]]=1
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
        tot_num_revs+=num_rev
        num_revs.append(num_rev)

        if max_num_revs<num_rev:
            max_num_revs = num_rev
        if min_num_revs>num_rev:
            min_num_revs = num_rev

        life_span = (maxDate - minDate).days
        life_spans.append(life_span)
        #print(life_span)
        if max_life_span< life_span:
            max_life_span = life_span
        if min_life_span>life_span:
            min_life_span = life_span
        active = num_rev/life_span
        activness.append(active)

        if max_activness<active:
            max_activness = num_rev
        if min_activness>active:
            min_activness = num_rev

        #print(activness)

    #print(str(min_life_span) + "\t" + str(max_life_span))

    a = np.array(life_spans)
    median = np.median(a)

    revo = np.array(num_revs)
    num_rev_median = np.median(revo)

    activo = np.array(activness)
    activness_median = np.median(activo)

    num_reviewers = len(reviewers_dict)
    #avg_num_revs = tot_num_revs/(len(product_list))
    return min_life_span,max_life_span,median,min_num_revs,max_num_revs,num_rev_median,min_activness,max_activness,activness_median,num_reviewers

def Read_Product_Polarties(productPolartiesFile):
    product_polarties_dict = dict()
    ignore_first = 0
    with open(productPolartiesFile, 'r') as fp:
        for line in fp:
            if ignore_first == 0:
                ignore_first = 1
                continue
            row = line.split('\t')
            numbers = []
            for i in range(1, len(row)):
                numbers.append(float(row[i]))
            try:
                found = product_polarties_dict[row[0]]
                print("Problem: found previous record for " + str(row[0]))
            except KeyError:
                    #print("missing polarities for " + str(row[0]))
                    product_polarties_dict[row[0]]=numbers

    print("product_polarties_dict")
    print(len(product_polarties_dict))
    return product_polarties_dict

def SummarizeSentencePolaritiesPerRatingPerPeriod_To_1(productPolartiesFile,timeperiods):
    ProductPolaritiesPerRatingPerPeriod = dict()
    with open(productPolartiesFile, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            numbers = []
            for i in range(1,((timeperiods*5*2)+1)):
                numbers.append(int(row[i]))
            try:
                found = ProductPolaritiesPerRatingPerPeriod[row[0]]
                print("Problem: found previous record for "+str(row[0]))
            except KeyError:
                if len(numbers)!=(timeperiods*5*2):
                    print("missing polarities for found only "+str(len(numbers))+" for "+str(row[0]))
                else:
                    #print(numbers)
                    new_numbers = [0,0,0,0,0,0,0,0,0,0]
                    index=0
                    for j in range(timeperiods):
                        for i in range (0,timeperiods*2,2):
                            new_numbers[i]+=numbers[index]
                            index+=1
                            new_numbers[i+1] += numbers[index]
                            index+=1
                    #print(index)
                    #print(new_numbers)
                    ProductPolaritiesPerRatingPerPeriod[row[0]] = new_numbers#numbers

    print("ProductPolaritiesPerRatingPerPeriod")
    print(len(ProductPolaritiesPerRatingPerPeriod))

    return ProductPolaritiesPerRatingPerPeriod


def Read_Product_Helpfulness(product_helpfulness_file_path):
    product_helpfulness_dict = dict()
    ignore_first = 0
    with open(product_helpfulness_file_path, 'r') as fp:
        for line in fp:
            if ignore_first == 0:
                ignore_first = 1
                continue
            row = line.split('\t')
            numbers = []
            for i in range(1, len(row)):
                numbers.append(int(row[i]))
            try:
                found = product_helpfulness_dict[row[0]]
                print("Problem: found previous record for " + str(row[0]))
            except KeyError:
                    #print("missing polarities for " + str(row[0]))
                    product_helpfulness_dict[row[0]]=numbers

    print("product_helpfulness_dict")
    print(len(product_helpfulness_dict))
    return product_helpfulness_dict
