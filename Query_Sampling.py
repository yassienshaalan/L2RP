from alogrithms import mergeSort
import numpy as np
import math

def get_num_reviews_per_product(product_path):
    #Count the number of reviews for a product
    count = 0
    with open(product_path, 'r') as filep:
        for item in filep:
            count+=1
    return count

def arrange_products_by_similarity_of_TQ_Score(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory,shuffle):
    # get num reviews per product
    product_reviews = dict()
    product_index_dict = dict()
    feature_dict = dict()
    index = 0
    products = []

    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            feature_dict[index] = line[0]
            index += 1
    index = 0
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]
            product_path = productBaseDirectory + productid + ".txt"
            product_index_dict[productid] = index
            feature_vector = feature_dict[index]
            rank = str(feature_vector).split(' ')
            products.append((productid, int(rank[0])))
            index += 1

    num_products = len(products)
    num_instances = int(round(num_products / sample_size, 0))
    mergeSort(products)
    products.reverse()
    new_products = []
    print("original num products "+str(num_products))
    upper_step = 3
    lower_step = 7

    size = len(products)
    upper_index = 0
    lower_index = size-1
    if shuffle ==1:
        while upper_index<=lower_index and len(new_products)<num_products:
            for j in range(upper_step):
                if len(new_products)<num_products:
                    new_products.append(products[upper_index])
                upper_index+=1

            for j in range(lower_step):
                if upper_index > lower_index or len(new_products)==num_products:
                    break
                else:
                    new_products.append(products[lower_index])
                lower_index -= 1
    else:
        new_products = products
    print("new num products "+str(len(new_products)))

    large_index = 0
    new_feature_vector = []
    for i in range(len(new_products)):
        #for j in range(sample_size):
        productid = new_products[large_index][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)
        large_index+=1

    print("writing new feature file")
    new_features_file_path = destination_directory + category_name + ".txt"
    filehandle = open(new_features_file_path, 'w')
    for i in range(len(new_feature_vector)):
        filehandle.write(new_feature_vector[i])
    filehandle.close()
    return

def arrange_products_by_Clustering(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory,shuffle):

    from Similarity import getFeatureVector,find_centers

    product_reviews = dict()
    product_index_dict = dict()
    feature_dict = dict()
    index = 0
    products = []

    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            feature_dict[index] = line[0]
            index += 1
    print("len old featu "+str(len(feature_dict)))
    index = 0
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]
            product_path = productBaseDirectory + productid + ".txt"
            product_index_dict[productid] = index
            #feature_vector = feature_dict[index]
            #rank = str(feature_vector).split(' ')
            #products.append((productid, int(rank[0])))
            index += 1


    features, features_dict = getFeatureVector(feature_category_path)
    num_products = len(features)
    print("Clustering")
    fv = np.array(features)
    print(fv.shape)
    mu, clusters = find_centers(fv, 100)
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
    new_features_file_path = destination_directory + category_name + ".txt"
    filehandle = open(new_features_file_path, 'w')
    for i in range(len(new_feature_vector)):
        filehandle.write(new_feature_vector[i])
    filehandle.close()

    '''
    num_products = len(products)
    num_instances = int(round(num_products / sample_size, 0))
    mergeSort(products)
    products.reverse()

    print("original num products "+str(num_products))
    upper_step = 3
    lower_step = 7

    size = len(products)
    upper_index = 0
    lower_index = size-1
    if shuffle ==1:
        while upper_index<=lower_index and len(new_products)<num_products:
            for j in range(upper_step):
                if len(new_products)<num_products:
                    new_products.append(products[upper_index])
                upper_index+=1

            for j in range(lower_step):
                if upper_index > lower_index or len(new_products)==num_products:
                    break
                else:
                    new_products.append(products[lower_index])
                lower_index -= 1
    else:
        new_products = products
    print("new num products "+str(len(new_products)))

    large_index = 0
    new_feature_vector = []
    for i in range(len(new_products)):
        productid = new_products[large_index][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)
        large_index+=1

    '''
    '''
    print("writing new feature file")
    new_features_file_path = destination_directory + category_name + ".txt"
    filehandle = open(new_features_file_path, 'w')
    for i in range(len(new_feature_vector)):
        filehandle.write(new_feature_vector[i])
    filehandle.close()'''
    return

