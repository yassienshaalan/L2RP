"""
Implementation of pairwise ranking using scikit-learn LinearSVC
Reference:
    "Large Margin Rank Boundaries for Ordinal Regression", R. Herbrich,
    T. Graepel, K. Obermayer 1999
    "Learning to rank from medical imaging data." Pedregosa, Fabian, et al.,
    Machine Learning in Medical Imaging 2012.
Authors: Fabian Pedregosa <fabian@fseoane.net>
         Alexandre Gramfort <alexandre.gramfort@inria.fr>
See also https://github.com/fabianp/pysofia for a more efficient implementation
of RankSVM using stochastic gradient descent methdos.
"""

import itertools
import numpy as np

from sklearn import svm, linear_model, cross_validation

def transform_pairwise(X, y):
    """Transforms data into pairs with balanced labels for ranking
    Transforms a n-class ranking problem into a two-class classification
    problem. Subclasses implementing particular strategies for choosing
    pairs should override this method.
    In this method, all pairs are choosen, except for those that have the
    same target value. The output is an array of balanced classes, i.e.
    there are the same number of -1 as +1
    Parameters
    ----------
    X : array, shape (n_samples, n_features)
        The data
    y : array, shape (n_samples,) or (n_samples, 2)
        Target labels. If it's a 2D array, the second column represents
        the grouping of samples, i.e., samples with different groups will
        not be considered.
    Returns
    -------
    X_trans : array, shape (k, n_feaures)
        Data as pairs
    y_trans : array, shape (k,)
        Output class labels, where classes have values {-1, +1}
    """
    X_new = []
    y_new = []
    y = np.asarray(y)
    if y.ndim == 1:
        y = np.c_[y, np.ones(y.shape[0])]
    comb = itertools.combinations(range(X.shape[0]), 2)
    for k, (i, j) in enumerate(comb):
        if y[i, 0] == y[j, 0] or y[i, 1] != y[j, 1]:
            # skip if same target or different group
            continue
        X_new.append(X[i] - X[j])
        y_new.append(np.sign(y[i, 0] - y[j, 0]))
        # output balanced classes
        if y_new[-1] != (-1) ** k:
            y_new[-1] = - y_new[-1]
            X_new[-1] = - X_new[-1]
    return np.asarray(X_new), np.asarray(y_new).ravel()


class RankSVM(svm.LinearSVC):
    """Performs pairwise ranking with an underlying LinearSVC model
    Input should be a n-class ranking problem, this object will convert it
    into a two-class classification problem, a setting known as
    `pairwise ranking`.
    See object :ref:`svm.LinearSVC` for a full description of parameters.
    """

    def fit(self, X, y):
        """
        Fit a pairwise ranking model.
        Parameters
        ----------
        X : array, shape (n_samples, n_features)
        y : array, shape (n_samples,) or (n_samples, 2)
        Returns
        -------
        self
        """
        X_trans, y_trans = transform_pairwise(X, y)
        super(RankSVM, self).fit(X_trans, y_trans)
        return self

    def decision_function(self, X):
        return np.dot(X, self.coef_.ravel())

    def predict(self, X):
        """
        Predict an ordering on X. For a list of n samples, this method
        returns a list from 0 to n-1 with the relative order of the rows of X.
        The item is given such that items ranked on top have are
        predicted a higher ordering (i.e. 0 means is the last item
        and n_samples would be the item ranked on top).
        Parameters
        ----------
        X : array, shape (n_samples, n_features)
        Returns
        -------
        ord : array, shape (n_samples,)
            Returns a list of integers representing the relative order of
            the rows in X.
        """
        if hasattr(self, 'coef_'):
            return np.argsort(np.dot(X, self.coef_.ravel()))
        else:
            raise ValueError("Must call fit() prior to predict()")

    def score(self, X, y):
        """
        Because we transformed into a pairwise problem, chance level is at 0.5
        """
        X_trans, y_trans = transform_pairwise(X, y)
        return np.mean(super(RankSVM, self).predict(X_trans) == y_trans)

def rankingAlgorithm1(X,y):
    true_coef = np.random.randn(n_features)

    Y = np.c_[y, np.mod(np.arange(n_samples), 5)]  # add query fake id
    # Y = y
    cv = cross_validation.KFold(n_samples, 5)
    train, test = next(iter(cv))
    # make a simple plot out of it

    '''
    pl.scatter(np.dot(X, true_coef), y)
    pl.title('Data to be learned')
    pl.xlabel('<X, coef>')
    pl.ylabel('y')
    #pl.show()
    '''
    # print the performance of ranking
    rank_svm = RankSVM().fit(X[train], Y[train])
    print('Performance of ranking ', rank_svm.score(X[test], Y[test]))

    ''' from old code
    # and that of linear regression
    ridge = linear_model.RidgeCV(fit_intercept=True)
    ridge.fit(X[train], y[train])
    X_test_trans, y_test_trans = transform_pairwise(X[test], y[test])
    score = np.mean(np.sign(np.dot(X_test_trans, ridge.coef_)) == y_test_trans)
    print('Performance of linear regression ', score)
    '''
    blocks = np.array([0, 1] * int((X.shape[0] / 2)))

    X_train, y_train, b_train = X[train], y[train], blocks[train]
    X_test, y_test, b_test = X[test], y[test], blocks[test]

    #ridge = linear_model.Ridge(1.)
    ridge = linear_model.RidgeCV(fit_intercept=True)
    ridge.fit(X_train, y_train)

    for i in range(2):
        tau, _ = stats.kendalltau(ridge.predict(X_test[b_test == i]), y_test[b_test == i])
        print('Kendall correlation coefficient for block %s: %.5f' % (i, tau))
    return

def rankingAlgorithm2(X,y):
    blocks = np.array([0, 1] * int((X.shape[0] / 2)))
    cv = cross_validation.StratifiedShuffleSplit(y, test_size=.5)
    train, test = next(iter(cv))

    X_train, y_train, b_train = X[train], y[train], blocks[train]
    X_test, y_test, b_test = X[test], y[test], blocks[test]

    # --------------------------------------------------------------------------------------

    # plot the result
    idx = (b_train == 0)
    np.random.seed(0)
    theta = np.deg2rad(60)
    w = np.array([np.sin(theta), np.cos(theta)])
    pl.scatter(X_train[idx, 0], X_train[idx, 1], c=y_train[idx], marker='^', cmap=pl.cm.Blues, s=100)
    pl.scatter(X_train[~idx, 0], X_train[~idx, 1], c=y_train[~idx], marker='o', cmap=pl.cm.Blues, s=100)
    pl.arrow(0, 0, 8 * w[0], 8 * w[1], fc='gray', ec='gray', head_width=0.5, head_length=0.5)
    pl.text(0, 1, '$w$', fontsize=20)
    pl.arrow(-3, -8, 8 * w[0], 8 * w[1], fc='gray', ec='gray', head_width=0.5, head_length=0.5)
    pl.text(-2.6, -7, '$w$', fontsize=20)
    pl.axis('equal')
    # pl.show()
    # ---------------------------------------------------------------------------------------
    ridge = linear_model.Ridge(1.)
    ridge.fit(X_train, y_train)
    coef = ridge.coef_ / np.linalg.norm(ridge.coef_)
    # ----------------------------------------------------------------------------------------
    pl.scatter(X_train[idx, 0], X_train[idx, 1], c=y_train[idx], marker='^', cmap=pl.cm.Blues, s=100)
    pl.scatter(X_train[~idx, 0], X_train[~idx, 1], c=y_train[~idx], marker='o', cmap=pl.cm.Blues, s=100)
    pl.arrow(0, 0, 7 * coef[0], 7 * coef[1], fc='gray', ec='gray', head_width=0.5, head_length=0.5)
    pl.text(2, 0, '$\hat{w}$', fontsize=20)
    pl.axis('equal')
    pl.title('Estimation by Ridge regression')
    # pl.show()
    # ----------------------------------------------------------------------------------------
    for i in range(2):
        tau, _ = stats.kendalltau(ridge.predict(X_test[b_test == i]), y_test[b_test == i])
        print('Kendall correlation coefficient for block %s: %.5f' % (i, tau))
    return


from sklearn.linear_model import LinearRegression, LassoLarsCV, RidgeCV
from sklearn.linear_model.base import LinearClassifierMixin, SparseCoefMixin, BaseEstimator


class ELM(BaseEstimator):

    def __init__(self, n_nodes, link='rbf', output_function='lasso', n_jobs=1, c=1):
        self.n_jobs = n_jobs
        self.n_nodes = n_nodes
        self.c = c

        if link == 'rbf':
            self.link = lambda z: np.exp(-z*z)
        elif link == 'sig':
            self.link = lambda z: 1./(1 + np.exp(-z))
        elif link == 'id':
            self.link = lambda z: z
        else:
            self.link = link

        if output_function == 'lasso':
            self.output_function = LassoLarsCV(cv=10, n_jobs=self.n_jobs)
        elif output_function == 'lr':
            self.output_function = LinearRegression(n_jobs=self.n_jobs)

        elif output_function == 'ridge':
            self.output_function = RidgeCV(cv=10)

        else:
            self.output_function = output_function

        return


    def H(self, x):

        n, p = x.shape
        xw = np.dot(x, self.w.T)
        xw = xw + np.ones((n, 1)).dot(self.b.T)
        return self.link(xw)

    def fit(self, x, y, w=None):

        n, p = x.shape
        self.mean_y = y.mean()
        if w == None:
            self.w = np.random.uniform(-self.c, self.c, (self.n_nodes, p))
        else:
            self.w = w

        self.b = np.random.uniform(-self.c, self.c, (self.n_nodes, 1))
        self.h_train = self.H(x)
        self.output_function.fit(self.h_train, y)

        return self

    def predict(self, x):
        self.h_predict = self.H(x)
        return self.output_function.predict(self.h_predict)

    def get_params(self, deep=True):
        return {"n_nodes": self.n_nodes,
                "link": self.link,
                "output_function": self.output_function,
                "n_jobs": self.n_jobs,
                "c": self.c}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self
import sklearn as sk

import matplotlib.pyplot as plt
from sklearn.externals import joblib
def estimateBestAlpha(X,y,modelSavePath):
    '''
    elm = ELM(n_nodes=30, output_function='lasso')
    gs = sk.grid_search.GridSearchCV(elm,cv=5,
                                     param_grid={"c": np.linspace(0.0001, 1, 50)},fit_params={}, scoring='mean_squared_error')
    gs.fit(X, y)
    print("best_params_")
    print(gs.best_params_['c'])
    return gs.best_params_['c']'''

    '''
    lasso = linear_model.Lasso()
    alphas = np.logspace(-4, -.5, 30)#np.linspace(0.00001, 1, 30)  # np.logspace(-4, -.5, 30)
    scores = list()
    scores_std = list()

    for alpha in alphas:
        lasso.alpha = alpha
        this_scores = cross_validation.cross_val_score(lasso, X, y, n_jobs=1)
        scores.append(np.mean(this_scores))
        scores_std.append(np.std(this_scores))
       '''

    '''
    plt.figure(figsize=(4, 3))
    plt.semilogx(alphas, scores)
    # plot error lines showing +/- std. errors of the scores
    plt.semilogx(alphas, np.array(scores) + np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.semilogx(alphas, np.array(scores) - np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.ylabel('CV score')
    plt.xlabel('alpha')
    plt.axhline(np.max(scores), linestyle='--', color='.5')
    plt.show()
    index = 0
    minIndex = 0
    min_score = -1000
    for score in scores:
        if score>min_score:
            min_score = score
            minIndex = index
        index+=1
    '''
    alphas = np.logspace(-4, -.5, 30)
    print("alphas")
    print(alphas)
    lasso_cv = linear_model.LassoCV(alphas=alphas)
    k_fold = cross_validation.KFold(len(X), 5)
    min_score = -1000
    for k, (train, test) in enumerate(k_fold):
        lasso_cv.fit(X[train], y[train])
        score = lasso_cv.score(X[test], y[test])
        if score > min_score:
            min_score = score
            minAlpha= lasso_cv.alpha_
        #print("[fold {0}] alpha: {1:.5f}, score: {2:.5f}".format(k, lasso_cv.alpha_,score ))

    joblib.dump(lasso_cv, modelSavePath, compress=9)
    return minAlpha

