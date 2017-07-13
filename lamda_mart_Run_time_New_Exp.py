from lamda_mart_Run_time import runLamadaMart_All_Categories_Sub_Cat_Experiment_Setup
from Data_Preparation_For_Learning import compute_Kendall_SubCat_Experiment_Setup,compute_Kendall_SubCat_Experiment_Setup_TQRank_Amazon
from ranking_metrics import *
import os
from alogrithms import mergeSort
from New_Data_Prepration_For_Learning import Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon
from Calc_NDCG import nDCGScoresBased
from Data_Preparation_For_Learning import Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Regression_Amazon
import subprocess
import  math


def compute_Kendall_SubCat_Experiment_Setup_Amazon(base_predictions_directory,drive,R_path,first_k,correlation_type):
    print("Computing Kendall's Tau for predicted values")
    all_product_indices = drive + "\Yassien_PhD\categories/"
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
                                            query_cat_map_file_path,correlation_type)
    return

def compute_NDCG_For_list(estimated_rank,relevancy):
    ndcg_file_path = "D:\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/ndcg.r"
    folahandle = open(ndcg_file_path, 'w')
    folahandle.write("library(StatRank)\n")
    folahandle.write("EstimatedRank <- c(")
    for i in range(len(relevancy)):
        if i == len(relevancy) - 1:
            folahandle.write(str(estimated_rank[i]) + ")\n")
        else:
            folahandle.write(str(estimated_rank[i]) + ",")
    folahandle.write("RelevanceLevel <- c(")
    for i in range(len(relevancy)):
        if i == len(relevancy) - 1:
            folahandle.write(str(relevancy[i]) + ")\n")
        else:
            folahandle.write(str(relevancy[i]) + ",")

    folahandle.write("Evaluation.NDCG(EstimatedRank, RelevanceLevel)\n")

    folahandle.close()
    output = 0
    with open(os.devnull, 'w') as devnull:
        out = subprocess.check_output(["C:\Program Files\R\R-3.3.2/bin/Rscript.exe", ndcg_file_path], stderr=devnull)
        out = out.strip()
        out = str(out)
        out = out.split("[1]")
        out = out[1].split("'")
        output = float(out[0])
    return output
