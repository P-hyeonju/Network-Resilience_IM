import networkx as nx
import matplotlib.pyplot as plt

def find_cut_sets():
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

    # cut sets 찾기
    cutsets = find_cut_sets(G, source, terminal)
    
    
def find_cut_sets(G, source, terminal):
    
    all_edges = list(G.edges())
    cutsets = []
    
    for r in range(1, len(all_edges) + 1):
        for 
    