def rankingAlgorithm5(X,y,n_samples,modelSavePath):


    gs = sk.grid_search.GridSearchCV(ELM(n_nodes=20, output_function='lasso'),
                                     cv=5,
                                     param_grid={"c": np.linspace(0.0001, 1, 10)},
                                     fit_params={},scoring='mean_squared_error')
    gs.fit(X, y)

    print("best_params_")
    print(gs.best_params_)
    print(gs.best_params_['c'])

    lasso = linear_model.Lasso()
    alphas = np.linspace(0.0001, 1, 50)#np.logspace(-4, -.5, 30)
    scores = list()
    scores_std = list()
    print("alphas")
    print(alphas)
    for alpha in alphas:
        lasso.alpha = alpha
        this_scores = cross_validation.cross_val_score(lasso, X, y, n_jobs=1)
        scores.append(np.mean(this_scores))
        scores_std.append(np.std(this_scores))

    plt.figure(figsize=(4, 3))
    plt.semilogx(alphas, scores)
    # plot error lines showing +/- std. errors of the scores
    plt.semilogx(alphas, np.array(scores) + np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.semilogx(alphas, np.array(scores) - np.array(scores_std) / np.sqrt(len(X)),
                 'b--')
    plt.ylabel('CV score')
    plt.xlabel('alpha')
    plt.axhline(np.max(scores), linestyle='--', color='.5')
    plt.show()

    lasso_cv = linear_model.LassoCV(alphas=alphas)
    k_fold = cross_validation.KFold(len(X), 5)
    for k, (train, test) in enumerate(k_fold):
        lasso_cv.fit(X[train], y[train])
        print("[fold {0}] alpha: {1:.5f}, score: {2:.5f}".
              format(k, lasso_cv.alpha_, lasso_cv.score(X[test], y[test])))
    trainLen = 4
    testLen = 4
    tau = 0
    return trainLen, testLen, tau
    return
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

def rankingAlgorithm4(X,y,n_samples,modelSavePath):

    # Loading the Digits dataset

    # Split the dataset in two equal parts
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=0)

    # Set the parameters by cross-validation
    tuned_parameters = {'alpha': [10 ** a for a in range(-6, -2)]}

    scores = ['precision', 'recall']
    regressionModel = linear_model.Lasso
    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        print()

        clf = GridSearchCV(regressionModel, tuned_parameters, cv=5,
                           scoring='mean_squared_error' % score)
        clf.fit(X_train, y_train)

        print("Best parameters set found on development set:")
        print()
        print(clf.best_params_)
        print()
        print("Grid scores on development set:")
        print()
        for params, mean_score, scores in clf.grid_scores_:
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean_score, scores.std() * 2, params))
        print()

        print("Detailed classification report:")
        print()
        print("The model is trained on the full development set.")
        print("The scores are computed on the full evaluation set.")
        print()
        y_true, y_pred = y_test, clf.predict(X_test)
        print(classification_report(y_true, y_pred))
        print()
    return
def rankingAlgorithm3(X,y,n_samples,modelSavePath):
    from sklearn.cross_validation import KFold

    from matplotlib import pyplot as plt
    '''
    from sklearn.cross_validation import cross_val_score
    ridge = linear_model.Lasso(alpha=0.1)
    scores = cross_val_score(ridge,X,y,scoring='mean_squared_error',cv=10)
    print("MSE")
    print(np.sqrt(-scores).mean())
    '''

    cv = KFold(n_samples, 5)
    AllPredictions = []
    AllTest = []
    testLen = 0
    trainLen = 0
    #ridge = linear_model.BayesianRidge(alpha_1=1e-06, alpha_2=1e-06, compute_score=False, copy_X=True,
     #  fit_intercept=True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
      # normalize=False, tol=0.001, verbose=False)
    #alphas = [0.01,0.02,0.1,0.2,0.0001]#np.logspace(-16, 3, num=50, base=2)

    min_Score = 10000000
    min_alpha = 0
    alphares = estimateBestAlpha(X,y,modelSavePath)
    print("alphares")
    print(alphares)
    #for alpha in alphas:
    #regressionModel = linear_model.Lasso(alpha=alphares)
    # ridge = linear_model.Ridge(1.)
    # ridge = linear_model.Lasso(alpha=0.1)

    tau = 0
    return trainLen, testLen, tau
    #print("alpha")
    #print(alpha)
    for train, test in cv:

        X_train = X[train]
        y_train = y[train]
        trainLen = len(X_train)

        X_test = X[test]
        y_test = y[test]
        testLen = len(X_test)


        # ridge = linear_model.RidgeCV(fit_intercept=True)
        regressionModel.fit(X_train, y_train)
        # print the performance of ranking
        #modelscore = regressionModel.score(X_test, y_test)

        #print('Performance of ranking ', modelscore)

        predictions = regressionModel.predict(X_test)

        for pred in predictions:
            AllPredictions.append(pred)
        for tes in y_test:
            AllTest.append(tes)
        #tau, _ = stats.kendalltau(predictions, y_test)


    # Saving the model
    joblib.dump(regressionModel, modelSavePath, compress=9)
    # Reading the model
    # ridge_new = joblib.load(modelSavePath)

    #taus, _ = stats.spearmanr(AllPredictions, AllTest)
    tau, _ = stats.kendalltau(AllPredictions, AllTest)
    tau = round(tau,3)
    #print('Kendall correlation coefficient for the test list : %.5f ' % (tau))

    return trainLen,testLen,tau

def buildFeatureListForCategory(catFilePath,productBaseDirectory):
    X = []  # list of samples each with list of features
    y = []  # contains the average as the expected value
    productList = []
    featureProduct = dict()
    index = 0
    with open(catFilePath, 'r') as fp:
        for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                featureList = []
                ratingTemproalCategory, ratingHelpfulnessCategory, n, average = analyzeProduct(productBaseDirectory,productId)
                periodDict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],}
                for i in range(len(ratingTemproalCategory)):
                    for item in ratingTemproalCategory[i]:
                        try:
                            record = periodDict[item]
                            record.append(ratingTemproalCategory[i][item])
                            periodDict[item] = record
                        except KeyError as e:
                            pass
                            # featureList.append(ratingTemproalCategory[i][item])
                five = 0
                avStart = 0
                sum = 0
                for key, value in periodDict.items():
                    for item in value:
                        featureList.append(item)
                        avStart +=(item*(five+1))
                        sum+=item
                        five+=1
                    if sum > 0:
                        avStart = avStart / sum

                    #featureList.append(avStart)
                    avStart = 0
                    five = 0
                    sum = 0

                n_features = len(featureList)
                if n_features != 55:
                    print("not 55")
                    print(periodDict)
                    print(ratingTemproalCategory)
                    print(n_features)
                    print(featureList)

                productList.append((productId,average))
                featureProduct[productId] = featureList
                X.append(featureList)
                y.append(average)
                index +=1
    return X,y,productList,featureProduct

def buildFeatureListForCategoryForDirichlet(catFilePath,productBaseDirectory):
    X = []  # list of samples each with list of features
    y = []  # contains the average as the expected value
    productList = []
    featureProduct = dict()
    index = 0
    with open(catFilePath, 'r') as fp:
        for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                featureList = []
                ratingTemproalCategory, ratingHelpfulnessCategory, n, average = analyzeProduct(productBaseDirectory,productId)
                periodDict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],}
                for i in range(len(ratingTemproalCategory)):
                    for item in ratingTemproalCategory[i]:
                        try:
                            record = periodDict[item]
                            record.append(ratingTemproalCategory[i][item])
                            periodDict[item] = record
                        except KeyError as e:
                            pass
                            # featureList.append(ratingTemproalCategory[i][item])
                five = 0
                avStart = 0
                sum = 0
                for key, value in periodDict.items():
                    for item in value:
                        featureList.append(item)
                        avStart +=(item*(five+1))
                        sum+=item
                        five+=1
                    if sum > 0:
                        avStart = avStart / sum

                    #featureList.append(avStart)
                    avStart = 0
                    five = 0
                    sum = 0

                n_features = len(featureList)
                if n_features != 55:
                    print("not 55")
                    print(periodDict)
                    print(ratingTemproalCategory)
                    print(n_features)
                    print(featureList)

                ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategory)
                prior = [2,2,2,2,2]
                retValue = dirichlet_mean(ratings, prior)
                productList.append((productId,average))
                featureProduct[productId] = featureList
                X.append(featureList)
                y.append(retValue)
                index +=1
    return X,y,productList,featureProduct
