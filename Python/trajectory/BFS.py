#!/usr/bin/python
def BFS(graph,start_node, goal_node):
    visited = [False]*len(graph) # Список посещенных узлов (вначале пуст)
    queue = [start_node] # Начинаем с узла-источника
    visited[start_node] = True
    while queue != []:    # пока мы имеем непустую очередь
        node = queue.pop(0) # извлекаем первый элемент в очереди. Метод .pop() без аргументов берет последний элемент
        if node == goal_node:
            return True # проверка на равенство узлов: если текущий равен финишному, то мы нашли путь между start_node и goal_node

        for child in graph[node]:
            if not visited[child]:
                queue.append(child)
                visited[child] = True
     
    return False # Если пройдясь по всем достижимым вершинам, мы не достигли финишной вершины - отвечаем "нет" на вопрос у сущетсвовании пути между start_node и goal_node
