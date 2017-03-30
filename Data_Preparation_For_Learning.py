import random
import shutil
import os
from alogrithms import mergeSort
from New_Query_Sampling import  DivideTrainingSetIntoQueries,DivideTestingSetIntoQueries

def get_num_reviews_per_product_local(product_path):
    #Count the number of reviews for a product
    count = 0
    with open(product_path, 'r') as filep:
        for item in filep:
            count+=1
    return count

def Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,local_destination,product_base_directory):

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
  num_actually_written = 0
  for product_line in training_products:
    produtid= str(product_line).split('\t')[0]
    product_file_path = product_base_directory+produtid+".txt"
    count = get_num_reviews_per_product_local(product_file_path)
    if count>50:
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
def Prepare_Training_Testing_Data_New_Experiment_Setup(query_size):
  category_source = "f:\Yassien_PhD\categories/"
  categories_source="f:\Yassien_PhD\Experiment_5\Categories/"
  source_features_path = "f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
  train_test_destination_stage1="f:\Yassien_PhD\Experiment_5\Train_Test_Category_Stage_1/"
  train_test_destination="f:\Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target/"
  product_base_directory ="f:\Yassien_PhD\Product_Reviews/"
  #Categories with small number of products < 5000 products do need cross validation
  categories_with_small_products = ["Industrial & Scientific","Arts, Crafts & Sewing","Computers & Accessories","Software"]


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
    training_ratio = 0.8
    source_category_path = category_source + category_name + ".txt"
    Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,modified_categories_with_indices,product_base_directory)
    source_feature_vector_path=source_features_path+category_name+".txt"
    cat_train_test_desination_directory_stage_1 = train_test_destination_stage1+category_name+"/"
    Retreive_Train_Test_Per_Category(source_feature_vector_path,category_name,modified_categories_with_indices,cat_train_test_desination_directory_stage_1)
    train_test_destination_for_cat = train_test_destination+category_name+"/"
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
    sales_rank_original_ranking_path = "f:\Yassien_PhD\Experiment_5\Categories_Ranked_by_Sales_Rank/"+category_name+".txt"
    modified_categories_with_indices = categories_source + category_name + "/"
    DivideTestingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,modified_categories_with_indices,sales_rank_original_ranking_path,query_size,new_q_index)

  return

