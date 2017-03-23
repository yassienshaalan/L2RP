from Similarity import getFeatureVector,find_centers
import  numpy as np
from Stats_Plotting_Learning_Data import get_num_revs_avg_rating
def Check_Cluter_Products_Num_Revs(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory):
    product_reviews = dict()
    product_index_dict = dict()
    product_id_index_dict = dict()
    feature_vec_dict = dict()
    index = 0
    products = []

    with open(feature_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            feature_vec_dict[index] = line[0]
            index += 1
    print("len old featu "+str(len(feature_vec_dict)))
    index = 0
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]
            product_path = productBaseDirectory + productid + ".txt"
            product_index_dict[index] = product_path
            product_id_index_dict[index] = productid
            index += 1


    features, features_dict = getFeatureVector(feature_category_path)
    num_products = len(features)
    print("Clustering")
    fv = np.array(features)
    print(fv.shape)
    num_clusters = int(num_products/sample_size)
    print("Num Clusters "+str(num_clusters))

    mu, clusters = find_centers(fv, num_clusters)

    print("Retrieving Clustered Data")
    new_features_file_path = destination_directory + category_name + ".txt"
    cluster_stats_file = destination_directory+ category_name+"_stats_" + ".txt"
    filehandle = open(new_features_file_path, 'w')
    stats_file_handle = open(cluster_stats_file,'w')
    new_feature_vector = []
    filehandle.write("##\n")
    stats_file_handle.write("##\n")
    for key, value in clusters.items():
        print("Num products per Cluster "+str(len(value)))
        num_revs =[]
        avg_ratings = []
        products = []
        for feature_vec in value:
            sum = 0
            for feat in feature_vec:
                sum += feat
            product_index = features_dict[sum]
            feature_vec_ret = feature_vec_dict[product_index]
            product_path = product_index_dict[product_index]
            productid=product_id_index_dict[product_index]
            products.append((productid))
            num,avg_rating = get_num_revs_avg_rating(product_path)
            num_revs.append(num)
            avg_ratings.append(round(avg_rating,3))
            new_feature_vector.append(feature_vec_ret)
            filehandle.write(feature_vec_ret)

        stats_file_handle.write("Num products per Cluster " + str(len(value))+"\n")
        for product in products:
            stats_file_handle.write(product+"\t")
        stats_file_handle.write("\n")
        for rev in num_revs:
            stats_file_handle.write(str(rev) + "\t")
        stats_file_handle.write("\n")
        for rating in avg_ratings:
            stats_file_handle.write(str(rating) + "\t")
        stats_file_handle.write("\n")
        stats_file_handle.write("##\n")
        print(num_revs)
        print(avg_ratings)
        filehandle.write("##\n")

    #print("Num new feature Vec len "+str(len(new_feature_vector)))
    return

sourceFeaturesDirectory = "f:\Yassien_PhD\Experiment_4/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
category_source = "f:\Yassien_PhD\categories/"#"C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
productBaseDirectory = "f:\Yassien_PhD/Product_Reviews/"
destination_directory = "f:\Yassien_PhD\Experiment_4/Clustering_Investigation/"
sample_size=10
category_name = "Arts, Crafts & Sewing"
feature_category_path = sourceFeaturesDirectory+category_name+".txt"
source_category_path=category_source+category_name+".txt"
Check_Cluter_Products_Num_Revs(feature_category_path,category_name,source_category_path,productBaseDirectory,sample_size,destination_directory)