def buildFeatureListForCategoryForGeneral(catFilePath,productBaseDirectory,category,option,featureSet,ProductPolaritiesPerRating ):
    X = []  # list of samples each with list of features
    y = []  # contains the average as the expected value
    productList = []
    featureProduct = dict()
    index = 0
    filePathExpertiese = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/UserHelpfulVotesPerCategoryNew/" + category
    userExpert = dict()
    with open(filePathExpertiese, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            userExpert[row[0]] = float(row[3])
    productpriceFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_prices.txt"
    prices = dict()
    with open(productpriceFile, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            prices[row[0]] = float(row[1])
    '''productPolartiesFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties.txt"
    postivePolarity = dict()
    negativePolarity = dict()
    with open(productPolartiesFile, 'r') as fp:
        for line in fp:
            row = line.split("\t")
            if len(row)>3:
                postivePolarity[row[0]] = float(row[2])
                negativePolarity[row[0]] = float(row[3])
            else:
                print("problem with this line len "+str(len(row))+" "+str(row))
    '''

    with open(catFilePath, 'r') as fp:
        for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                featureList = []
                ratingTemproalCategory, ratingHelpfulnessCategory, n, average,numReviews,numFeedBackPerDayDictionary,numHelpFeedPerDayDictionary = analyzeProduct(productBaseDirectory,productId)
                periodDict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],}
                for i in range(len(ratingTemproalCategory)):
                    for item in ratingTemproalCategory[i]:
                        try:
                            record = periodDict[item]
                            record.append(ratingTemproalCategory[i][item])
                            periodDict[item] = record
                        except KeyError as e:
                            pass
                            # featureList.append(ratingTemproalCategory[i][item])
                five = 0
                avStart = 0
                sum = 0
                if featureSet == 1: #We'll add only the basic feature set
                    retValue = average
                    ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategory)
                    for key, value in ratings.items():
                        featureList.append(value)  # Feature Number of reviews with specific star rating
                    # Adding Polarity

                    AllPolarities = []
                    try:
                        AllPolarities = ProductPolaritiesPerRating[productId]
                    except KeyError:
                        print("failed to find Positive polarity to product " + productId)
                        pass
                    if len(AllPolarities) == 20:
                        # +ve Polarity for 5 ratings
                        featureList.append(int(AllPolarities[1]))
                        featureList.append(int(AllPolarities[5]))
                        featureList.append(int(AllPolarities[9]))
                        featureList.append(int(AllPolarities[13]))
                        featureList.append(int(AllPolarities[17]))
                        # -ve Polarity for 5 ratings
                        featureList.append(int(AllPolarities[2]))
                        featureList.append(int(AllPolarities[6]))
                        featureList.append(int(AllPolarities[10]))
                        featureList.append(int(AllPolarities[14]))
                        featureList.append(int(AllPolarities[18]))
                    '''
                    polarity = 0
                    try:
                        polarity = postivePolarity[productId]
                    except KeyError as e:
                        print("failed to find Positive polarity to product " + productId)
                        pass
                    featureList.append(polarity)  # Feature Product Positive Polarity
                    polarity = 0
                    try:
                        polarity = negativePolarity[productId]
                    except KeyError as e:
                        print("failed to find Negative polarity to product " + productId)
                        pass
                    featureList.append(polarity)  # Feature Product Negative Polarity
                    '''
                    numFeedBacks = []
                    for key, value in numFeedBackPerDayDictionary.items():
                        listofDays = value
                        numFeedBackPerRating = 0
                        for item in listofDays:
                            numFeedBackPerRating+=item[0]
                        numFeedBacks.append(numFeedBackPerRating)

                    numHelpFeedBacks = []
                    for key, value in numHelpFeedPerDayDictionary.items():
                        listofDays = value
                        numFeedBackPerRating = 0
                        for item in listofDays:
                            numFeedBackPerRating += item[0]
                        numHelpFeedBacks.append(numFeedBackPerRating)

                    numNonHelpFeedBacks = []
                    for i in range(len(numFeedBacks)):
                        numNonHelpFeedBacks.append(numFeedBacks[i]-numHelpFeedBacks[i])
                    #print(numFeedBacks)
                    #print(numNonHelpFeedBacks)
                    #print(numHelpFeedBacks)
                    for item in numHelpFeedBacks:      #Adding Helpful votes per star ratings
                        featureList.append(item)
                    for item in numNonHelpFeedBacks:  # Adding Non Helpful votes per star ratings
                        featureList.append(item)
                    if len(featureList) < 17:
                        print("Problem with features ")
                        print(numFeedBackPerDayDictionary)
                        print((numHelpFeedPerDayDictionary))

                    featureProduct[productId] = featureList
                    productList.append((productId, retValue))
                    X.append(featureList)
                    y.append(retValue)

                else:
                    for key, value in periodDict.items():
                        for item in value:
                            featureList.append(item)
                            avStart +=(item*(five+1))
                            sum+=item
                            five+=1
                        if sum > 0:
                            avStart = avStart / sum

                        #featureList.append(avStart)
                        avStart = 0
                        five = 0
                        sum = 0

                    n_features = len(featureList)
                    if n_features != 55:#features 55 from 5 star rating levels in 11 periods
                        print("not 55")
                        print(periodDict)
                        print(ratingTemproalCategory)
                        print(n_features)
                        print(featureList)
                    expoValue = 0
                    if option == 1:
                        prior = [2,2,2,2,2]
                        ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategory)
                        retValue = dirichlet_mean(ratings, prior)
                    elif option == 2:

                        productFileName = productBaseDirectory+productId+".txt"
                        expoValue = computeExponentialScore(productFileName, userExpert)
                        #print(featureList)

                    # will add dricilet and the exponential score as additional features
                    #--------------------------------------------------------------------------------------------------------------------
                    prior = [2, 2, 2, 2, 2]
                    retValue = 0
                    #ratings = aggregateRatingsForAllTimePeriods(ratingTemproalCategory)
                    #retValue = dirichlet_mean(ratings, prior)
                    featureList.append(numReviews)#Feature 56 Number of reviews
                    featureList.append(expoValue)#Feature 57 exp model
                    # --------------------------------------------------------------------------------------------------------------------
                    productPrice = 0
                    try:
                        productPrice = prices[productId]
                        if productPrice == -1:
                            productPrice = 0
                    except KeyError as e:
                        print("failed to find price to product "+productId)
                        pass
                    featureList.append(productPrice)# Feature 58 Product Price
                    #---------------------------------------------------------------------------------------------------------------------
                    #Adding Polarity
                    polarity = 0
                    try:
                        polarity = postivePolarity[productId]
                    except KeyError as e:
                        print("failed to find Positive polarity to product " + productId)
                        pass
                    featureList.append(polarity)  # Feature 59 Product Positive Polarity
                    polarity = 0
                    try:
                        polarity = negativePolarity[productId]
                    except KeyError as e:
                        print("failed to find Negative polarity to product " + productId)
                        pass
                    featureList.append(polarity)  # Feature 60 Product Negative Polarity
                    # ---------------------------------------------------------------------------------------------------------------------
                    productList.append((productId,retValue))
                    featureProduct[productId] = featureList
                    X.append(featureList)
                    y.append(retValue)
                index +=1
    return X,y,productList,featureProduct

from Testing import  divideReviewsByRatingLevelByTimePeriods

def buildFeatureListForCategoryForTimePeriods(catFilePath,productBaseDirectory,ProductPolaritiesPerRatingPerPeriod,dataset_type,timeperiods ):
    X = []  # list of samples each with list of features
    y = []  # contains the average as the expected value
    productList = []
    featureProduct = dict()
    index = 0
    with open(catFilePath, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            productId = row[0]
            productId = productId.split('\n')
            productId = productId[0]
            featureList = []
            productFilePath=productBaseDirectory+productId+".txt"
            polarties =  []
            try:
                polarties = ProductPolaritiesPerRatingPerPeriod[productId]
            except KeyError:
                print("didn't find polarites for "+str(productId))

            reviewRatingLevelTimeDict = divideReviewsByRatingLevelByTimePeriods(productFilePath, timeperiods,dataset_type)
            ratingLevelPerTimePeriod = dict()
            helpfulPerRatingPerTimePeriod = dict()
            nonHelpfulPerRatingPerTimePeriod = dict()

            for key, value in reviewRatingLevelTimeDict.items():
                ratingsDictionary = value
                ratingLevels = []
                helpful=[]
                nonhelpful = []
                for key2, value2 in ratingsDictionary.items():
                    if len(value2) !=0:
                        reviews = value2
                        ratingLevels.append(len(reviews))
                        numHelpful = 0
                        numNonHelpful = 0
                        for review in reviews:
                            if dataset_type=="amazon":
                                if review[3]!="" and review[4]!="":
                                    numFeedback = int(review[3])
                                    numHelpful+= int(review[4])
                                    nonhelpf=numFeedback-int(review[4])
                                    numNonHelpful+=nonhelpf
                                else:
                                    numFeedback = 0
                                    numHelpful += 0
                                    nonhelpf = numFeedback
                                    numNonHelpful += nonhelpf
                            elif dataset_type=="yelp":
                                votes = str(review[2]).split(',')
                                funny=int(votes[0].split(':')[1])
                                useful=int(votes[1].split(':')[1])
                                cool=int(votes[2].split(':')[1].split('}')[0])
                                numHelpful=useful+cool
                                numNonHelpful=funny

                        helpful.append(numHelpful)
                        nonhelpful.append(numNonHelpful)
                    else:
                        ratingLevels.append(0)
                        helpful.append(0)
                        nonhelpful.append(0)
                ratingLevelPerTimePeriod[key]=ratingLevels
                helpfulPerRatingPerTimePeriod[key] = helpful
                nonHelpfulPerRatingPerTimePeriod[key] = nonhelpful

            #Adding Num reviews per rating level per time period
            #print("Num reviews per rating")
            for key, value in ratingLevelPerTimePeriod.items():
                ratingLevels = value
                #print(ratingLevels)
                for numRatingsPerLevel in ratingLevels:
                    featureList.append(numRatingsPerLevel)
            #print(" Num helpful votes per rating")
            # Adding Num helpful votes per rating level per time period
            for key, value in helpfulPerRatingPerTimePeriod.items():
                ratingLevels = value
                #print(ratingLevels)
                for numRatingsPerLevel in ratingLevels:
                    featureList.append(numRatingsPerLevel)
            # Adding Num non helpful votes per rating level per time period
            #print(" Num non helpful votes per rating")
            for key, value in nonHelpfulPerRatingPerTimePeriod.items():
                ratingLevels = value
               # print(ratingLevels)
                for numRatingsPerLevel in ratingLevels:
                    featureList.append(numRatingsPerLevel)

            # Adding +ve and -ve polarities per rating level per time period
            if len(polarties) != (timeperiods*5*2):
                print("Missing polarities " + str(len(polarties)))
            for polarity in polarties:
                featureList.append(polarity)


            if len(featureList) !=(timeperiods*25):
                print("missing features "+str(len(featureList)))
            retValue = 0
            productList.append((productId, retValue))
            featureProduct[productId] = featureList
            X.append(featureList)
            y.append(retValue)
            index+=1
            print(index)

    return X,y,productList,featureProduct
def buildFeatureListForCategoryRetDict(catFilePath,productBaseDirectory):
    X = []  # list of samples each with list of features
    y = []  # Product IDs
    index = 0
    with open(catFilePath, 'r') as fp:
        for line in fp:
                row = line.split('\t')
                productId = row[0]
                productId = productId.split('\n')
                productId = productId[0]
                featureList = []
                ratingTemproalCategory, ratingHelpfulnessCategory, n, average = analyzeProduct(productBaseDirectory,productId)
                periodDict = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [],}
                for i in range(len(ratingTemproalCategory)):
                    for item in ratingTemproalCategory[i]:
                        try:
                            record = periodDict[item]
                            record.append(ratingTemproalCategory[i][item])
                            periodDict[item] = record
                        except KeyError as e:
                            pass
                            # featureList.append(ratingTemproalCategory[i][item])
                five = 0
                avStart = 0
                sum = 0
                for key, value in periodDict.items():
                    for item in value:
                        featureList.append(item)
                        avStart +=(item*(five+1))
                        sum+=item
                        five+=1
                    if sum > 0:
                        avStart = avStart / sum

                    #featureList.append(avStart)
                    avStart = 0
                    five = 0
                    sum = 0

                n_features = len(featureList)
                if n_features != 55:
                    print("not 55")
                    print(periodDict)
                    print(ratingTemproalCategory)
                    print(n_features)
                    print(featureList)


                X.append(featureList)
                y.append(productId)
                index +=1
    return X,y
import math

'''   for sorting sales rank
    sales_dict = []
    sales_rank = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_sales_rank/"+filename
    with open(sales_rank, 'r') as fp:
        for line in fp:
            row = line.split("\t")
            product = row[0]
            row = row[1].split("\n")
            salesrank = int(row[0])
            sales_dict.append((product,salesrank))

    onlyNeededList = []
    for item in (productList):
        for sale in sales_dict:
            if item[0]==sale[0]:
                onlyNeededList.append(sale)
                break

    quickSort(onlyNeededList)
    print(onlyNeededList)
    onlyNeededDict = dict()
    for item in (sales_dict):
        onlyNeededDict[item[0]]=item[1]

    '''
