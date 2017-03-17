__author__ = 's3525116'

def extractFirstString(inputString):
    start = 0
    concatenated = ""
    for char in inputString:
        if (char == '"' and start == 0) or (char == '"' and start == 1)or (char == ',' and start == 1):
            start = start + 1
            continue
        if (char == '[' and start == 1) or (char == ']' and start == 1)or (char == ' ' and start == 1) or (char == '{' and start == 1)or (char == '\\' and start == 1):
            continue
        if start == 2 and char !='"':
            concatenated = concatenated + char
        elif start == 2 and char =='"':
            return concatenated
    print("start")
    print(start)
    return concatenated
def extractAsin(inputString):
    start = 0
    concatenated = ""
    for char in inputString:
        if (char == ':' and start == 0):
            start = start + 1
            continue
        if (char == ' ' and start == 1):
            start = start + 1
            continue
        if (char == "'" and start == 2):
            start = start + 1
            continue
        if start == 3 and char !="'":
            concatenated = concatenated + char
        elif start == 3 and char =="'":
            return concatenated
    return concatenated
def extractUnixTime(inputString):
    start = 0
    concatenated = ""
    for char in inputString:
        if char == '"' and start == 0:
            start = start + 1
            continue
        if start == 1 and char ==':':
            continue
        if start == 1 and char !=':' and char != ',':
            concatenated = concatenated + char
        if char ==',':
            break
    retInt = int(concatenated)

    return retInt
def extractRatingTime(inputString):
    start = 0
    hasDigits = 0
    concatenated = ""
    for char in inputString:
        if char == '"' and start == 0:
            start = start + 1
            continue
        if (start == 1 and char ==':') or (start == 1 and char =='(') or (start == 1 and char ==')') or (start == 1 and char =='[') or (start == 1 and char ==']')or (start == 1 and char =="\\"):
            continue
        if start == 1 and char !=':' and char != ',':
            temp = char
            if temp.isdigit() == True:
                hasDigits = hasDigits + 1
            concatenated = concatenated + char
        if char ==',':
            break
    percent = 0.0
    if len(concatenated) > 0 :
        percent = float(hasDigits)/float(len(concatenated))

    retNum = ""

    if percent >= 0.50 :
        try:
            retNum = float(concatenated)
        except ValueError as e:
            print("inputString")
            print(inputString)
            print("concatenated")
            print(concatenated)
            print("percent")
            print(percent)
    else:
        retNum = ""

    return retNum

def extractHelpful(inputString):

    start = 0
    hasDigits = 0
    concatenated = ""
    for char in inputString:
        if char == '"' and start == 0:
            start = start + 1
            continue
        if start == 1 and char ==':':
            continue
        if start == 1 and char =='[':
            continue
        if start == 1 and char !=':' and char != ',':
            temp = char
            if temp.isdigit() == True:
                hasDigits = hasDigits + 1
            concatenated = concatenated + char
        if char ==',':
            break

    percent = 0
    if len(concatenated) > 0:
        percent = float(hasDigits)/float(len(concatenated))

    if percent >= 0.5:
        try:
            retInt = int(concatenated)
        except OSError as e:
            retInt = ""
    else:
        retInt = ""

    #retInt = int(concatenated)

    return retInt

def extractNumVotes(inputString):

    start = 0
    concatenated = ""
    startconcat = 0
    hasDigits = 0
    for char in inputString:
        if char == '"' and start == 0:
            start = start + 1
            continue
        if start == 1 and char ==':':
            continue
        if start == 1 and char =='[':
            continue
        if start == 1 and char ==',':
            startconcat = 1
            continue
        if char ==']':
            break
        if startconcat == 1:
            temp = char
            if temp.isdigit() == True:
                hasDigits = hasDigits + 1
            concatenated = concatenated + char

    #retInt = int(concatenated)
    percent = 0
    if len(concatenated) > 0:
        percent = float(hasDigits)/float(len(concatenated))

    if percent >= 0.5:
        try:
            retInt = int(concatenated)
        except OSError as e:
            retInt = ""
    else:
        retInt = ""

    return retInt

def extractSalesRank(inputString):
    start = 0
    categories = ""
    rank = -1
    concatenated = ""
    startconcat = 0
    hasDigits = 0
    for char in inputString:
        if char == '{' and start == 0:
            start = start + 1
            continue
        if start == 1 and char =="'":
            start = start + 1
            continue
        if start == 2 and char =="'":
            start = start + 1
            categories = concatenated
            concatenated = ""
            start = start + 1
            continue
        if start == 2 and char !="'":
            concatenated = concatenated + char
            continue
        if start == 3 and char ==":":
            start = start + 1
            continue
        if start == 4 and char !='}' and char !=" " and char !=":":
            temp = char
            if temp.isdigit() == True:
                hasDigits = hasDigits + 1
            concatenated = concatenated + char
            continue
        if start == 4 and char =='}':
            percent = float(hasDigits)/float(len(concatenated))
            if percent >= 0.7:
                rank = int(concatenated)
            else:
                return ("None",-1)
            break
    return (categories,rank)