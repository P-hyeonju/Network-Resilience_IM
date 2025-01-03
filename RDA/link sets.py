import networkx as nx
import matplotlib.pyplot as plt

def find_linksets():
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
                G.add_edge(i + 1, j + 1)  # MATLAB 인덱스 기반이므로 +1

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
    
    # link sets 나타내기
    print("Link Sets:")
    for i, path in enumerate(linksets, start=1):
        print(f"Path {i}: {path}")
        
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

find_linksets()