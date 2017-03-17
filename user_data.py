__author__ = 's3525116'
import csv
from helper_Functions import *

class Member:
    def __init__(self,memeberId,memberName,numReviews,memberRank,memberBirthday,memberLocation,memberState,selfDescription,userName):
        self.memeberId = memeberId
        self.memberName = memberName
        self.numReviews = numReviews
        self.memberRank = memberRank
        self.memberBirthday = memberBirthday
        self.memberLocation = memberLocation
        self.memberState = memberState
        self.selfDescription = selfDescription
        self.userName = userName
#-----------------------------------------------------------------------------------------------------------------------
def readUserData(filePath,allMembers):
    '''
    Parsing file amazon-member-shortSummary.txt
    MEMBER INFO
    <member id> <member name> <#reviews> (location) <In my own words>
    '''
    print("Procedure to Parse Members' Data")
    print("Started")
    counter = 0
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    recordStarted = 0
    recordFinished = 0
    record = []
    for row in reader:
       temp = [i.split('\t') for i in row]
       strMemInfo = str(temp[0])
       if 'MEMBER' in strMemInfo and 'INFO' in strMemInfo:
           if recordStarted == 1:
              recordFinished = 1
           else:
               recordStarted = 1
               record = []

       if recordFinished != 1:
            strMemInfo = str(temp[0])
            if 'MEMBER' not in strMemInfo and 'INFO' not in strMemInfo:
                record.append(temp)

       if recordFinished == 1:
           recordStarted = 1
           recordFinished = 0
           memId = 0
           memName = ""
           convertedNum = 0
           memDescription = ""
           nameDone = 0
           locationDone = 0
           location = ""
           for i in range(len(record)):
            str1 = str(record[i])
            toto = str1
            if i == 0: #This is the first line where the important data relies e.g.[['AFVQZQ8PW0L', 'Harriet Klausner', '11343', '']]
                toto = str1.split()
                for k in range(len(toto)):
                    if k == 0:  #get the member id
                        memId = extractMemberId(toto[k])
                    else:
                        ret = RepresentsInt(toto[k])
                        if ret != -1:
                            convertedNum = ret
                            memName = extractMemberName(memName)
                            nameDone = 1
                        else:
                            if nameDone == 0:
                                memName = memName + " " +str(toto[k])
                            else:
                                if locationDone == 0:
                                    if ')' in str(toto[k]):
                                        location = location + " "+str(toto[k])
                                        location = getLocation(location)
                                        locationDone = 1
                                    else:
                                        location = location + " "+str(toto[k])
                                else:
                                    memDescription = memDescription + str(toto[k])

            else:
                memDescription = memDescription + toto
           memDescription = extractMemberName(memDescription)
           allMembers.append(Member(memId,memName,convertedNum,"","",location,"",memDescription,""))
           record = []


       counter = counter + 1
       #if counter == 100:
        #break
    print("Finished")
    return
#-----------------------------------------------------------------------------------------------------------------------
def readUserLocationData(filePath):
    '''
    Parsing file amazon-memberinfo-locations.txt
    <username> <member rank> <birthday> <location> <name> <memberid> <state>
    '''
    print("Procedure to Parse Members' Location Data")
    print("Started")
    memLocationsDict = {}
    records = []
    counter = 0
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    recordStarted = 0
    recordFinished = 0
    record = []
    for row in reader:
       temp = [i.split('\t') for i in row]
       men = str(temp[0])
       toka = men.split("'")
       if len(toka) !=14 and len(toka) !=15:
           '''Ignoring unconsistent records
           '''
       else:
           record = []
           for term in toka:
            if term !="[" and term !=', ' and term!="]":
               record.append(term)
           #records = dict([(record[5], record)])
           records.append(record)

       counter = counter + 1
       #if counter == 100:
        #   break
    memLocationsDict = dict([(record[5], record) for record in records])
    print("len Dictionary")
    print(len(memLocationsDict))
    print("Finished")
    return memLocationsDict
