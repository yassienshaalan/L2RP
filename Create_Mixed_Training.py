def merge_sort(l):
    length = len(l)
    cut=length/2
    if length<=1:
        return l
    print("cut " +str(cut))
    left = merge_sort(l[:int(cut)])
    right = merge_sort(l[int(cut):])
    return merge(left,  right)

def merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i][1] <= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result

def mergeSort(alist):
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i][1] < righthalf[j][1]:
                alist[k]=lefthalf[i]
                i=i+1
            else:
                alist[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            alist[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            alist[k]=righthalf[j]
            j=j+1
            k=k+1

def create_mixed_queries(total_num_queries,cat_percent_dict,categories,num_prod_per_query,sourceDirct,destDirect):
    print("This procedure create a number of mixed queries to be used for training")
    output_file_path = destDirect+"training_"+str(total_num_queries)+"__"
    for i in range(len(categories)):
        if i == len(categories)-1:
            output_file_path += str(cat_percent_dict[categories[i]])
        else:
            output_file_path+=str(cat_percent_dict[categories[i]])+"_"
    output_file_path+=".txt"
    filehandle = open(output_file_path, 'w')
    query_id = 0

    for cat in categories:
        queries_so_far = 0
        cat_path = sourceDirct+str(cat)+".txt"
        num_queries_per_cat_to_consider = int((cat_percent_dict[cat]/100)*total_num_queries)
        print(cat+" "+str(cat_percent_dict[cat])+"% makes "+str(num_queries_per_cat_to_consider))
        index = 0
        queries = []
        print("------------------------------------------------------------------------------------")
        with open(cat_path, 'r') as fp:
            for line in fp:
                if index%num_prod_per_query == 0 and index!=0: #That's a query finished
                    queries_so_far+=1
                    tempList = []
                    temp_index = 0
                    for query in queries:
                        row = query.split(" ")
                        tempList.append((temp_index,int(row[0])))
                        temp_index+=1

                    mergeSort(tempList)

                    temp_index=0
                    for i in range(len(tempList)):
                        temp = tempList[i]
                        newtuple = (temp[0],temp_index)
                        tempList[i]=newtuple
                        temp_index+=1

                    for i in range(len(tempList)):
                        query = queries[tempList[i][0]]
                        row = query.split(" ")
                        filehandle.write(str(num_prod_per_query-1-tempList[i][1])+" ")
                        filehandle.write("qid:"+str(query_id)+" ")
                        for j in range(2,len(row)):
                            if j == len(row)-1:
                                filehandle.write(row[j])
                            else:
                                filehandle.write(row[j] + " ")
                    query_id+=1
                    queries=[]#clear to start to collect another
                else:
                    queries.append(line)
                index+=1
                if queries_so_far == num_queries_per_cat_to_consider:
                    break
    import  shutil
    shutil.copy2(output_file_path,destDirect+'train.txt')
    shutil.copy2(output_file_path, destDirect + 'valid.txt')
    return


total_num_queries=150
a = {'import': 'trade', 1: 7.8}

cat_percent_dict={    'Arts, Crafts & Sewing':0,
                      'Industrial & Scientific':0,
                      'Jewelry':0,
                      'Toys & Games':0,
                      'Video Games':0,
                      'Computers & Accessories':0,
                      'Software':33,
                      'Cell Phones & Accessories':33,
                      'Electronics':34}

categories = ["Arts, Crafts & Sewing","Industrial & Scientific","Jewelry","Toys & Games","Video Games","Computers & Accessories","Software","Cell Phones & Accessories","Electronics"]
sourceDirct="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\All_Categories_Data_25_Basic_Features_With_10_Time_Interval_TQ_Target_For_Ranking/"
destDirect="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 2\Mixed_Queries_For_Training/"
num_prod_per_query = 10
create_mixed_queries(total_num_queries,cat_percent_dict,categories,num_prod_per_query,sourceDirct,destDirect)