'''             Count number of products for certain dataset

directory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Sorted_Categories/categories_sorted_non_verified/categores_sorted_sales_rank_dataset_more_300/"
for filename in os.listdir(directory):
    path = directory + filename
    counter = 0

    with open(path, 'r') as fp:
        for line in fp:
            counter += 1

    # print("Considering "+filename +' '+str(counter))
    print(counter)
'''
def writeTrainingFileForJavaLib(X,y,categoryId,FilePath,normalize):
    ''' File Format
    <line> .=. <relevance> qid:<qid> <feature>:<value> ... <feature>:<value>
    <relevance> .=. <integer>
    <qid> .=. <positive integer>
    <feature> .=. <positive integer>
    <value> .=. <float>'''

    maxFeatureValues = []
    minFeatureValues = []
    #print("len(X[0]")
    #print(len(X[0]))
    for i in range(len(X[0])):
        maxFeatureValues.append(-1000)
        minFeatureValues.append(10000000)
    #print("maxFeatureValues")
    #print(len(maxFeatureValues))
    #print(maxFeatureValues)
    #Normalizing Features between 0 and 1
    for i in range(len(y)):
        features = X[i]
        for j in range(len(features)):
            if j < len(maxFeatureValues) and j <len(minFeatureValues):
                if int(features[j]) > maxFeatureValues[j]:
                    maxFeatureValues[j] = int(features[j])
                if int(features[j]) < minFeatureValues[j]:
                    minFeatureValues[j] = int(features[j])

    filehandle = open(FilePath, 'a')
    for i in range(len(y)):
        filehandle.write(str(int(y[i])))
        filehandle.write(' ')
        filehandle.write("qid:")
        filehandle.write(str(categoryId))
        filehandle.write(' ')
        features = X[i]
        for j in range(len(features)):
            filehandle.write(str(j+1))
            filehandle.write(":")
            if normalize == 1:
                if j < len(maxFeatureValues) and j < len(minFeatureValues):
                    if(maxFeatureValues[j]-minFeatureValues[j])>0:
                        #filehandle.write(str(float((features[j]))))#(str(float((features[j]-minFeatureValues[j])/(maxFeatureValues[j]-minFeatureValues[j]))))
                        filehandle.write((str(float((features[j] - minFeatureValues[j]) / (maxFeatureValues[j] - minFeatureValues[j])))))
                    else:
                        filehandle.write("0")
                else:
                    filehandle.write("0")

            else:
                filehandle.write(str(float(features[j])))

            #filehandle.write(str(features[j]))
            if j !=len(features)-1:
                filehandle.write(' ')
        filehandle.write("\n")
    return
def writingFromOneFile(sourceFilePath, FilePath):
    filehandle = open(FilePath, 'a')
    with open(sourceFilePath, 'r') as fp:
        for line in fp:
            filehandle.write(line)
    filehandle.close()
    return
def writeTrainingFileForPythonLib(X,y,categoryId,FilePath):
    ''' File Format
        <line> .=. <relevance>,<qid>, blank ,<feature>:<value>
        <relevance> .=. <integer>
        <qid> .=. <positive integer>
        <feature> .=. <positive integer>
        <value> .=. <float>'''

    filehandle = open(FilePath, 'a')
    for i in range(len(y)):
        filehandle.write(str(int(y[i])))
        filehandle.write(' ,')
        filehandle.write(str(categoryId))
        filehandle.write(',0,')
        features = X[i]
        for j in range(len(features)):
            filehandle.write(str(float(features[j])))
            if j != len(features) - 1:
                filehandle.write(' ,')
        filehandle.write("\n")
    return
def prepareTrainingTestingSetSVM(categories_path,productBaseDirectory,training_Set,testing_Set,validating_Set,for_lib,setFilePath):
    counter = 0
    for filename in os.listdir(categories_path):
        catFilePath = categories_path + filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        start = 0

        for cat in training_Set:
            if cat == categoryName:
                start = 1
                print("Training set for " + for_lib)
                FilePath = setFilePath+"train.txt"
                break
        for cat in testing_Set:
            if cat == categoryName:
                start = 1
                print("Testing set for " + for_lib)
                FilePath = setFilePath + "test.txt"
                break
        for cat in validating_Set:
            if cat == categoryName:
                start = 1
                print("Validating set for "+for_lib)
                FilePath = setFilePath + "valid.txt"
                break
        if start == 1:
            print("Starting " + categoryName)
            X = []  # list of samples each with list of features
            y = []  # contains the average as the expected value
            option = 2
            print("collecting features...............................................................")
            label = []
            with open(catFilePath, 'r') as fp:
                for line in fp:
                    row = line.split("\t")
                    label.append(row[1].split("\n")[0])
            X, y, productList, featureProduct = buildFeatureListForCategoryForGeneral(catFilePath, productBaseDirectory,category, 2)  # buildFeatureListForCategory(catFilePath,productBaseDirectory)
            XNew = []
            y = []
            yTemp = []
            for item in (productList):
                # y.append([item[1]])
                XNew.append(featureProduct[item[0]])
            X = np.array(XNew)
            y = label
            # yTemp = label
            tempList = []
            for item in label:
                tempList.append((item, int(item)))
                yTemp.append(int(item))

            mergeSort(tempList)

            newTempList = dict()
            index = 1
            for item in tempList:
                newTempList[(item[0])] = len(tempList) - index
                index += 1

            index = 0
            for item in range(len(yTemp)):
                val = newTempList[str(yTemp[index])]
                yTemp[index] = val
                index += 1

            # Transform the label to numbers from 0 to n where n is the best rank
            y = yTemp
            y = np.array(y)
            n_samples = len(y)
            y = np.ravel(y)
            # if n_samples > 50:
            # print("Finsished Collecting Products Data")
            # modelSavePath = 'C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Learning_Models/GThan100/LassRegression/'+categoryName+'.pkl'

            print("Writing..............................................................................")
            writeTrainingFileForJavaLib(X, y, counter, FilePath,normalize)

            # writeTrainingFileForPythonLib(X,y,counter,FilePath)
            # trainLen, testLen,tau = rankingAlgorithm3(X, y,n_samples,modelSavePath)
            # Sampels Train Test Tau
            # print("Considered "+categoryName+' '+str(n_samples)+' '+str(trainLen)+' '+str(testLen)+' '+str(tau))
            counter += 1
    return
def prepareTrainingTestingForAll(categories_path,sourceFeaturesDirectory,training_Set,testing_Set,validating_Set,for_lib,setFilePath):

    categoryFileDict = dict()
    for filename in os.listdir(sourceFeaturesDirectory):
        catFilePath = sourceFeaturesDirectory + filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        categoryFileDict[categoryName] = catFilePath
    counter = 0
    for filename in os.listdir(categories_path):
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]
        start = 0

        for cat in training_Set:
            if cat == categoryName:
                start = 1
                print("Training set for " + for_lib)
                FilePath = setFilePath+"train.txt"
                break
        for cat in testing_Set:
            if cat == categoryName:
                start = 1
                print("Testing set for " + for_lib)
                FilePath = setFilePath + "test.txt"
                break
        for cat in validating_Set:
            if cat == categoryName:
                start = 1
                print("Validating set for "+for_lib)
                FilePath = setFilePath + "valid.txt"
                break
        if start == 1:
            print("Fetching " + categoryName)
            sourceFilePath = categoryFileDict[categoryName]
            print("Writing..............................................................................")
            writingFromOneFile(sourceFilePath, FilePath)
            print("Done..............................................................................")
            counter += 1
    return
def prepareTrainingTestingDataForAllCategories(startFromCat,categories_path,productBaseDirectory,destFilePath,normalize,featureSet):
    counter = 0
    print("Preparing Features Data For All Categories")
    ProductPolaritiesPerRating = readSentencePolaritiesPerRating()
    start = 0
    for filename in os.listdir(categories_path):
        catFilePath = categories_path + filename
        category = filename
        categoryName = category.split(".txt")
        categoryName = categoryName[0]

        if startFromCat == categoryName:
            start = 1
        FilePath = destFilePath + category

        print("Starting " + categoryName)
        if start == 1:
            X = []  # list of samples each with list of features
            y = []  # contains the average as the expected value
            option = 2
            print("collecting features...............................................................")
            label = []
            with open(catFilePath, 'r') as fp:
                for line in fp:
                    row = line.split("\t")
                    label.append(row[1].split("\n")[0])

            X, y, productList, featureProduct = buildFeatureListForCategoryForGeneral(catFilePath, productBaseDirectory,category, 2,featureSet,ProductPolaritiesPerRating)  # buildFeatureListForCategory(catFilePath,productBaseDirectory)
            XNew = []
            y = []
            yTemp = []
            for item in (productList):
                # y.append([item[1]])
                XNew.append(featureProduct[item[0]])
            X = np.array(XNew)
            y = label
            # yTemp = label
            tempList = []
            for item in label:
                tempList.append((item, int(item)))
                yTemp.append(int(item))

            mergeSort(tempList)

            newTempList = dict()
            index = 1
            for item in tempList:
                newTempList[(item[0])] = len(tempList) - index
                index += 1

            index = 0
            for item in range(len(yTemp)):
                val = newTempList[str(yTemp[index])]
                yTemp[index] = val
                index += 1

            # Transform the label to numbers from 0 to n where n is the best rank
            y = yTemp
            y = np.array(y)
            print("Writing..............................................................................")
            writeTrainingFileForJavaLib(X, y, counter, FilePath,normalize)
            print("Finished..............................................................................")
        counter += 1
    return

def prepareTrainingTestingDataForAllCategoriesL2R(categoriesList,categorybaseDirectory,productBaseDirectory,destFilePath,normalize,productPolartiesFile,dataset_type,timeperiods):
    counter = 0
    print("Preparing Features Data For All Categories L2R for "+dataset_type+" "+str(timeperiods)+" periods")
    ProductPolaritiesPerRatingPerPeriod = readSentencePolaritiesPerRatingPerPeriod(productPolartiesFile,timeperiods)
    start = 0
    for categoryName in categoriesList:
        catFilePath = categorybaseDirectory + categoryName+".txt"
        print("Considering " + categoryName)

        X = []  # list of samples each with list of features
        y = []  # contains the average as the expected value
        option = 2
        print("collecting features...............................................................")
        label = []
        with open(catFilePath, 'r') as fp:#adding the label in case of Amazon its the sales rank in case of yelp its dirichlet
            for line in fp:
                row = line.split("\t")
                if dataset_type == "amazon":
                    label.append(row[1].split("\n")[0])
                elif dataset_type=="yelp":
                    label.append(row[2].split("\n")[0])

        X, y, productList, featureProduct = buildFeatureListForCategoryForTimePeriods(catFilePath, productBaseDirectory,ProductPolaritiesPerRatingPerPeriod,dataset_type,timeperiods)
        XNew = []
        y = []
        yTemp = []
        for item in (productList):
            # y.append([item[1]])
            XNew.append(featureProduct[item[0]])
        X = np.array(XNew)
        y = label

        # yTemp = label
        tempList = []
        for item in label:
            if dataset_type=="amazon":
                tempList.append((item, int(item)))
                yTemp.append(int(item))
            elif dataset_type=="yelp":
                tempList.append((item, float(item)))
                yTemp.append(float(item))

        mergeSort(tempList)
        if dataset_type=="yelp":
          tempList.reverse()

        newTempList = dict()
        index = 1
        for item in tempList:
            newTempList[(item[0])] = len(tempList) - index
            index += 1

        index = 0
        for item in range(len(yTemp)):
            val = newTempList[str(yTemp[index])]
            yTemp[index] = val
            index += 1

        # Transform the label to numbers from 0 to n where n is the best rank
        y = yTemp
        y = np.array(y)
        FilePath = destFilePath + categoryName+".txt"
        print("Writing..............................................................................")
        writeTrainingFileForJavaLib(X, y, counter, FilePath,normalize)
        print("Finished..............................................................................")
        counter += 1
    return

