import os
from datetime import datetime
import  math

def writePolarityLine(filehandle1,productid,totalPostive,totalNegative,numSentences):
    try:
        filehandle1.write(productid)
        filehandle1.write("\t")
        filehandle1.write(str(totalPostive))
        filehandle1.write("\t")
        filehandle1.write(str(totalNegative))
        filehandle1.write("\t")
        filehandle1.write(str(numSentences))
        filehandle1.write("\n")
    except IOError as e:
        print("error writing for  " + productid)
        pass
    return

def splitParagraphIntoSentences(paragraph):
    ''' break a paragraph into sentences
        and return a list '''
    import re
    # to split by multile characters

    #   regular expressions are easiest (and fastest)
    sentenceEnders = re.compile('[.!?]')
    if len(paragraph) >0 and paragraph !=" ":
        try :
            sentenceList = sentenceEnders.split(paragraph)
        except TypeError:
            sentenceList = []
            pass
    else:
        sentenceList = []
    return sentenceList

def extractProductPolarties():
    print("Extracting Polarities for all products in Amazon Dataset")
    print("We write the number of +ve Sentiments and number of -ve Sentiments")
    file_to_write = "D:\Yassien_PhD\Experiment_6/product_polarties.txt"
    filehandle1 = open(file_to_write, 'w')
    filehandle1.write("ProductID    NumPositive   NumNegative  NumSentences\n")
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
        print(productid)
        numSentences = 0
        computed = 1
        inputFile = "C:\SentiTemp/test.txt"
        try:
            filehandle = open(inputFile, 'w')
        except IOError as e:
            print("error writing in file "+inputFile)
            inputFile = "C:\SentiTemp/test1.txt"
            try:
                filehandle = open(inputFile, 'w')
            except IOError as e:
                print("error writing in file " + inputFile)
                print("failed")
                computed = 0
                pass
            pass
        with open(productFile, 'r') as fp:
            for line in fp:
                row = line.split("\t")
                text = ""
                if len(row)>8:
                    text+=row[6]+"\t"
                    text += row[7]
                #print(text)
                sentences = splitParagraphIntoSentences(text)
                for sent in sentences:
                    if len(sent)>1:
                        #print(sent)
                        numSentences+=1
                        filehandle.write(sent)
                        filehandle.write("\n")

                filehandle.write("---")
                filehandle.write("\n")
                #print("------------------------------")

        filehandle.close()

        if computed == 1:
            os.chdir("C:\SentiTemp/")
            command = "java -jar SentiStrengthCom.jar sentidata C:\SentiTemp/ input " + inputFile
            os.system(command)
            fileToRead = "C:\SentiTemp/test0_out.txt"

            commentPolarityTotal = 0
            commentPolarity = 0
            totalPostive = 0
            totalNegative = 0
            try:
                with open(fileToRead, 'r') as sentiStrfp:
                    bIgnoreFirst = 0
                    for senti in sentiStrfp:
                        if bIgnoreFirst == 0:
                            bIgnoreFirst = 1
                            continue
                        sentSplit = senti.split('\t')
                        if sentSplit[2] == "\n":
                            continue

                        if sentSplit[2] == "---\n":
                            commentPolarityTotal += commentPolarity
                            commentPolarity = 0
                        else:
                            numPostive = int(sentSplit[0])
                            numNegative = int(sentSplit[1])
                            sentPolarity = numPostive + numNegative
                            totalPostive+=numPostive
                            totalNegative+=numNegative
                            #print(str(totalPostive)+" "+str(totalNegative))
                            '''if sentPolarity >= 0:
                                commentPolarity+=1
                                totalPostive+=1
                            else:
                                commentPolarity-=1
                                totalNegative += 1
                                '''



                os.remove(inputFile)
                os.remove(fileToRead)
            except IOError as e:
                print("error writing in file " + fileToRead)
                writePolarityLine(filehandle1, productid, 0, 0, 0)
                pass
            writePolarityLine(filehandle1, productid, totalPostive, totalNegative, numSentences)
        else:
            writePolarityLine(filehandle1, productid, 0, 0, 0)

        counter += 1
        print(counter)
    filehandle1.close()
    print("Found " + str(counter) + " Product Polarities")
    return
def extract_Weighted_Product_Polarities():
    print("Extracting Polarities for all products in Amazon Dataset")
    print("We write the number of weighted +ve Sentiments and number of -ve Sentiments")
    file_to_write = "D:\Yassien_PhD\Experiment_6/weighted_product_polarties.txt"
    filehandle1 = open(file_to_write, 'w')
    filehandle1.write("ProductID    WeightedPositive   WeightedNegative  WeightedTotal \n")
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
                    product_dict[product_id] = 0

    counter = 0
    for key, value in product_dict.items():
        productFile = product_base_directory + key + ".txt"
        productid = key
        print(str(counter)+" "+str(productid))
        total_postive, total_neg, total_polarity = extractWeightedPolartiesPerProduct(productFile)
        filehandle1.write(productid)
        filehandle1.write("\t")
        filehandle1.write(str(total_postive))
        filehandle1.write("\t")
        filehandle1.write(str(total_neg))
        filehandle1.write("\t")
        filehandle1.write(str(total_polarity))
        filehandle1.write("\n")
        counter+=1


    filehandle1.close()
    return
