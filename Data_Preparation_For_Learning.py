import random
import shutil
import os
from alogrithms import mergeSort
from New_Query_Sampling import  DivideTrainingSetIntoQueries,DivideTestingSetIntoQueries, Clustering_Products

def get_num_reviews_per_product_local(product_path):
    #Count the number of reviews for a product
    count = 0
    with open(product_path, 'r') as filep:
        for item in filep:
            count+=1
    return count
def Write_Number_Reviews_For_All_Categories():
    category_source = "d:\Yassien_PhD\categories/"
    product_base_directory = "d:\Yassien_PhD\Product_Reviews/"
    destenation_directory = "d:/Yassien_PhD/Number_of_reviews_per_product/"
    Categories = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    for category_name in Categories:
        print("Processing "+category_name)
        source_category_path = category_source + category_name + ".txt"
        dest_cat_path = destenation_directory+ category_name + ".txt"
        filehandle = open(dest_cat_path,'w')
        with open(source_category_path, 'r') as filep:
            for item in filep:
                line = item.split('\t')
                productid = line[0]
                product_file_path = product_base_directory + productid + ".txt"
                count = get_num_reviews_per_product_local(product_file_path)
                filehandle.write(str(productid)+"\t"+str(count)+"\n")
        filehandle.close()
    return
def Query_Sampling_For_New_Experiment_Setup(training_products,products_num_revs_path,sampling_choice,query_size):
    products_num_revs_dict = dict()
    with open(products_num_revs_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            products_num_revs_dict[line[0]]=int(line[1])

    final_training_set = []
    index = 0
    temp_list = []
    for product_line in training_products:
        produtid = str(product_line).split('\t')[0]
        if sampling_choice == 1 or sampling_choice == 2:
            count = products_num_revs_dict[produtid]
            if sampling_choice == 2 and count >50:
                pair = (index,count)
                temp_list.append(pair)
            elif sampling_choice == 1:
                pair = (index, count)
                temp_list.append(pair)
        index+=1
    #print("temp list before")
    #print(temp_list)
    mergeSort(temp_list)
    temp_list.reverse()
    #print("temp list after")
    #print(temp_list)
    total_num_prods = len(temp_list)
    new_list = []
    index_top = 0
    num_taken_top = 0
    index_bottom = total_num_prods-1

    num_to_take_top = int(query_size / 2)
    num_to_take_bottom = query_size - num_to_take_top
    print("num_to_take_top "+str(num_to_take_top))
    print("num_to_take_bottom " + str(num_to_take_bottom))

    num_taken_bottom = num_to_take_bottom


   # print("total_num_prods "+str(total_num_prods))
    if sampling_choice == 2:
        while len(new_list)<total_num_prods:
            #print("index_top "+str(index_top))
            #print("index_bottom "+str(index_bottom))
            if num_taken_top <num_to_take_top:
                if index_top==index_bottom:
                    new_list.append(temp_list[index_bottom])
                    break
                new_list.append(temp_list[index_top])
                num_taken_top+=1
                index_top+=1
            elif num_taken_bottom == num_to_take_bottom and num_taken_top == num_to_take_top:
                num_taken_top = 0

            if num_taken_bottom < num_to_take_bottom:
                if index_top == index_bottom:
                    new_list.append(temp_list[index_bottom])
                    break
                new_list.append(temp_list[index_bottom])
                num_taken_bottom += 1
                index_bottom -= 1
            elif num_taken_bottom == num_to_take_bottom and num_taken_top == num_to_take_top:
                num_taken_bottom = 0
        temp_list = new_list
    for i in range(len(temp_list)):
        pro_index = temp_list[i][0]
        final_training_set.append(training_products[pro_index])

    return final_training_set
def Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,local_destination,product_base_directory,drive,query_size,source_feature_vector_path):

  print("Processing "+category_name)
  index = 0
  product_list = []
  productid_index_dict = dict()
  #Copying the original categories file for reference
  shutil.copy2(source_category_path,local_destination)

  with open(source_category_path, 'r') as filep:
    for item in filep:
      line = item.split('\t')
      productid = line[0]
      product_line = item#line[0]
      productid_index_dict[productid]=index
      product_list.append(product_line)
      index += 1
  total_num_products = len(product_list)

  print("Total Num Products "+str(total_num_products))
  num_training = int(total_num_products*training_ratio)
  num_testing = total_num_products-num_training
  print("num_training " + str(num_training))
  print("num_testing " + str(num_testing))

  training_products = []
  testing_products = []
  indo = 0

  while len(product_list)>num_testing:
    # Code randomization
    choice = random.choice(list(product_list))
    #choice = product_list[indo]
    training_products.append(choice)
    #print("Choice "+str(choice))
    product_list.remove(choice)
    #indo+=1
    #print(product_list)

  testing_products = product_list
  old_total = len(training_products)+len(testing_products)
  #Here we inject whatever query sampling we need
  sampling_choice =1 #means arrange by number of reviews
  products_num_revs_path = drive+"Yassien_PhD/Number_of_reviews_per_product/"+category_name+".txt"
  #training_products=Query_Sampling_For_New_Experiment_Setup(training_products,products_num_revs_path,sampling_choice,query_size)
  training_products = Clustering_Products(training_products,source_feature_vector_path,source_category_path,products_num_revs_path)
  ######################################################################################################################
  print("Final num_training now " + str(len(training_products)))
  print("Final num_testing was " + str(len(testing_products)))
  final_total = len(training_products) + len(testing_products)
  print("Final total "+str(final_total))
  print("Old Total "+str(old_total))
  print("Final after num_training " + str(len(training_products)))
  if old_total !=final_total:
      new_list = []
      new_testing_count = int(len(training_products)*0.1)
      print("new_testing_count " + str(new_testing_count))
      for i in range(new_testing_count):
          new_list.append(testing_products[i])
      testing_products = new_list
  print("AFter Adjustment***************************************************************")

  print("Final after num_testing " + str(len(testing_products)))
  final_total = len(training_products) + len(testing_products)
  print("Final after total " + str(final_total))
  print("Writing Files")
  training_filepath = local_destination + "training.txt"
  training_index_filepath = local_destination + "training_index.txt"
  filehandle = open(training_filepath, 'w')
  filehandle_index = open(training_index_filepath, 'w')
  num_actually_written = 0
  for product_line in training_products:
    produtid= str(product_line).split('\t')[0]
    product_file_path = product_base_directory+produtid+".txt"
    #count = get_num_reviews_per_product_local(product_file_path)
    #if count>50:
    filehandle.write(product_line)
    filehandle_index.write(str(productid_index_dict[produtid])+"\n")
    num_actually_written+=1
  filehandle.close()
  filehandle_index.close()
  print("Final num_actually_written " + str((num_actually_written)))

  testing_filepath = local_destination + "testing.txt"
  testing_index_filepath = local_destination + "testing_index.txt"
  filehandle = open(testing_filepath, 'w')
  filehandle_index = open(testing_index_filepath, 'w')
  for product_line in testing_products:
    produtid = str(product_line).split('\t')[0]
    filehandle.write(product_line)
    filehandle_index.write(str(productid_index_dict[produtid]) + "\n")
  filehandle.close()
  filehandle_index.close()

  print("------------------------------------------------")
  return
def Retreive_Train_Test_Per_Category(source_feature_vector_path,category_name,modified_categories,cat_desination_directory):
  print("Processing "+category_name)
  try:
    os.stat(cat_desination_directory)
  except:
    os.mkdir(cat_desination_directory)

  trainin_index_filepath = modified_categories + "training_index.txt"
  testing_index_filepath = modified_categories + "testing_index.txt"
  training_indices = []
  testing_indices = []
  with open(trainin_index_filepath, 'r') as filep:
    for item in filep:
      training_indices.append(int(item))

  with open(testing_index_filepath, 'r') as filep:
    for item in filep:
      testing_indices.append(int(item))

  feature_vect_dict = dict()
  index = 0
  with open(source_feature_vector_path, 'r') as filep:
    for line in filep:
      feature_vect_dict[index]=line
      index+=1
  num_products = len(feature_vect_dict)

  training_feat_vec_filepath = cat_desination_directory + "training.txt"
  filehandle = open(training_feat_vec_filepath, 'w')
  for i in range(len(training_indices)):
    feat_vec = feature_vect_dict[training_indices[i]]
    filehandle.write(feat_vec)

  filehandle.close()


  testing_feat_vec_filepath = cat_desination_directory + "testing.txt"
  filehandle = open(testing_feat_vec_filepath, 'w')
  for i in range(len(testing_indices)):
    feat_vec = feature_vect_dict[testing_indices[i]]
    filehandle.write(feat_vec)

  filehandle.close()

  return

