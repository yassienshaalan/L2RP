import os
import shutil
categoriesList = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
dest_directory = "F:\Yassien_PhD\Product_Reviews/"
productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
categoriesDirectory = "c:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
print(len(categoriesList))
for i in range(len(categoriesList)):
    categoryName=categoriesList[i]
    print("Considering "+categoryName)
    counter = 0
    cat_file_path = categoriesDirectory+categoryName+".txt"
    with open(cat_file_path, 'r') as filep:
        for item in filep:
            product = item.split('\t')
            product_file = productBaseDirectory+product[0]+".txt"
            shutil.copy2(product_file, dest_directory)
            counter+=1
    print("Copied "+str(counter))