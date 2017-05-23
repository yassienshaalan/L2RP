from lamda_mart_Run_time import runLamadaMart_All_Categories_Sub_Cat_Experiment_Setup
from Data_Preparation_For_Learning import compute_Kendall_SubCat_Experiment_Setup,compute_Kendall_SubCat_Experiment_Setup_TQRank_Amazon
from ranking_metrics import *
import os
from alogrithms import mergeSort


def compute_Kendall_SubCat_Experiment_Setup_Amazon(base_predictions_directory,drive,R_path,first_k):
    print("Computing Kendall's Tau for predicted values")
    all_product_indices = drive + "\Yassien_PhD\Experiment_5\All_Products_Per_Cat_Indices/"
    query_map_code_file_path = drive + "\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8/query_code_map.txt"
    testing_queries_path = drive + "\Yassien_PhD\Experiment_6\Randomized_Queryset/testing.txt"
    coded_queries_directory = drive + "\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    categories_with_large_products = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games",
                                      "Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories",
                                      "Electronics"]
    query_cat_map_file_path = drive + "\Yassien_PhD\Experiment_6\Randomized_Queryset/query_cat_map_test.txt"

    testing_queries = []
    with open(testing_queries_path, 'r') as fp:
        for line in fp:
            testing_queries.append(line.split('\t')[0])
    compute_Kendall_SubCat_Experiment_Setup(base_predictions_directory, drive, R_path, first_k, all_product_indices,
                                            query_map_code_file_path, testing_queries,
                                            coded_queries_directory, categories_with_large_products,
                                            query_cat_map_file_path)
    return


def compute_Ranking_Metrics_SubCat_Experiment_Setup_Amazon(base_predictions_directory):

    r_directory = base_predictions_directory+"R_Difference/"
    maps = []
    avg_ndcg = 0
    num_queries = 0
    for file_name in os.listdir(r_directory):
        qid = file_name.split('.')[0]
        file_path = r_directory+file_name
        ranks = []
        with open(file_path, 'r') as fp:
            for line in fp:
                line = line.split('\t')
                ranks.append((int(line[1].split('\n')[0]),int(line[0])))
        #print(ranks)
        mergeSort(ranks)
        #print(ranks)
        ranks.reverse()
        #print(ranks)
        rs = []
        for item in ranks:
            rs.append(item[0])
        #print(rs)
        ndcg = ndcg_at_k(rs,8)
        #print(len(rs))
        #p_10 = precision_at_k(rs,8)
        #maps.append(rs)
        avg_ndcg+=ndcg
        print(qid+"\t"+str(round(ndcg,3)))
        num_queries+=1
        #print("********************************************************************")
    #map = mean_average_precision(maps)
    #print(map)
    avg_ndcg/=num_queries
    print(str(round(avg_ndcg,3)))
    return




drive = "d:/"
amazon_base_learning_directory = "\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/"
yelp_base_learning_directory = "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
base_learning_directory = drive+ amazon_base_learning_directory
dataset_type="amazon"
exp_type ="lamda_new"
print("Starting The Learning proces")
#runLamadaMart_All_Categories_Sub_Cat_Experiment_Setup(base_learning_directory,learning_lib_directory,exp_type)
rename=1
#R_path = "C:\Program Files\R\R-3.2.2/bin/Rscript.exe"  # RMIT
R_path ="C:\Program Files\R\R-3.3.2/bin/Rscript.exe" #Laptop

compute_Kendall_SubCat_Experiment_Setup_Amazon(base_learning_directory,drive,R_path,-1)
#compute_Kendall_SubCat_Experiment_Setup_TQRank_Amazon(base_learning_directory,drive,R_path,-1)
compute_Ranking_Metrics_SubCat_Experiment_Setup_Amazon(base_learning_directory)

print("Done")