def arrange_products_by_similarity_of_num_reviews(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory,sort):
    # get num reviews per product
    product_reviews = dict()
    product_index_dict = dict()
    feature_dict = dict()
    index = 0
    products_with_small_num_revs = []  # <70
    products_with_large_num_revs = []  # >70

    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            feature_dict[index] = line[0]
            index += 1
    index = 0
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]

            product_path = productBaseDirectory + productid + ".txt"
            num_reviews = get_num_reviews_per_product(product_path)
            product_reviews[productid] = num_reviews
            product_index_dict[productid] = index
            # print(productid +" "+str(num_reviews))
            if num_reviews <= 70:
                products_with_small_num_revs.append((productid, num_reviews))
            else:
                products_with_large_num_revs.append((productid, num_reviews))
            index += 1
    num_products = len(products_with_large_num_revs) + len(products_with_small_num_revs)
    num_instances = int(round(num_products / sample_size, 0))
    if sort == 1:
        mergeSort(products_with_small_num_revs)
        products_with_small_num_revs.reverse()
        mergeSort(products_with_large_num_revs)
        products_with_large_num_revs.reverse()
    large_index = 0
    new_feature_vector = []
    print("Large "+str(len(products_with_large_num_revs))+" Small "+str(len(products_with_small_num_revs)))
    for i in range(len(products_with_large_num_revs)):
        #for j in range(sample_size):
        productid = products_with_large_num_revs[large_index][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)
        large_index+=1

    small_index=0
    for j in range(len(products_with_small_num_revs)):
        productid = products_with_small_num_revs[small_index][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)
        small_index += 1

    print("writing new feature file")
    new_features_file_path = destination_directory + category_name + ".txt"
    filehandle = open(new_features_file_path, 'w')
    for i in range(len(new_feature_vector)):
        filehandle.write(new_feature_vector[i])
    filehandle.close()
    return

def arrange_products_by_num_reviews(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory,sort):

    #get num reviews per product
    product_reviews = dict()
    product_index_dict = dict()
    feature_dict = dict()
    index=0
    products_with_small_num_revs= []#<70
    products_with_large_num_revs = []#>70

    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            feature_dict[index]=line[0]
            index+=1
    index = 0
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]

            product_path = productBaseDirectory+productid+".txt"
            num_reviews = get_num_reviews_per_product(product_path)
            product_reviews[productid]=num_reviews
            product_index_dict[productid]=index
            #print(productid +" "+str(num_reviews))
            if num_reviews<=70:
                products_with_small_num_revs.append((productid,num_reviews))
            else:
                products_with_large_num_revs.append((productid,num_reviews))
            index+=1

    num_products = len(products_with_large_num_revs) + len(products_with_small_num_revs)
    if sort == 1:
       # print(products_with_small_num_revs)
        mergeSort(products_with_small_num_revs)
        #print(products_with_small_num_revs)
        #print(products_with_large_num_revs)
        mergeSort(products_with_large_num_revs)
        products_with_large_num_revs.reverse()
        #print(products_with_large_num_revs)
    print("Num products "+str(num_products))
    #print("products_with_small_num_revs "+str(len(products_with_small_num_revs)))
    #print("products_with_large_num_revs " + str(len(products_with_large_num_revs)))
    num_from_small_per_sample=0
    num_from_large_per_sample = 0
    if len(products_with_large_num_revs)>len(products_with_small_num_revs):
        num_from_small_per_sample=int(math.ceil(((len(products_with_small_num_revs)/len(products_with_large_num_revs))*sample_size)))
        num_from_large_per_sample=sample_size-num_from_small_per_sample
    else:
        percent = math.ceil(((len(products_with_large_num_revs) / len(products_with_small_num_revs)) * sample_size))
        num_from_large_per_sample = int(percent)
        num_from_small_per_sample = sample_size - num_from_large_per_sample

    #print("num_from_large_per_sample "+str(num_from_large_per_sample))
    #print("num_from_small_per_sample " + str(num_from_small_per_sample))


    new_feature_vector = []
    small_index = 0
    large_index = 0
    total_num_products_consumed = 0
    num_small_products_consumed = 0
    num_large_products_consumed = 0
    num_instances = int(round(num_products/sample_size,0))

    for i in range(num_instances):
        for j in range(num_from_large_per_sample):
            if large_index<len(products_with_large_num_revs):
                productid = products_with_large_num_revs[large_index][0]
                index = product_index_dict[productid]
                feature_vec = feature_dict[index]
                new_feature_vector.append(feature_vec)
                large_index+=1

        for j in range(num_from_small_per_sample):
            if small_index < len(products_with_small_num_revs):
                productid = products_with_small_num_revs[small_index][0]
                index = product_index_dict[productid]
                feature_vec = feature_dict[index]
                new_feature_vector.append(feature_vec)
                small_index += 1

    #If there exist some products not added
    for i in range(large_index,len(products_with_large_num_revs)):
        productid = products_with_large_num_revs[i][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)

    for i in range(small_index, len(products_with_small_num_revs)):
        productid = products_with_small_num_revs[i][0]
        index = product_index_dict[productid]
        feature_vec = feature_dict[index]
        new_feature_vector.append(feature_vec)

    #print("len new_feature_vector "+str(len(new_feature_vector)))
    #print("small_index "+str(small_index))
    #print("large_index " + str(large_index))
    print("writing new feature file")
    new_features_file_path = destination_directory+category_name+".txt"
    filehandle = open(new_features_file_path, 'w')
    for i in range(len(new_feature_vector)):
        filehandle.write(new_feature_vector[i])
    filehandle.close()
    print("Num_Products Num_with_large_revs Num_with_small_revs num_large_per_sample num_small_per_sample")
    print(str(num_products)+" "+str(len(products_with_large_num_revs))+" "+str(len(products_with_small_num_revs))+" "+str(num_from_large_per_sample)+" "+str(num_from_small_per_sample))
    return


