import sys
import math
import testPromoter
__author__ = 'khabbabsultra'



class leaf:
    '''
        This would be at the end of the tree
        would hold either of the two boolean values
        in self.value.
    '''
    def __init__(self,value):
        self.value = value

class node:

    '''
     2


    '''
    def __init__(self, attribute):
        self.attribute = attribute
        self.children = []


# this will hold all the columns with
# with the key being the column index
# this will only hold the attributes
col = {}

# this dictionary will hold the boolean
# values
boolCol = {}


# the 2 different booleans.
testPromoter.diffBool = []


def fileInput():

    with open(sys.argv[1]) as f:
        for index, line in enumerate(f):
            splitBySpace = line.split(' ')
            boolCol.setdefault(index,splitBySpace[1].replace('\n',''))

            # the split by comma is only for the
            # test case, in validation and training
            # there are no commas.
            data = splitBySpace[0].split(',')

            # data = splitBySpace[0] # used for the actually example.
            for wordIndex ,atrribute in enumerate(data):
                if col.get(wordIndex) == None:
                    col.setdefault(wordIndex, [atrribute])
                else:
                    col.get(wordIndex).append(atrribute)
                # col.setdefault(index,[].append(data[index]))

        boolValues = boolCol.values()
        for i, atrCol in enumerate(col.values()):
            # print type(atrCol)
            col.__setitem__(i,zip(atrCol,boolValues))

        testPromoter.diffBool = list(set(boolCol.values()))
        # print boolCol
        print col
        # print "entropy (3,2): "+str(getEntropy(2.0,3.0))


# def getEntropy(pos, neg):
#     """
#     takes two values positive and negative
#     returns the entropy
#     returns a float
#     """
#     # countEach = dict(zip(attrList,map(attrList.count,attrList)))
#     # indexEach = countEach.iterkeys()
#     total = neg + pos
#     if neg != 0.0 and pos != 0.0:
#         return -((pos / total)*math.log(pos/total, 2) + (neg / total)*math.log(neg/total, 2))
#     else:
#         return 0.0


def ent(listTuple, targetAttr):

    total = float(len(filter(lambda x: x[0] == targetAttr,listTuple)))

    # print [i[1] for i in listTuple if i[1] == testPromoter.diffBool[1]]
    # checks to see how many times a certain boolean appears.
    checkBool = float(len([i[1] for i in listTuple if i[1] == testPromoter.diffBool[0] and i[0] == targetAttr]))

    print 'in ent'
    print total
    print checkBool

    if checkBool != 0.0 and checkBool != total:
        otherBool = total - checkBool
        return -((checkBool / total)*math.log(checkBool/total, 2) + ((otherBool) / total)*math.log(otherBool/total, 2))
    else:
        return 0.0


def getGain(manEnt, indList, targetAttrCol):

     """
     returns the gain using a main entropy which is being compared to
     the attribute in the attrCol.

     This function is not to get the overall gain, that will be calculated
     separately. This only for the tree nodes.

     example:
        this calculates the Gain(Sunny,Wind) from our tennis example.
        getGrain(0.97, [1,2,8,9,11], ['Weak','Strong','Weak'...] )
     """
     #list of different elements in attrCol
     #would return ['High','Normal']
     # when attrCol contains all the
     #wind attributes

     listOfElems = [i[0] for i in targetAttrCol]

     setOfElems = set([i[0] for i in targetAttrCol])

     countElements = [(float(listOfElems.count(i)),i) for i in setOfElems]

     indAttrCol = [targetAttrCol[j] for j in indList]

     totalElems = float(len(listOfElems))

     subEnt = 0.0
     for i in countElements:
         subEnt+=(i[0]/totalElems)*ent(indAttrCol,i[1])

     # for i in difElements:
     print countElements
     return manEnt - subEnt


if __name__ == '__main__':
    fileInput()