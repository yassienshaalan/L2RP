import StanfordDependencies
'''
dependencies = parser.parseToStanfordDependencies("Pick up the tire pallet.")
tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]
print("tupleResult")
print(tupleResult)

assertEqual(tupleResult, [('prt', 'Pick', 'up'),('det', 'pallet', 'the'),('nn', 'pallet', 'tire'),('dobj', 'Pick', 'pallet')])


sd = StanfordDependencies.get_instance(jpype='C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/')
print("sd")
print(sd)'''

#from nltk.parse.stanford import StanfordDependencyParser
#path_to_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser.jar'
#path_to_models_jar = 'path_to/stanford-parser-full-2014-08-27/stanford-parser-3.4.1-models.jar'
path_to_jar = 'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/stanford-english-corenlp-2016-01-10-models.jar'
#stanford-english-corenlp-2016-01-10-models.jar'
'''
dependency_parser = StanfordDependencies.get_instance(jar_filename=path_to_jar)
sent = dependency_parser.convert_tree('(S1 (NP (DT some) (JJ blue) (NN moose)))')
print("sent")
print(sent)
for token in sent:
    print(token)
'''
import os
java_path = "C:/Program Files/Java/jre1.8.0_112/bin/java.exe"
os.environ['JAVAHOME'] = java_path

from nltk.parse.stanford import StanfordDependencyParser
from nltk.parse.stanford import StanfordParser
'''
path_to_jar = 'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/stanford-parser.jar'
path_to_models_jar = 'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/stanford-english-corenlp-2016-01-10-models.jar'
parser=StanfordParser(model_path=path_to_models_jar)
lista = list(parser.raw_parse("the quick brown fox jumps over the lazy dog"))
print("lista")
print(lista)'''
#import jpype
#dependency_parser = StanfordDependencyParser(path_to_jar, path_to_models_jar)
#jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (path_to_jar),)
#jpype.startJVM(jpype.getDefaultJVMPath())
#dependency_parser = StanfordDependencies.get_instance(jar_filename=path_to_jar)
#path_to_models_jar = 'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/stanford-english-corenlp-2016-01-10-models.jar'
#sent = dependency_parser.convert_tree('(S1 (NP (DT some) (JJ blue) (NN moose)))')

#print("sent")
#print(sent)
import numpy
import scipy
'''
t1=numpy.random.normal(-2.5,0.1,100)
print(len(t1))
t2=numpy.random.normal(2.5,0.1,100)
print(len(t2))
kl = scipy.stats.entropy(t2,t1)
print(kl)
'''
import numpy as np
#Read features from product categories
catFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2\All_Categories_Data_25_Basic_Features_With_10_Time_Interval_TQ_Target_For_Ranking/"
catList =["Arts, Crafts & Sewing","Industrial & Scientific","Jewelry"]
allCats = np.empty(len(catList),dtype=object)
catIndex = 0
for cat in catList:
    catAugFilePath=catFilePath+cat+".txt"
    print("Considering " + cat)
    AllFeatures = []
    with open(catAugFilePath, 'r') as fp:
        for line in fp:
            vector = np.zeros(250)
            tuple = line.split(' ')
            #print(tuple)
            index = 0
            for i in range(2,len(tuple)):
                feature = tuple[i].split(':')
                vector[index]=(float(feature[1]))
                index+=1
            AllFeatures.append(vector)
    allCats[catIndex]=AllFeatures
    catIndex+=1

counter = 2235
for i in range(1,len(allCats)):
    featureFromA = []
    for vector in allCats[i-1]:
        if vector[0]==0:
            featureFromA.append(0.01)
        else:
            featureFromA.append(vector[0])
        if len(featureFromA)==counter:
            break
    print(len(featureFromA))
    print(featureFromA)

    featureFromB = []
    for vector in allCats[i]:
        if vector[0] == 0:
            featureFromB.append(0.01)
        else:
            featureFromB.append(vector[0])
        if len(featureFromB) == counter:
            break
    print(len(featureFromB))
    print(featureFromB)

    kl = scipy.stats.entropy(featureFromB, featureFromA)
    print("kl")
    print(kl)


    break

