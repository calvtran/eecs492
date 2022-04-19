
'''
INSTRUCTIONS: This is a DEMO example of how to use the NODE class correctly.
To run: $python dt_demo.py 
'''

from dt import Node


def main():

    # $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    # DEMO OF NODE CLASS: look at this closely to see how to use the Node class.


    # hardcoded data for demonstrating the Node class on set 1
    # of course in your code these will be created by the ID3 algorithm instead
    dataPoints=[['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                ['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                ['YELLOW', 'SMALL', 'STRETCH', 'CHILD', 'F'],
                ['YELLOW', 'SMALL', 'DIP', 'ADULT', 'F'],
                ['YELLOW', 'SMALL', 'DIP', 'CHILD', 'F'],
                ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                ['YELLOW', 'LARGE', 'STRETCH', 'CHILD', 'F'],
                ['YELLOW', 'LARGE', 'DIP', 'ADULT', 'F'],
                ['YELLOW', 'LARGE', 'DIP', 'CHILD', 'F'],
                ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                ['PURPLE', 'SMALL', 'STRETCH', 'CHILD', 'F'],
                ['PURPLE', 'SMALL', 'DIP', 'ADULT', 'F'],
                ['PURPLE', 'SMALL', 'DIP', 'CHILD', 'F'],
                ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                ['PURPLE', 'LARGE', 'STRETCH', 'CHILD', 'F'],
                ['PURPLE', 'LARGE', 'DIP', 'ADULT', 'F'],
                ['PURPLE', 'LARGE', 'DIP', 'CHILD', 'F']]
    stretchData=[['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                 ['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                 ['YELLOW', 'SMALL', 'STRETCH', 'CHILD', 'F'],
                 ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                 ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                 ['YELLOW', 'LARGE', 'STRETCH', 'CHILD', 'F'],
                 ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                 ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
                 ['PURPLE', 'SMALL', 'STRETCH', 'CHILD', 'F'],
                 ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                 ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T'],
                 ['PURPLE', 'LARGE', 'STRETCH', 'CHILD', 'F']]
    dipData=[['YELLOW', 'SMALL', 'DIP', 'ADULT', 'F'],
             ['YELLOW', 'SMALL', 'DIP', 'CHILD', 'F'],
             ['YELLOW', 'LARGE', 'DIP', 'ADULT', 'F'],
             ['YELLOW', 'LARGE', 'DIP', 'CHILD', 'F'],
             ['PURPLE', 'SMALL', 'DIP', 'ADULT', 'F'],
             ['PURPLE', 'SMALL', 'DIP', 'CHILD', 'F'],
             ['PURPLE', 'LARGE', 'DIP', 'ADULT', 'F'],
             ['PURPLE', 'LARGE', 'DIP', 'CHILD', 'F']]
    adultData=[['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
               ['YELLOW', 'SMALL', 'STRETCH', 'ADULT', 'T'],
               ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
               ['YELLOW', 'LARGE', 'STRETCH', 'ADULT', 'T'],
               ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
               ['PURPLE', 'SMALL', 'STRETCH', 'ADULT', 'T'],
               ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T'],
               ['PURPLE', 'LARGE', 'STRETCH', 'ADULT', 'T']]
    childData=[['YELLOW', 'SMALL', 'STRETCH', 'CHILD', 'F'],
               ['YELLOW', 'LARGE', 'STRETCH', 'CHILD', 'F'],
               ['PURPLE', 'SMALL', 'STRETCH', 'CHILD', 'F'],
               ['PURPLE', 'LARGE', 'STRETCH', 'CHILD', 'F']]


    # create a root node
    rootNode=Node(0,"root","ROOT",dataPoints)

    # debugInfo() prints all the relevant info in a node to terminal
    print("\nDEMO: Created a root node:\n")
    rootNode.debugInfo()


    # createChild() returns the created child Node (by reference b/c Python)
    childNode=rootNode.createChild("act","STRETCH",stretchData)

    # debugInfo() also prints all its' children's info
    print("\nDEMO: Whole tree After creating a child Node:\n")
    rootNode.debugInfo()

    # child Nodes can have children Nodes of their own
    grandChildNode = childNode.createChild("age","ADULT",adultData)

    # We can change properties using the returned reference (like a pointer)
    # This is needed for the category value for the leaves.
    grandChildNode.category="T"
    print("\nDEMO: This is the grandChild Node:\n")
    grandChildNode.debugInfo()


    # using " = createChild(...)" will overwrite the previous REFERENCE
    # but the previous OBJECT will stay intact
    grandChildNode = childNode.createChild("age","CHILD",childData)
    grandChildNode.category="F"
    # i.e age=ADULT still exists and is in place,
    #   but "grandChildNode" now references age=CHILD

    childNode=rootNode.createChild("act","DIP",dipData)
    childNode.category="F"

    print("\nDEMO: After finishing the tree:\n")
    rootNode.debugInfo()

    # output() will print the "pretty" version of the tree to file AND terminal
    print("\nDEMO: Final output looks like:\n")
    dt = rootNode.output_dt()
    print(dt)


if __name__ == "__main__":
    main()

