import os
import shutil


destCopyDirectory="C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment_3\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_mixed_lamda/ada"

shutil.copy2(
    'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Rank_Lib/RankLib-2.1-patched.jar',destCopyDirectory)

os.chdir(destCopyDirectory)

command = "java -jar RankLib-2.1-patched.jar -train train.txt -ranker 4 -kcv 5 -kcvmd models/ -kcvmn ca -metric2t NDCG@10 -metric2T ERR@10"
#command = "java -jar RankLib-2.1-patched.jar -train train.txt -ranker 4 -kcv 5 -kcvmd models/ -kcvmn ca -metric2t NDCG@10 -metric2T ERR@10"
os.system(command)

'''
import  nltk
#nltk.set_proxy('http://bproxy.rmit.edu.au:8080', ('USERNAME', 'PASSWORD'))
#nltk.download()
nltk.data.path.append("C://nltk_data//")
from nltk.corpus import brown
brown.categories()
'''