def compute_Ranking_Metrics_SubCat_Experiment_Setup_Amazon(base_predictions_directory):

    r_directory = base_predictions_directory+"R_Difference/"
    maps = []
    avg_ndcg = 0
    new_avg_ndcg = 0
    num_queries = 0
    avg_p_10=0
    mean_avg_p = 0
    print("qid\tndcg@10")
    for file_name in os.listdir(r_directory):
        qid = file_name.split('.')[0]
        file_path = r_directory+file_name
        ranks = []

        #print(file_name)
        preds = []
        ytrue =[]
        with open(file_path, 'r') as fp:
            for line in fp:
                line = line.split('\t')
                #ranks.append((int(line[1].split('\n')[0]),int(line[0])))
                ranks.append((int(line[0]), int(line[1].split('\n')[0])))
                ytrue.append(int(line[0]))
                preds.append(int(line[1]))
        #print("Before")
        #print(ranks)
        mergeSort(ranks)
        #print("After")
        #print(ranks)
        #ranks.reverse()
        #print(ytrue)
        #print(preds)

        rs = []
        estimated_rank = []
        relevancy = []
        precion = []
        for item in ranks:
            rs.append(len(ranks)-item[0])
            #The new one
            estimated_rank.append(len(ranks)+1-item[1])
            relevancy.append(len(ranks)+1-item[0])
            if item[0]==1 or item[0]==2 or item[0]==3 or item[0]==4 or item[0]==5:
                precion.append(1)
            else:
                precion.append(0)
        #print(precion)
        #print(rs)
        #print("len is "+str(len(rs)))
        if len(rs)>=10:
            #new_ndcg = nDCGScoresBased(preds,ytrue,10)
            #rs = [3,3,3,2,2,2,1,1,1,0]
            #ndcg = ndcg_at_k(rs,10)
            new_rs = rs
            new_rs = [8,10,	12,	13,	4,	1,	14,	5,	2,	11,	3,	9,	6,	0,	7]
            #print(relevancy)
            #print(estimated_rank)

            #print(float(out[0]))
            #for i in rs:
             #   new_rs.append(len(rs)-i+1)
            #print(rs)
            #print("New rs")
            #print(new_rs)
            #new_rs = [20.375053908,5.0943969723,24.69364005,20.522695427,45.354892604,34.443118029,28.130445862,3.8190658939,6.3543450327,3.8992726996]
            #print(new_rs)
            #mymy=ndcg_at_k(new_rs,10)
                #print(out[0])
            #mymy = sklearn.metrics.ndcg_score(relevancy,estimated_rank,k=10)
            #print("here is my "+str(mymy))
            new_ndcg = compute_NDCG_For_list(estimated_rank,relevancy)
            #new_ndcg = mymy
            #print(len(rs))
            #my_ndcg = ndcg_at_k(relevancy, 10)
            #print("here "+str(my_ndcg))
            #p_10 = precision_at_k(precion,10)
            #avg_p_10+=p_10
            #print(p_10)
            maps.append(precion)
            #avg_ndcg+=ndcg
            if math.isnan(new_ndcg):
                print("problem with "+str(new_ndcg))
                print(len(relevancy))
                print(relevancy)
                print(estimated_rank)
                max_size = int(len(estimated_rank)/2)
                estimated_rank = estimated_rank[:max_size]
                relevancy = relevancy[:max_size]
                new_ndcg = compute_NDCG_For_list(estimated_rank, relevancy)
                print("tried to fix "+str(new_ndcg))
                if math.isnan(new_ndcg)==0:
                    new_avg_ndcg += new_ndcg
                    print(qid + "\t" + str(round(new_ndcg, 3)) + " " + str(len(relevancy)))
                    num_queries += 1
            else:
                new_avg_ndcg+=new_ndcg
                print(qid+"\t"+str(round(new_ndcg,3))+" "+str(len(relevancy)))
                num_queries+=1

        #print("********************************************************************")
    #avg_ndcg /= num_queries
    #print("Num Queries "+str(num_queries)+" "+str(new_avg_ndcg))
    new_avg_ndcg/=num_queries
    #avg_p_10/= num_queries
    #print("Avg_NDCG " + str(round(avg_ndcg, 3)))
    print("NDCG " + str(round(new_avg_ndcg, 3)))
    #print("Avg_P " + str(round(avg_p_10, 3)))
    #map = mean_average_precision(maps)
    #print("Map "+str(round(map,3)))

    return




drive = "d:/"
amazon_base_learning_directory = "\Yassien_PhD\Experiment_6\Train_Test_Category_TQ_Target_Sub_Cat_Setup/"
yelp_base_learning_directory = "\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Experiment_3\Train_Test_Category_With_Time_Interval_TQ_Target_Sub_Cat_Setup/"
base_learning_directory = drive+ amazon_base_learning_directory
dataset_type="amazon"
exp_type ="ranknet"
#learning_lib_directory =drive+"Yassien_PhD\Experiment 2\Lamda_Java/"
learning_lib_directory = "C:\RankLib_New_Code/trunk/bin/"
#R_path = "C:\Program Files\R\R-3.2.2/bin/Rscript.exe"  # RMIT
R_path ="C:\Program Files\R\R-3.3.2/bin/Rscript.exe" #Laptop


print("Starting The Learning process")

#Adjust_Training_Testing_Data_Per_Cat_From_All_Cat_Data_Regression_Amazon(drive)

#Prepare_Training_Testing_Data_Sub_Cat_Experiment_Setup_Amazon(drive)


#runLamadaMart_All_Categories_Sub_Cat_Experiment_Setup(base_learning_directory,learning_lib_directory,exp_type)

compute_Kendall_SubCat_Experiment_Setup_Amazon(base_learning_directory,drive,R_path,-1,0)#Last parameter is 1 for kendall 0 for spearman
#compute_Kendall_SubCat_Experiment_Setup_TQRank_Amazon(base_learning_directory,drive,R_path,-1)
#compute_Ranking_Metrics_SubCat_Experiment_Setup_Amazon(base_learning_directory)
compute_Kendall_SubCat_Experiment_Setup_Amazon(base_learning_directory,drive,R_path,10,0)
print("Done")