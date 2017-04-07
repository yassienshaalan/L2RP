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
            if count >30:
                pair = (index,count)
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
def Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,local_destination,product_base_directory,drive,query_size):

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
  sampling_choice =2 #means arrange by number of reviews
  products_num_revs_path = drive+"Yassien_PhD/Number_of_reviews_per_product/"+category_name+".txt"
  #training_products=Query_Sampling_For_New_Experiment_Setup(training_products,products_num_revs_path,sampling_choice,query_size)

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
  source_features_path = drive+"Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
  train_test_destination_stage1=drive+"Yassien_PhD\Experiment_5\Train_Test_Category_Stage_1/"
  train_test_destination=drive+"Yassien_PhD\Experiment_5\Train_Test_Category_With_10_Time_Interval_TQ_Target/"
  product_base_directory =drive+"Yassien_PhD\Product_Reviews/"
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
    training_ratio = 0.9
    source_category_path = category_source + category_name + ".txt"
    Randomize_Product_List_and_Picktraining(source_category_path,category_name, training_ratio,modified_categories_with_indices,product_base_directory,drive,query_size)
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
    sales_rank_original_ranking_path = drive+"Yassien_PhD\Experiment_5\Categories_Ranked_by_Sales_Rank/"+category_name+".txt"
    modified_categories_with_indices = categories_source + category_name + "/"
    DivideTestingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,modified_categories_with_indices,sales_rank_original_ranking_path,query_size,new_q_index)

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
        # print("query Before ")
        # print(query)
        mergeSort(query)
        query.reverse()
        # print("query After ")
        # print(query)
        num_pro_per_query = len(query)
        query_pred = []
        for j in range(num_pro_per_query):
            query_pred.append((j, predictions[index]))
            index += 1
            # print("Query Pred Before")
            # print(query_pred)
        mergeSort(query_pred)
        query_pred.reverse()
        # print("Query Pred after")
        # print(query_pred)
        file_path = r_difference_folder_path + "R_Difference_" + str(i) + ".txt"
        filehandle = open(file_path, 'w')
        # print(query_pred)
        for k in range(len(query_pred)):
            filehandle.write(str(query[k][0] + 1) + "\t" + str(query_pred[k][0] + 1) + "\n")
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
        avg_kendall += abs(ken)
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