def extractWeightedPolartiesPerProduct(product_file_path):

    minDate = datetime(2050, 12, 31)
    maxDate = datetime(1950, 1, 1)
    pos_weight, neg_weight=0,0
    inputFile = "C:\SentiTemp/test.txt"
    try:
        filehandle = open(inputFile, 'w')
    except IOError as e:
        print("error writing in file " + inputFile)
        inputFile = "C:\SentiTemp/test1.txt"
        try:
            filehandle = open(inputFile, 'w')
        except IOError as e:
            print("error writing in file " + inputFile)
            print("failed")
            computed = 0
            pass
        pass

    product_dates = []
    with open(product_file_path, 'r') as filep:
        for item in filep:
            review = item.split('\t')
            datesplit = review[2].split(',')
            monthDay = datesplit[0]
            month = ""
            day = ""
            monthDone = 0
            for char in monthDay:
                if char != " " and monthDone == 0:
                    month = month + char
                if char == " ":
                    monthDone = 1
                if monthDone == 1:
                    day = day + char

            if len(datesplit) > 1 and datesplit[1] != ' ' and len(datesplit[1]) <= 5:
                year = int(datesplit[1])
                month = int(month)
                day = int(day)
                currentDay = datetime(year, month, day)
                product_dates.append(currentDay)
                if currentDay > maxDate:
                    maxDate = currentDay
                if currentDay < minDate:
                    minDate = currentDay

            row = item.split('\t')
            text = ""
            if len(row) > 8:
                text += row[6] + "\t"
                text += row[7]
            # print(text)
            sentences = splitParagraphIntoSentences(text)
            for sent in sentences:
                if len(sent) > 1:
                    # print(sent)
                    filehandle.write(sent)
                    filehandle.write("\n")

            filehandle.write("---")
            filehandle.write("\n")
            # print("------------------------------")
    num_revs = 0
    filehandle.close()
    numSentences = 0
    computed = 1
    postive_sents = []
    negative_sents = []
    rev_tot_polarity = []
    all_num_sentences = []
    num_sentences=0
    if computed == 1:
        os.chdir("C:\SentiTemp/")
        command = "java -jar SentiStrengthCom.jar sentidata C:\SentiTemp/ input " + inputFile
        os.system(command)
        fileToRead = "C:\SentiTemp/test0_out.txt"

        commentPolarityTotal = 0
        commentPolarity = 0
        totalPostive = 0
        totalNegative = 0
        try:
            with open(fileToRead, 'r') as sentiStrfp:
                bIgnoreFirst = 0
                for senti in sentiStrfp:
                    if bIgnoreFirst == 0:
                        bIgnoreFirst = 1
                        continue
                    sentSplit = senti.split('\t')
                    if sentSplit[2] == "\n":
                        continue

                    if sentSplit[2] == "---\n":
                        commentPolarityTotal += commentPolarity
                        commentPolarity = 0
                        all_num_sentences.append(numSentences)
                        postive_sents.append(totalPostive)
                        negative_sents.append(totalNegative)
                        rev_tot_polarity.append(totalPostive + totalNegative)
                        numSentences=0
                        totalPostive = 0
                        totalNegative = 0

                    else:
                        num_sentences+=1
                        numPostive = int(sentSplit[0])
                        numNegative = int(sentSplit[1])
                        totalPostive += numPostive
                        totalNegative += numNegative

            os.remove(inputFile)
            os.remove(fileToRead)
        except IOError as e:
            print("error writing in file " + fileToRead)
            pass
    print("DAtes "+str(len(product_dates)))
    print("pos "+str(len(postive_sents)))
    print("pos " + str(len(negative_sents)))
    print("pos " + str(len(all_num_sentences)))
    print("pos " + str(len(rev_tot_polarity)))
    total_pos_weight = 0
    total_neg_weight = 0
    total_polarity_weight =0
    for i in range(len(product_dates)):
        weight = ((product_dates[i] - minDate).days) / (maxDate - minDate).days
        sum = postive_sents[i]+abs(negative_sents[i])
        if sum !=0:
            pos_weight_temp = weight * (postive_sents[i]/sum)#(totalPostive / total_votes) * rating
        else:
            pos_weight_temp = 0
        if sum!=0:
            neg_weight_temp = weight * (abs(negative_sents[i])/sum)#(abs(totalNegative) / total_votes) * rating
        else:
            neg_weight_temp =0
        tot_weight_temp = weight * (postive_sents[i]+negative_sents[i])
        #print(str(tot_weight_temp) + " " +str(pos_weight_temp) + " " + str(neg_weight_temp))
        expValue_pos = (math.e ** pos_weight_temp)
        expValue_neg = (math.e ** neg_weight_temp)
        exp_Value_tot = (math.e ** tot_weight_temp)
        #print(str(exp_Value_tot) + " " +str(expValue_pos) + " " + str(expValue_neg))
        total_pos_weight += expValue_pos
        total_neg_weight += expValue_neg
        total_polarity_weight+=exp_Value_tot
        #print("------------------")
        num_revs+=1


    #print("Num revs "+str(num_revs))
    if num_revs:
        total_pos_weight/=num_revs
        total_neg_weight /= num_revs
        total_polarity_weight/=num_revs

    return total_pos_weight,total_neg_weight,total_polarity_weight

#extractProductPolarties()
#extract_Weighted_Product_Polarities()