import networkx as nx
import itertools
import matplotlib.pyplot as plt


def rda_algorithm():
    # 네트워크를 인접 행렬로 표현
    adj_matrix = [
        [0, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 0, 0],
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0]
    ]

    # 유향 그래프 생성
    G = nx.DiGraph()
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                G.add_edge(i + 1, j + 1)

    # 그래프 시각화
    node_positions = {
        1: (0, 1), 2: (1, 0), 3: (1, 2),
        4: (2, 0), 5: (2, 2), 6: (3, 1)
    }
    plt.figure()
    nx.draw(G, pos=node_positions, with_labels=True, node_size=500, node_color="lightblue", arrowsize=20)
    plt.title("Graph Visualization")
    plt.show()

    # 소스 노드와 종단 노드 정의
    source = 1
    terminal = 6

    # 그래프 분해 및 신뢰도 계산
    reliability = evaluate_network_reliability(G, source, terminal)
    disjoint_cut_sets, failure_probability = calculate_disjoint_cut_sets_and_failure_probability(G, source, terminal)

    # 결과 출력
    print("\nDisjoint Link Sets (by m-th order decomposition):")
    for i, path in enumerate(find_mth_order_paths(G.copy(), source, terminal), start=1):
        print(f"Path {i}: {path}")

    print("\nNetwork Reliability: {:.4f}".format(reliability))

    print("\nDisjoint Cut Sets:")
    for i, cut_set in enumerate(disjoint_cut_sets, start=1):
        print(f"Cut Set {i}: {cut_set}")

    print("\nNetwork Failure Probability: {:.4f}".format(failure_probability))


# BFS를 사용하여 소스에서 종단까지의 최단 경로 찾기
def bfs_shortest_path(G, source, terminal):

    parents = {source: None}
    for u, v in nx.bfs_edges(G, source):
        if v not in parents:
            parents[v] = u
        if v == terminal:
            break

    path = []
    current = terminal
    while current is not None:
        path.append(current)
        current = parents[current]

    return path[::-1]


# 그래프를 m차로 분해하여 모든 사건(최단 경로)을 식별
def find_mth_order_paths(G, source, terminal):

    paths = []
    remaining_nodes = set(G.nodes())

    while nx.has_path(G, source, terminal):
        shortest_path = bfs_shortest_path(G, source, terminal)
        if not shortest_path:
            break
        paths.append(shortest_path)

        # 현재 경로의 중간 노드 제거
        for node in shortest_path[1:-1]:
            if node in remaining_nodes:
                remaining_nodes.remove(node)

        # 남은 노드로 그래프 재구성
        G = G.subgraph(remaining_nodes).copy()

    return paths


# 네트워크 신뢰도 평가
def evaluate_network_reliability(G, source, terminal):
    example_probabilities = {1: 0.95, 2: 0.9, 3: 0.85, 4: 0.9, 5: 0.8, 6: 0.95}
    paths = find_mth_order_paths(G.copy(), source, terminal)

    total_reliability = 0
    path_probabilities = []

    # 각 경로의 확률 계산
    for path in paths:
        path_probability = 1
        for node in path[1:-1]:  # 소스/종단 노드 제외
            path_probability *= example_probabilities[node]
        path_probabilities.append(path_probability)

    # 교집합 기반 조정
    for r in range(1, len(path_probabilities) + 1):
        for subset in itertools.combinations(path_probabilities, r):
            subset_probability = 1
            for prob in subset:
                subset_probability *= prob

            if r % 2 == 1:
                total_reliability += subset_probability
            else:
                total_reliability -= subset_probability

    return total_reliability


# Disjoint Cut Set 식별 및 네트워크 실패 확률
def calculate_disjoint_cut_sets_and_failure_probability(G, source, terminal):
    
    example_failure_probabilities = {1: 0.05, 2: 0.1, 3: 0.15, 4: 0.1, 5: 0.2, 6: 0.05}
    all_nodes = list(G.nodes())
    all_nodes.remove(source)
    all_nodes.remove(terminal)

    disjoint_cut_sets = []
    failure_probability = 0

    # 가능한 모든 노드 조합 탐색
    for r in range(1, len(all_nodes) + 1):
        for node_subset in itertools.combinations(all_nodes, r):
            G_copy = G.copy()
            G_copy.remove_nodes_from(node_subset)

            # 소스에서 종단까지 이어진 경로가 없으면 Cut Set으로 간주
            if not nx.has_path(G_copy, source, terminal):
                # 새로운 Cut Set이 기존 Cut Sets와 독립적인지 확인
                if all(set(node_subset).isdisjoint(existing) for existing in disjoint_cut_sets):
                    disjoint_cut_sets.append(set(node_subset))

                    # 실패 확률 계산
                    set_probability = 1
                    for node in node_subset:
                        set_probability *= example_failure_probabilities[node]
                    failure_probability += set_probability

    return disjoint_cut_sets, failure_probability



rda_algorithm()
