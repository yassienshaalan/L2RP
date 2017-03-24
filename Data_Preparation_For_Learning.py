import random
import shutil
import os
from alogrithms import mergeSort

def Randomize_Product_List_and_Picktraining(source_category_path, training_ratio,local_destination):

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

  while len(product_list)>num_testing:
    choice = random.choice(list(product_list))
    training_products.append(choice)
    #print("Choice "+str(choice))
    product_list.remove(choice)
    #print(product_list)
  testing_products = product_list

  print("Final num_training " + str(len(training_products)))
  print("Final num_testing " + str(len(testing_products)))
  print("Final total "+str(len(training_products)+len(testing_products)))
  print("Writing Files")

  training_filepath = local_destination + "training.txt"
  training_index_filepath = local_destination + "training_index.txt"
  filehandle = open(training_filepath, 'w')
  filehandle_index = open(training_index_filepath, 'w')
  for product_line in training_products:
    produtid= str(product_line).split('\t')[0]
    filehandle.write(product_line)
    filehandle_index.write(str(productid_index_dict[produtid])+"\n")
  filehandle.close()
  filehandle_index.close()

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
def DivideTrainingSetIntoQueries(cat_train_test_desination_directory,category_name,train_test_destination_for_cat,query_size):

  #This funciton still divides the queries randomly taking the first sample_size as one query and the rest
  print("Processing " + category_name)

  try:
    os.stat(train_test_destination_for_cat)
  except:
    os.mkdir(train_test_destination_for_cat)

  training_file_path = cat_train_test_desination_directory+"training.txt"
  all_queries = []
  index = 0
  num_products = 0
  with open(training_file_path, 'r') as filep:
    query = []
    for line in filep:
      if len(query)<query_size:
        query.append(line)
        index+=1
      else:
        index=0
        all_queries.append(query)
        query=[]
        query.append(line)
      num_products+=1

  print("The index when out "+str(index))
  if len(query)!=0:
    for product in query:
      all_queries[len(all_queries)-1].append(product)

  print("Num products "+str(num_products))
  print("How many queries "+str(len(all_queries)))
  print("The length of each query")
  num_products_assigned_to_q = 0
  for query in all_queries:
    num_products_assigned_to_q+=len(query)
    index = 0
    query_pair =[]
    for product_line in query:
      rank = str(product_line).split(' ')[0]
      query_pair.append((index,int(rank)))
      index+=1
    print(query_pair)
    mergeSort(query_pair)
    print(query_pair)


  print("The num of products in queries "+str(num_products_assigned_to_q))

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

category_source = "f:\Yassien_PhD\categories/"
categories_source="f:\Yassien_PhD\Experiment_5\Categories/"
source_features_path = "f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
train_test_destination_stage1="f:\Yassien_PhD\Experiment_5\Train_Test_Category_Stage_1/"
train_test_destination="f:\Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target/"
#Categories with small number of products < 5000 products do need cross validation
categories_with_small_products = ["Industrial & Scientific","Arts, Crafts & Sewing","Computers & Accessories","Software"]


#Categories with large number of products > 5000 products we don't need cross_Validation randomize and take 80%
categories_with_large_products=["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]#[ "Jewelry","Toys & Games", "Video Games" , "Cell Phones & Accessories", "Electronics"]
for category_name in categories_with_large_products:
  '''modified_categories_with_indices= categories_source+category_name+"/"
  #training_ratio = 0.8
  #source_category_path = category_source + category_name + ".txt"
  #Randomize_Product_List_and_Picktraining(source_category_path, training_ratio,local_destination)
  source_feature_vector_path=source_features_path+category_name+".txt"
  cat_train_test_desination_directory_stage_1 = train_test_destination_stage1+category_name+"/"
  #Retreive_Train_Test_Per_Category(source_feature_vector_path,category_name,modified_categories,cat_desination_directory)
  train_test_destination_for_cat = train_test_destination+category_name+"/"
  query_size = 10
  DivideTrainingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,query_size)
  break
  '''
  sourceCategory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\All_Categories_Data_25_Basic_Features_With_10_Time_Interval_TQ_Target_For_Ranking/"+category_name+".txt"
  destinationCategory="F:\Yassien_PhD\Experiment_5\Categories_Ranked_by_TQ_Rank/"+category_name+".txt"
  PrepareCategoriesWithSalesRankRanking(sourceCategory,destinationCategory,category_name)
