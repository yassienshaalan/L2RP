#Author: Yassien Shaalan


def createNewVerifiedDataset(verfied_directory, original_dataset, output_dictionary):
    print("This procedure adds the verified purchase field to previous dataset")
    missingFilehandle = open(output_dictionary+"Missing",'w')
    for category in os.listdir (verfied_directory):
        path = verfied_directory +"/"+category
        print("Consider "+category)
        for Product in os.listdir (path):
            productPath = path+"/"+Product
            countReviewsVerified = 0
            userVerified = dict()
            with open(productPath, 'r') as fp:
              for line in fp:
                countReviewsVerified = countReviewsVerified + 1
                review = line.split(' ')
                reviewSplit = line.split('\t')
                revID = review[0]
                revVerified = -1
                if len(reviewSplit)>1:
                    revVerified = reviewSplit[1]
                else:
                    print(reviewSplit)
                userVerified[revID] = revVerified
            productOriginalFile = original_dataset+Product
            writePath = output_dictionary
            fileToWrite = category+"/"+Product
            filehandle = open(writePath+fileToWrite,'w')
            with open(productOriginalFile, 'r') as fp:
                for line in fp:
                    review = line.split('\t')
                    userVer = -1
                    try:
                        userVer = userVerified[review[0]]
                    except KeyError as e:
                        missingFilehandle.write(category)
                        missingFilehandle.write("\t")
                        missingFilehandle.write(Product)
                        missingFilehandle.write("\t")
                        missingFilehandle.write(review[0])
                        missingFilehandle.write("\n")
                        pass
                    reviewnew = line.split('\r')
                    newline = str(str(reviewnew[0])+'\t'+str(userVer))
                    filehandle.write(newline)
                    filehandle.write("\n")
                filehandle.close()

    return
def sanityCheck(verfied_directory, original_dataset, output_dictionary):
    
    return
#----------------------------------------------------------------------------------
import sys
import os
#----------------------------------------------------------------------------------

if __name__ == "__main__":
    x = str(sys.argv[1])
    y = str(sys.argv[2])
    z = str(sys.argv[3])
    sys.stdout.write(str(createNewVerifiedDataset(x,y,z)))
