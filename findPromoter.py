import sys
import math
import numpy as np
__author__ = 'khabbabsultra'


entSys = 0.0



class Column:



    def __init__(self,colNum,line,entropyDict):
        self.line = line
        self.colNum = colNum
        self.entropyDict = entropyDict


def fileInput():

    entSys = getTotalEnt()

    print entSys

    getCols()

def getCols():

    '''loading all the cols in the dictionary
    while the lines go in the lines dictionary

    a,t,c,g

    '''
    lines = dict()
    col = dict()

    values = {'a','c','t','g'}
    indEnt = {}
    tempFloat = 0.0
    # charar = np.chararray((58,58))

    #print charar

    # loading all the columns in the col dictionary
    with open(sys.argv[1]) as f:
        for index, line in enumerate(f):
            lines.__setitem__(index,line)
            # print index
            for y, letter in enumerate(line):
                if y <= 58:
                    temp = col.get(y)
                    if temp != None:
                        col.__setitem__(y,str(temp)+letter)
                    else:
                        col.__setitem__(y,letter)

        #print col
        boolLine = col.get(58)

        for index, line in enumerate(col.itervalues()):

            if index <= 56:
                print str(index)+" : "+line
                for nucleo in values:
                # tempFloat = len(filter(lambda x: x == nucleo, line))
                    tempCount = 0.0
                    countPos = 0.0
                    countNeg = 0.0
                    for i, foo in enumerate(line):
                        if foo == nucleo:
                            tempCount+=1
                            if boolLine[i] == '+':
                                countPos+=1
                    countNeg = tempCount - countPos
                    # print nucleo+": "+str(tempCount)+"  +: "+str(countPos)+" -:"+str(countNeg)
                    probPos=countPos/tempCount
                    probNeg=countNeg/tempCount

                    if probNeg != 0.0 and probPos != 0.0:
                        # print "posProb :"+str(probPos) + " negProb :"+str(probNeg)
                        print nucleo+": "+str(-probPos*math.log(probPos,2) -probNeg*math.log(probNeg,2))


def getTotalEnt():

    totallines=0.0
    totalpos=0.0
    totalneg=0.0
    prob=[]
    with open(sys.argv[1]) as f:
        for line in f:
            totallines+=1
            if (line[58] == '+'):
                totalpos+=1
            else:
                totalneg+=1

        prob.append(totalpos / totallines)
        prob.append(totalneg / totallines)
        ent = 0.0
        for i in prob:
           ent += -i*math.log(i,2)

    return ent

if __name__ == '__main__':
    fileInput()