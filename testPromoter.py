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
    def __init__(self,attribute, name):
        self.attribute = attribute
        self.name = name

    def __repr__(self,level=0):
        ret = "\t"*level+repr(self.name + '==>' +self.attribute)+"\n"
        return ret
class node:

    '''
     2
    '''
    def __init__(self, attribute):
        self.attribute = attribute
        self.name = ''
        self.children = []

    def __repr__(self, level=0):
        ret = "\t"*level+repr(str(self.attribute)+'==>'+self.name)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret



# this will hold all the columns with
# with the key being the column index
# this will only hold the attributes
col = {}

# this dictionary will hold the boolean
# values
boolCol = {}


# the 2 different booleans.
testPromoter.diffBool = []

# testPromoter.root = None

def fileInput():

    with open(sys.argv[1]) as f:
        for index, line in enumerate(f):
            splitBySpace = line.split(' ')
            boolCol.setdefault(index,splitBySpace[1].replace('\n',''))

            # the split by comma is only for the
            # test case, in validation and training
            # there are no commas.
            # data = splitBySpace[0].split(',')

            data = splitBySpace[0] # used for the actually example.
            for wordIndex ,atrribute in enumerate(data):
                if col.get(wordIndex) == None:
                    col.setdefault(wordIndex, [atrribute])
                else:
                    col.get(wordIndex).append(atrribute)
                # col.setdefault(index,[].append(data[index]))

        boolValues = boolCol.values()
        for i, atrCol in enumerate(col.values()):

            col.__setitem__(i,zip(atrCol,boolValues))

        testPromoter.diffBool = list(set(boolCol.values()))

        totalVal =  len(boolCol.values())
        pos = len([i for i in boolCol.values() if i == testPromoter.diffBool[0]])

        totalSystemEnt =  round(getEntropy(float(pos),float(totalVal - pos)),2)

        # tempRange = range(0, totalVal)
        # getMainGains = [getGain(totalSystemEnt,tempRange, col[i]) for i in col]


        # maxGainIndex = getMainGains.index(max(getMainGains))




        root = start_tree(range(0,totalVal), totalSystemEnt)

        print root

        if len(sys.argv) == 3:
            runValidation(root,sys.argv[2])





def runValidation(root, file):


    with open(file) as f:
        for line in f:
            print line




def validateLine():
    pass



def start_tree(indRange,entropy):


    gains = [getGain(entropy,indRange,col[i]) for i in col]

    # print gains
    # print '\n'
    indexOfMaxGain = gains.index(max(gains))

    listOfTuple = [col[indexOfMaxGain][i] for i in indRange ]

    listOfElems = [i[0] for i in listOfTuple]

    setOfElems = set(listOfElems)




    countElements = [(float(listOfElems.count(i)),i) for i in setOfElems]

    # listOfTuple = [col[indexOfMaxGain][i] for i in indRange ]

    myNode = node(indexOfMaxGain)



    col[indexOfMaxGain] = []
    # print myNode
    for attr in setOfElems:

        # if len(setOfElems) == 1:
        #     myNode.name = attr

        # print len(setOfElems)
        tempEnt = ent(listOfTuple, attr)
        if tempEnt == 0.0:
            #would return a leaf


            temp = [i[1] for i in listOfTuple if i[0] == attr]
            if len(temp) != 0.0:
                # print 'leafNode, at ' + attr + " ==> "+temp[0]
            #returns a leaf node with one of the boolean values
            #has the value

                myNode.children.append(leaf(temp[0], attr))
            else:
                print attr
                print listOfTuple
                myNode.children.append(leaf('here', attr))
        else:
            # would return node
            # print 'Node at '+ attr
            # print 'ent: '+ str(tempEnt)
            indtemp = [i for i,j in enumerate(listOfTuple) if j[0] == attr]
            # print indtemp
            # myNode.name = attr
            tempNode = start_tree(indtemp,tempEnt)
            tempNode.name = attr
            myNode.children.append(tempNode)



    return myNode




def grow_tree(listOfTuple, colIndex):


    listOfElems = [i[0] for i in listOfTuple]




    # if len(set([i[1] for i in listOfTuple])) == 1:
    #     return leaf(listOfElems[0][1])
    #
    # else:

    setOfElems = set(listOfElems)

    countElements = [(float(listOfElems.count(i)),i) for i in setOfElems]

    for i in setOfElems:
        # print 'entropy for ' + i
        tempEnt = ent(listOfTuple, i)
        if tempEnt == 0.0:
            #would return a leaf
            print 'leafNode, at ' + i
        else:
            # would return node
            print 'Node at '+ i
            print 'ent: '+ str(tempEnt)








def getEntropy(pos, neg):
    """
    takes two values positive and negative
    returns the entropy
    returns a float
    """
    # countEach = dict(zip(attrList,map(attrList.count,attrList)))
    # indexEach = countEach.iterkeys()
    total = neg + pos
    if neg != 0.0 and pos != 0.0:
        return -((pos / total)*math.log(pos/total, 2) + (neg / total)*math.log(neg/total, 2))
    else:
        return 0.0


def ent(listTuple, targetAttr):

    total = float(len(filter(lambda x: x[0] == targetAttr,listTuple)))

    # print [i[1] for i in listTuple if i[1] == testPromoter.diffBool[1]]
    # checks to see how many times a certain boolean appears.
    checkBool = float(len([i[1] for i in listTuple if i[1] == testPromoter.diffBool[0] and i[0] == targetAttr]))

    # print 'in ent :' + targetAttr
    # print total
    # print checkBool

    if checkBool != 0.0 and checkBool != total:
        otherBool = total - checkBool

        temp = -((checkBool / total)*math.log(checkBool/total, 2) + ((otherBool) / total)*math.log(otherBool/total, 2))
        # print temp
        return temp

        # if the entropy is going to be zero it should
        # return the boolean value ['yes','no'] ['+','-']
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
     if len(targetAttrCol) == 0:
         return 0.0
     else:
        listOfElems = [i[0] for i in targetAttrCol]

        setOfElems = set([i[0] for i in targetAttrCol])

        countElements = [(float(listOfElems.count(i)),i) for i in setOfElems]

        indAttrCol = [targetAttrCol[j] for j in indList]

        totalElems = float(len(listOfElems))

        subEnt = 0.0
        for i in countElements:
            entValue = ent(indAttrCol,i[1])

        # fix this
        #     if type(entValue) != 'str':
            subEnt+=(i[0]/totalElems)*entValue


     # for i in difElements:
     # print countElements
        return manEnt - subEnt



if __name__ == '__main__':
    fileInput()