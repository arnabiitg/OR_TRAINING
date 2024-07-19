def dsatur(num_vertices, edges):

    graph = [[] for _ in range(num_vertices)]
    for (u, v) in edges:
        graph[u].append(v)
        graph[v].append(u)
    
    colors = [-1] * num_vertices  
    saturation = [0] * num_vertices 
    degrees = [len(graph[i]) for i in range(num_vertices)]  


    def select_vertex():
        max_sat = max([saturation[v] for v in range(num_vertices) if colors[v] == -1])
        candidates = [v for v in range(num_vertices) if colors[v] == -1 and saturation[v] == max_sat]

        if len(candidates) == 1:
            return candidates[0]
        else:
            return max(candidates, key=lambda v: degrees[v])
    
    current_vertex = max(range(num_vertices), key=lambda v: saturation[v])
    colors[current_vertex] = 0
    
    while -1 in colors:
        for neighbor in graph[current_vertex]:
            if colors[neighbor] == -1:
                unique_colors = set(colors[adj] for adj in graph[neighbor] if colors[adj] != -1)
                saturation[neighbor] = len(unique_colors)
        
        current_vertex = select_vertex()
        
        available_colors = [True] * num_vertices
        for neighbor in graph[current_vertex]:
            if colors[neighbor] != -1:
                available_colors[colors[neighbor]] = False
        colors[current_vertex] = available_colors.index(True)
    
    return colors

