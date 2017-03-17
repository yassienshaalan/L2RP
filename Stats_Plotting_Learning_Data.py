import matplotlib.pyplot as plt

def get_num_revs(product_path):
    #Count the number of reviews for a product
    count = 0
    with open(product_path, 'r') as filep:
        for item in filep:
            count+=1
    return count
def get_num_revs_original_case(source_category_path,productBaseDirectory):
    index = 0
    # products_with_small_num_revs = []  # <70
    # products_with_large_num_revs = []  # >70
    random_product_distribution = []
    x = []
    y = []
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]

            product_path = productBaseDirectory + productid + ".txt"
            num_reviews = get_num_revs(product_path)
            random_product_distribution.append((productid, num_reviews))
            x.append(index + 1)
            print(index)
            y.append(num_reviews)
            '''if num_reviews <= 70:
                products_with_small_num_revs.append((productid, num_reviews))
            else:
                products_with_large_num_revs.append((productid, num_reviews))'''
            index += 1

    return x, y


def get_num_revs_large_to_small_distribution(source_category_path,productBaseDirectory):

    index = 0
    products_with_small_num_revs = []  # <70
    products_with_large_num_revs = []  # >70
    random_product_distribution = []
    x=[]
    y=[]
    with open(source_category_path, 'r') as filep:
        for item in filep:
            line = item.split('\t')
            productid = line[0]

            product_path = productBaseDirectory+ productid + ".txt"
            num_reviews = get_num_revs(product_path)
            #random_product_distribution.append((productid, num_reviews))
            #x.append(index+1)
            #print(index)
            #y.append(num_reviews)
            if num_reviews <= 70:
                products_with_small_num_revs.append((productid, num_reviews))
            else:
                products_with_large_num_revs.append((productid, num_reviews))
            #index += 1
    for pro in products_with_large_num_revs:
        x.append(index)
        y.append(pro[1])
        print(index)
        index+=1

    for pro in products_with_small_num_revs:
        x.append(index)
        y.append(pro[1])
        print(index)
        index+=1
    return x,y

category_name = "Industrial & Scientific"
source_category_path="d:\Yassien_PhD\categories/"+category_name+".txt"
productBaseDirectory="d:\Yassien_PhD/Product_Reviews/"
x,y=get_num_revs_large_to_small_distribution(source_category_path,productBaseDirectory)
#plt.scatter(x, y, alpha=0.5)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel('Products')
ax.set_ylabel('Num Reviews')
ax.scatter(x, y)
fig.suptitle(category_name, fontsize=14, fontweight='bold')
plt.show()