def adjustSalesRankOrder(category_name,source_category_path,old_feature_path,new_feature_path,sales_destination_directory):
    index = 0
    original_products_salesrank = dict()
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            original_products_salesrank[index]=item
            index+=1
    old_features_dict = dict()
    index=0
    with open(old_feature_path, 'r') as filep:
        for item in filep:
            line = item.split(' ')
            old_features_dict[line[0]]=index
            index+=1
    index = 0
    new_features_dict = dict()
    with open(new_feature_path, 'r') as filep:
        for item in filep:
            line = item.split(' ')
            new_features_dict[line[0]] = index
            index += 1

    sales_rank_new_order = np.empty(len(old_features_dict), dtype="object")

    for key,value in old_features_dict.items():
        new_index = new_features_dict[key]
        sales_rank_line = original_products_salesrank[value]
        result = str(sales_rank_line)
        #print(result)
        sales_rank_new_order[new_index]=result

    #print(sales_rank_new_order)
    new_sales_rank_file_path = sales_destination_directory+category_name+".txt"
    filehandle = open(new_sales_rank_file_path, 'w')
    for i in range(len(sales_rank_new_order)):
        filehandle.write(sales_rank_new_order[i])
    filehandle.close()

    return


sourceFeaturesDirectory = "f:\Yassien_PhD\Experiment_4/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
category_source = "f:\Yassien_PhD\categories/"#"C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
productBaseDirectory = "f:\Yassien_PhD/Product_Reviews/"
destination_directory = "f:\Yassien_PhD\Experiment_4/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals_Sim_by_Clustering/"
sales_destination_directory= "f:\Yassien_PhD\Experiment_4/categories_sales_rank/"
sample_size = 10
categoryList = ["Industrial & Scientific","Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
for category in categoryList:
    feature_category_path = sourceFeaturesDirectory+category+".txt"
    source_category_path=category_source+category+".txt"
    print("Considering "+category)
    sort = 0
    #arrange_products_by_num_reviews(feature_category_path,category,source_category_path,productBaseDirectory,sample_size,destination_directory,sort)
    #arrange_products_by_similarity_of_num_reviews(feature_category_path,category,source_category_path,productBaseDirectory,sample_size,destination_directory)
    arrange_products_by_Clustering(feature_category_path,category,source_category_path,productBaseDirectory,sample_size,destination_directory,1)
    #arrange_products_by_similarity_of_num_reviews(feature_category_path, category, source_category_path,productBaseDirectory, sample_size, destination_directory,sort)
    old_feature_path= feature_category_path
    new_feature_path=destination_directory+category+".txt"
    adjustSalesRankOrder(category,source_category_path,old_feature_path,new_feature_path,sales_destination_directory)
