from alogrithms import mergeSort
import os
from Similarity import getFeatureVector,find_centers,getFeatureVector_From_Dict
import numpy as np
def DivideTrainingSetIntoQueries(cat_train_test_desination_directory,category_name,train_test_destination_for_cat,query_size,validation_ratio):

  #This funciton just divides the queries randomly taking the first sample_size as one query and the rest
  print("Processing Training set for " + category_name)

  try:
    os.stat(cat_train_test_desination_directory)
  except:
    os.mkdir(cat_train_test_desination_directory)

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

  #print("The index when out "+str(index))
  if len(query)!=0:
    for product in query:
      all_queries[len(all_queries)-1].append(product)

  print("Num products "+str(num_products))
  print("How many queries "+str(len(all_queries)))

  new_relabled_queries = []


  num_products_assigned_to_q = 0
  new_query_index = 0
  for query in all_queries:
    num_products_assigned_to_q+=len(query)
    index = 0
    query_pair =[]
    for product_line in query:
      rank = str(product_line).split(' ')[0]
      query_pair.append((index,int(rank)))
      index+=1

    #print("query_pair before ")
    #print(query_pair)
    given_query_pair=[]
    for p in query_pair:
        given_query_pair.append(p)

    mergeSort(query_pair)
    query_pair.reverse()
    #print("query pair after")
    #print(query_pair)
    #print("given_query_pair")
    #print(given_query_pair)
    rank = len(query_pair)-1
    correct_rank = 0
    for qpair in given_query_pair:
        new_query = ""
        correct_rank=0
        for p in query_pair:
            if p[0]== qpair[0]:
                break
            else:
                correct_rank+=1
        correct_rank = len(query_pair)-1-correct_rank
        #print("qpair[0] "+str(qpair[0]))
        #print("correct_rank is "+str(correct_rank))
        old_query=query[qpair[0]]
        new_query=str(correct_rank)+' '
        old_query_iter = str(old_query).split(' ')
        for i in range(1,len(old_query_iter)):
            if i == 1:
                temp = old_query_iter[i].split(':')
                new_q_index = temp[0]+":"+str(new_query_index)
                new_query += new_q_index + ' '
            else:
                if i == len(old_query_iter)-1:
                    new_query+=old_query_iter[i]
                else:
                    new_query += old_query_iter[i] + ' '
        new_relabled_queries.append(new_query)
        rank-=1
    new_query_index+=1

  num_inst_for_validation = int(len(new_relabled_queries)*validation_ratio)
  print("Num for valiation " + str(num_inst_for_validation))
  #Adjusting the number of validation to be divisible by query_size so that we don't have a non complete query in the validation and training sets
  if num_inst_for_validation%10!=0:
      div =round(num_inst_for_validation/query_size)
      div*=query_size
      num_inst_for_validation=num_inst_for_validation+(div-num_inst_for_validation)


  num_inst_for_training = len(new_relabled_queries)-num_inst_for_validation
  print("Num for valiation "+str(num_inst_for_validation))
  print("Num for final training "+str(num_inst_for_training))
  new_training_file_path = train_test_destination_for_cat + "train.txt"
  filehandle_training = open(new_training_file_path, 'w')
  new_validation_file_path = train_test_destination_for_cat + "valid.txt"
  filehandle_validation = open(new_validation_file_path, 'w')
  print("Writing new relabled queries")
  index = 0
  for query in new_relabled_queries:
      #Make training same as validation
      filehandle_validation.write(query)
      filehandle_training.write(query)
      '''#This way the validation is a divided part of the training
      if index<num_inst_for_validation:
          filehandle_validation.write(query)
      else:
          filehandle_training.write(query)
      '''
      index+=1

  print("The num of products in queries @ the end "+str(num_products_assigned_to_q))
  filehandle_validation.close()
  filehandle_training.close()
  print("Finished ")
  return new_query_index