def PrepareCategoriesWithSalesRankRanking(sourceCategorypath,destinationCategorypath,category_name):
  print("Processing " + category_name)

  ranks = []
  with open(sourceCategorypath, 'r') as filep:
    for line in filep:
      ranks.append(int(line.split(' ')[0]))
  products = []
  with open(destinationCategorypath, 'r') as filep:
    for line in filep:
      products.append(line.split('\t')[0])
  if len(ranks)!=len(products):
    print("Non Equal lengths ranks is "+str(len(ranks))+" products "+str(len(products)))
    print(products)
  filehandle = open(destinationCategorypath, 'w')
  for i in range(len(products)):
    filehandle.write(str(products[i])+"\t"+str(ranks[i])+"\n")

  filehandle.close()

  return
def Prepare_Training_Testing_Data_New_Experiment_Setup(query_size,drive):
  #drive = "d:/"
  category_source = drive+"Yassien_PhD\categories/"
  categories_source=drive+"Yassien_PhD\Experiment_5\Categories/"
  source_features_path = drive+"Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_5_Time_Intervals/"
  train_test_destination_stage1=drive+"Yassien_PhD\Experiment_5\Train_Test_Category_Stage_1/"
  train_test_destination=drive+"Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target/"
  product_base_directory =drive+"Yassien_PhD\Product_Reviews/"

  #Categories with large number of products > 5000 products we don't need cross_Validation randomize and take 80%
  categories_with_large_products=["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]#[ "Jewelry","Toys & Games", "Video Games" , "Cell Phones & Accessories", "Electronics"]
  for category_name in categories_with_large_products:
    ################################################################################################################################################################
    #'''
    #This part of the code to randomize all products within one group and then pick 80% randomly for training and 20% for testing keeping the indices of each set to be able to formulate the queries
    modified_categories_with_indices= categories_source+category_name+"/"
    try:
      os.stat(modified_categories_with_indices)
    except:
      os.mkdir(modified_categories_with_indices)
    training_ratio = 0.9
    source_category_path = category_source + category_name + ".txt"
    source_feature_vector_path = source_features_path + category_name + ".txt"
    cat_train_test_desination_directory_stage_1 = train_test_destination_stage1 + category_name + "/"
    train_test_destination_for_cat = train_test_destination + category_name + "/"


    Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,modified_categories_with_indices,product_base_directory,drive,query_size,source_feature_vector_path)
    Retreive_Train_Test_Per_Category(source_feature_vector_path,category_name,modified_categories_with_indices,cat_train_test_desination_directory_stage_1)
    #'''
    ################################################################################################################################################################

    ################################################################################################################################################################
    #This part was just to prepare to get the sales rank and the TQ rank for all products in all categories to be utilized in forming the training and testing sets
    '''sourceCategory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\All_Categories_Data_25_Basic_Features_With_10_Time_Interval_TQ_Target_For_Ranking/"+category_name+".txt"
    destinationCategory="F:\Yassien_PhD\Experiment_5\Categories_Ranked_by_TQ_Rank/"+category_name+".txt"
    PrepareCategoriesWithSalesRankRanking(sourceCategory,destinationCategory,category_name)'''
    ################################################################################################################################################################
    #This part converts the randomized training and testing sets into queries with the given size

    cat_train_test_desination_directory_stage_1 = train_test_destination_stage1 + category_name + "/"
    train_test_destination_for_cat = train_test_destination + category_name + "/"
    try:
      os.stat(train_test_destination_for_cat)
    except:
      os.mkdir(train_test_destination_for_cat)
    train_test_destination_for_cat+= "/Cutoff_10/"
    modified_categories_with_indices = categories_source + category_name + "/"
    validation_ratio = 0.2
    new_q_index = DivideTrainingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,query_size,validation_ratio)
    sales_rank_original_ranking_path = drive+"Yassien_PhD\Experiment_5\Categories_Ranked_by_Sales_Rank/"+category_name+".txt"
    modified_categories_with_indices = categories_source + category_name + "/"
    DivideTestingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,modified_categories_with_indices,sales_rank_original_ranking_path,query_size,new_q_index)

  return

def Randomize_Queries_List_training_Testing_FromSubCats(queries_directory,randomized_queries_dest,training_ratio):
    print("This proedure randomizes queries for training and testing")
    queries_list = []
    for file_name in os.listdir(queries_directory):
        queries_list.append(int(file_name.split('.')[0]))

    print("Total # Queries "+ str(len(queries_list)))
    training_queries = []
    testing_queries = []
    num_training = int(len(queries_list)*training_ratio)
    num_testing = len(queries_list)-num_training

    while len(queries_list) > num_testing:
        # Code randomization
        choice = random.choice(list(queries_list))
        training_queries.append(choice)
        queries_list.remove(choice)

    testing_queries = queries_list
    #Sorting testing and training query ids
    training_queries.sort()
    testing_queries.sort()
    print("Training # Queries " + str(len(training_queries)))
    print("Training Queries ")
    print(training_queries)
    training_file_path = randomized_queries_dest+"training.txt"
    filehandle = open(training_file_path,'w')
    for query in training_queries:
        filehandle.write(str(query)+"\n")
    filehandle.close
    print("Testing # Queries " + str(len(testing_queries)))
    print("testing_queries Queries ")
    print(testing_queries)
    testing_file_path = randomized_queries_dest + "testing.txt"
    filehandle = open(testing_file_path, 'w')
    for query in testing_queries:
        filehandle.write(str(query) + "\n")
    filehandle.close
    return training_queries,testing_queries

def Relabel_Products_Within_query(query,new_query_index):
    num_products_assigned_to_q = len(query)
    index = 0
    query_pair = []
    for product_line in query:
        rank = str(product_line).split(' ')[0]
        query_pair.append((index, int(rank)))
        index += 1

    #print("query_pair before ")
    #print(query_pair)
    given_query_pair = []
    for p in query_pair:
        given_query_pair.append(p)

    mergeSort(query_pair)
    query_pair.reverse()
    #print("query pair after")
    #print(query_pair)
    #print("given_query_pair")
    #print(given_query_pair)
    rank = len(query_pair) - 1
    correct_rank = 0
    relabled_queries = []
    for qpair in given_query_pair:
        new_query = ""
        correct_rank = 0
        for p in query_pair:
            if p[0] == qpair[0]:
                break
            else:
                correct_rank += 1
        correct_rank = len(query_pair) - 1 - correct_rank
        # print("qpair[0] "+str(qpair[0]))
        #print("correct_rank is "+str(correct_rank))
        old_query = query[qpair[0]]
        new_query = str(correct_rank) + ' '
        old_query_iter = str(old_query).split(' ')
        for i in range(1, len(old_query_iter)):
            if i == 1:
                temp = old_query_iter[i].split(':')
                new_q_index = temp[0] + ":" + str(new_query_index)
                new_query += new_q_index + ' '
            else:
                if i == len(old_query_iter) - 1:
                    new_query += old_query_iter[i]
                else:
                    new_query += old_query_iter[i] + ' '
        relabled_queries.append(new_query)
        rank -= 1

    return relabled_queries
