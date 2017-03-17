from datetime import datetime
import os
def computeMajorityVoteForProductCategories(category_path,categoryName):
    print("Procedure to read category File, get a product from it and read its file and compute the average and write to a file for a cetegory file")
    print("This file willl contain each product_ID Sales_Rank")
    print("Considering " + category_path)
    #product_Id Category sales_rank
    print("Started")
    start = datetime.now()
    print(start)
    filehandle = open("F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + categoryName + ".txt",'w')
    num_products = 0
    with open(category_path, 'r') as fpcat:
        for line in fpcat:
            row = line.split('\t')
            product = row[0]
            product_file_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"+product+".txt"
            overallRate = 0
            counter = 0
            num_products+=1
            with open(product_file_path, 'r') as filep:
                   for item in filep:
                        review = item.split('\t')
                        overallRate = overallRate + float(review[5])
                        counter = counter + 1
            print(num_products)
            filehandle.write(product)
            filehandle.write("\t")
            overallRate = overallRate/counter
            overallRate = round(overallRate,4)
            filehandle.write(str(overallRate))
            filehandle.write("\n")

    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computerankusinghelpfulnessForProductCategories(category_path,categoryName):
    print("Procedure to read category File, get a product from it and read its file and compute the average and write to a file for a cetegory file")
    print("This file willl contain each product_ID Sales_Rank")
    print("Considering " + category_path)
    #product_Id Category sales_rank
    print("Started")
    start = datetime.now()
    print(start)
    filehandle = open("F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + categoryName + ".txt",'w')
    num_products = 0
    with open(category_path, 'r') as fpcat:
        for line in fpcat:
            row = line.split('\t')
            product = row[0]
            product_file_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"+product+".txt"
            overallRate = 0
            counter = 0
            num_products+=1
            #print("------------------------")
            with open(product_file_path, 'r') as filep:
                   for item in filep:
                        review = item.split('\t')
                        helpful =float(review[4])
                        total_votes = 0
                        if review[3] != "":
                            nonhelpful =float(review[3])-helpful
                        else:
                            nonhelpful = total_votes - helpful
                        #print("helpful "+str(helpful) +" nonhelpful " + str(nonhelpful))
                        if (helpful-nonhelpful)!=0:
                            overallRate = overallRate + float(review[5])*(helpful-nonhelpful)
                        else:
                            overallRate = overallRate + float(review[5])
                        counter = counter + 1
            print(num_products)
            filehandle.write(product)
            filehandle.write("\t")
            overallRate = overallRate/counter
            overallRate = round(overallRate,4)
            filehandle.write(str(overallRate))
            filehandle.write("\n")

    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return
def computerankusingpolartiesForProductCategories(category_path,categoryName):
    print("Procedure to read category File, get a product from it and read its file and compute the total comment polarity and write to a file for a cetegory file")
    print("This file willl contain each product_ID Sales_Rank")
    print("Considering " + category_path)
    #product_Id Category sales_rank
    print("Started")
    start = datetime.now()
    polarity_file_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties_Per_RatingLevel.txt"
    product_polarity_dict = dict()
    first_line = 0
    with open(polarity_file_path, 'r') as fpcat:
        for line in fpcat:
            if first_line ==  0:
                first_line = 1
                continue

            row = line.split('\t')
            print(row[0])
            total_polarity_val = int(row[1])+int(row[5])+int(row[9])+int(row[13])+int(row[17])
            product_polarity_dict[row[0]]=total_polarity_val

    print(start)
    filehandle = open("F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + categoryName + ".txt",'w')
    num_products = 0
    with open(category_path, 'r') as fpcat:
        for line in fpcat:
            row = line.split('\t')
            product = row[0]
            total_polarity_val=product_polarity_dict[product]
            num_products+=1
            print(num_products)
            filehandle.write(product)
            filehandle.write("\t")
            filehandle.write(str(total_polarity_val))
            filehandle.write("\n")

    filehandle.close()
    Finished = datetime.now()
    done = Finished - start
    print("Finished in "+str(round(done.total_seconds()/60,3))+" minutes")
    return


def computerankusingdirichiletForProductCategories(category_path,categoryName):
    print("Procedure to read category File, get a product from it and read its file and compute the dirichilet and write to a file for a cetegory file")
    print("This file willl contain each product_ID Sales_Rank")
    print("Considering " + category_path)
    # product_Id Category sales_rank
    print("Started")
    start = datetime.now()

    print(start)

    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    destDirectory="F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/"
    computeNormalDirichelet(productBaseDirectory, category_path, categoryName, destDirectory)
    Finished = datetime.now()
    done = Finished - start
    print("Finished in " + str(round(done.total_seconds() / 60, 3)) + " minutes")

#
from dirichlet_True_Rating import computeNormalDirichelet

categoryList = ["Arts, Crafts & Sewing","Industrial & Scientific", "Jewelry", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
categories_Path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
for cat in categoryList:
    current_path= categories_Path+cat+".txt"
    #computeMajorityVoteForProductCategories(current_path,cat)
    #computerankusingpolartiesForProductCategories(current_path, cat)
    #computerankusinghelpfulnessForProductCategories(current_path, cat)
    #computerankusingdirichiletForProductCategories(current_path, cat)

categoriesList = ["Arts","Industrial", "Jewelry" ,"Toys", "Video Games","Computers", "Software", "Cell Phones", "Electronics"]
orig_catNames = ["Arts, Crafts & Sewing","Industrial & Scientific", "Jewelry","Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]

from Learn_Ranking.RankingHelper import createSortedRankAndRunR

for i in range(len(categoriesList)):
    categoryName = categoriesList[i]
    orig_CatName = orig_catNames[i]

    original_directory = "F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + orig_CatName + "/"
    new_directory = "F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + categoryName + "/"
    print("Will Rename folder")
    os.chmod(original_directory, 0o777)
    os.rename(original_directory, new_directory)
    print("Renamed the folder")
    categoryMainDirectory = "F:\Yassien_PhD\Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_Transfer/" + categoryName + "/"
    createSortedRankAndRunR(categoryMainDirectory, "Lamda", categoryName, orig_CatName)

    os.chmod(new_directory, 0o777)

    os.rename(new_directory, original_directory)
    print("Returned the folder back to original name")

    #'''