def DivideTestingSetIntoQueries(cat_train_test_desination_directory_stage_1,category_name,train_test_destination_for_cat,modified_categories_with_indices,sales_rank_original_ranking_path,query_size,start_index):
    print("Processing Testing set for " + category_name)
    testing_file_path = cat_train_test_desination_directory_stage_1 + "testing.txt"
    all_queries = []
    index = 0
    num_products = 0
    testing_indices =[]
    testing_indices_path = modified_categories_with_indices+"testing_index.txt"
    with open(testing_indices_path, 'r') as filep:
        for line in filep:
            testing_indices.append(int(line))

    all_products = []

    with open(sales_rank_original_ranking_path, 'r') as filep:
        for line in filep:
            all_products.append(line.split('\t')[1])


    with open(testing_file_path, 'r') as filep:
        query = []
        for line in filep:
            if len(query) < query_size:
                query.append(line)
                index += 1
            else:
                index = 0
                all_queries.append(query)
                query = []
                query.append(line)
            num_products += 1

    # print("The index when out "+str(index))
    if len(query) != 0:
        for product in query:
            all_queries[len(all_queries) - 1].append(product)

    print("Num products " + str(num_products))
    print("How many queries " + str(len(all_queries)))

    new_relabled_queries = []
    new_ttesting_file_path = train_test_destination_for_cat + "test.txt"
    filehandle_testing = open(new_ttesting_file_path, 'w')
    num_products_assigned_to_q = 0
    new_query_index = start_index
    product_index = 0
    for query in all_queries:
        num_products_assigned_to_q += len(query)
        index = 0
        query_pair = []
        for product_line in query:
            sales_index = testing_indices[product_index]
            rank = all_products[sales_index]
            TQ_Rank = product_line.split(' ')[0]
            #print("TQ Rank "+str(str(product_line).split(' ')[0]))
            #print("Sales Rank "+str(rank))
            #rank = str(product_line).split(' ')[0] This is the TQ rank we will replace that with the sales rank
            query_pair.append((index, int(TQ_Rank)))#int(rank)))#Testing with putting TQ rank
            index += 1
        #print("before ")
        #print(query_pair)
        given_query_pair = []
        for p in query_pair:
            given_query_pair.append(p)
        mergeSort(query_pair)
        query_pair.reverse()
        #print("after ")
        #print(query_pair)
        rank = len(query_pair)-1
        #print("given_query_pair")
        #print(given_query_pair)
        for qpair in given_query_pair:
            new_query = ""
            old_query = query[qpair[0]]
            correct_rank = 0
            for p in query_pair:
                if p[0] == qpair[0]:
                    break
                else:
                    correct_rank += 1
            correct_rank = len(query_pair) - 1 - correct_rank
            #print("qpair[0] "+str(qpair[0]))
            #print("correct_rank is "+str(correct_rank))
            #new_query = str(rank) + ' '
            new_query = str(correct_rank) + ' '
            old_query_iter = str(old_query).split(' ')

            for i in range(1, len(old_query_iter)):
                if i == 1:
                    temp = old_query_iter[i].split(':')
                    new_q_index = temp[0] + ":" + str(new_query_index)#if you put start_index
                    new_query += new_q_index + ' '
                else:
                    if i == len(old_query_iter) - 1:
                        new_query += old_query_iter[i]
                    else:
                        new_query += old_query_iter[i] + ' '
            new_relabled_queries.append(new_query)
            rank -= 1
        new_query_index += 1
    print("The num of products in queries @ the end " + str(num_products_assigned_to_q))
    print("Writing relabled Testing set with sales rank")
    for query in new_relabled_queries:
        filehandle_testing.write(query)

    filehandle_testing.close()
    print("Finished")
    print("###########################################################################################################")
    return

def Clustering_Products(training_products,feature_category_path,source_category_path,products_num_revs_path):

    total_num_products = len(training_products)
    print("Input num "+str(total_num_products))
    products_num_revs_dict = dict()
    with open(products_num_revs_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            products_num_revs_dict[line[0]] = int(line[1])

    training_to_process = []
    for productline in training_products:
        try:
            count = products_num_revs_dict[str(productline).split('\t')[0]]
            if count>0:
                training_to_process.append(productline)
        except KeyError:
            pass
    training_products = training_to_process
    print("Now ")
    print(len(training_products))
    feature_input_dict = dict()
    product_index_dict = dict()
    index = 0
    list_of_indices = []
    print(source_category_path)
    with open(source_category_path, 'r') as filep:
        for item in filep:
            productid = item.split('\t')[0]
            for train_line in training_products:
                if productid == str(train_line).split('\t')[0]:
                    product_index_dict[index] = train_line
                    list_of_indices.append(index)
                    break
            index+=1
    index = 0
    print("len product_index_dict "+str(len(product_index_dict)))
    print("len training_products " + str(len(training_products)))
    print("len list_of_indices " + str(len(list_of_indices)))
    #print(list_of_indices)
    if len(product_index_dict) !=len(training_products):
        print("Error Severe problem in clustering ")

    index = 0
    print(feature_category_path)
    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            if index in list_of_indices:
                feature_input_dict[index]= line[0]
            index+= 1

    print("len feature_dict " + str(len(feature_input_dict)))
    features, features_sum_dict = getFeatureVector_From_Dict(feature_input_dict)
    print("Clustering")
    fv = np.array(features)
    print("Features shape for clustering "+str(fv.shape))
    num_required_clusters = int(len(training_products)/10)
    print("Num of requested clusters are " + str(num_required_clusters))
    mu, clusters = find_centers(fv, num_required_clusters)
    print("Num of clusters are "+str(len(mu)))

    print("Retrieving Clustered Data")
    new_training_data = []
    for key, value in clusters.items():
        sum = 0
        for feature_vec in value:
            sum = 0
            for feat in feature_vec:
                sum += feat
            product_index = features_sum_dict[sum]
            indo = 0
            for key,value in feature_input_dict.items():
                if indo == product_index:
                    product_index=key
                    break
                indo+=1
            train_line = product_index_dict[product_index]
            new_training_data.append(train_line)
    print("len of new_training_data"+str(len(new_training_data)))
    '''
    print("Retrieving Clustered Data")
    new_feature_vector = []
    for key, value in clusters.items():
        sum = 0
        for feature_vec in value:
            sum = 0
            for feat in feature_vec:
                sum += feat
            product_index = features_dict[sum]
            feature_vec = feature_dict[product_index]
            new_feature_vector.append(feature_vec)

    print("Num new feature Vec len "+str(len(new_feature_vector)))
    print("writing new feature file")

    '''
    #print(new_training_data)
    return new_training_data