def Pick_Feature_Data_For_Given_Queries(randomized_queries_path,queries_directory,all_product_indices,query_map_code_file_path,training_testing_dest_directory,features_base_directory,train,categories_with_large_products):

    query_ids = []
    with open(randomized_queries_path, 'r') as fp:
        for line in fp:
            query_ids.append(line.split('\n')[0])
    print(query_ids)

    query_id_map_list = dict()
    ignore_first_line = 0
    with open(query_map_code_file_path, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_map_list[row[0]]=(row[1],row[2].split('\n')[0]) #add query id mapped to main Category and then sub_category
    #print(query_id_map_list)


    all_product_cat_indices = dict()
    all_category_feature_vect_dict = dict()

    for category_name in categories_with_large_products:
        indicies_file_path = all_product_indices + category_name + ".txt"
        all_product_indices_dict = dict()
        ignore_first_line = 0
        print(indicies_file_path)
        with open(indicies_file_path, 'r') as fp:
            for line in fp:
                if ignore_first_line == 0:
                    ignore_first_line = 1
                    continue
                row = line.split('\t')
                all_product_indices_dict[row[0]]=int(row[1])
        all_product_cat_indices[category_name]=all_product_indices_dict
        query_feat_file_path = features_base_directory + category_name + ".txt"
        all_vectors = []
        with open(query_feat_file_path, 'r') as fp:
            for feature_row in fp:
                all_vectors.append(feature_row.split('\n')[0])
        all_category_feature_vect_dict[category_name]=all_vectors
    #print(len(all_product_indices_dict))
    #print(all_product_indices_dict)
    train_file_path =""
    test_file_path=""
    if train == 1:
        train_file_path=training_testing_dest_directory+"train.txt"
        filehandle = open(train_file_path,'w')
    else:
        test_file_path = training_testing_dest_directory+"test.txt"
        filehandle = open(test_file_path, 'w')

    for query_row in query_ids:
        queryid = query_row
        print(queryid)
        query_ind = queryid#queryid.split('_')[1]
        query_cat_sub_cat = query_id_map_list[queryid]
        query_category = query_cat_sub_cat[0]
        query_sub_category = query_cat_sub_cat[1]
        query_file_path = queries_directory+queryid+".txt"
        query_data = []
        with open(query_file_path, 'r') as fp:
            for line in fp:
                product_id = line.split('\n')[0]
                all_product_indices_dict=all_product_cat_indices[query_category]
                product_index = int(all_product_indices_dict[product_id])
                #print(product_id+" "+str(product_index))
                '''query_feat_file_path = features_base_directory+query_category+".txt"
                all_vectors = []
                with open(query_feat_file_path, 'r') as fp:
                    for feature_row in fp:
                        all_vectors.append(feature_row.split('\n')[0])
                #print(all_vectors[product_index])
                '''
                #print(query_category)
                #print(product_index)
                #print(len(all_category_feature_vect_dict[query_category]))
                #print(all_category_feature_vect_dict)
                query_data.append(all_category_feature_vect_dict[query_category][product_index])
        #print(len(query_data))
        #print(query_data)
        #for pro_feat in query_data:
         #   print(pro_feat)

        relabled_query = Relabel_Products_Within_query(query_data,query_ind)
        #print("Relabled ")
        for pro_feat in relabled_query:
            #print(pro_feat)
            filehandle.write(pro_feat+"\n")

    filehandle.close()
    if train == 1:
        shutil.copy2(train_file_path, training_testing_dest_directory+"valid.txt")
    return
def Pick_Training_Testing_Features(randomized_queries_dest,queries_directory,all_product_indices,query_map_code_file_path,training_testing_dest_directory,features_base_directory,categories_with_large_products):
    print("This procedure fetches the feature vector for each product associated to each query")
    #First we start fetching training data
    randomized_training_path = randomized_queries_dest + "training.txt"
    Pick_Feature_Data_For_Given_Queries(randomized_training_path,queries_directory,all_product_indices,query_map_code_file_path,training_testing_dest_directory,features_base_directory,1,categories_with_large_products)
    #Next we start fetching testing data
    randomized_testing_path = randomized_queries_dest + "testing.txt"
    Pick_Feature_Data_For_Given_Queries(randomized_testing_path, queries_directory, all_product_indices,
                                        query_map_code_file_path, training_testing_dest_directory,
                                        features_base_directory, 0,categories_with_large_products)

    return
from RankingHelper import Collect_Queries_With_Given_Num_Products
def Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Regression_Amazon(drive):
    base_training_directory =drive+"\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/"
    training_query_cat_path = drive+"\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map_train.txt"
    test_query_cat_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map_test.txt"
    all_cat_traning_file_path = base_training_directory+"train.txt"
    all_cat_testing_file_path = base_training_directory + "test.txt"
    orig_catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games",
                     "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Regression(drive, base_training_directory, training_query_cat_path,
                                                           test_query_cat_path, all_cat_traning_file_path,
                                                           all_cat_testing_file_path, orig_catNames)
    return

def Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Yelp(drive):
    base_training_directory =drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    training_query_cat_path = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map_train.txt"
    test_query_cat_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map_test.txt"
    all_cat_traning_file_path = base_training_directory+"train.txt"
    all_cat_testing_file_path = base_training_directory + "test.txt"
    orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data(drive, base_training_directory, training_query_cat_path,
                                                           test_query_cat_path, all_cat_traning_file_path,
                                                           all_cat_testing_file_path, orig_catNames)
    return
def Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Amazon(drive):
    base_training_directory =drive+"\Yassien_PhD\Experiment_5\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    training_query_cat_path = drive+"\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map_train.txt"
    test_query_cat_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map_test.txt"
    all_cat_traning_file_path = base_training_directory+"train.txt"
    all_cat_testing_file_path = base_training_directory + "test.txt"
    orig_catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games",
                     "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data(drive, base_training_directory, training_query_cat_path,
                                                           test_query_cat_path, all_cat_traning_file_path,
                                                           all_cat_testing_file_path, orig_catNames)
    return

def Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data(drive,base_training_directory,training_query_cat_path,test_query_cat_path,all_cat_traning_file_path,
                                                           all_cat_testing_file_path,orig_catNames):

    training_query_cat_dict = dict()
    testing_query_cat_dict = dict()
    with open(training_query_cat_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)-1):
                queries.append(row[i])
            queries.append(row[len(row)-1].split('\n')[0])
            training_query_cat_dict[row[0]]=queries

    #print("training")
    #print(training_query_cat_dict)

    with open(test_query_cat_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)-1):
                queries.append(row[i])
            queries.append(row[len(row)-1].split('\n')[0])
            testing_query_cat_dict[row[0]]=queries

    #print("testing")
    #print(testing_query_cat_dict)
    for category_name in orig_catNames:
        print("Considering "+category_name)
        dest_directory=base_training_directory+category_name+"/"
        try:
            os.stat(dest_directory)
        except:
            os.mkdir(dest_directory)
        training_cat_queries = training_query_cat_dict[category_name]
        new_training_file_path = dest_directory+"train.txt"
        filhandle = open(new_training_file_path,'w')
        num_quries_found = 0
        prev_id = -1
        with open(all_cat_traning_file_path, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                qid = row[1].split(':')[1]
                if qid in training_cat_queries:
                    filhandle.write(line)
                    if qid !=prev_id:
                        num_quries_found+=1
                        prev_id = qid

        filhandle.close()
        print("Original Num Training queries "+str(len(training_cat_queries))+" Written num queries "+str(num_quries_found))
        shutil.copy2(new_training_file_path,dest_directory+"valid.txt")

        testing_cat_queries = testing_query_cat_dict[category_name]
        new_test_file_path = dest_directory + "test.txt"
        filhandle = open(new_test_file_path, 'w')
        num_quries_found=0
        prev_id = -1
        with open(all_cat_testing_file_path, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                qid = row[1].split(':')[1]

                if qid in testing_cat_queries:
                    filhandle.write(line)
                    if qid !=prev_id:
                        num_quries_found+=1
                        prev_id = qid
        filhandle.close()
        print("Original Num Testing queries " + str(len(testing_cat_queries)) + " Written num queries " + str(num_quries_found))
        print("*****************************************************************************************************************")
    return
def Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Regression(drive,base_training_directory,training_query_cat_path,test_query_cat_path,all_cat_traning_file_path,
                                                           all_cat_testing_file_path,orig_catNames):

    query_main_directory  = drive+"\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/"
    query_map_file_path = query_main_directory+"query_code_map.txt"
    tq_rank_main_directory=drive+"\Yassien_PhD\Experiment_5\Categories_Ranked_by_TQ_Rank/"
    query_id_cat_sub_cat_dict = dict()
    ignore_first_line = 0
    with open(query_map_file_path, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_cat_sub_cat_dict[row[0]]=(row[1],row[2])

    training_query_cat_dict = dict()
    testing_query_cat_dict = dict()
    with open(training_query_cat_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)-1):
                queries.append(row[i])
            queries.append(row[len(row)-1].split('\n')[0])
            training_query_cat_dict[row[0]]=queries

    #print("training")
    #print(training_query_cat_dict)

    with open(test_query_cat_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)-1):
                queries.append(row[i])
            queries.append(row[len(row)-1].split('\n')[0])
            testing_query_cat_dict[row[0]]=queries


    #print("testing")
    #print(testing_query_cat_dict)
    for category_name in orig_catNames:
        print("Considering "+category_name)
        dest_directory=base_training_directory+category_name+"/"
        try:
            os.stat(dest_directory)
        except:
            os.mkdir(dest_directory)

        cat_tq_product_dict= dict()
        cat_tq_file_path = tq_rank_main_directory+category_name+".txt"
        with open(cat_tq_file_path, 'r') as fp:
            for line in fp:
                row = line.split('\t')
                cat_tq_product_dict[row[0]]=row[1].split('\n')[0]
        continue_train = 1
        try:
            training_cat_queries = training_query_cat_dict[category_name]
        except KeyError:
            print(category_name+" not found in training")
            continue_train = 0

        if continue_train == 1:
            new_training_file_path = dest_directory+"train.txt"
            filhandle = open(new_training_file_path,'w')
            num_quries_found = 1
            prev_id = -1
            index = 0
            product_list = []
            with open(all_cat_traning_file_path, 'r') as fp:
                for line in fp:
                    row = line.split(' ')
                    qid = row[1].split(':')[1]
                    if prev_id == -1:
                        prev_id = qid
                        index=0
                    product_cat = query_id_cat_sub_cat_dict[qid][0]
                    product_sub_cat = query_id_cat_sub_cat_dict[qid][1].split('\n')[0]
                    #print(product_cat+" "+product_sub_cat)

                    if qid in training_cat_queries:

                        if qid !=prev_id:
                            num_quries_found+=1
                            prev_id = qid
                            index=0

                        query_file_path = query_main_directory + product_cat + "/" + product_sub_cat + ".txt"
                        #if qid !=prev_id or len(product_list)==0:
                        product_list=[]
                        with open(query_file_path, 'r') as fp:
                            for newline in fp:
                                newline = newline.split('\n')
                                product_list.append(newline[0])

                        if index<len(product_list):
                            #print("qid is "+str(qid)+"  index "+str(index))
                            tq_rank = cat_tq_product_dict[product_list[index]]
                            index += 1
                            filhandle.write(str(tq_rank)+" ")
                            for i in range(2,len(row)):
                                if i == len(row)-1:
                                    filhandle.write(row[i])
                                else:
                                    filhandle.write(row[i] + " ")

                        else:
                            print("didn't find index "+str(index))
                            print("len prod list "+str(len(product_list)))
                            print(qid)
                            print(query_file_path)



            filhandle.close()
            print("Original Num Training queries "+str(len(training_cat_queries))+" Written num queries "+str(num_quries_found))
            shutil.copy2(new_training_file_path,dest_directory+"valid.txt")
        try:
            testing_cat_queries = testing_query_cat_dict[category_name]
        except KeyError:
            print(category_name+" not found in testing")
            continue
        new_test_file_path = dest_directory + "test.txt"
        filhandle = open(new_test_file_path, 'w')
        num_quries_found = 1
        prev_id = -1
        index = 0
        product_list = []
        with open(all_cat_testing_file_path, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                qid = row[1].split(':')[1]
                if prev_id == -1:
                    prev_id = qid
                    index=0
                product_cat = query_id_cat_sub_cat_dict[qid][0]
                product_sub_cat = query_id_cat_sub_cat_dict[qid][1].split('\n')[0]

                if qid in testing_cat_queries:
                    if qid !=prev_id:
                        num_quries_found+=1
                        prev_id = qid
                        index=0

                    query_file_path = query_main_directory + product_cat + "/" + product_sub_cat + ".txt"
                    #if qid !=prev_id or len(product_list)==0:
                    product_list=[]
                    with open(query_file_path, 'r') as fp:
                        for newline in fp:
                            newline = newline.split('\n')
                            product_list.append(newline[0])

                    if index<len(product_list):
                        #print("qid is "+str(qid)+"  index "+str(index))
                        tq_rank = cat_tq_product_dict[product_list[index]]
                        index += 1
                        filhandle.write(str(tq_rank)+" ")
                        for i in range(2,len(row)):
                            if i == len(row)-1:
                                filhandle.write(row[i])
                            else:
                                filhandle.write(row[i] + " ")

                    else:
                        print("didn't find index "+str(index))
                        print("len prod list "+str(len(product_list)))
                        print(qid)
                        print(query_file_path)
        filhandle.close()
        print("Original Num Testing queries " + str(len(testing_cat_queries)) + " Written num queries " + str(num_quries_found))
        print("*****************************************************************************************************************")

    return
def Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon(drive):
    print("This procedure performs the preparation of the training and testing from queries based on sub categories for all cagegories at once Amazon Dataset")
    orig_catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games",
                     "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    query_cat_folder = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category/"
    for cat in orig_catNames:
        print("Considering "+cat)
        category_folder=query_cat_folder+cat+"/"
        desired_num_products=8
        dest_directory="D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/"+cat+"/"
        '''try:
            os.stat(dest_directory)
        except:
            os.mkdir(dest_directory)
        Collect_Queries_With_Given_Num_Products(category_folder,desired_num_products,dest_directory)'''

    #Extract_and_Code_Queries_From_Sub_Categories()
    queries_directory = drive+"\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    all_product_indices = drive+"\Yassien_PhD\Experiment_5\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive+"\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    training_testing_dest_directory = drive+"\Yassien_PhD\Experiment_5\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    randomized_queries_dest = drive+"\Yassien_PhD\Experiment_5\Randomized_Queryset/"
    features_base_directory = drive+"\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
    categories_with_large_products = orig_catNames
    training_ratio = 0.8
    validation_ratio = 0.2
    #Randomize_Queries_List_training_Testing_FromSubCats(queries_directory,randomized_queries_dest,training_ratio)
    Pick_Training_Testing_Features(randomized_queries_dest,queries_directory,all_product_indices,query_map_code_file_path,training_testing_dest_directory,features_base_directory,categories_with_large_products)

    return

def Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Yelp(drive):
    print("This procedure performs the preparation of the training and testing from queries based on sub categories for all cagegories at once Yelp Dataset")
    orig_catNames = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    query_cat_folder = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Queries_Per_Product_Category/"
    for cat in orig_catNames:
        print("Considering "+cat)
        category_folder=query_cat_folder+cat+"/"
        desired_num_products=8
        dest_directory=drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/"+cat+"/"
        '''try:
            os.stat(dest_directory)
        except:
            os.mkdir(dest_directory)
        Collect_Queries_With_Given_Num_Products(category_folder,desired_num_products,dest_directory)'''
    extracted_queries_base = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/"
    base_dest = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    coded_query_map_path = extracted_queries_base + "query_code_map.txt"
    #Extract_and_Code_Queries_From_Sub_Categories(extracted_queries_base,base_dest,coded_query_map_path,orig_catNames)
    queries_directory = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    all_product_indices = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    training_testing_dest_directory = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    randomized_queries_dest = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/"
    features_base_directory = drive+"\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Different_time_feature_vectors\All_Categories_Data_25_Basic_Features_With_1_Time_Intervals/"
    training_ratio = 0.8
    validation_ratio = 0.2
    #Randomize_Queries_List_training_Testing_FromSubCats(queries_directory,randomized_queries_dest,training_ratio)
    Pick_Training_Testing_Features(randomized_queries_dest,queries_directory,all_product_indices,query_map_code_file_path,training_testing_dest_directory,features_base_directory,orig_catNames)

    return
def Old_Kendall_Tau_Measuring_On_All_Predictions_Level(products_to_test,predictions,base_predictions_directory,category_name,R_path,correlationFileHandle):
    # This is the old measuring of kendall tau metric
    if len(products_to_test) != len(predictions):
        print("Error Un even lists")
        print("Num products from sales " + str(len(products_to_test)) + " From predictions " + str(len(predictions)))

    #print("#####################################")
    #print("After Sorting")
    mergeSort(products_to_test)
    mergeSort(predictions)
    products_to_test.reverse()  # reverse as it is ordered in ascending order and in our notation the higher the value the better the rank
    predictions.reverse()
    #print(products_to_test)
    #print(predictions)

    # Create sorted sales rank file
    print("Writing sorted sales rank file ")
    file_path = base_predictions_directory + category_name + "/Cutoff_10/" + "Sorted_Sales_Rank.txt"
    filehandle = open(file_path, 'w')
    filehandle.write("Index\tRank\n")
    for sales_rank in products_to_test:
        filehandle.write(str(sales_rank[0]) + "\t" + str(sales_rank[1]) + "\n")
    filehandle.close()

    # Create sorted predictions
    print("Writing sorted predictions file ")
    file_path = base_predictions_directory + category_name + "/Cutoff_10/" + "Sorted_Predictions.txt"
    filehandle = open(file_path, 'w')
    filehandle.write("Index\tValue\n")
    for pred in predictions:
        filehandle.write(str(pred[0]) + "\t" + str(pred[1]) + "\n")
    filehandle.close()

    # Create R_Difference file where you put the two
    print("Writing R_Difference File for kendall Calculation")
    r_difference_path = base_predictions_directory + category_name + "/Cutoff_10/" + "R_Difference.txt"
    filehandle = open(r_difference_path, 'w')
    for i in range(len(products_to_test)):
        filehandle.write(str(i + 1) + "\t")
        initial_index = products_to_test[i][0]
        temp_index = 0
        for pred in predictions:
            if initial_index == pred[0]:
                break
            temp_index += 1
        filehandle.write(str(temp_index + 1) + "\n")
    filehandle.close()

    from Testing import runKenallExtractScript, writeCorrelationRScriptOneFile
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptOneFile(r_difference_path, 1,
                                                     base_predictions_directory + category_name + "/Cutoff_10/")
    print(rScriptFilePath)
    print("Kendall value is ")
    kendall = runKenallExtractScript(rScriptFilePath, R_path)
    print("The avg Kendall ")
    print(kendall)
    correlationFileHandle.write(category_name + "\t\t" + str(kendall) + "\n")
    return

def New_Kendall_Tau_Measuring_On_Query_Level(base_predictions_directory,category_name,products_to_test,R_path,correlationFileHandle):
    # Here is the new kendall tau metric measurment which will be on the query base and then we average the results from Sales Rank way
    # '''
    r_difference_folder_path = base_predictions_directory + category_name + "/Cutoff_10/R_Difference/"
    try:
        os.stat(r_difference_folder_path)
    except:
        os.mkdir(r_difference_folder_path)

    testing_path = base_predictions_directory + category_name + "/Cutoff_10/" + "test.txt"
    query_ranks = []
    prods_per_query = []
    num_products = 0
    query = []
    queryid = ""
    nums = 0
    with open(testing_path, 'r') as filep:
        for line in filep:
            row = line.split(' ')
            if queryid == "":
                queryid = row[1]
                nums += 1
                num_products += 1
                continue

            if queryid != row[1]:
                queryid = row[1]
                prods_per_query.append(nums)
                nums = 1
                num_products += 1
            else:
                nums += 1
                num_products += 1

    if nums > 0:
        prods_per_query.append(nums)

    # print("Nums per query")
    # print(prods_per_query)
    # print("****************************************************")
    index = 0
    for k in range(len(prods_per_query)):
        nums = prods_per_query[k]
        inner = 0
        query = []
        for z in range(index, index + nums):
            pair = products_to_test[z]
            pair = (inner, pair[1])
            products_to_test[z] = pair
            query.append(products_to_test[z])
            # print(products_to_test[z])
            inner += 1
        query_ranks.append(query)
        index += nums
        # print("****************************************************")
    print("Num Products " + str(num_products))
    predictions = []

    predictions_path = base_predictions_directory + category_name + "/Cutoff_10/" + "predictions.txt"
    with open(predictions_path, 'r') as filep:
        for line in filep:
            predictions.append(float(line))

    query_predictions = []

    index = 0
    for i in range(len(query_ranks)):
        query = query_ranks[i]
        #print("query Before ")
        #print(query)
        given_salesrank_query = []
        for p in query:
            given_salesrank_query.append(p)
        mergeSort(query)
        #query.reverse()
        #print("query After ")
        #print(query)
        num_pro_per_query = len(query)
        final_sales_list = []
        correct_rank = 0
        for p in given_salesrank_query:
            correct_rank=0
            for pp in query:
                if p[0]==pp[0]:
                    break
                else:
                    correct_rank+=1
            correct_rank=num_pro_per_query-1-correct_rank
            final_sales_list.append(correct_rank)
        #print("final_sales_list ")
        #print(final_sales_list)


        query_pred = []
        for j in range(num_pro_per_query):
            query_pred.append((j, predictions[index]))
            index += 1
            # print("Query Pred Before")
            # print(query_pred)
        given_pred_query = []
        for p in query_pred:
            given_pred_query.append(p)

        #print("query pred before ")
        #print(query_pred)
        mergeSort(query_pred)
        query_pred.reverse()
        #print("query pred after ")
        #print(query_pred)
        # print("Query Pred after")
        # print(query_pred)
        final_pres_list = []
        for p in given_pred_query:
            correct_rank = 0
            for pp in query_pred:
                if p[0] == pp[0]:
                    break
                else:
                    correct_rank += 1
            correct_rank = num_pro_per_query - 1 - correct_rank
            final_pres_list.append(correct_rank)

        #print("final_pres_list")
        #print(final_pres_list)
        file_path = r_difference_folder_path + "R_Difference_" + str(i) + ".txt"
        filehandle = open(file_path, 'w')
        # print(query_pred)
        #old way
        #for k in range(len(query_pred)):
         #   filehandle.write(str(query[k][0] + 1) + "\t" + str(query_pred[k][0] + 1) + "\n")
        for k in range(len(final_pres_list)):
            filehandle.write(str(final_sales_list[k])+ "\t" + str(final_pres_list[k] + 1) + "\n")
        filehandle.close()
        # print(query_pred[i][0])
        # print("-----------------------------------------")
        query_predictions.append(query_pred)
    # print(query_predictions)

    from Testing import runKenallExtractScript, writeCorrelationRScriptNew
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptNew(base_predictions_directory + category_name + "/Cutoff_10/", 1)
    print("Kendall value is ")
    kendall = runKenallExtractScript(rScriptFilePath, R_path)
    avg_kendall = 0
    all_kendall_path = base_predictions_directory + category_name + "/Cutoff_10/kendalls.txt"
    filehandle = open(all_kendall_path, 'w')
    for ken in kendall:
        avg_kendall += (ken)
        filehandle.write(str(ken) + "\n")
    filehandle.close()

    avg_kendall = avg_kendall / len(kendall)
    print("Avg Kendal " + str(avg_kendall))
    correlationFileHandle.write(category_name + "\t\t" + str(avg_kendall) + "\n")
    return

def New_Kendall_Tau_Measuring_On_Testing_Set(base_predictions_directory,category_name,R_path,correlationFileHandle):
    # Here is the new kendall tau metric measurment which will be on the query base and then we average the results from testing file

    r_difference_folder_path = base_predictions_directory + category_name + "/Cutoff_10/R_Difference/"
    try:
        os.stat(r_difference_folder_path)
    except:
        os.mkdir(r_difference_folder_path)

    testing_path = base_predictions_directory + category_name + "/Cutoff_10/" + "test.txt"
    query_ranks = []
    num_products = 0
    query = []
    queryid = ""
    with open(testing_path, 'r') as filep:
        for line in filep:
            row = line.split(' ')
            if queryid == "":
                queryid = row[1]
                query.append(int(row[0]))
                num_products += 1
                continue

            if queryid != row[1]:
                queryid = row[1]
                query_ranks.append(query)
                query = []
                query.append(int(row[0]))
                num_products += 1
            else:
                query.append(int(row[0]))
                num_products += 1

    if len(query) > 0:
        query_ranks.append(query)
    # print(query_ranks)
    print("Num Products " + str(num_products))
    predictions = []

    predictions_path = base_predictions_directory + category_name + "/Cutoff_10/" + "predictions.txt"
    with open(predictions_path, 'r') as filep:
        for line in filep:
            predictions.append(float(line))

    query_predictions = []

    index = 0
    for i in range(len(query_ranks)):
        query = query_ranks[i]
        num_pro_per_query = len(query)
        query_pred = []
        for j in range(num_pro_per_query):
            query_pred.append((j, predictions[index]))
            index += 1
            # print(query_pred)
        mergeSort(query_pred)
        # print(query_pred)
        file_path = r_difference_folder_path + "R_Difference_" + str(i) + ".txt"
        filehandle = open(file_path, 'w')
        # print(query_pred)
        for k in range(len(query_pred)):
            filehandle.write(str(query[k] + 1) + "\t" + str(query_pred[k][0] + 1) + "\n")
        filehandle.close()
        # print(query_pred[i][0])
        # print("-----------------------------------------")
        query_predictions.append(query_pred)
    # print(query_predictions)

    from Testing import runKenallExtractScript, writeCorrelationRScriptNew
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptNew(base_predictions_directory + category_name + "/Cutoff_10/", 1)
    print("Kendall value is ")
    kendall = runKenallExtractScript(rScriptFilePath, R_path)
    avg_kendall = 0
    all_kendall_path = base_predictions_directory + category_name + "/Cutoff_10/kendall.txt"
    filehandle = open(all_kendall_path, 'w')
    for ken in kendall:
        avg_kendall += ken
        filehandle.write(str(ken) + "\n")
    filehandle.close()
    avg_kendall = avg_kendall / len(kendall)
    print("Avg Kendal " + str(avg_kendall))
    correlationFileHandle.write(category_name + "\t\t" + str(avg_kendall) + "\n")
    return

def compute_Kendall_SubCat_Experiment_Setup_Yelp(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    # training_testing_dest_directory = drive + "\Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    testing_queries_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    query_cat_map_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map.txt"
    testing_queries = []
    with open(testing_queries_path, 'r') as fp:
        for line in fp:
            testing_queries.append(line.split('\n')[0])
    compute_Kendall_SubCat_Experiment_Setup(base_predictions_directory, drive, R_path, first_k, all_product_indices,
                                            query_map_code_file_path, testing_queries,
                                            coded_queries_directory, categories_with_large_products,
                                            query_cat_map_file_path)
    return
def compute_Kendall_SubCat_Experiment_Setup_Amazon(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\Experiment_5\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    # training_testing_dest_directory = drive + "\Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target_Sub_Cat_Setup/"
    testing_queries_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games",
                                      "Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories",
                                      "Electronics"]
    query_cat_map_file_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map.txt"

    testing_queries = []
    with open(testing_queries_path, 'r') as fp:
        for line in fp:
            testing_queries.append(line.split('\n')[0])
    compute_Kendall_SubCat_Experiment_Setup(base_predictions_directory, drive, R_path, first_k, all_product_indices,
                                            query_map_code_file_path, testing_queries,
                                            coded_queries_directory, categories_with_large_products,
                                            query_cat_map_file_path)
    return
def compute_Kendall_SubCat_Experiment_Setup_Per_Cat_Yelp(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    coded_queries_directory = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    query_cat_map_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map.txt"

    test_query_cat_path = "D:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map_test.txt"
    compute_Kendall_SubCat_Experiment_Setup_Per_Cat(base_predictions_directory, drive, R_path, first_k,
                                                    all_product_indices, query_map_code_file_path,
                                                    coded_queries_directory,
                                                    categories_with_large_products, query_cat_map_file_path,
                                                    test_query_cat_path)

    return
def compute_Kendall_SubCat_Experiment_Setup_Per_Cat_Amazon(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\Experiment_5\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    #testing_queries_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games",
                                      "Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories",
                                      "Electronics"]
    query_cat_map_file_path = drive + "\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map.txt"

    test_query_cat_path = "D:\Yassien_PhD\Experiment_5\Randomized_Queryset/query_cat_map_test.txt"
    compute_Kendall_SubCat_Experiment_Setup_Per_Cat(base_predictions_directory, drive, R_path, first_k,
                                                    all_product_indices, query_map_code_file_path,
                                                    coded_queries_directory,
                                                    categories_with_large_products, query_cat_map_file_path,
                                                    test_query_cat_path)
    return

def compute_Kendall_SubCat_Experiment_Setup_Per_Cat(base_predictions_directory, drive, R_path, first_k,
                                                    all_product_indices,query_map_code_file_path,coded_queries_directory,
                                                    categories_with_large_products,query_cat_map_file_path,
                                                    test_query_cat_path):


    testing_query_cat_dict = dict()
    with open(test_query_cat_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)-1):
                queries.append(row[i])
            queries.append(row[len(row)-1].split('\n')[0])
            testing_query_cat_dict[row[0]]=queries
    query_id_map_dict = dict()
    ignore_first_line = 0
    with open(query_map_code_file_path, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_map_dict[row[0]] = (
            row[1], row[2].split('\n')[0])  # add query id mapped to main Category and then sub_category
    kendal_tau_per_cat = dict()
    original_base_directory = base_predictions_directory
    for category_name in categories_with_large_products:
        print("Considering "+category_name)
        base_predictions_directory=original_base_directory+category_name+"/"
        all_predictions = []
        prediction_file_path = base_predictions_directory + "predictions.txt"
        with open(prediction_file_path, 'r') as fp:
            for line in fp:
                all_predictions.append(float(line.split('\n')[0]))

        all_product_sales_dict = dict()

        indicies_file_path = all_product_indices + category_name + ".txt"
        ignore_first_line = 0
        with open(indicies_file_path, 'r') as fp:
            for line in fp:
                if ignore_first_line == 0:
                    ignore_first_line = 1
                    continue
                row = line.split('\t')
                all_product_sales_dict[row[0]] = row[2]

        r_difference_directory = base_predictions_directory + "R_Difference"
        try:
            os.stat(r_difference_directory)
        except:
            os.mkdir(r_difference_directory)
        r_difference_directory += "/"

        prediction_index = 0
        testing_queries = testing_query_cat_dict[category_name]
        #print("testing_query_cat_dict")
        #print(testing_queries)
        for test_query in testing_queries:
            query_fille_path = coded_queries_directory + test_query + ".txt"
            #print(test_query)
            query_product_salesrank = []
            query_product_prediction = []
            index = 0
            with open(query_fille_path, 'r') as fp:
                for line in fp:
                    productid = line.split('\n')[0]
                    # print(productid+" "+all_product_sales_dict[productid])
                    query_product_salesrank.append((index, int(all_product_sales_dict[productid])))
                    index += 1
            # print(query_product_salesrank)
            index = 0
            for i in range(len(query_product_salesrank)):
                query_product_prediction.append((index, all_predictions[prediction_index]))
                prediction_index += 1
                index += 1
            relabled_salesrank_query = Relabel_Query(query_product_salesrank)
            # print(relabled_salesrank_query)
            # print(query_product_prediction)
            # print(query_product_prediction)
            relabled_prediction_query = Relabel_Query(query_product_prediction)
            # print(relabled_prediction_query)
            qid = test_query  # test_query.split('_')[1]
            r_query_file_path = r_difference_directory + qid + ".txt"
            filehandle = open(r_query_file_path, 'w')

            for i in range(len(relabled_salesrank_query)):
                if first_k == -1:
                    filehandle.write(str(len(relabled_salesrank_query) - relabled_salesrank_query[i][1]) + "\t" + str(
                        len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
                    # filehandle.write(str(relabled_salesrank_query[i][1]) + "\t" + str(relabled_prediction_query[i][1]) + "\n")
                else:
                    if ((len(relabled_salesrank_query) - relabled_salesrank_query[i][1])) <= first_k:
                        filehandle.write(str(len(relabled_salesrank_query) - relabled_salesrank_query[i][1]) + "\t" + str(
                            len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
            filehandle.close()

        from Testing import runKenallExtractFromNewScript, writeCorrelationRScriptNew_Method
        # Creating the R Script to run Kendall tau

        rScriptFilePath = writeCorrelationRScriptNew_Method(base_predictions_directory, 1)
        #print("Kendall value is ")
        kendall = runKenallExtractFromNewScript(rScriptFilePath, R_path)
        kendall.sort()
        avg_kendall = 0
        all_kendall_path = base_predictions_directory + "kendalls.txt"

        filehandle = open(all_kendall_path, 'w')
        for ken in kendall:
            avg_kendall += (ken[1])
            filehandle.write(str(ken[0]) + "\t" + str(ken[1]) + "\n")
            #print(str(ken[0]) + "\t" + str(ken[1]))

        avg_kendall = avg_kendall / len(kendall)
        filehandle.write("Average" + "\t" + str(avg_kendall) + "\n")
        print("Overall Avg Kendal " + str(round(avg_kendall, 3)))
        filehandle.close()
        kendal_tau_per_cat[category_name]=round(avg_kendall, 3)
    print("*****************************************************")
    for key,value in kendal_tau_per_cat.items():
        print(key+"\t"+str(value))
    return
def compute_Kendall_SubCat_Experiment_Setup(base_predictions_directory,drive,R_path,first_k,all_product_indices,query_map_code_file_path,testing_queries,
                                            coded_queries_directory,categories_with_large_products,query_cat_map_file_path,correlation_type):
    print("This procedure computes the kendall tau for the new learning subcategory experiment setup ")

    query_id_map_dict = dict()
    ignore_first_line = 0
    with open(query_map_code_file_path, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_map_dict[row[0]]=(row[1],row[2].split('\n')[0]) #add query id mapped to main Category and then sub_category


    #print(testing_queries)

    all_predictions = []
    prediction_file_path = base_predictions_directory+"predictions.txt"
    with open(prediction_file_path, 'r') as fp:
        for line in fp:
            all_predictions.append(float(line.split('\n')[0]))

    all_product_sales_dict = dict()

    for category_name in categories_with_large_products:
        indicies_file_path = all_product_indices + category_name + ".txt"
        ignore_first_line = 0
        with open(indicies_file_path, 'r') as fp:
            for line in fp:
                #if ignore_first_line == 0:
                 #   ignore_first_line = 1
                  #  continue
                row = line.split('\t')
                all_product_sales_dict[row[0]] = row[1]

    r_difference_directory = base_predictions_directory+"R_Difference"
    try:
        os.stat(r_difference_directory)
    except:
        os.mkdir(r_difference_directory)
    r_difference_directory+="/"
    #correlationFileHandle = open(base_predictions_directory+"correlation.txt", 'w')
    #correlationFileHandle.write("Query\t\tKendal Tau\n")

    #print(all_product_sales_dict)
    prediction_index = 0
    for test_query in testing_queries:
        query_fille_path  = coded_queries_directory+test_query+".txt"
        print(test_query)
        query_product_salesrank = []
        query_product_prediction = []
        index = 0
        #print(query_fille_path)
        with open(query_fille_path, 'r') as fp:
            for line in fp:
                #print(line)
                productid = line.split('\n')[0]
                #print(productid+" "+all_product_sales_dict[productid])
                query_product_salesrank.append((index,int(all_product_sales_dict[productid])))
                index+=1
        #print(query_product_salesrank)
        index = 0
        for i in range(len(query_product_salesrank)):
            #print("prediction_index "+str(prediction_index)+" "+str(len(all_predictions)))
            query_product_prediction.append((index,all_predictions[prediction_index]))
            prediction_index+=1
            index+=1
        #print("SalesRank")
        relabled_salesrank_query = Relabel_Query(query_product_salesrank)
        #print(relabled_salesrank_query)
        #print(query_product_prediction)
        #print(query_product_prediction)
        #print("Prediction")
        relabled_prediction_query = Relabel_Query(query_product_prediction)
        #print(relabled_prediction_query)
        #print("*****************************************")
        qid = test_query#test_query.split('_')[1]
        r_query_file_path = r_difference_directory+qid + ".txt"
        filehandle = open(r_query_file_path,'w')

        for i in range(len(relabled_salesrank_query)):
            if first_k == -1:
                filehandle.write(str(relabled_salesrank_query[i][1]+1) + "\t" + str(len(relabled_salesrank_query)-relabled_prediction_query[i][1]) + "\n")
                #filehandle.write(str(relabled_salesrank_query[i][1]) + "\t" + str(relabled_prediction_query[i][1]) + "\n")
            else:
                if (relabled_salesrank_query[i][1])<first_k:
                    #filehandle.write(str(len(relabled_salesrank_query)-relabled_salesrank_query[i][1])+"\t"+str(relabled_prediction_query[i][1])+"\n")
                    filehandle.write(str(relabled_salesrank_query[i][1] + 1) + "\t" + str(len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
        filehandle.close()


    from Testing import runKenallExtractFromNewScript, writeCorrelationRScriptNew_Method
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptNew_Method(base_predictions_directory, correlation_type)
    print("Kendall value is ")
    kendall = runKenallExtractFromNewScript(rScriptFilePath, R_path)
    kendall.sort()
    avg_kendall = 0
    all_kendall_path = base_predictions_directory +"kendalls.txt"
    filehandle = open(all_kendall_path, 'w')
    for ken in kendall:
        avg_kendall += (ken[1])
        filehandle.write(str(ken[0]) +"\t"+str(ken[1])+ "\n")
        print(str(ken[0]) +"\t"+str(ken[1]))


    avg_kendall = avg_kendall / len(kendall)
    filehandle.write("Average" + "\t" + str(avg_kendall) + "\n")
    if correlation_type == 1:
        print("Overall Avg Kendal " + str(round(avg_kendall,3)))
    else:
        print("Overall Avg Spearman " + str(round(avg_kendall, 3)))
    filehandle.close()

    prod_cat_dict = dict()

    with open(query_cat_map_file_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1, len(row)):
                queries.append(int(row[i]))
            prod_cat_dict[row[0]] = queries
    for key, value in prod_cat_dict.items():
        # print(key)
        # print(value)
        avg_kendall = 0
        for ken in kendall:
            if ken[0] in value:
                # print("in " +str(ken[0]))
                avg_kendall += ken[1]
        avg_kendall = avg_kendall / len(value)
        print(key +" "+ str(round(avg_kendall, 3)))

    return
def compute_Kendall_SubCat_Experiment_Setup_TQRank_Amazon(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\categories/"#"\Yassien_PhD\Experiment_5\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    testing_queries_path = drive + "\Yassien_PhD\Experiment_6\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    actual_testing_file_path = drive+"\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/test.txt"
    categories_with_large_products = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games",
                                      "Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories",
                                      "Electronics"]
    query_cat_map_file_path = drive + "\Yassien_PhD\Experiment_6\Randomized_Queryset/query_cat_map_test.txt"
    compute_Kendall_SubCat_Experiment_Setup_TQRank(base_predictions_directory, R_path, first_k,
                                                   all_product_indices, query_map_code_file_path,
                                                   testing_queries_path, coded_queries_directory,
                                                   categories_with_large_products,
                                                   query_cat_map_file_path,actual_testing_file_path)
    return
def compute_Kendall_SubCat_Experiment_Setup_TQRank_Yelp(base_predictions_directory,drive,R_path,first_k):
    all_product_indices = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    testing_queries_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Cafes", "Chinese","Mexican" , "Italian","American (Traditional)", "Thai", "Bars", "Japanese", "American (New)"]
    query_cat_map_file_path = drive + "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Randomized_Queryset/query_cat_map.txt"
    actual_testing_file_path = drive + "\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/test.txt"
    compute_Kendall_SubCat_Experiment_Setup_TQRank(base_predictions_directory, R_path, first_k,
                                                   all_product_indices, query_map_code_file_path,
                                                   testing_queries_path, coded_queries_directory,
                                                   categories_with_large_products,
                                                   query_cat_map_file_path,actual_testing_file_path)
    return

def compute_Kendall_SubCat_Experiment_Setup_TQRank(base_predictions_directory,R_path,first_k,all_product_indices,query_map_code_file_path,
                                                   testing_queries_path,coded_queries_directory,categories_with_large_products,
                                                   query_cat_map_file_path,actual_testing_file_path):
    print("This procedure computes the kendall tau for the new learning subcategory experiment setup ")
    query_id_map_dict = dict()
    ignore_first_line = 0
    with open(query_map_code_file_path, 'r') as fp:
        for line in fp:
            if ignore_first_line == 0:
                ignore_first_line = 1
                continue
            row = line.split('\t')
            query_id_map_dict[row[0]]=(row[1],row[2].split('\n')[0]) #add query id mapped to main Category and then sub_category
    testing_queries = []
    with open(testing_queries_path, 'r') as fp:
        for line in fp:
            testing_queries.append(line.split('\t')[0])

    all_tq_ranks = []
    with open(actual_testing_file_path, 'r') as fp:
        for line in fp:
            all_tq_ranks.append(line.split(" ")[0])
    #print("TQraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaanks")
    #print(all_tq_ranks)
    all_product_sales_dict = dict()
    for category_name in categories_with_large_products:
        indicies_file_path = all_product_indices + category_name + ".txt"
        ignore_first_line = 0
        with open(indicies_file_path, 'r') as fp:
            for line in fp:
                #if ignore_first_line == 0:
                 #   ignore_first_line = 1
                  #  continue
                row = line.split('\t')
                all_product_sales_dict[row[0]] = row[1]#Return to cat sales rank original
                #all_product_tqrank_dict[row[0]] = row[3]

    #print("Salesraaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaanks")
    #print(all_product_sales_dict)

    r_difference_directory = base_predictions_directory+"R_Difference"
    try:
        os.stat(r_difference_directory)
    except:
        os.mkdir(r_difference_directory)
    r_difference_directory+="/"

    prediction_index = 0
    tq_index = 0
    for test_query in testing_queries:
        query_fille_path  = coded_queries_directory+test_query+".txt"
        print(test_query)
        query_product_salesrank = []
        query_product_prediction = []
        index = 0
        with open(query_fille_path, 'r') as fp:
            for line in fp:
                productid = line.split('\n')[0]
                if test_query == "97":
                    print(productid)
                #print(productid+" "+all_product_sales_dict[productid])
                query_product_salesrank.append((index,int(all_product_sales_dict[productid])))
                query_product_prediction.append((index, float(all_tq_ranks[tq_index])))#all_product_tqrank_dict[productid])))
                tq_index+=1
                index+=1
        index = 0
        if test_query == "97":
            print("SalesRank")
            print(query_product_salesrank)
        #Relabel labels the given set from low value to high as in the case of sales rank
        relabled_salesrank_query = Relabel_Query(query_product_salesrank)#THE LOWER THE NUMBER THE BETTER THE RANK
        if test_query == "97":
            print(relabled_salesrank_query)
        if test_query == "97":
            print("Predicitions")
            print(query_product_prediction)
        #As the predictions are the high the better we need to reverse the order when writing
        relabled_prediction_query = Relabel_Query(query_product_prediction)#THE HIGHER THE NUMBER THE BETTER THE RANK
        if test_query == "97":
            print(relabled_prediction_query)
        #print("********************************************")
        #print(relabled_prediction_query)
        qid = test_query#test_query.split('_')[1]
        r_query_file_path = r_difference_directory+qid + ".txt"
        filehandle = open(r_query_file_path,'w')
        #A Note to remember 1 is the highest rank and N is the lowest
        for i in range(len(relabled_salesrank_query)):
            if first_k == -1:
                #Here we add 1 to make it ranked from 1 to n
                filehandle.write(str(relabled_salesrank_query[i][1] + 1) + "\t" + str(len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
                #filehandle.write(str(len(relabled_salesrank_query)-relabled_salesrank_query[i][1]) + "\t" + str(relabled_prediction_query[i][1]) + "\n")
                #filehandle.write(str(relabled_salesrank_query[i][1]) + "\t" + str(relabled_prediction_query[i][1]) + "\n")
            else:
                if ((relabled_salesrank_query[i][1]))<first_k:
                    #filehandle.write(str(len(relabled_salesrank_query)-relabled_salesrank_query[i][1])+"\t"+str(relabled_prediction_query[i][1])+"\n")
                    filehandle.write(str(relabled_salesrank_query[i][1] + 1) + "\t" + str(len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
        filehandle.close()


    from Testing import runKenallExtractFromNewScript, writeCorrelationRScriptNew_Method
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptNew_Method(base_predictions_directory, 1)
    print("Kendall value is ")
    kendall = runKenallExtractFromNewScript(rScriptFilePath, R_path)
    kendall.sort()
    avg_kendall = 0
    all_kendall_path = base_predictions_directory +"kendalls.txt"
    filehandle = open(all_kendall_path, 'w')
    for ken in kendall:
        avg_kendall += (ken[1])
        filehandle.write(str(ken[0]) +"\t"+str(ken[1])+ "\n")
        print(str(ken[0]) +"\t"+str(ken[1]))


    avg_kendall = avg_kendall / len(kendall)
    filehandle.write("Average" + "\t" + str(avg_kendall) + "\n")
    print("All Queries Avg Kendal " + str(round(avg_kendall,3)))
    filehandle.close()

    prod_cat_dict = dict()

    with open(query_cat_map_file_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            queries = []
            for i in range(1,len(row)):
                queries.append(int(row[i]))
            prod_cat_dict[row[0]]=queries
    print(prod_cat_dict)
    print(kendall)
    for key,value in prod_cat_dict.items():
        #print(key)
        #print(value)
        avg_kendall=0
        for ken in kendall:
            if ken[0] in value:
                #print("in " +str(ken[0]))
                avg_kendall+=ken[1]
            else:
                print(ken[0])
        avg_kendall=avg_kendall/len(value)
        print(key+" "+str(round(avg_kendall,3)))

    #Computing the kendall for products under a cat for a given score like average,TQ...etc
    '''scores_file_path = "D:\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/label_score.txt"
    func_scores_dict = dict()
    query_product_salesrank=[]
    query_product_prediction=[]
    index = 0
    with open(scores_file_path, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            func_scores_dict[row[0]]=row[1]
            query_product_salesrank.append((index, int(all_product_sales_dict[row[0]])))
            query_product_prediction.append((index, row[1].split('\n')[0]))
            index+=1
    relabled_salesrank_query = Relabel_Query(query_product_salesrank)  # THE LOWER THE NUMBER THE BETTER THE RANK
    relabled_prediction_query = Relabel_Query(query_product_prediction)  # THE HIGHER THE NUMBER THE BETTER THE RANK

    filehandle = open("D:\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/temp_kend.txt", 'w')
    # A Note to remember 1 is the highest rank and N is the lowest
    for i in range(len(relabled_salesrank_query)):
            # Here we add 1 to make it ranked from 1 to n
            filehandle.write(str(relabled_salesrank_query[i][1] + 1) + "\t\t" + str(len(relabled_salesrank_query) - relabled_prediction_query[i][1]) + "\n")
    filehandle.close()
    #'''
    return
def Relabel_Query(query_pair):
    given_query_pair = []
    for p in query_pair:
        given_query_pair.append(p)
   # print(query_pair)
    mergeSort(query_pair)
    query_pair.reverse()
    #print("query pair after")
    #print(query_pair)
    #print("given_query_pair")
    #print(given_query_pair)
    rank = len(query_pair) - 1
    correct_rank = 0
    relabled_query = []
    index = 0
    for qpair in given_query_pair:
        new_query = ""
        correct_rank = 0
        for p in query_pair:
            if p[0] == qpair[0]:
                break
            else:
                correct_rank += 1

        correct_rank = len(query_pair) - 1 - correct_rank
        #print(correct_rank)
        relabled_query.append((index,correct_rank))
        index+=1
    return relabled_query
def compute_Kendall_New_Experiment_Setup(base_predictions_directory,categories_sales_rank,categories_with_testing_indices,lib,R_path):
  categories = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games","Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories","Electronics"]
  print("This procedure computes the kendall tau for the new learning experiment setup ")
  correlationFilePath = base_predictions_directory + "correlation_" + lib + ".txt"
  correlationFileHandle = open(correlationFilePath, 'w')
  correlationFileHandle.write("Category\t\tKendal Tau")
  correlationFileHandle.write("\n")
  for category_name in categories:

      print("Processing "+category_name)

      testing_indices = []
      testing_indices_path = categories_with_testing_indices+category_name+ "/" + "testing_index.txt"
      with open(testing_indices_path, 'r') as filep:
        for line in filep:
          testing_indices.append(int(line))

      #print(testing_indices)
      all_products = []

      sales_rank_original_ranking_path=categories_with_testing_indices+"/"+category_name+"/"+category_name+".txt"#categories_sales_rank+category_name+".txt"
      with open(sales_rank_original_ranking_path, 'r') as filep:
        for line in filep:
          sales = int(line.split('\t')[1])
          all_products.append(sales)

      products_to_test = []
      index = 0
      for i in range(len(testing_indices)):
        product_index = testing_indices[i]
        sales_rank = all_products[product_index]
        products_to_test.append((index,sales_rank))
        index+=1
      #print("Before Sorting")
      #print(products_to_test)

      predictions = []
      index = 0
      predictions_path = base_predictions_directory+category_name+"/Cutoff_10/"+"predictions.txt"
      with open(predictions_path, 'r') as filep:
        for line in filep:
          predictions.append((index,float(line)))
          index+=1
      #print(predictions)

      #Old_Kendall_Tau_Measuring_On_All_Predictions_Level(products_to_test, predictions, base_predictions_directory,category_name, R_path, correlationFileHandle)

      #New_Kendall_Tau_Measuring_On_Testing_Set(base_predictions_directory, category_name, R_path,correlationFileHandle)

      New_Kendall_Tau_Measuring_On_Query_Level(base_predictions_directory, category_name, products_to_test, R_path,correlationFileHandle)

      #break

  correlationFileHandle.close()
   #'''
  return

from RankingHelper import Create_Queries_For_Product_Category,Create_Coded_Queries_Repository

def Extract_and_Code_Queries_From_Sub_Categories(extracted_queries_base,base_dest,coded_query_map_path,orig_catNames):
    #extracted_queries_base = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8/"
    #base_dest = "D:\Yassien_PhD\Experiment_5\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    #coded_query_map_path = extracted_queries_base + "query_code_map.txt"
    #orig_catNames = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    filehandle = open(coded_query_map_path, 'w')
    filehandle.write("Query_id      Category      Query_File_Path\n")
    start_from = 0
    for categoryname in orig_catNames:
        print("Considering " + categoryname)
        cat_query_path = extracted_queries_base + categoryname + "/"
        start_from = Create_Coded_Queries_Repository(cat_query_path, base_dest, coded_query_map_path, categoryname,
                                                     start_from, filehandle)

    filehandle.close()
    return