def preparefirstEightSetsForSVM():
    AllTrainingSets = []
    AllTestingSets = []
    # ------------------------------------------------------------------------------------------
    # set1
    training_Set = ["Appliances",
                    "Gift",
                    "Cards",
                    "Store",
                    "Automotive",
                    "Baby",
                    "Home",
                    "Improvement",
                    "Magazines",
                    "Office",
                    "Products",
                    "Prime",
                    "Pantry",
                    "Computers & Accessories",
                    "Industrial & Scientific",
                    "Software"]
    testing_Set = ["Camera &amp; Photo",
                   "Arts, Crafts & Sewing",
                   "Watches",
                   "Jewelry",
                   "Electronics",
                   "Patio, Lawn & Garden",
                   "Pet Supplies",
                   "Video Games",
                   "Grocery & Gourmet Food",
                   "Shoes",
                   "Home &amp; Kitchen"]
    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set2
    training_Set = ["Camera &amp; Photo",
                    "Arts, Crafts & Sewing",
                    "Watches",
                    "Jewelry",
                    "Electronics",
                    "Patio, Lawn & Garden",
                    "Pet Supplies",
                    "Video Games",
                    "Grocery & Gourmet Food",
                    "Shoes",
                    "Home &amp; Kitchen"]
    testing_Set = ["Appliances",
                   "Gift",
                   "Cards",
                   "Store",
                   "Automotive",
                   "Baby",
                   "Home",
                   "Improvement",
                   "Magazines",
                   "Office",
                   "Products",
                   "Prime",
                   "Pantry",
                   "Computers & Accessories",
                   "Industrial & Scientific",
                   "Software"]
    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set3
    training_Set = ["Camera &amp; Photo",
                    "Arts, Crafts & Sewing",
                    "Watches",
                    "Jewelry",
                    "Electronics",
                    "Patio, Lawn & Garden",
                    "Pet Supplies",
                    "Video Games",
                    "Grocery & Gourmet Food",
                    "Shoes",
                    "Home &amp; Kitchen"]

    testing_Set = ["Beauty",
                   "Clothing",
                   "Kitchen & Dining",
                   "Toys & Games",
                   "Cell Phones & Accessories",
                   "Sports &amp; Outdoors",
                   "Health & Personal Care",
                   "Musical Instruments",
                   "Music",
                   "Movies & TV",
                   "Books"]
    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set4

    training_Set = ["Beauty",
                    "Clothing",
                    "Kitchen & Dining",
                    "Toys & Games",
                    "Cell Phones & Accessories",
                    "Sports &amp; Outdoors",
                    "Health & Personal Care",
                    "Musical Instruments",
                    "Music",
                    "Movies & TV",
                    "Books"]
    testing_Set = ["Camera &amp; Photo",
                   "Arts, Crafts & Sewing",
                   "Watches",
                   "Jewelry",
                   "Electronics",
                   "Patio, Lawn & Garden",
                   "Pet Supplies",
                   "Video Games",
                   "Grocery & Gourmet Food",
                   "Shoes",
                   "Home &amp; Kitchen"]

    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set5
    training_Set = ["Appliances",
                    "Gift Cards Store",
                    "Automotive",
                    "Baby",
                    "Home Improvement",
                    "Magazines",
                    "Office Products",
                    "Prime Pantry",
                    "Computers & Accessories",
                    "Industrial & Scientific",
                    "Software",
                    "Camera & amp; Photo",
                    "Arts, Crafts & Sewing",
                    "Watches",
                    "Jewelry",
                    "Electronics",
                    "Patio, Lawn & Garden"]

    testing_Set = ["Pet Supplies",
                   "Video Games",
                   "Grocery & Gourmet Food",
                   "Shoes",
                   "Home & amp; Kitchen",
                   "Beauty",
                   "Clothing",
                   "Kitchen & Dining",
                   "Toys & Games",
                   "Cell Phones & Accessories",
                   "Sports & amp; Outdoors",
                   "Health & Personal Care",
                   "Musical Instruments",
                   "Music",
                   "Movies & TV",
                   "Books"]

    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set6
    training_Set = ["Pet Supplies",
                    "Video Games",
                    "Grocery & Gourmet Food",
                    "Shoes",
                    "Home & amp; Kitchen",
                    "Beauty",
                    "Clothing",
                    "Kitchen & Dining",
                    "Toys & Games",
                    "Cell Phones & Accessories",
                    "Sports & amp; Outdoors",
                    "Health & Personal Care",
                    "Musical Instruments",
                    "Music",
                    "Movies & TV",
                    "Books"]
    testing_Set = ["Appliances",
                   "Gift Cards Store",
                   "Automotive",
                   "Baby",
                   "Home Improvement",
                   "Magazines",
                   "Office Products",
                   "Prime Pantry",
                   "Computers & Accessories",
                   "Industrial & Scientific",
                   "Software",
                   "Camera & amp; Photo",
                   "Arts, Crafts & Sewing",
                   "Watches",
                   "Jewelry",
                   "Electronics",
                   "Patio, Lawn & Garden"]

    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set7
    training_Set = ["Appliances",
                    "Gift Cards Store",
                    "Automotive",
                    "Office Products",
                    "Prime Pantry",
                    "Computers & Accessories",
                    "Camera & amp; Photo",
                    "Arts, Crafts & Sewing",
                    "Watches",
                    "Jewelry",
                    "Beauty",
                    "Clothing",
                    "Kitchen & Dining",
                    "Toys & Games",
                    "Shoes",
                    "Home & amp; Kitchen",
                    "Music"]

    testing_Set = ["Baby",
                   "Home Improvement",
                   "Magazines",
                   "Industrial & Scientific",
                   "Software",
                   "Electronics",
                   "Patio, Lawn & Garden",
                   "Pet Supplies",
                   "Video Games",
                   "Grocery & Gourmet Food",
                   "Cell Phones & Accessories",
                   "Sports & amp; Outdoors",
                   "Health & Personal Care",
                   "Musical Instruments",
                   "Movies & TV",
                   "Books"]

    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    # ------------------------------------------------------------------------------------------
    # set8
    training_Set = ["Baby",
                    "Home Improvement",
                    "Magazines",
                    "Industrial & Scientific",
                    "Software",
                    "Electronics",
                    "Patio, Lawn & Garden",
                    "Pet Supplies",
                    "Video Games",
                    "Grocery & Gourmet Food",
                    "Cell Phones & Accessories",
                    "Sports & amp; Outdoors",
                    "Health & Personal Care",
                    "Musical Instruments",
                    "Movies & TV",
                    "Books"]

    testing_Set = ["Appliances", "Gift Cards Store", "Automotive", "Office Products", "Prime Pantry",
                   "Computers & Accessories", "Camera & amp; Photo", "Arts, Crafts & Sewing", "Watches", "Jewelry",
                   "Beauty", "Clothing", "Kitchen & Dining", "Toys & Games", "Shoes", "Home & amp; Kitchen", "Music"]

    AllTrainingSets.append(training_Set)
    AllTestingSets.append(testing_Set)
    return AllTrainingSets,AllTestingSets