#-----------------------------------------------------------------------------------------------------------------------
def combineUserDataToOne(allMembers,memLocations,filePath):
    uniqueUserData = []
    print("Procedure to Combine All User Data into One and Write it in AllUserData.txt file")
    print("Started")
    alldatafile = open(filePath,'w')
    print("Size of Members")
    print(len(allMembers))
    #for memLocation in memLocations:
    counter = 0
    counterNonFound = 0
    for memData in allMembers:
       #memLocation = memLocations.get(memData.memeberId)
       try:
           memLocation = next(v for (k,v) in memLocations.items() if memData.memeberId in k)
           if memLocation != None:
            #if memData.memeberId == memLocation[5]:
                memData.userName = memLocation[0]
                memData.memberRank = memLocation[1]
                memData.memberBirthday = memLocation[2]
                memData.memberState = memLocation[6]
                alldatafile.write("MEMBER INFO")
                alldatafile.write("\n")
                alldatafile.write(str(memData.memeberId))
                alldatafile.write("\n")
                alldatafile.write(memData.memberName)
                alldatafile.write("\n")
                alldatafile.write(memData.memberBirthday)
                alldatafile.write("\n")
                alldatafile.write(memData.memberLocation)
                alldatafile.write("\n")
                alldatafile.write(memData.memberRank)
                alldatafile.write("\n")
                alldatafile.write(memData.memberState)
                alldatafile.write("\n")
                alldatafile.write(str(memData.numReviews))
                alldatafile.write("\n")
                alldatafile.write(memData.selfDescription)
                alldatafile.write("\n")
                alldatafile.write(memData.userName)
                alldatafile.write("\n")
                #uniqueUserData.append(memData)
                counter = counter + 1
           else:
               #print(memData.memeberId)
                counterNonFound = counterNonFound + 1
       except StopIteration:
            pass
    alldatafile.close()
    print("common users")
    print(counter)
    print("Not Found")
    print(counterNonFound)
    print("Finished")
    return uniqueUserData
#-----------------------------------------------------------------------------------------------------------------------
def printMember(member):
  print("MemID:"+member.memeberId)
  print("MemName:"+member.memberName)
  print("MemBD:"+member.memberBirthday)
  print("MemLO:"+member.memberLocation)
  print("MemRK:"+str(member.memberRank))
  print("MemST:"+member.memberState)
  print("MemNumRV:"+str(member.numReviews))
  print("MemDS:"+member.selfDescription)
  print("MemUN:"+member.userName)
  return
def printMembers(allMembers):
  for member in allMembers:
      printMember(member)
  return
def readAllUserData(filePath):
    '''
    Parsing file AllUserData.txt
    MEMBER INFO
    <member id> <member name> <birthday> <location>  <member rank> <state> <#reviews>  <In my own words> <username>
    '''
    #This function return a dictonary of members with the key of member id
    print("Procedure to Parse All Members' Data")
    print("Started")
    allMembers = []
    counter = 0
    data_initial = open(filePath, "rU")
    reader = csv.reader((line.replace('\0','') for line in data_initial), delimiter='\n')
    counter = 0
    fieldCounter = 0
    for row in reader:
       if len(row) == 0:
           tempStr = ""
       else:
           tempStr = str(row[0])

       if 'MEMBER' in tempStr and 'INFO' in tempStr:
           fieldCounter = 0
           member = Member("","","","","","","","","")
           continue
       if fieldCounter == 0:
        member.memeberId = extractString(tempStr)
       elif fieldCounter == 1:
           member.memberName = extractString(tempStr)
       elif fieldCounter == 2:
           member.memberBirthday = extractString(tempStr)
       elif fieldCounter == 3:
           member.memberLocation = extractString(tempStr)
       elif fieldCounter == 4:
           member.memberRank = RepresentsIntVersion2(extractString(tempStr))
       elif fieldCounter == 5:
           member.memberState = extractString(tempStr)
       elif fieldCounter == 6:
           member.numReviews = RepresentsIntVersion2(extractString(tempStr))
       elif fieldCounter == 7:
           member.selfDescription = extractString(tempStr)
       elif fieldCounter == 8:
           member.userName = extractString(tempStr)
           allMembers.append(member)

       fieldCounter = fieldCounter + 1

       counter = counter + 1
       #if counter == 100:
        #break
    memDictionary = dict([(memeber.memeberId, memeber) for memeber in allMembers])
    print("Finished")
    return memDictionary
#-----------------------------------------------------------------------------------------------------------------------
def searchForMemeber(memDictionary,memeberId):
   memeber = None
   numTries = 4
   for i in range(numTries):
       foundMember = searchInDictionary(memDictionary,memeberId)
       if foundMember != None:
           memeber = foundMember
           break
       else:
           memeberId = loseLastChar(memeberId)
   return memeber
#-----------------------------------------------------------------------------------------------------------------------
def searchInDictionary(memDictionary,memeberId):
   memeber = None
   try:
       foundMember = next(v for (k,v) in memDictionary.items() if memeberId in k)
       if foundMember != None:
           memeber = foundMember
   except StopIteration:
       pass
   return memeber

#-----------------------------------------------------------------------------------------------------------------------