import networkx as nx
import matplotlib.pyplot as plt
import math


def s_rda_algorithm():
    # 네트워크를 인접 행렬로 표현
    adj_matrix = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    # 노드 신뢰도 정의
    node_reliabilities = {1: 0.95, 2: 0.9, 3: 0.85, 4: 0.9, 5: 0.8, 6: 0.95}

    # 유향 그래프 생성
    G = nx.DiGraph()
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                # 가중치로 노드 신뢰도를 음의 로그로 변환하여 설정
                G.add_edge(i + 1, j + 1, weight=-math.log(node_reliabilities[j + 1]))

    # 노드 위치 설정
    node_positions = {
        1: (0, 1), 2: (1, 0), 3: (1, 2),
        4: (2, 0), 5: (2, 2), 6: (3, 1)
    }

    # 네트워크 시각화
    plt.figure()
    nx.draw(G, pos=node_positions, with_labels=True)
    plt.show()

    # 소스와 종단 노드 정의
    source = 1
    terminal = 6

    # 가장 신뢰할 수 있는 경로 식별
    most_reliable_path, path_reliability = find_most_reliable_path(G, source, terminal, node_reliabilities)

    print(f"Most Reliable Path: {most_reliable_path}")
    print(f"Path Reliability: {path_reliability:.4f}")


# 가장 신뢰할 수 있는 경로
def find_most_reliable_path(G, source, terminal, node_reliabilities):

    # 노드 신뢰도를 기반으로 음의 로그 값 사용
    reliability_labels = {node: -math.inf for node in G.nodes()}  # 초기값: 매우 낮은 신뢰성
    reliability_labels[source] = math.log(node_reliabilities[source])  # 소스 노드 초기값

    permanently_labeled = set()  # 영구적으로 라벨된 노드
    temporarily_labeled = set(G.nodes())  # 임시 라벨된 노드

    predecessors = {}  # 경로 재구성을 위한 부모 노드 저장

    while temporarily_labeled:
        # 임시 라벨된 노드 중 가장 높은 신뢰도를 가진 노드 선택
        current_node = max(temporarily_labeled, key=lambda node: reliability_labels[node])

        if reliability_labels[current_node] == -math.inf:
            break  # 연결되지 않은 노드가 남아있을 경우 중단

        permanently_labeled.add(current_node)
        temporarily_labeled.remove(current_node)

        # 종단 노드에 도달하면 종료
        if current_node == terminal:
            break

        # 현재 노드와 연결된 이웃 노드들의 라벨 업데이트
        for neighbor in G.successors(current_node):
            if neighbor not in permanently_labeled:
                new_reliability = reliability_labels[current_node] + math.log(node_reliabilities[neighbor])
                if new_reliability > reliability_labels[neighbor]:
                    reliability_labels[neighbor] = new_reliability
                    predecessors[neighbor] = current_node

    # 경로 재구성
    path = []
    current = terminal
    while current in predecessors or current == source:
        path.insert(0, current)
        current = predecessors.get(current, None)

    # 경로 신뢰도 계산
    path_reliability = math.exp(reliability_labels[terminal]) if terminal in permanently_labeled else 0

    return path, path_reliability


# S-RDA 알고리즘 실행
s_rda_algorithm()
