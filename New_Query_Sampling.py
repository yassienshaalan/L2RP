from alogrithms import mergeSort
import os

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
    mergeSort(query_pair)
    query_pair.reverse()
    #print("query pair after")
    #print(query_pair)
    rank = len(query_pair)-1

    for qpair in query_pair:
        new_query = ""
        old_query=query[qpair[0]]
        new_query=str(rank)+' '
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

        mergeSort(query_pair)
        query_pair.reverse()
        rank = len(query_pair)-1

        for qpair in query_pair:
            new_query = ""
            old_query = query[qpair[0]]
            new_query = str(rank) + ' '
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
