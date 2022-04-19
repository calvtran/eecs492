#  _____    ______              _____      __  __   ______
# |  __ \  |  ____|     /\     |  __ \    |  \/  | |  ____|
# | |__) | | |__       /  \    | |  | |   | \  / | | |__
# |  _  /  |  __|     / /\ \   | |  | |   | |\/| | |  __|
# | | \ \  | |____   / ____ \  | |__| |   | |  | | | |____
# |_|  \_\ |______| /_/    \_\ |_____/    |_|  |_| |______|

'''
INSTRUCTIONS:
To run: $python dt.py [dataSetName]
Ex: $python dt.py set0.data
'''

import sys
import math


def read_input():
    '''
    We've done all of the file parsing here for you, since
    tedious file I/O is not the goal of this project.
    '''
    
    features = [] # all the attributes (as class objects)
    data = [] # all the data points
    dataSetName = "DATA SET NAME NOT INITIALIZED"

    with open(str(sys.argv[1]), 'r') as inFile:
        dataMode=False
        for line in inFile:
            if line[0] == "%":
                0  # do nothing
            elif line[:9] == "@relation":
                dataMode=False
                dataSetName = line[10:]
            elif line[:10] == "@attribute":
                dataMode=False
                newFeature = Feature()
                string = line[11:].split()
                newFeature.name = string[0]
                for val in string[1:]:
                    newFeature.vals.append(val.strip(','))
                newFeature.vals[-1] = newFeature.vals[-1][:-1]  # remove }
                newFeature.vals[0] = newFeature.vals[0][1:]  # remove {
                features.append(newFeature)
            elif line[:5] == "@data":
                dataMode = True
            elif dataMode == True:
                data.append([])
                for word in line.strip().split(','):
                    data[-1].append(word)
                data[-1][-1] = data[-1][-1].replace('\r\n', '')  # remove \r\n

    # print what was input to the program
    print("I found these attributes:")
    for feature in features:
        feature.debugInfo()
    print("\nI found these datapoints:")
    for datum in data:
        print ("  " + str(datum))

    return features, data, dataSetName



'''
class to pair attribute names with all allowed values
It's named "feature" to not be confused with "attribute" in the Node class
the attribute in Node class is of type string
'''
class Feature:
    def __init__(self):
        self.name = "  "
        self.vals = []

    def debugInfo(self):
        print("  "+self.name+str(self.vals))


class Node:
    def __init__(self,depth,attribute,attributeValue,dataPoints):

        # Values set on construction:
        self.depth=depth#depth of the node 0 is root (whole dataset)
        self.data=dataPoints#the list of data points belonging to this node
        self.children=[]#the list of Nodes that are children to this one

        # attribute is a string and not a Feature class because it has ONE value
        # the Feature class includes ALL possible values for input parsing.
        self.attribute = attribute#the attribute (e.g. color)
        self.attributeValue=attributeValue#the attribute VALUE (e.g. purple)


        # Value that must be set manually each time:
        self.category="NULL"#the category to assign at end (only for leaves)

        # the list of all attribute VALUES that were already selected before now
        # useful for knowing which can still be selected by
        self.ancestors=[]

    '''
    This will print the "pretty" version of the tree to file and terminal
    DO NOT CHANGE THIS!  This is 95% of the reason for the skeleton.
    This ensures that your program will output in the format we expect.
    '''
    def output_dt(self):
        string = ("|   " * (self.depth-1) + self.attribute + " = "
                + self.attributeValue + ": " + self.category + " ("
                + str(len(self.data)) + ")\n")
        if self.children==[]:
            return string
        for x in self.children:
            string = string + x.output_dt()
        return string

    '''
    This will print all the info of a Node and its children to terminal
    Use this only for debugging if necessary.
    '''
    def debugInfo(self):
        if self.children==[]: # leaf node
            print(self.attribute+":"+self.attributeValue
                  +"; depth="+str(self.depth)
                  +"; ancestors="+str(self.ancestors)
                  +"; cat="+str(self.category)+";\n"
                  +"data=" + str(self.data)+"\n")
        else:
            print(self.attribute+":"+self.attributeValue
                  +"; depth="+str(self.depth)
                  +"; ancestors=" + str(self.ancestors)+";\n"
                  +"data=" + str(self.data)+"\n")
        for c in self.children:
            c.debugInfo()

    '''
    This creates a child of the node it is called on.
    It requires the attribute, value, and data to populate itself.
    It sets the depth correctly to be one more than parent
    It places the child in the list of children of the parent.
    '''
    def createChild(self,attribute,attributeValue,dataPoints):
        self.children.append(Node(self.depth+1,attribute,
                                  attributeValue,dataPoints))
        self.children[-1].ancestors=self.ancestors+[self.attribute+":"+self.attributeValue]
        return self.children[-1]#returns child (by reference b/c Python)



# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
# Fill in recursive algorithm here
def ID3(Node, features):
    print("The ID3 algorithm is not yet implemented.\n"
          +"This was a hardcoded run.")


    ###### TODO: Implement this function ########
    # print(features[0].name)
    # Node.debugInfo()
    # Create root node for tree
    # rootNode = Node(0, "root", "ROOT", Node.data)
    # rootNode.debugInfo()
    bestEntropy = math.inf
    bestAttr = None
    for att in range(len(features)):
        counts = {}
        for ex in Node.data:    
            if ex[att] not in counts:
                counts[ex[att]] = 1
            else:
                counts[ex[att]] += 1
        print(features[att].name, counts)
        print(features[att].vals)
        currEntropy = calcEntropy(counts)
        if currEntropy < bestEntropy:
            bestEntropy = currEntropy
            bestAttr = (features[att].name, att)    # ( feature_name, feature_index )
            attrValue = max(counts, key= lambda x: counts[x])
    
    print("Best attr:", bestAttr[0])
    print("attrValue =", attrValue)
    childData = []
    for ex in Node.data:
        if ex[bestAttr[1]] == attrValue:
            childData.append(ex)
    # print("childData =", childData)
    childNode = Node.createChild(bestAttr[0], attrValue, childData)
    # ID3(childNode, features)

def calcEntropy(counts):
    h = 0
    total = sum(counts.values())
    for k in counts:
        p = counts[k] / total
        # print("p =", p)
        h -= p * math.log2(p)
    print("H =", h)
    return h

def calcIG(counts):
    r = 0
    total = sum(counts.values())
    for k in counts:
        p = counts[k] / total
        r += p * calcEntropy(counts)
    return calcEntropy(counts) - r

def main():
    
    if len(sys.argv)!=2:
        print("ERROR: I need one argument, the input file.\n")

    ## read input file ##
    features, data, dataSetName = read_input()


    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # This is the main driver.  
    # You need to implement ID3 function

    rootNode=Node(0,"root","ROOT",data)
    ID3(rootNode, features)



    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

    # This is needed to print your final tree.
    dt = rootNode.output_dt()
    print(dt)


if __name__ == "__main__":
    main()
