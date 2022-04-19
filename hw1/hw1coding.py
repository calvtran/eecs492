# -*- coding: utf-8 -*-
"""
Homework 1 EECS 492 Coding Portion
"""
# Use the given functions, importing different ones will not work on the autograder
from typing import Dict
import numpy as np
import json
import queue

# Create a node class used to keep track of the parent of a visited item and its cost.
# Note you only need this class for baconbfs and A* functions, not bfs.
# You also need to implement methods so this node object can be used in a 
# priority queue (useful in A*)
class Node:
    # Initialize the node object and store the name, parent, and cost in self.
    def __init__(self, name, parent, cost=1):
        self.name = name
        self.parent = parent
        self.cost = cost
    
    # Return the parent node of this object
    def getParent(self):
        return self.parent
    
    # Return the name or label stored in this node object.
    def getName(self):
        return self.name
    
    # Return the cost stored in this node object.
    def getCost(self):
        return self.cost

    # Return a boolean value that is True if this node object's cost is less than
    # the "other" node's cost. False otherwise.
    def __lt__(self, other):
        return (self.cost < other.cost)
    
    # Return a boolean value that is True if this node object's cost is greater than
    # the "other" node's cost. False otherwise.
    def __gt__(self, other):
        return (self.cost > other.cost)
    
    # Return a boolean value that is True if this node object's cost is equal to
    # the "other" node's cost. False otherwise.
    def __eq__(self, other):
        return (self.cost == other.cost)
    
        
# Here we define our graph object that has three functions associated with it.
# Construct a graph and call each method to explore different types of 
# search.
class Graph:
    
    def __init__(self):
        self.graph={
            0:[1,2],
            1:[0,3],
            2:[0,3,5],
            3:[1,2,4,5],
            4:[3,5,6],
            5:[2,3,4,6,7,8],
            6:[4,5,7],
            7:[5,6,8,9],
            8:[5,7],
            9:[7]
            }
        self.adjmatrix=np.array(
                        [[0, 1, 3, 0, 0, 0, 0, 0, 0, 0],
                        [1, 0, 0, 3, 0, 0, 0, 0, 0, 0],
                        [3, 0, 0, 4, 0, 7, 0, 0, 0, 0],
                        [0, 3, 4, 0, 4, 2, 0, 0, 0, 0],
                        [0, 0, 0, 4, 0, 1, 2, 0, 0, 0],
                        [0, 0, 7, 2, 1, 0, 7, 5, 1, 0],
                        [0, 0, 0, 0, 2, 7, 0, 4, 0, 0],
                        [0, 0, 0, 0, 0, 5, 4, 0, 5, 1],
                        [0, 0, 0, 0, 0, 1, 0, 5, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]])
        
        self.heuristic=np.array([
       [ 0.,  0.,  2.,  3.,  6.,  5.,  8., 10.,  6., 11.],
       [ 0.,  0.,  3.,  2.,  5.,  4.,  7.,  9.,  5., 10.],
       [ 2.,  3.,  0.,  3.,  6.,  5.,  8., 10.,  6., 11.],
       [ 3.,  2.,  3.,  0.,  2.,  1.,  4.,  6.,  2.,  7.],
       [ 6.,  5.,  6.,  2.,  0.,  0.,  1.,  5.,  1.,  6.],
       [ 5.,  4.,  5.,  1.,  0.,  0.,  2.,  4.,  0.,  5.],
       [ 8.,  7.,  8.,  4.,  1.,  2.,  0.,  3.,  3.,  4.],
       [10.,  9., 10.,  6.,  5.,  4.,  3.,  0.,  4.,  0.],
       [ 6.,  5.,  6.,  2.,  1.,  0.,  3.,  4.,  0.,  5.],
       [11., 10., 11.,  7.,  6.,  5.,  4.,  0.,  5.,  0.]])

        with open('bacon.json', 'r') as infile:
            self.bacon = json.load(infile)
    
    # Use self.graph to implement breadth first search. Return the list of expanded
    # nodes (in integer form). Start and end are each an integer representing a label in the graph.
    # If you cannot find a path return the expanded list.
    def bfs(self, start, end):
        node = start
        frontier = queue.Queue()
        frontier.put(start)
        reached = [start]
        expanded = []

        if node == end:
            return expanded
        while not frontier.empty():
            node = frontier.get()
            children = self.graph[node]
            expanded.append(node)
            for ch in range(len(children)):
                child = children[ch]
                if child == end:
                    return expanded
                if child not in reached:
                    reached.append(child)
                    frontier.put(child)

        return expanded
                
    
    # First, implement the Node class given above.
    # Adapt breadth first search into a Bacon Number calculator using
    # Node objects to keep track of parents. Start and end are both names of
    # actors or actresses. In order to calculate the Bacon number use Kevin 
    # Bacon as end. Return the path (in integer form) from start to end. Use self.bacon as the
    # graph for this part of the assignment.
    # If you cannot find a path return the expanded list.
    def bacon_bfs(self, start, end):
        g = self.bacon
        node = Node(start, None)
        frontier = queue.Queue()
        frontier.put(node)
        reached = [node.getName()]
        expanded = []

        if node.getName() == end:
            return []
        while not frontier.empty():
            node = frontier.get()
            children = g[node.getName()]
            expanded.append(node)
            for ch in range(len(children)):
                child = Node(children[ch], node)
                if child.getName() == end:
                    path = [end]
                    parent = child.getParent()
                    while parent.getName() != start:
                        path.insert(0, parent.getName())
                        parent = parent.getParent()

                    path.insert(0, start)
                    return path

                if child.getName() not in reached:
                    reached.append(child.getName())
                    frontier.put(child)


        return expanded
    
    
    # Implement the A* algorithm on self.graph also using self.adjmatrix to retrieve
    # weights in the graph and self.heuristic as the heuristics for the graph. 
    # Start and end are both integers representing the name of the node to
    # start and end at. Hint: queue.PriorityQueue() is helpful. Return the path
    # (in integer form) from start to end. 
    # If you cannot find a path return the expanded list.
    def Astar(self, start, end):
        e_weight = self.adjmatrix
        h = self.heuristic
        pq = queue.PriorityQueue()
        trace : Dict[int, int] = {}
        trace[start] = None
        cost_so_far: Dict[int, int] = {}
        cost_so_far[start] = 0
        expanded = []
        
        node = Node(start, None, 0)

        if node.getName() == end:
            return [start]

        cost = e_weight[start, start] + h[start, start]
        pq.put((cost, node))

        while not pq.empty():
            node = pq.get()[1]
            curr = node.getName()

            children = self.graph[curr]
            expanded.append(curr)
            for c in range(len(children)):
                child = children[c]
                new_cost = cost_so_far[curr] + e_weight[curr, child]

                if child not in cost_so_far or new_cost < cost_so_far[child]:
                    cost_so_far[child] = new_cost
                    cost = new_cost + h[child, end]
                    pq.put((cost, Node(child, node, cost)))
                    trace[child] = curr

                    if child == end:
                        path = [end]
                        p = trace[child]
                        while p != None:
                            path.insert(0, p)
                            p = trace[p]
                        return path
        return expanded
                
            
# Main method showing examples of how to run each function 
if __name__=="__main__":
    g=Graph()
    bfs = g.bfs(0,9)
    # print("bfs =", bfs)
    b_bfs = g.bacon_bfs('Robin Williams', 'Kevin Bacon')
    # print("b_bfs =", b_bfs)
    astar = g.Astar(3,4)
    print("astar =", astar)
        
        
        
        
        
        
        
        