def compute_Kendall_New_Experiment_Setup(base_predictions_directory,categories_sales_rank,categories_with_testing_indices,query_size,lib,R_path):
  categories = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games","Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories","Electronics"]
  print("This procedure computes the kendall tau for the new learning experiment setup ")
  correlationFilePath = base_predictions_directory + "correlation_" + lib + ".txt"
  correlationFileHandle = open(correlationFilePath, 'w')
  correlationFileHandle.write("Category\t\tKendal Tau")
  correlationFileHandle.write("\n")
  for category_name in categories:

    print("Processing "+category_name)

    '''testing_indices = []
    testing_indices_path = categories_with_testing_indices+category_name+ "/" + "testing_index.txt"
    with open(testing_indices_path, 'r') as filep:
      for line in filep:
        testing_indices.append(int(line))

    print(testing_indices)
    all_products = []

    sales_rank_original_ranking_path=categories_sales_rank+category_name+".txt"
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
    print("Before Sorting")
    print(products_to_test)

    predictions = []
    index = 0
    predictions_path = base_predictions_directory+category_name+"/Cutoff_10/"+"predictions.txt"
    with open(predictions_path, 'r') as filep:
      for line in filep:
        predictions.append((index,float(line)))
        index+=1
    print(predictions)

    #This is the old measuring of kendall tau metric
    if len(products_to_test) != len(predictions):
      print("Error Un even lists")
      print("Num products from sales "+str(len(products_to_test)) +" From predictions "+str(len(predictions)))

    print("#####################################")
    print("After Sorting")
    mergeSort(products_to_test)
    mergeSort(predictions)
    products_to_test.reverse()#reverse as it is ordered in ascending order and in our notation the higher the value the better the rank
    predictions.reverse()
    print(products_to_test)
    print(predictions)

    #Create sorted sales rank file
    print("Writing sorted sales rank file ")
    file_path = base_predictions_directory + category_name + "/Cutoff_10/" + "Sorted_Sales_Rank.txt"
    filehandle = open(file_path, 'w')
    filehandle.write("Index\tRank\n")
    for sales_rank in products_to_test:
      filehandle.write(str(sales_rank[0])+"\t"+str(sales_rank[1])+"\n")
    filehandle.close()

    #Create sorted predictions
    print("Writing sorted predictions file ")
    file_path = base_predictions_directory + category_name + "/Cutoff_10/" + "Sorted_Predictions.txt"
    filehandle = open(file_path, 'w')
    filehandle.write("Index\tValue\n")
    for pred in predictions:
      filehandle.write(str(pred[0]) + "\t" + str(pred[1])+"\n")
    filehandle.close()

    # Create R_Difference file where you put the two
    print("Writing R_Difference File for kendall Calculation")
    r_difference_path = base_predictions_directory + category_name + "/Cutoff_10/" + "R_Difference.txt"
    filehandle = open(r_difference_path, 'w')
    for i in range(len(products_to_test)):
      filehandle.write(str(i+1)+"\t")
      initial_index = products_to_test[i][0]
      temp_index = 0
      for pred in predictions:
        if initial_index == pred[0]:
          break
        temp_index+=1
      filehandle.write(str(temp_index + 1) + "\n")
    filehandle.close()

    from Testing import runKenallExtractScript,writeCorrelationRScriptOneFile
    #Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptOneFile(r_difference_path, 1,base_predictions_directory + category_name + "/Cutoff_10/")
    print(rScriptFilePath)
    print("Kendall value is ")
    kendall = runKenallExtractScript(rScriptFilePath, R_path)
    correlationFileHandle.write(category_name+"\t\t"+str(kendall)+"\n")

  correlationFileHandle.close()
    '''
    # Here is the new kendall tau metric measurment which will be on the query base and then we average the results
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
          queryid= row[1]
          query.append(int(row[0]))
          num_products+=1
          continue

        if queryid!= row[1]:
          queryid = row[1]
          query_ranks.append(query)
          query = []
          query.append(int(row[0]))
          num_products += 1
        else:
          query.append(int(row[0]))
          num_products += 1


    if len(query)>0:
      query_ranks.append(query)
    #print(query_ranks)
    print("Num Products "+str(num_products))
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
        query_pred.append((j,predictions[index]))
        index+=1
      #print(query_pred)
      mergeSort(query_pred)
      #print(query_pred)
      file_path = r_difference_folder_path +"R_Difference_"+str(i)+".txt"
      filehandle = open(file_path, 'w')
      #print(query_pred)
      for k in range(len( query_pred)):
        filehandle.write(str(query[k]+1)+"\t"+str(query_pred[k][0]+1)+"\n")
      filehandle.close()
        #print(query_pred[i][0])
      #print("-----------------------------------------")
      query_predictions.append(query_pred)
    #print(query_predictions)

    from Testing import runKenallExtractScript, writeCorrelationRScriptNew
    # Creating the R Script to run Kendall tau

    rScriptFilePath = writeCorrelationRScriptNew(base_predictions_directory + category_name + "/Cutoff_10/", 1)
    print("Kendall value is ")
    kendall = runKenallExtractScript(rScriptFilePath, R_path)
    avg_kendall = 0
    all_kendall_path = base_predictions_directory + category_name + "/Cutoff_10/kendall.txt"
    filehandle = open(all_kendall_path, 'w')
    for ken in kendall:
      avg_kendall+=ken
      filehandle.write(str(ken)+"\n")
    filehandle.close()
    avg_kendall = avg_kendall/len(kendall)
    print("Avg Kendal "+str(avg_kendall))
    correlationFileHandle.write(category_name + "\t\t" + str(avg_kendall) + "\n")

  correlationFileHandle.close()
  return

#Prepare_Training_Testing_Data_New_Experiment_Setup(10)
