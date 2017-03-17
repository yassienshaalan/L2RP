from math import *
from decimal import Decimal


class Similarity():
    """ Five similarity measures function """

    def euclidean_distance(self, x, y):
        """ return euclidean distance between two lists """

        return sqrt(sum(pow(a - b, 2) for a, b in zip(x, y)))

    def manhattan_distance(self, x, y):
        """ return manhattan distance between two lists """

        return sum(abs(a - b) for a, b in zip(x, y))

    def minkowski_distance(self, x, y, p_value):
        """ return minkowski distance between two lists """

        return self.nth_root(sum(pow(abs(a - b), p_value) for a, b in zip(x, y)),
                             p_value)

    def nth_root(self, value, n_root):
        """ returns the n_root of an value """

        root_value = 1 / float(n_root)
        return round(Decimal(value) ** Decimal(root_value), 3)

    def cosine_similarity(self, x, y):
        """ return cosine similarity between two lists """

        numerator = sum(a * b for a, b in zip(x, y))
        denominator = self.square_rooted(x) * self.square_rooted(y)
        return round(numerator / float(denominator), 6)

    def square_rooted(self, x):
        """ return 3 rounded square rooted value """

        return round(sqrt(sum([a * a for a in x])), 3)

    def jaccard_similarity(self, x, y):

        """ returns the jaccard similarity between two lists """

        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)
def getFeatureVector(file_path):
    features=[]
    index = 0
    features_dict = dict()
    with open(file_path, 'r') as filep:
        for item in filep:
            line = item.split(' ')
            featureVect = []
            sum=0
            for i in range(2,len(line)):
                value = line[i].split(':')
                featureVect.append(float(value[1]))
                sum+=float(value[1])
            #featureVect.append(index)
            features_dict[sum]=index
            index+=1
            features.append(featureVect)
    return features,features_dict


import numpy as np
import random as random

def cluster_points(X, mu):
    clusters = {}
    for x in X:
        bestmukey = min([(i[0], np.linalg.norm(x - mu[i[0]])) \
                         for i in enumerate(mu)], key=lambda t: t[1])[0]
        try:
            clusters[bestmukey].append(x)
        except KeyError:
            clusters[bestmukey] = [x]
    return clusters


def reevaluate_centers(mu, clusters):
    newmu = []
    keys = sorted(clusters.keys())
    for k in keys:
        newmu.append(np.mean(clusters[k], axis=0))
    return newmu


def has_converged(mu, oldmu):
    return (set([tuple(a) for a in mu]) == set([tuple(a) for a in oldmu]))

def find_centers(X, K):
    # Initialize to K random centers
    oldmu = random.sample(list(X), K)
    mu = random.sample(list(X), K)
    while not has_converged(mu, oldmu):
        oldmu = mu
        # Assign all points in X to clusters
        clusters = cluster_points(X, mu)
        # Reevaluate centers
        mu = reevaluate_centers(oldmu, clusters)
    return (mu, clusters)

def init_board(N):
    X = np.array([(random.uniform(-1, 1), random.uniform(-1, 1)) for i in range(N)])
    return X


def main():
        """ the main function to create Similarity class instance and get used to it """

        #measures = Similarity()

        #print(measures.euclidean_distance([0, 3, 4, 5], [7, 6, 3, -1]))
        #print(measures.jaccard_similarity([0, 3, 4, 5], [7, 6, 3, -1]))
        #print(measures.cosine_similarity([0, 3, 4, 5], [7, 6, 3, -1]))
        #print(measures.jaccard_similarity([0, 1, 2, 5, 6], [0, 2, 3, 5, 7, 9]))


        '''file_path = "f:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/Arts, Crafts & Sewing.txt"
        features,features_dict = getFeatureVector(file_path)
        for key,value in features_dict.items():
            print(str(key)+" "+str(value))'''

        '''num_buckets = 100
        buckets = []
        diff = 1/num_buckets
        total_diff = 0
        for i in range(num_buckets+1):
            buckets.append(total_diff)
            total_diff+=diff
        print(buckets)
        feature_buckets = []
        for i in range(len(buckets)):
            feature_buckets.append([])

        num_products = len(features)
        print("num_products "+str(num_products))
        for i in range(1,len(features)):
            similarity = measures.cosine_similarity(features[0],features[i])
            #print(similarity)
            for j in range(len(buckets)-1):
                if similarity >= buckets[j] and similarity<buckets[j+1]:
                    feature_buckets[j].append(i)
        num_disposed_products = 0
        for i in range(len(buckets)):
            num_disposed_products+=len(feature_buckets[i])
            print(len(feature_buckets[i]))
            print(feature_buckets[i])

        print("num_disposed_products")
        print(num_disposed_products)'''


        #Clustering part
        #X = init_board(100)
        #print(X.shape)
        #print(X)

        '''fv= np.array(features)
        print(fv.shape)
        mu, clusters = find_centers(fv,100)
        print("mu")
        print(len(mu))
        print("clusters")
        num_objs=0
        for key,value in clusters.items():
            #print(key)
            num_objs+=len(value)
            print(len(value))
            #print(value[0][250])
            sum=0
            for feat in value[0]:
                sum+=feat
            print(sum)
            print(features_dict[sum])
            break
        print("num_objs")
        print(num_objs)'''



#if __name__ == "__main__":
   # main()