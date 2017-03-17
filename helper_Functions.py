__author__ = 's3525116'
#-----------------------------------------------------------------------------------------------------------------------
def extractMemberId(inputString):
    memberID = ""
    for char in inputString:
        if char !='[' and char != "'" and char != ",":
            memberID = memberID + char
    return memberID
#-----------------------------------------------------------------------------------------------------------------------
def extractMemberName(inputString):
    memberName = ""
    for char in inputString:
        if char !='[' and char != "'" and char != "]" and char != ",":
            memberName = memberName + char
        elif char == "," or char == "'" or char == '"':
            memberName = memberName + " "

    return memberName
#-----------------------------------------------------------------------------------------------------------------------
def getLocation(inputString):
    memberLocation = ""
    for char in inputString:
        if char !='(' and char != ")" and char != "," and char !='[' and char !=']':
            memberLocation = memberLocation + char
        elif char == "," or char == "'" or char == '"':
            memberLocation = memberLocation + " "

    return memberLocation
#-----------------------------------------------------------------------------------------------------------------------
def RepresentsInt(inputString):
    print("inputString")
    print(inputString)
    nSize = len(inputString)
    counter = 0
    newInt = -1
    comboInt = ""
    for char in inputString:
        if char.isdigit():
            counter = counter + 1
            comboInt = comboInt + char
    print("counter")
    print(counter)
    print("nSize")
    print(nSize)
    if counter == nSize - 3 and counter != 0:
        newInt = int(comboInt)
    else:
        newInt = -1

    return newInt
#-----------------------------------------------------------------------------------------------------------------------
def RepresentsIntVersion2(inputString):
    nSize = len(inputString)
    counter = 0
    newInt = -1
    comboInt = ""
    for char in inputString:
        if char.isdigit():
            counter = counter + 1
            comboInt = comboInt + char
    if counter == nSize and counter != 0:
        newInt = int(comboInt)
    else:
        newInt = -1

    return newInt
#-----------------------------------------------------------------------------------------------------------------------
def extractString(inputString):
    memberID = ""
    for char in inputString:
        if char !='[' and char != "'" and char != ",":
            memberID = memberID + char
    return memberID
#-----------------------------------------------------------------------------------------------------------------------
def contains(allReviews, filter):
    for x in allReviews:
        if filter(x):
            return True
    return False
#-----------------------------------------------------------------------------------------------------------------------
def loseLastChar(inputString):
    result = inputString[:-1]
    return result
#-----------------------------------------------------------------------------------------------------------------------