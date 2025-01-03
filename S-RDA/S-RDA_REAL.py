import networkx as nx
import itertools
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
                G.add_edge(i + 1, j + 1)

    # 그래프 시각화
    node_positions = {
        1: (0, 1), 2: (1, 0), 3: (1, 2),
        4: (2, 0), 5: (2, 2), 6: (3, 1)
    }
    plt.figure()
    nx.draw(G, pos=node_positions, with_labels=True)
    plt.show()

    # 소스와 종단 노드 정의
    source = 1
    terminal = 6

    # Critical Link Sets 기반 네트워크 신뢰성 계산
    network_reliability = evaluate_network_reliability_critical(G.copy(), source, terminal, node_reliabilities)

    # Critical Cut Sets 및 실패 확률 계산
    critical_cut_sets, failure_probability = calculate_disjoint_cut_sets_and_failure_probability(G.copy(), source, terminal, node_reliabilities)

    # 결과 출력
    print(f"\nNetwork Reliability: {network_reliability:.4f}")
    print("\nCritical Cut Sets:")
    for i, cut_set in enumerate(critical_cut_sets, start=1):
        print(f"Cut Set {i}: {cut_set}")
    print(f"\nNetwork Failure Probability: {failure_probability:.4f}")


def find_most_reliable_path(G, source, terminal, node_reliabilities):

    # Dijkstra 알고리즘을 수정하여 가장 신뢰할 수 있는 경로를 식별

    reliability_labels = {node: -math.inf for node in G.nodes()}
    reliability_labels[source] = math.log(node_reliabilities[source])
    permanently_labeled = set()
    temporarily_labeled = set(G.nodes())
    predecessors = {}

    while temporarily_labeled:
        current_node = max(temporarily_labeled, key=lambda node: reliability_labels[node])
        if reliability_labels[current_node] == -math.inf:
            break

        permanently_labeled.add(current_node)
        temporarily_labeled.remove(current_node)

        if current_node == terminal:
            break

        for neighbor in G.successors(current_node):
            if neighbor not in permanently_labeled:
                new_reliability = reliability_labels[current_node] + math.log(node_reliabilities[neighbor])
                if new_reliability > reliability_labels[neighbor]:
                    reliability_labels[neighbor] = new_reliability
                    predecessors[neighbor] = current_node

    path = []
    current = terminal
    while current in predecessors or current == source:
        path.insert(0, current)
        current = predecessors.get(current, None)

    path_reliability = math.exp(reliability_labels[terminal]) if terminal in permanently_labeled else 0
    return path, path_reliability


def evaluate_network_reliability_critical(G, source, terminal, node_reliabilities):

    # Critical Link Sets를 기반으로 네트워크 신뢰성을 계산

    critical_link_sets = []
    visited_nodes = set()

    while nx.has_path(G, source, terminal):
        path, path_reliability = find_most_reliable_path(G, source, terminal, node_reliabilities)
        unique_nodes = set(path[1:-1]) - visited_nodes
        if unique_nodes:
            critical_link_sets.append(unique_nodes)
            visited_nodes.update(unique_nodes)
        for node in path[1:-1]:
            if node in G:
                G.remove_node(node)

    # Inclusion-Exclusion Principle로 중복 제거
    return apply_inclusion_exclusion(critical_link_sets, node_reliabilities)


def apply_inclusion_exclusion(critical_link_sets, node_reliabilities):

    # Inclusion-Exclusion Principle 정의

    total_reliability = 0
    for r in range(1, len(critical_link_sets) + 1):
        for subset in itertools.combinations(critical_link_sets, r):
            intersection = set.union(*subset)  
            set_probability = 1
            for node in intersection:
                set_probability *= node_reliabilities[node]
            if r % 2 == 1:
                total_reliability += set_probability
            else:
                total_reliability -= set_probability
    return total_reliability


def calculate_disjoint_cut_sets_and_failure_probability(G, source, terminal, node_reliabilities):

    # Critical Cut Sets와 실패 확률 계산

    example_failure_probabilities = {node: 1 - prob for node, prob in node_reliabilities.items()}
    all_nodes = list(G.nodes())
    all_nodes.remove(source)
    all_nodes.remove(terminal)

    critical_cut_sets = []
    failure_probability = 0

    for r in range(1, len(all_nodes) + 1):
        for node_subset in itertools.combinations(all_nodes, r):
            G_copy = G.copy()
            G_copy.remove_nodes_from(node_subset)
            if not nx.has_path(G_copy, source, terminal):
                if all(set(node_subset).isdisjoint(existing) for existing in critical_cut_sets):
                    critical_cut_sets.append(set(node_subset))
                    set_probability = 1
                    for node in node_subset:
                        set_probability *= example_failure_probabilities[node]
                    failure_probability += set_probability
    return critical_cut_sets, failure_probability


s_rda_algorithm()
