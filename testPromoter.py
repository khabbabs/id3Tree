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
     This is the node
     contains children which is list
     the children could either be other nodes
     or leaf nodes
    '''
    def __init__(self, attribute):
        self.attribute = attribute
        self.name = ''
        self.children = []


    # helps printing the trees in a nice format.
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



def fileInput():

    '''
        File input reads in the files loads the training set
        using a dictionary with key being the column index

        how to run:

             python testPromoter.py training.txt validation.txt
    '''

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


        boolValues = boolCol.values()
        for i, atrCol in enumerate(col.values()):

            col.__setitem__(i,zip(atrCol,boolValues))

        testPromoter.diffBool = list(set(boolCol.values()))


        # This section of code calculates
        # total system entropy
        totalVal =  len(boolCol.values())
        pos = len([i for i in boolCol.values() if i == testPromoter.diffBool[0]])
        totalSystemEnt =  round(getEntropy(float(pos),float(totalVal - pos)),2)



        # Starts building the tree
        root = grow_tree(range(0,totalVal), totalSystemEnt)

        print root

        # checks to see if there is a validation
        # set. Runs validation on the set

        if len(sys.argv) == 3:
            runValidation(root,sys.argv[2])





def runValidation(root, file):

    '''

        runs validation on each line from the validation set
        returns the statistics

    '''

    i = 0.0
    j = 0.0
    with open(file) as f:
        for line in f:
            splited = line.split(' ')
            j+=1
            if validateLine(root,splited[0]) == splited[1].replace('\n',''):
                i+=1
                if splited[1].replace('\n','') == '+':
                    print 'here'

        print "correct: " + str(i) + " total :" + str(j) +" "+ str(float(i / j) * 100)+" accuracy"



def validateLine(root, line):

    '''
        given a validation line, runs the tree data structure
        recursively, when it reaches a leaf node it returns
        the associated boolean value
    '''
    if root.__class__ is leaf:
        return root.attribute
    else:
         for child in root.children:
            if line[root.attribute] == child.name:
                return validateLine(child, line)



def grow_tree(indRange,entropy):

    '''
    grows the tree given a list of indices and an entropy
    this function grows the tree recursively.

    In the tennis example it would look something like
    grow_tree([0,1,7,9,10], 0.94)
    for the sunny attribute

    while the starting iteration for the
    tree would be grow_tree(range(0,14), 0.97)

    '''

    gains = [getGain(entropy,indRange,col[i]) for i in col]


    indexOfMaxGain = gains.index(max(gains))

    listOfTuple = [col[indexOfMaxGain][i] for i in indRange ]

    listOfElems = [i[0] for i in listOfTuple]

    setOfElems = set(listOfElems)




    myNode = node(indexOfMaxGain)



    for attr in setOfElems:

        tempEnt = ent(listOfTuple, attr)
        if tempEnt == 0.0:
            #would return a leaf
            temp = [i[1] for i in listOfTuple if i[0] == attr]
            myNode.children.append(leaf(temp[0], attr))
        else:
            # would return node
            indtemp = [i for i,j in enumerate(listOfTuple) if j[0] == attr]
            tempNode = grow_tree(indtemp,tempEnt)
            tempNode.name = attr
            myNode.children.append(tempNode)

    return myNode



def getEntropy(pos, neg):
    """
    takes two values positive and negative
    returns the entropy
    returns a float

    This is only used to calculate the total
    system entropy

    """

    total = neg + pos
    if neg != 0.0 and pos != 0.0:
        return -((pos / total)*math.log(pos/total, 2) + (neg / total)*math.log(neg/total, 2))
    else:
        return 0.0


def ent(listTuple, targetAttr):

    '''
        This calculates an entropy given a list, along with the
        the target attribute.

    '''


    total = float(len(filter(lambda x: x[0] == targetAttr,listTuple)))


    # checks to see how many times a certain boolean appears.
    checkBool = float(len([i[1] for i in listTuple if i[1] == testPromoter.diffBool[0] and i[0] == targetAttr]))


    if checkBool != 0.0 and checkBool != total:
        otherBool = total - checkBool
        temp = -((checkBool / total)*math.log(checkBool/total, 2) + ((otherBool) / total)*math.log(otherBool/total, 2))
        return temp
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
            subEnt+=(i[0]/totalElems)*entValue

        return manEnt - subEnt



if __name__ == '__main__':
    fileInput()