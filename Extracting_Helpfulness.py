import os
def extractProductHelfpulness():
    print("Extracting Helpfulness for all products in Amazon Dataset")
    print("We write the number of Helpful and number of Non Helpful")
    file_to_write = "D:\Yassien_PhD\Experiment_6/product_Helpfluness.txt"
    filehandle1 = open(file_to_write, 'w')
    filehandle1.write("ProductID    NumHelpful   NumNonHelpful \n")
    product_base_directory = "D:\Yassien_PhD\Product_Reviews/"
    only_needed_prodcuts_dirc = "D:\Yassien_PhD\Experiment_6\Queries_Per_Product_Category_Num_Pro_GT_8_Coded/"
    product_dict = dict()
    for filename in os.listdir(only_needed_prodcuts_dirc):
        query_file_path = only_needed_prodcuts_dirc + filename
        with open(query_file_path, 'r') as fp:
            for line in fp:
                product_id = line.split("\n")[0]
                try:
                    product_dict[product_id]
                except KeyError:
                    product_dict[product_id]=0

    counter = 0
    for key,value in product_dict.items():
        productFile = product_base_directory + key+".txt"
        productid = key
        #print(productid)
        print(counter)
        total_helpful = 0
        total_non_helpful = 0
        counter+=1
        with open(productFile, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                helpful = 0
                non_helpful = 0
                num_feed_back = 0
                if len(row)>=4 and row[3]!='':
                    num_feed_back = int(row[3])
                if len(row)>=5:
                    helpful = int(row[4])

                if num_feed_back>=0:
                    non_helpful = num_feed_back -helpful
                #print("Helfpul "+str(helpful)+" NonHelfpul "+str(non_helpful))
                total_helpful+=helpful
                total_non_helpful+=non_helpful

        #print("total_helpful " + str(total_helpful) + " total_non_helpful " + str(total_non_helpful))
        filehandle1.write(productid+"\t"+str(total_helpful)+"\t"+str(total_non_helpful)+"\n")

    filehandle1.close()
    return

#extractProductHelfpulness()