def prepareKFoldForSVM():
    AllTrainingSets = []
    AllTestingSets = []
    #Fold 1
    training = ['Automotive', 'Baby', 'Home Improvement', 'Music', 'Office Products', 'Computers & Accessories','Industrial & Scientific', 'Software', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Health & Personal Care','Jewelry', 'Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Grocery & Gourmet Food', 'Shoes','Home &amp; Kitchen', 'Beauty', 'Clothing', 'Kitchen & Dining', 'Toys & Games', 'Cell Phones & Accessories']
    testing = ['Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Magazines', 'Watches']
    AllTrainingSets.append(training)
    AllTestingSets.append(testing)
    # Fold 2
    training = ['Automotive', 'Baby', 'Home Improvement', 'Music', 'Office Products', 'Computers & Accessories', 'Industrial & Scientific', 'Software', 'Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Magazines', 'Watches', 'Pet Supplies', 'Video Games', 'Grocery & Gourmet Food', 'Camera &amp; Photo', 'Home &amp; Kitchen', 'Beauty', 'Clothing', 'Kitchen & Dining', 'Toys & Games', 'Cell Phones & Accessories']
    testing = ['Arts, Crafts & Sewing', 'Health & Personal Care', 'Jewelry', 'Electronics', 'Patio, Lawn & Garden', 'Shoes']
    AllTrainingSets.append(training)
    AllTestingSets.append(testing)
    # Fold 3
    training = ['Automotive', 'Baby', 'Home Improvement', 'Music', 'Office Products', 'Computers & Accessories', 'Industrial & Scientific', 'Software', 'Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Magazines', 'Arts, Crafts & Sewing', 'Health & Personal Care', 'Jewelry', 'Electronics', 'Patio, Lawn & Garden', 'Shoes', 'Clothing', 'Kitchen & Dining', 'Watches', 'Cell Phones & Accessories', 'Beauty']
    testing = ['Toys & Games', 'Pet Supplies', 'Video Games', 'Grocery & Gourmet Food', 'Camera &amp; Photo', 'Home &amp; Kitchen']
    AllTrainingSets.append(training)
    AllTestingSets.append(testing)
    # Fold 4
    training = ['Pet Supplies', 'Arts, Crafts & Sewing', 'Baby', 'Books', 'Camera &amp; Photo', 'Cell Phones & Accessories', 'Computers & Accessories', 'Electronics', 'Grocery & Gourmet Food', 'Health & Personal Care', 'Home &amp; Kitchen', 'Home Improvement', 'Industrial & Scientific', 'Jewelry', 'Kitchen & Dining', 'Magazines', 'Movies & TV', 'Musical Instruments', 'Patio, Lawn & Garden', 'Shoes', 'Sports &amp; Outdoors', 'Toys & Games', 'Video Games', 'Watches']
    testing = ['Office Products', 'Automotive', 'Beauty', 'Clothing', 'Music', 'Software']
    AllTrainingSets.append(training)
    AllTestingSets.append(testing)
    # Fold 5
    training = ['Pet Supplies', 'Beauty', 'Software', 'Camera &amp; Photo', 'Toys & Games', 'Clothing', 'Music', 'Grocery & Gourmet Food', 'Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Magazines', 'Arts, Crafts & Sewing', 'Health & Personal Care', 'Jewelry', 'Electronics', 'Patio, Lawn & Garden', 'Shoes', 'Home &amp; Kitchen', 'Automotive', 'Watches', 'Office Products', 'Video Games']
    testing = ['Computers & Accessories', 'Industrial & Scientific', 'Baby', 'Kitchen & Dining', 'Home Improvement', 'Cell Phones & Accessories']
    AllTrainingSets.append(training)
    AllTestingSets.append(testing)

    return AllTrainingSets, AllTestingSets
def prepareKFoldForLamdaMart():
    AllTrainingSets = []
    AllValidatingSets = []
    AllTestingSets = []
    print("Preparing 5Folds for Lamdamart")
    # Fold 1
    training = ['Appliances', 'Gift Cards Store', 'Automotive', 'Baby', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Watches', 'Jewelry', 'Beauty', 'Clothing', 'Kitchen & Dining']
    validating = ['Home Improvement', 'Magazines', 'Office Products', 'Prime Pantry', 'Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Cell Phones & Accessories', 'Sports &amp; Outdoors', 'Musical Instruments']
    testing = ['Computers & Accessories', 'Industrial & Scientific', 'Software', 'Grocery & Gourmet Food', 'Shoes', 'Home &amp; Kitchen', 'Music', 'Movies & TV', 'Books', 'Toys & Games', 'Health & Personal Care']
    AllTrainingSets.append(training)
    AllValidatingSets.append(validating)
    AllTestingSets.append(testing)
    # Fold 2
    training = ['Home Improvement', 'Magazines', 'Office Products', 'Prime Pantry', 'Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Cell Phones & Accessories', 'Sports &amp; Outdoors', 'Musical Instruments']
    validating = ['Computers & Accessories', 'Industrial & Scientific', 'Software', 'Grocery & Gourmet Food', 'Shoes', 'Home &amp; Kitchen', 'Music', 'Movies & TV', 'Books', 'Toys & Games', 'Health & Personal Care']
    testing = ['Appliances', 'Gift Cards Store', 'Automotive', 'Baby', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Watches', 'Jewelry', 'Beauty', 'Clothing', 'Kitchen & Dining']
    AllTrainingSets.append(training)
    AllValidatingSets.append(validating)
    AllTestingSets.append(testing)
    # Fold 3
    training =['Appliances', 'Gift Cards Store', 'Automotive', 'Baby', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Watches', 'Jewelry', 'Beauty', 'Clothing', 'Kitchen & Dining']
    validating = ['Computers & Accessories', 'Industrial & Scientific', 'Software', 'Grocery & Gourmet Food', 'Shoes', 'Home &amp; Kitchen', 'Music', 'Movies & TV', 'Books', 'Toys & Games', 'Health & Personal Care']
    testing = ['Home Improvement', 'Magazines', 'Office Products', 'Prime Pantry', 'Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Cell Phones & Accessories', 'Sports &amp; Outdoors', 'Musical Instruments']
    AllTrainingSets.append(training)
    AllValidatingSets.append(validating)
    AllTestingSets.append(testing)
    # Fold 4
    training = ['Home Improvement', 'Magazines', 'Office Products', 'Prime Pantry', 'Computers & Accessories', 'Industrial & Scientific', 'Software', 'Appliances', 'Gift Cards Store', 'Automotive', 'Baby']
    validating = ['Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Shoes', 'Home &amp; Kitchen', 'Music', 'Movies & TV', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Watches']
    testing = ['Cell Phones & Accessories', 'Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Toys & Games', 'Health & Personal Care', 'Jewelry', 'Beauty', 'Clothing', 'Kitchen & Dining']
    AllTrainingSets.append(training)
    AllValidatingSets.append(validating)
    AllTestingSets.append(testing)
    # Fold 5
    training = ['Cell Phones & Accessories', 'Sports &amp; Outdoors', 'Musical Instruments', 'Movies & TV', 'Books', 'Toys & Games', 'Health & Personal Care', 'Jewelry', 'Beauty', 'Clothing', 'Kitchen & Dining']
    validating = ['Home Improvement', 'Magazines', 'Office Products', 'Prime Pantry', 'Computers & Accessories', 'Industrial & Scientific', 'Software', 'Appliances', 'Gift Cards Store', 'Automotive', 'Baby']
    testing = ['Electronics', 'Patio, Lawn & Garden', 'Pet Supplies', 'Video Games', 'Shoes', 'Home &amp; Kitchen', 'Music', 'Movies & TV', 'Camera &amp; Photo', 'Arts, Crafts & Sewing', 'Watches']
    AllTrainingSets.append(training)
    AllValidatingSets.append(validating)
    AllTestingSets.append(testing)
    return AllTrainingSets,AllValidatingSets, AllTestingSets

def relableOneSet(oneSet):
    newLabledSet = []
    tempList = []
    yTemp = []
    for record in oneSet:
        tempRecord = str(record)
        tempRecord = tempRecord.split(" ")
        #print(tempRecord[0])
        tempList.append((tempRecord[0], int(tempRecord[0])))
        yTemp.append(int(tempRecord[0]))

    mergeSort(tempList)

    newTempList = dict()
    index = 0
    for item in tempList:
       newTempList[(item[0])] =  index
       index += 1

    index = 0
    for item in range(len(yTemp)):
       val = newTempList[str(yTemp[index])]
       yTemp[index] = val
       index+=1

    index = 0
    #print("New Set After relabel")
    for record in oneSet:
        tempRecord = str(record)
        tempRecord = tempRecord.split(" ")
        val = yTemp[index]#newTempList[tempRecord[0]]
        newLine = ""
        newLine+=str(val)+" "
        for i in range(1,len(tempRecord)):
            if i == len(tempRecord)-1:
                newLine += tempRecord[i]
            else:
                newLine+=tempRecord[i]+" "
        newLabledSet.append(newLine)
        index+=1

    return newLabledSet
def relabelSets(originalSet):
    previousSet = ""
    oneSet = []
    relabledSet = []
    numSets = 0
    newSet = []
    for record in originalSet:
        tempRecord = str(record)
        tempRecord = tempRecord.split(" ")
        if previousSet!=tempRecord[1]:
            previousSet = tempRecord[1]
            newSet = []
            if len(oneSet)>0:
                newSet = relableOneSet(oneSet)
                relabledSet.append(newSet)
                numSets+=1
                oneSet = []
                oneSet.append(record)
            else:
                oneSet.append(record)
        else :
            oneSet.append(record)

    if len(oneSet) > 0:
        newSet = relableOneSet(oneSet)
        relabledSet.append(newSet)
        numSets += 1

    return relabledSet
def prepareTraininTestingFromOneCategory(categoryPath,destDirectory,threshold,lamda,oneTesting,train_percent):
    counter = 0
    patch = 0
    records = []
    patches = []
    print(categoryPath)
    patches.append("qid:0")
    numRecords = 0
    with open(categoryPath, 'r') as fp:
        for line in fp:
            if counter%threshold == 0 and counter!=0:
                patch+=1
                temp = "qid:" + str(patch)
                patches.append(temp)
                numRecords = 0
            row = line.split(" ")
            newLine = row[0] + " "
            newLine += "qid:" + str(patch) + " "
            for i in range(2, len(row)):
                if i == len(row) - 1:
                    newLine += row[i]
                else:
                    newLine += row[i] + " "
            counter += 1
            records.append(newLine)
            numRecords += 1

    numPatches = patch + 1

    #Fixing batches with less number of items adding ti to the last one
    if numRecords<threshold:
        print("num records for "+str(patch)+" is "+str(numRecords)+" so we're adjusting")
        del patches[-1]
        index = len(records)-numRecords
        numPatches -= 1
        for i in range(numRecords):
            record = str(records[index])
            record = record.split(" ")
            newrecord = record[0]+" "+"qid:"+str(numPatches-1)+" "
            for i in range(2, len(record)):
                if i == len(row) - 1:
                    newrecord += row[i]
                else:
                    newrecord += row[i] + " "

            records[index] = newrecord
            index+=1

    #print(patches)
    try:
        os.stat(destDirectory)
    except:
        os.mkdir(destDirectory)


    numTraining = int(train_percent*numPatches)#(int)(numPatches / 5) * 4
    numTesting = numPatches - numTraining
    print("numPatches "+str(numPatches))
    print("numTraining "+str(numTraining))
    print("numTesting " + str(numTesting))
    index = 0
    #Forming batches
    allBatches = []
    oneBatch = []
    for batch in patches:
        if index%numTesting==0 and index!=0:
            allBatches.append(oneBatch)
            oneBatch = []
            oneBatch.append(batch)
        else:
            oneBatch.append(batch)
        index+=1

    if len(oneBatch)>0:
        allBatches.append(oneBatch)

    size = len(allBatches)

    '''if len(allBatches[size-1])<len(allBatches[size-2]):
        lastbatch = allBatches[size-1]
        oneBefore = list(allBatches[size-2])
        for item in lastbatch:
            oneBefore.append(item)
        allBatches[size - 2] =  oneBefore
        del allBatches[-1]'''

    print("All Possible combinations "+str(len(allBatches)))
    allTraining = []
    allTesting = []
    index = 0
    for batch in allBatches:
        allTesting.append(batch)
        innerIndex = 0
        training = []
        for another in allBatches:
            if index == innerIndex:
                innerIndex += 1
                continue
            else:
                training.append(another)
            innerIndex+=1
        allTraining.append(training)
        index+=1

    combinedTestingOneQuery = []
    #Combining Testing Query set for case of one instance testing
    size = len(allTesting)
    if oneTesting == 1:
        for i in range(size):
            oneTestingDict = dict()
            TestingBatch = allTesting[i]
            for item in TestingBatch:
                oneTestingDict[item]=TestingBatch[0]
            combinedTestingOneQuery.append(oneTestingDict)
        OneQueryAllTestingRecords = []
        for comb in combinedTestingOneQuery:
            productsForQuery = []
            for key, value in comb.items():
                for record in records:
                    lineTemp = str(record)
                    lineTemp = lineTemp.split(" ")
                    if lineTemp[1] == key:
                        newProductLine = lineTemp[0]
                        newProductLine+=" "
                        newProductLine += value+" "
                        for i in range(2, len(lineTemp)):
                            if i == len(lineTemp) - 1:
                                newProductLine += lineTemp[i]
                            else:
                                newProductLine += lineTemp[i] + " "
                        productsForQuery.append(newProductLine)

            newTestingRecords = relabelSets(productsForQuery)
            OneQueryAllTestingRecords.append(newTestingRecords)

    originalRanking = destDirectory+"original_ranking.txt"
    originalRankingHandle = open(originalRanking, 'w')
    for line in records:
        originalRankingHandle.write(line)
    originalRankingHandle.close()

    newRecords = relabelSets(records)


    for i in range(size):
        newDirectory = destDirectory+"Set_"+str(i+1)+"/"
        try:
            os.stat(newDirectory)
        except:
            os.mkdir(newDirectory)

        testFilePath = newDirectory + "test.txt"
        filehandleTesting = open(testFilePath, 'w')
        trainFilePath = newDirectory + "train.txt"
        filehandleTraining = open(trainFilePath, 'w')
        if lamda ==1:
            validFilePath = newDirectory + "valid.txt"
            filehandleValid = open(validFilePath, 'w')
        index = 0
        #relabel for each set to be from 0 to n
        if oneTesting == 1:
            TestingSet = OneQueryAllTestingRecords[i]
            for item in TestingSet:
               for it in item:
                   filehandleTesting.write(it)
        num_valid = int(numTraining*0.3)
        num_train = numTraining-num_valid
        training_index = 0
        for set in newRecords:
            counter = 0
            is_test = 0
            for line in set:
                lineTemp = str(line)
                lineTemp = lineTemp.split(" ")
                if lineTemp[1] in allTesting[i]:
                    if oneTesting==0:
                        filehandleTesting.write(line)
                        is_test = 1

                else:
                    is_test = 0
                    if training_index<num_train or lamda!=1:
                        filehandleTraining.write(line)
                    else:
                        if lamda == 1:
                            filehandleValid.write(line)

                index += 1
                counter+=1
            if is_test == 0:
                training_index += 1
            #print("This set contains "+str(counter) +" records")

        filehandleTesting.close()
        filehandleTraining.close()
        if lamda == 1:
            filehandleValid.close()


    print("Done writing "+str(index)+" records for "+category)
    return
def prepareTraininTestingFromOneCategory_with_specificTesting(categoryPath,destDirectory,threshold,lamda,oneTesting,train_percent,Categories_Indices_for_testing,category_name,Categories_For_testing_learning_with_greater_100,original_categories_path):
    counter = 0
    patch = 0
    #records = []
    patches = []
    print(categoryPath)
    patches.append("qid:0")
    numRecords = 0
    testing_indices=[]
    indices_file_path=Categories_Indices_for_testing+category_name+".txt"
    with open(indices_file_path, 'r') as fp:
        for line in fp:
            testing_indices.append(int(line))
    num_testing_must_be_used = int(len(testing_indices)/threshold)
    print("Num with gt 100 is "+str(num_testing_must_be_used))
    current_index = 0
    num_products = 0
    with open(categoryPath, 'r') as fp:
        for line in fp:
            num_products+=1
    numPatches=int(num_products/threshold)
    print("num_products "+str(num_products))
    print("Num patches "+str(numPatches))

    numTraining = int(train_percent * numPatches)  # (int)(numPatches / 5) * 4
    numTesting = numPatches - numTraining

    print("numTraining "+str(numTraining))
    print("numTesting " + str(numTesting))
    num_products_to_include = 0
    if numTesting>num_testing_must_be_used:
        num_products_to_include=(numTesting-num_testing_must_be_used)*threshold
    print("len testing_indices "+str(len(testing_indices)))
    training_set = []
    testing_set=[]
    with open(categoryPath, 'r') as fp:
        for line in fp:
            if current_index in testing_indices or num_products_to_include!=0:
                if counter % threshold == 0 and counter != 0:
                    patch += 1
                    temp = "qid:" + str(patch)
                    patches.append(temp)
                    numRecords = 0
                row = line.split(" ")
                newLine = row[0] + " "
                newLine += "qid:" + str(patch) + " "
                for i in range(2, len(row)):
                    if i == len(row) - 1:
                        newLine += row[i]
                    else:
                        newLine += row[i] + " "
                counter += 1
                testing_set.append(newLine)
                numRecords += 1
                if current_index not in testing_indices:
                    num_products_to_include-=1
                    testing_indices.append(current_index)
            current_index+=1

    print("len testing_indices " + str(len(testing_indices)))

    patch+=3
    training_set = []
    current_index=0
    patches = []
    patches.append("qid:"+str(patch))
    indices_of_testing_file_path = Categories_For_testing_learning_with_greater_100 + category_name + ".txt"
    filehandle = open(indices_of_testing_file_path, 'w')
    counter=0
    with open(categoryPath, 'r') as fp:
        for line in fp:
            if current_index not in testing_indices :
                if counter % threshold == 0 and counter != 0:
                    patch += 1
                    temp = "qid:" + str(patch)
                    patches.append(temp)
                    numRecords = 0
                row = line.split(" ")
                newLine = row[0] + " "
                newLine += "qid:" + str(patch) + " "
                for i in range(2, len(row)):
                    if i == len(row) - 1:
                        newLine += row[i]
                    else:
                        newLine += row[i] + " "
                counter += 1
                training_set.append(newLine)
                numRecords += 1

            current_index += 1
    #if numTesting>len(patches):#means that the length of testing set is not enough
    counter=0
    file_path= original_categories_path+category_name+".txt"
    with open(file_path, 'r') as fp:
        for line in fp:
            if counter in testing_indices:
                filehandle.write(line)
            counter+=1
    filehandle.close()
    testing_set = relabelSets(testing_set)
    training_set= relabelSets(training_set)
    try:
        os.stat(destDirectory)
    except:
        os.mkdir(destDirectory)
    set_1_dirct = destDirectory+"/Set_1/"
    try:
        os.stat(set_1_dirct)
    except:
        os.mkdir(set_1_dirct)
    training_file_path = set_1_dirct+"train.txt"
    valid_file_path  = set_1_dirct+"valid.txt"
    testing_file_path = set_1_dirct+"test.txt"
    filehandle = open(testing_file_path, 'w')
    for query in testing_set:
        for line in query:
            filehandle.write(line)
    filehandle.close()
    filehandle = open(training_file_path, 'w')
    filehandle2 = open(valid_file_path, 'w')
    for query in training_set:
        for line in query:
            filehandle.write(line)
            filehandle2.write(line)
    filehandle.close()
    filehandle2.close()

    return
def prepareTraininTestingForRegressionPerCategory(categoryPath,destDirectory):
    counter = 0
    patch = 0
    records = []
    numRecords = 0
    with open(categoryPath, 'r') as fp:
        for line in fp:
            records.append(line)
            numRecords += 1
    numTraining = (int)(numRecords / 5) * 4
    numTesting = numRecords - numTraining
    print("numRecords " + str(numRecords) + " numTraining " + str(numTraining) + " numTesting " + str(numTesting))
    TestingSets = []
    testingSet = []
    index = 0
    set = 1
    recordsDict = dict()
    for i in range(numRecords):
        if index == numTesting:
            index = 0
            testingSet.append(records[i])
            recordsDict[i]=set
            TestingSets.append(testingSet)
            testingSet = []
            set+=1
        else:
            testingSet.append(records[i])
            index+=1
            recordsDict[i] = set
    if (len(testingSet))>0:
        TestingSets.append(testingSet)


    TrainingSets = []
    for j in range(len(TestingSets)):
        #testSet = TestingSets[i]
        trainingSet = []
        currentSet = j+1
        for i in range(numRecords):
            record = records[i]
            recordSet = recordsDict[i]
            if recordSet != currentSet:
                trainingSet.append(record)

        TrainingSets.append(trainingSet)

    size = len(TrainingSets)
    for i in range(size):
        newDirectory = destDirectory + "Set_" + str(i + 1) + "/"
        try:
            os.stat(newDirectory)
        except:
            os.mkdir(newDirectory)

        testFilePath = newDirectory + "test.txt"
        filehandleTesting = open(testFilePath, 'w')
        testSet = TestingSets[i]
        for test in testSet:
            filehandleTesting.write(test)
        filehandleTesting.close()

        trainFilePath = newDirectory + "train.txt"
        filehandleTraining = open(trainFilePath, 'w')
        trainSet = TrainingSets[i]
        for train in trainSet:
            filehandleTraining.write(train)
        filehandleTraining.close()

        print("Finished Writing Set " + (str(i + 1)))

    #'''
    return
def copyTrainingTestingLamdaMartFromSVM(svmDirectory,lamdaDirectory,addValid):
    try:
        os.stat(lamdaDirectory)
    except:
        os.mkdir(lamdaDirectory)

    for folder in os.listdir(svmDirectory):
        setFilePath = svmDirectory + folder
        if os.path.isdir(setFilePath):
            newDirectory = lamdaDirectory+folder
            try:
                os.stat(newDirectory)
            except:
                os.mkdir(newDirectory)
            for file in os.listdir(setFilePath):
                setFilePath1 = setFilePath+"/" + file
                if file == "train.txt":
                    shutil.copy2(setFilePath1, newDirectory)
                    if addValid:
                        valid = newDirectory+"/"+"valid.txt"
                        shutil.copy2(setFilePath1, valid)
                else:
                    shutil.copy2(setFilePath1, newDirectory)
        else:
            shutil.copy2(setFilePath,lamdaDirectory)
    return
def backAllPredictionsInOneFileStraight(sourceDirectory):
    print("Procedure to Collect predictions of different folds into one prediction file straight forward")
    allPredictionsFilePath = sourceDirectory + "AllPredictions.txt"
    filehandleAllPredicitons = open(allPredictionsFilePath, 'w')
    counter = 0
    for folder in os.listdir(sourceDirectory):
        setFilePath = sourceDirectory + folder
        if os.path.isdir(setFilePath):
            for filename in os.listdir(setFilePath):
                if filename == "predictions.txt":
                    predictionFilePath = setFilePath+"/"+filename
                    with open(predictionFilePath, 'r') as fp:
                        for line in fp:
                            filehandleAllPredicitons.write(line)
                            counter+=1

    filehandleAllPredicitons.close()
    print("Done, written "+str(counter)+" records")
    return

def readSentencePolaritiesPerRating():
    productPolartiesFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties_Per_RatingLevel.txt"
    ProductPolaritiesPerRating = dict()
    with open(productPolartiesFile, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            rowSize = len(row)
            numbers = []
            if rowSize > 1:
                for i in range(1, rowSize):
                    if len(row[i]) > 3:
                        tempNum = row[i].replace(" ", "")
                        num = ""
                        for item in tempNum:
                            if item == '-':
                                num += item
                                continue
                            if item == '0' and num == "":
                                numbers.append(item)
                            else:
                                if item != '\n':
                                    num += item
                        if len(num) > 0:
                            numbers.append(int(num))
                            num = ""
                    else:
                        if row[i] != '\n':
                            numbers.append(int(row[i]))

                if len(numbers) != 20:
                    print(len(numbers))
                    print(row)
                    print(numbers)
                else:
                    ProductPolaritiesPerRating[row[0]]= numbers


    print("ProductPolaritiesPerRating")
    print(len(ProductPolaritiesPerRating))

    return ProductPolaritiesPerRating

def readSentencePolaritiesPerRatingPerPeriod(productPolartiesFile,timeperiods):
    #productPolartiesFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/product_polarties_Per_RatingLevelPerTimePeriod.txt"
    ProductPolaritiesPerRatingPerPeriod = dict()
    with open(productPolartiesFile, 'r') as fp:
        for line in fp:
            row = line.split('\t')
            numbers = []
            for i in range(1,((timeperiods*5*2)+1)):
                numbers.append(int(row[i]))
            try:
                found = ProductPolaritiesPerRatingPerPeriod[row[0]]
                print("Problem: found previous record for "+str(row[0]))
            except KeyError:
                if len(numbers)!=(timeperiods*5*2):
                    print("missing polarities for found only "+str(len(numbers))+" for "+str(row[0]))
                else:
                    ProductPolaritiesPerRatingPerPeriod[row[0]] = numbers

    #print("ProductPolaritiesPerRatingPerPeriod")
    #print(len(ProductPolaritiesPerRatingPerPeriod))

    return ProductPolaritiesPerRatingPerPeriod

def changeSalesRankTargetToAverageToCategories(categoriesList,sourceBasicFeaturesDirectory,destinationDirectory):

    originalcategories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    for cat in categoriesList:
        catFilePath = sourceBasicFeaturesDirectory+cat+".txt"
        newFileCatPath = destinationDirectory+cat+".txt"
        filehandle = open(newFileCatPath, 'w')
        originalCatFilePath = originalcategories_path+cat+".txt"
        productList = []
        with open(originalCatFilePath, 'r') as fp:
            for line in fp:
                tuple = line.split('\t')
                productList.append(tuple[0])
        print("Considering " + cat +" "+ str(len(productList)))
        index = 0
        with open(catFilePath, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                productId = productList[index]
                resulTemproalCategoryRating, resulTemproalHelpfulnessWeight, n, average, numReviews, numFeedBackDictionary, numHelpFeedDictionary, ratingsDateDictionary = analyzeProduct(productBaseDirectory,productId)
                result = str(average)+" "
                for i in range(1,len(row)):
                    if i == len(row)-1:
                        result += row[i]
                    else:
                        result+=row[i]+" "
                filehandle.write(result)
                print(productId+" "+str(index))
                index+=1
        filehandle.close()
    return
def changeSalesRankTargetToTQRankToCategories(categoriesList,sourceBasicFeaturesDirectory,destinationDirectory):
    print("Procedure to change the label to TQ Rank of given feature list")
    originalcategories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    for cat in categoriesList:
        catFilePath = sourceBasicFeaturesDirectory+cat+".txt"
        newFileCatPath = destinationDirectory+cat+".txt"
        filehandle = open(newFileCatPath, 'w')
        originalCatFilePath = originalcategories_path+cat+".txt"
        filePathExpertiese = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/UserHelpfulVotesPerCategoryNew/" + cat+".txt"
        userExpert = dict()
        with open(filePathExpertiese, 'r') as fp:
            for line in fp:
                row = line.split('\t')
                userExpert[row[0]] = float(row[3])
        productList = []
        with open(originalCatFilePath, 'r') as fp:
            for line in fp:
                tuple = line.split('\t')
                productList.append(tuple[0])
        print("Considering " + cat +" "+ str(len(productList)))
        index = 0
        with open(catFilePath, 'r') as fp:
            for line in fp:
                row = line.split(' ')
                productId = productList[index]
                productFileName = productBaseDirectory + productId + ".txt"
                expoValue = computeExponentialScore(productFileName, userExpert)
                result = str(expoValue)+" "
                for i in range(1,len(row)):
                    if i == len(row)-1:
                        result += row[i]
                    else:
                        result+=row[i]+" "
                filehandle.write(result)
                print(productId+" "+str(index))
                index+=1
        filehandle.close()
    return
from temp_Function import *
from scipy import stats
import pylab as pl
from dirichlet_True_Rating import aggregateRatingsForAllTimePeriods
from dirichlet_True_Rating import dirichlet_mean
from dirichlet_True_Rating import computeExponentialScore
import shutil
if __name__ == '__main__':
    # as showcase, we will create some non-linear data
    # and print the performance of ranking vs linear regression

    #setting the number of samples and features
    '''
    n_samples, n_features = 300, 55
    np.random.seed(1)
    true_coef = np.random.randn(n_features)
     categoryNameStart = "Appliances"
        seconCat= "Gift Cards Store"
        thridCat = "Musical Instruments"
         #FilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/train.txt"
        '''

    #AllTrainingSets, AllTestingSets = preparefirstEightSetsForSVM()

    #AllTrainingSets, AllTestingSets = prepareKFoldForSVM()

    #AllTrainingSets, AllValidating, AllTestingSets = prepareKFoldForLamdaMart()

    #Preparing the Feature data one time to be used next
    # '''
    #'''
    #Here it extracts the features and create a file per category for all its products

    # *******************************Yelp Dataset feature extraction configuration**************************************************************************************
    '''
    categories_path = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/Resturants_Categories/"
    productBaseDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/ProductReviews_New/"
    destFilePath = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/All_Categories_Data_25_Basic_Features_With_1_Time_Intervals/"
    productPolartiesFile = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset/product_polarties_Per_RatingLevelPer_1_TimePeriod.txt"
    normalize = 1
    featureSet = 1 #This is the 17 basic features 5 Num Star Rating 5 +ve Polarity 5 -ve Polarity 5 Num Helpful per rating 5 Non-Helpful Per Rating
    categoriesList = ["Mexican", "Cafes", "Chinese", "Thai", "American (Traditional)", "Italian", "American (New)","Japanese", "Bars"]
    '''
    # ********************************************************************************************************************************************************************

    #prepareTrainingTestingDataForAllCategories(startFromCat,categories_path, productBaseDirectory, destFilePath,normalize,featureSet)
    dataset_type = "amazon"
    # *******************************Amazon Dataset feature extraction configuration**************************************************************************************
    '''
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/categories/"
    productBaseDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Product_Reviews/"
    destFilePath = "F:\Yassien_PhD\Experiment_4/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
    productPolartiesFile = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\Experiment 3/product_polarties_Per_RatingLevelPer_10_TimePeriod.txt"
    normalize = 1
    featureSet = 1  # This is the 17 basic features 5 Num Star Rating 5 +ve Polarity 5 -ve Polarity 5 Num Helpful per rating 5 Non-Helpful Per Rating
    categoriesList = ["Jewelry", "Toys & Games", "Arts, Crafts & Sewing", "Video Games", "Computers & Accessories","Software", "Cell Phones & Accessories", "Electronics"]
    #categoriesList = ["Industrial & Scientific"]


    timeperiods=1
    prepareTrainingTestingDataForAllCategoriesL2R(categoriesList,categories_path,productBaseDirectory,destFilePath,normalize,productPolartiesFile,dataset_type,timeperiods)
    '''
    #'''

    '''
    # Collecting the 5fold dataset for SvM------------------------------------------------------------------------------
    AllTrainingSets, AllTestingSets = prepareKFoldForSVM()
    print("Preparing Learning Data for SVM")
    for i in range(len(AllTestingSets)):
        print("Creating Fold_"+str(i+1))
        for_lib = "SVM"
        categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
        setFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Test/K_Fold/Set_"+str(i+1)+"/"
        sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_Features/"
        validating_Set = ""

        prepareTrainingTestingForAll(categories_path,sourceFeaturesDirectory,AllTrainingSets[i],AllTestingSets[i],validating_Set,for_lib,setFilePath)
    #'''
    # ------------------------------------------------------------------------------------------

    '''# Collecting the 5fold dataset for LamdaMart------------------------------------------------------------------------
    #AllTrainingSets, AllValidating, AllTestingSets = prepareKFoldForLamdaMart()
    AllTrainingSets, AllTestingSets = prepareKFoldForSVM()
    print("Preparing Learning Data for LamdaMart")
    for i in range(len(AllTestingSets)):
        print("Creating Fold_"+str(i+1))
        for_lib = "LamdaMart"
        categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
        setFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold/Set_"+str(i+1)+"/"
        #sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_Features_Not_Normalized/"
        sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_Features/"
        validating_Set = ""
        #prepareTrainingTestingForAll(categories_path,sourceFeaturesDirectory,AllTrainingSets[i],AllTestingSets[i],AllValidating[i],for_lib,setFilePath)
        prepareTrainingTestingForAll(categories_path, sourceFeaturesDirectory, AllTrainingSets[i], AllTestingSets[i],"", for_lib, setFilePath)
    # '''

    '''
    AllTrainingSets = []
    AllValidatingSets = []
    AllTestingSets = []
    AllTrainingSets.append(['Appliances', 'Arts, Crafts & Sewing', 'Camera &amp; Photo', 'Electronics', 'Home Improvement', 'Jewelry','Office Products', 'Watches'])
    AllTestingSets.append([['Appliances', 'Arts, Crafts & Sewing', 'Camera &amp; Photo', 'Electronics', 'Home Improvement', 'Jewelry','Office Products', 'Watches']])
    validating = [['Appliances', 'Arts, Crafts & Sewing', 'Camera &amp; Photo', 'Electronics', 'Home Improvement', 'Jewelry','Office Products', 'Watches']]
    AllValidatingSets.append(validating)
    print("Creating additional Testingset")
    for_lib = "LamdaMart"
    categories_path = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three\categories/"
    setFilePath = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/Original_Set/"
    sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_9_Basic_Features/"
    prepareTrainingTestingForAll(categories_path, sourceFeaturesDirectory, AllTrainingSets[0], AllTestingSets[0],AllValidatingSets[0], for_lib, setFilePath)
    #'''

    #'''
    #cutoffs = [3, 5, 10, 20, 30, 40,50,60,70,100,120,150,160,180,200,220]
    #cutoffs = [10]
    #cutoffs = [3, 5, 10, 20, 30, 40, 50, 60, 70, 100, 120, 150, 160, 180, 200, 220, 250, 280, 300, 350, 400,500,600]

    import os

    #'''
    cutoffs = [10]
    categoryList = ["Industrial & Scientific", "Jewelry", "Arts, Crafts & Sewing", "Toys & Games", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    #categoryList = ["Cell Phones & Accessories", "Electronics"]
    #categoryList = ["Jewelry"]
    #categoryList = ["Mexican", "Cafes", "Chinese", "Thai", "American (Traditional)", "Italian", "American (New)", "Japanese", "Bars"]
    timeperiods=10
    print("training/testing sets building for " + dataset_type + " " + str(timeperiods) + " periods")
    for category in categoryList:
    #category = "Industrial & Scientific"

        #catDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda/" + category
        catDirectory = "f:\Yassien_PhD\Experiment_4\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_samp/" + category
        try:
            os.stat(catDirectory)
        except:
            os.mkdir(catDirectory)


        '''
        catDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_test_spec/" + category
        try:
            os.stat(catDirectory)
        except:
            os.mkdir(catDirectory)

        catDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_test_spec/" + category
        try:
            os.stat(catDirectory)
        except:
            os.mkdir(catDirectory)
            #'''

        for i in range(len(cutoffs)):
            cutoff = "Cutoff_" + str(cutoffs[i])  # str((i+1)*10)

            # *******************************Yelp training/testing sets building configuration**************************************************************************************
            #sourceFeaturesDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\All_Categories_Data_25_Basic_Features_With_1_Time_Intervals/"
            #destDirectorySvm = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__With_1_Time_Interval_TQ_Target_25_lamda/"+category+"/"+cutoff+"/"
            # *******************************Amazon training/testing sets building configuration**************************************************************************************
            sourceFeaturesDirectory = "f:\Yassien_PhD\Experiment_4/All_Categories_Data_25_Basic_Features_With_10_Time_Intervals_Sim_by_Clustering/"
            destDirectorySvm = "f:\Yassien_PhD\Experiment_4/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25_lamda_samp/"+category+"/"+cutoff+"/"
            # ********************************************************************************************************************************************************************
            threshold = cutoffs[i]#(i+1)*10
            catPath = sourceFeaturesDirectory + category + ".txt"
            lamda = 1
            print("Preparing data for LamdaMart")
            oneTesting = 0
            prepareTraininTestingFromOneCategory(catPath,destDirectorySvm,threshold,lamda,oneTesting,0.8)
            #Categories_For_testing_learning_with_greater_100="F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_For_testing_learning_with_greater_100/"
            #Categories_Indices_for_testing = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\Categories_Indices_for_testing/"
            #prepareTraininTestingFromOneCategory_with_specificTesting(catPath,destDirectorySvm,threshold,lamda,oneTesting,0.8,Categories_Indices_for_testing,category,Categories_For_testing_learning_with_greater_100,categories_path)

            #print("Preparing data for SVM Map")
            #destDirectoryLamda = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Map/K_Fold_PerCategory_Basic/" + category + "/" + cutoff + "/"

            lamda = 1
            # prepareTraininTestingFromOneCategory(catPath, destDirectory, threshold, lamda,oneTesting)
            #destDirectoryLamda=destDirectorySvm
            #copyTrainingTestingLamdaMartFromSVM(destDirectorySvm, destDirectoryLamda)

            print("Preparing data for SVM Light")
            lamda = 0
            destDirectoryLamda = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Svm_Light/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25/" + category + "/" + cutoff + "/"
            #copyTrainingTestingLamdaMartFromSVM(destDirectorySvm, destDirectoryLamda,0)
            #prepareTraininTestingFromOneCategory(catPath, destDirectoryLamda, threshold, lamda, oneTesting)

            print("Preparing data for Lamdamart")
            lamda = 1
            #prepareTraininTestingFromOneCategory(catPath, destDirectory, threshold, lamda,oneTesting)
            destDirectoryLamda = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/Lamda_Java/K_Fold_PerCategory_Basic__With_10_Time_Interval_TQ_Target_25/" + category + "/" + cutoff + "/"
            #copyTrainingTestingLamdaMartFromSVM(destDirectorySvm,destDirectoryLamda,1)

    #'''


    '''

    #This is the regression preparation code

    #categoriesList = ["Industrial & Scientific", "Jewelry", "Toys & Games", "Arts, Crafts & Sewing", "Video Games","Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    print("Preparing Data For Regression")
    sourceFeaturesDirectory = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\All_Categories_Data_25_Basic_Features_With_10_Time_Intervals/"
    for category in categoriesList:

    #category = "Industrial & Scientific"
    #for i in range(6):
    #sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features/"
        catPath = sourceFeaturesDirectory + category + ".txt"
        destDirectorySvmReg = "F:\Yassien_PhD\yelp_dataset_challenge_academic_dataset\K_Fold_PerCategory_Basic__Regression_TQ_Target_25_lamda/" + category + "/"
        print(destDirectorySvmReg)
        try:
            os.stat(destDirectorySvmReg)
        except:
            os.mkdir(destDirectorySvmReg)
        prepareTraininTestingForRegressionPerCategory(catPath,destDirectorySvmReg)
    #'''
    ''''
    categoriesList = ["Industrial & Scientific", "Jewelry", "Toys & Games", "Arts, Crafts & Sewing", "Video Games", "Computers & Accessories", "Software", "Cell Phones & Accessories", "Electronics"]
    sourceFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features/"
    destFeaturesDirectory = "C:\Yassien_RMIT PhD\Datasets\TruthDiscovery_Datasets\Web data Amazon reviews/Unique_Products_Stanford_three/Experiment 2/All_Categories_Data_25_Basic_Features_With_TQ_Target_For_Ranking/"
    #changeSalesRankTargetToAverageToCategories(categoriesList,sourceFeaturesDirectory,destFeaturesDirectory)
    #changeSalesRankTargetToTQRankToCategories(categoriesList,sourceFeaturesDirectory,destFeaturesDirectory)
    #'''
    print("Done")