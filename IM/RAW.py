import networkx as nx
import matplotlib.pyplot as plt
import numpy as np



# 네트워크 모델링

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1,2), (2,3), (2,4), (3,5), (4,5), (5,6)])

node_positions = {1: (0,1), 2: (1,1), 3: (2,2), 4: (2,0), 5: (3,1), 6: (4,1)}

plt.figure()
nx.draw(G, pos=node_positions, with_labels=True, node_size=200, node_color="lightblue", arrowsize=10)
plt.show()


source = 1
terminal = 6

p_i = 0.01
num_samples = 1000000



# 네트워크 작동 여부 함수

def network_function(G, source, terminal):
    if source not in G.nodes or terminal not in G.nodes:
        return 0
    if nx.has_path(G, source, terminal):
        return 1
    else:
        return 0
    


# 구성 요소 i가 파괴되었을 때 네트워크 실패 확률

def Pr_i_failed(G, source, terminal, failed_node, p_i, num_samples):
    nodes = [node for node in G.nodes if node != failed_node and node != source and node != terminal]    # 소스와 터미널 노드, 요소 i 제외
    
    # 초기 실패 횟수 0으로 설정
    failure_count = 0
    
    # 몬테카를로 시뮬레이션을 통해 파괴 노드 결정 후 네트워크 실패 확률 계산
    for _ in range(num_samples):
        G_copy = G.copy()
        G_copy.remove_node(failed_node) # 구성 요소 i를 파괴로 가정했으므로 i 또한 제거            
        failed_nodes = [node for node in nodes if np.random.rand() < p_i]
        G_copy.remove_nodes_from(failed_nodes)
        
        if network_function(G_copy, source, terminal) == 0:
            failure_count += 1
            
    return failure_count / num_samples



# 원래 상태의 네트워크 실패 확률

def Pr_original_failure(G, source, terminal, p_i, num_samples):
    nodes = [node for node in G.nodes if node != source and node != terminal]    # 소스와 터미널 노드 제외
    
    # 초기 실패 횟수 0으로 설정
    failure_count = 0
    
    # 몬테카를로 시뮬레이션을 통해 네트워크 실패 확률 계산
    for _ in range(num_samples):
        G_copy = G.copy()
        failed_nodes = [node for node in nodes if np.random.rand() < p_i]
        G_copy.remove_nodes_from(failed_nodes)
        
        if network_function(G_copy, source, terminal) == 0:
            failure_count += 1
            
    return failure_count / num_samples



# 위험 달성 가치 척도 RAW 계산

def RAW(G, source, terminal, target_node, p_i, num_samples):
    Pr_net_failure_failed_i = Pr_i_failed(G, source, terminal, target_node, p_i, num_samples)
    Pr_net_failure_origin = Pr_original_failure(G, source, terminal, p_i, num_samples)
    
    return Pr_net_failure_failed_i / Pr_net_failure_origin

target_node = int(input("노드 i: "))
RAW_val = RAW(G, source, terminal, target_node, p_i, num_samples)
print(f"위험 달성 가치 척도 RAW = {RAW_val}")