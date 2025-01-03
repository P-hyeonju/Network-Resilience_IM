import networkx as nx
import matplotlib.pyplot as plt

def find_disjoint_linksets():
    # 네트워크를 행렬로 표현
    adj_matrix = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    # 유향 그래프 생성
    G = nx.DiGraph()  # 방향성 그래프
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(i + 1, j + 1)  # 노드를 1부터 표현하기 위해

    # 노드 좌표 설정
    node_positions = {
        1: (0, 1), 2: (1, 0), 3: (1, 2),
        4: (2, 0), 5: (2, 2), 6: (3, 1)
    }

    # 네트워크 plot
    plt.figure()
    nx.draw(G, pos=node_positions, with_labels=True)
    plt.show()
    
    # 소스 노드와 종단 노드 정의
    source = 1
    terminal = 6

    # link sets 찾기
    linksets = find_all_paths(G, source, terminal)
    disjoint_link_sets = []
    used_links = set()
    
    for path in linksets:
        is_disjoint = True
        current_links = set()
        
        for i in range(len(path) - 1):
            link = (path[i], path[i + 1])
            current_links.add(link)
            
        if current_links & used_links:
            is_disjoint = False
        
        if is_disjoint:
            disjoint_link_sets.append(path)
            used_links.update(current_links)
            
    
    # disjoint link sets 나타내기
    print("Disjoint Link Sets:")
    for i, path in enumerate(disjoint_link_sets, start=1):
        print(f"Path {i}: {path}")
            
    return disjoint_link_sets

        
        
        
def find_all_paths(G, source, terminal):
    paths = []
    stack = [[source]]
    
    while stack:
        current_path = stack.pop()
        current_node = current_path[-1]
        
        if current_node == terminal:
            paths.append(current_path)
        else:
            neighbors = list(G.successors(current_node))
            for neighbor in neighbors:
                if neighbor not in current_path:
                    stack.append(current_path + [neighbor])
    return paths

find_disjoint_linksets()