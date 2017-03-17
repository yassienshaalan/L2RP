from RankingHelper import createSortedRankAndRunR
from RankingHelper import computeCategoryStatistics


categoryName="Industrial & Scientific"

categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
#createSortedRankAndRunR(categoryMainDirectory,"Lamda_mart",categoryName)

categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/K_Fold_PerCategory_Basic__With_Average_Target_25/"+categoryName+"/"
#createSortedRankAndRunR(categoryMainDirectory,"SVM",categoryName)

categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Light/K_Fold_PerCategory_25_Basic_Features/"+categoryName+"/"
#createSortedRankAndRunR(categoryMainDirectory,"SVM Light",categoryName)

newCatName = "Industrial & Scientific"
categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Regression/K_Fold_PerCategory_Basic__With_Average_Target_25/"+newCatName+"/"
createSortedRankAndRunR(categoryMainDirectory,"SVM_Light_Regression",categoryName)




#categoryMainDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold_PerCategory_25_Basic_Features/"+categoryName+"/"
#computeCategoryStatistics(categoryMainDirectory)

