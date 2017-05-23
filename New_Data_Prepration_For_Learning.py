from ranking import computeExponentialScore
from alogrithms import mergeSort
import shutil

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
def Extract_Features_For_Training_Testing(randomized_queries_dest,queries_directory,training_testing_dest_directory,product_review_base_dirc):
    print("Extracting features for testing set")
    queries_file_path = randomized_queries_dest+"testing.txt"
    queries_set = []
    with open(queries_file_path, 'r') as filep:
        for line in filep:
            queries_set.append(line.split('\t')[0])
    queries_feature_file_path = training_testing_dest_directory+"test.txt"
    filehandle = open(queries_feature_file_path,'w')
    Extract_Features_For_Query_List(queries_set,queries_directory, product_review_base_dirc, filehandle)
    #******************************************************************************************************************
    print("Extracting features for training set")
    queries_file_path = randomized_queries_dest + "training.txt"
    queries_set=[]
    with open(queries_file_path, 'r') as filep:
        for line in filep:
            queries_set.append(line.split('\t')[0])
    queries_feature_file_path = training_testing_dest_directory + "train.txt"
    filehandle = open(queries_feature_file_path, 'w')
    Extract_Features_For_Query_List(queries_set, queries_directory, product_review_base_dirc, filehandle)
    shutil.copy2(queries_feature_file_path,training_testing_dest_directory+"valid.txt")
    return
def Extract_Features_For_Query_List(queries,queries_directory,product_review_base_dirc,filehandle):
    all_features = []
    for query in queries:
        print("Processing query id "+str(query))
        query_file_path = queries_directory+query+".txt"
        product_list = []
        with open(query_file_path, 'r') as filep:
            for line in filep:
                product_list.append(line.split('\n')[0])

        print("Num products "+str(len(product_list)))
        print("Extracting Features ")
        user_helpfulness_dict = Get_User_Helpfulness_Per_Group_of_Products(product_list,product_review_base_dirc)
        product_TQ_score = dict()
        product_exp_dirichelet = dict()
        pro_indx_list = []
        index = 0
        for product in product_list:
            product_file_path = product_review_base_dirc+product+".txt"
            tq_score = computeExponentialScore(product_file_path,user_helpfulness_dict)
            product_TQ_score[tq_score]=product
            #**********Calculating 5 Dirichlet features for product level
            product_rating_dict = Get_Product_Rating_Level_Dict(product_file_path)
            product_expected_props = dirichlet_probability(product_rating_dict)
            product_exp_dirichelet[product]=product_expected_props
            pro_indx_list.append((index,tq_score))
            index+=1
            print(index)
        mergeSort(pro_indx_list)
        rank = 0
        product_id_rank = dict()
        for val in pro_indx_list:
            product_id = product_TQ_score[val[1]]
            product_id_rank[product_id] = rank
            rank+=1

        for product in product_list:
            feature_vec = []
            rank = product_id_rank[product]
            product_level_dirichlet_features = product_exp_dirichelet[product]
            #filehandle.write(str(rank)+" "+"qid:"+str(query)+" ")
            feature_vec.append(rank)
            feature_vec.append(query)
            for item in product_level_dirichlet_features:
                #filehandle.write(str(index)+":"+str(item)+" ")
                feature_vec.append(item)

            #filehandle.write("\n")
            all_features.append(feature_vec)


    num_features = len(all_features[0])-2
    min_values = []
    max_values = []

    print("Normalizing Features")

    for i in range(num_features):
        max_values.append(-1000)
        min_values.append(10000000)
    for features in all_features:
        #print(features[6])
        for j in range(2,len(features)):
            if (features[j]) > max_values[j-2]:
                max_values[j-2] = (features[j])
            if (features[j]) < min_values[j-2]:
                min_values[j-2] = (features[j])
    #print("min_values")
    #print(min_values)
    #print("max_values")
    #print(max_values)
    #
    print("Writing Features")
    for features in all_features:
        filehandle.write(str(features[0]) + " " + "qid:" + str(features[1]) + " ")
        index =1
        for j in range(2,len(features)):
            value = (features[j]-min_values[j-2])/(max_values[j-2]-min_values[j-2])
            filehandle.write(str(index)+":"+str(value)+" ")
            index+=1
        filehandle.write("\n")
    filehandle.close()
    return
def Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon(drive):
    print("This procedure performs the preparation of the training and testing from queries based on sub categories for all cagegories at once Amazon Dataset")
    categories = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games",
                     "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]

    queries_directory = drive+"Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    query_map_code_file_path = drive+"Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
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

    Extract_Features_For_Training_Testing(randomized_queries_dest,queries_directory,training_testing_dest_directory,product_review_base_dirc)

    return

Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon("d:/")