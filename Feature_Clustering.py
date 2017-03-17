from time import time
import numpy as np
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

np.random.seed(42)

digits = load_digits()
data = scale(digits.data)

n_samples, n_features = data.shape
n_digits = len(np.unique(digits.target))
labels = digits.target

sample_size = 300

#print("n_digits: %d, \t n_samples %d, \t n_features %d"% (n_digits, n_samples, n_features))


#print(79 * '_')
#print('% 9s' % 'init' '    time  inertia    homo   compl  v-meas     ARI AMI  silhouette')


'''def bench_k_means(estimator, name, data):
    t0 = time()
    estimator.fit(data)
    print('% 9s   %.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f    %.3f'
          % (name, (time() - t0), estimator.inertia_,
             metrics.homogeneity_score(labels, estimator.labels_),
             metrics.completeness_score(labels, estimator.labels_),
             metrics.v_measure_score(labels, estimator.labels_),
             metrics.adjusted_rand_score(labels, estimator.labels_),
             metrics.adjusted_mutual_info_score(labels,  estimator.labels_),
             metrics.silhouette_score(data, estimator.labels_,
                                      metric='euclidean',
                                      sample_size=sample_size)))

bench_k_means(KMeans(init='k-means++', n_clusters=n_digits, n_init=10),
              name="k-means++", data=data)

bench_k_means(KMeans(init='random', n_clusters=n_digits, n_init=10),
              name="random", data=data)

# in this case the seeding of the centers is deterministic, hence we run the
# kmeans algorithm only once with n_init=1
pca = PCA(n_components=n_digits).fit(data)
bench_k_means(KMeans(init=pca.components_, n_clusters=n_digits, n_init=1),
              name="PCA-based",
              data=data)
print(79 * '_')
from sklearn import cluster, datasets
iris = datasets.load_iris()
X_iris = iris.data
y_iris = iris.target
k_means = cluster.KMeans(n_clusters=3)
k_means.fit(X_iris)

#print(k_means.labels_[::10])'''

'''from scipy import cluster
from matplotlib import pyplot
tests = np.reshape( np.random.uniform(0,100,60), (30,2) )
initial = [cluster.vq.kmeans(tests,i) for i in range(1,10)]
cent, var = initial[3]
assignment,cdist = cluster.vq.vq(tests,cent)
pyplot.scatter(tests[:,0], tests[:,1], c=assignment)
pyplot.show()'''



'''from sklearn.decomposition import PCA
from sklearn.datasets import load_iris
iris = load_iris()
pca = PCA(n_components=2).fit(iris.data)
pca_2d = pca.transform(iris.data)


import pylab as pl
print(iris.target)
for i in range(0, pca_2d.shape[0]):
 if iris.target[i] == 0:
    c1 = pl.scatter(pca_2d[i,0],pca_2d[i,1],c='r', marker='+')
 elif iris.target[i] == 1:
     c2 = pl.scatter(pca_2d[i,0],pca_2d[i,1],c='g',marker='o')
 elif iris.target[i] == 2:
    c3 = pl.scatter(pca_2d[i,0],pca_2d[i,1],c='b', marker='*')
pl.legend([c1, c2, c3], ['Setosa', 'Versicolor','Virginica'])
pl.title('Iris dataset with 3 clusters and known outcomes')
pl.show()'''

import matplotlib.pyplot as plt
import numpy
import scipy.cluster.hierarchy as hcluster

# generate 3 clusters of each around 100 points and an orphan vector
N=100
data = numpy.random.randn(3*N,2)
data[:N] += 5
data[-N:] += 10
data[-1:] -= 20

feature_file_path ="F:\Yassien_PhD\Experiment_4\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals\Arts, Crafts & Sewing.txt"
target = []
features = []
with open(feature_file_path, 'r') as filep:
    for item in filep:
        review = item.split(' ')
        target.append(review[0])
        feat_vect = []
        for i in range(2,len(review)):
            feat_vect.append(float(review[i].split(':')[1]))
        features.append(feat_vect)

data = np.array(features)

# clustering
thresh = 0.7
clusters = hcluster.fclusterdata(data, thresh, criterion="distance")
#k_means = cluster.KMeans(n_clusters=30)
#k_means.fit(data)
print(type(clusters))
for clus in clusters:
    print(clus)
# plotting
plt.use("ggplot")
plt.scatter(*numpy.transpose(data), c=clusters)
plt.axis("equal")
title = "threshold: %f, number of clusters: %d" % (thresh, len(set(clusters)))
plt.title(title)
plt.show()
