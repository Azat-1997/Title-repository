#!/usr/bin/python

def DFS(graph, start, end):
    
    # Find path from start to end
    V = len(graph)
    # visited status
    vertices = [0] * V
    # if vertices 0 - is mean white 1 - grey, 2 - black
    # use stack to keep nodes ,instead recursive call
    stack = [start]
    vertices[start] = 1

    while stack:
        
        stack_pop_status = True
            
        node = stack[-1]
    # if we didn't find unvisited nodes, we remove current node from stack and return to previous one
    
        if stack_pop_status:
            # remove vertices and dye to black
            vertices[node] == 2
            stack.pop()

    # mark the node
        if node == end:
            return True
    
        for neigbore in graph[node]:
        
            if vertices[neigbore] == 0:
                # add node and go deeper
                stack.append(neigbore)
                stack_pop_status = False
                vertices[neigbore] = 1
            
        
            
    return False
