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



# 조건부 확률 척도 CPM

def CPM(G, source, terminal, target_node, p_i, num_samples):
    nodes = [node for node in G.nodes if node != source and node != terminal]    # 소스와 터미널 노드 제외
    
    # 초기 실패 횟수 0으로 설정
    system_failure_count = 0
    target_failure_count = 0
    
    # 몬테카를로 시뮬레이션을 통해 시스템 파괴 확률 계산
    for _ in range(num_samples):
        G_copy = G.copy()
        failed_nodes = [node for node in nodes if np.random.rand() < p_i]
        G_copy.remove_nodes_from(failed_nodes)
        
        # 시스템 파괴 횟수 계산
        if network_function(G_copy, source, terminal) == 0:
            system_failure_count += 1
            
            # 시스템 파괴 시 구성 요소 i가 파괴된 횟수 계산
            if target_node in failed_nodes:
                target_failure_count += 1
    
    # 시스템 파괴 확률
    Pr_sys_failure = system_failure_count / num_samples
    
    # 시스템 파괴 시 구성 요소 i 파괴 확률
    Pr_i_failure_given_system_failure = target_failure_count / num_samples
    
    return Pr_i_failure_given_system_failure / Pr_sys_failure

target_node = int(input("노드 i(2~5): "))
CPM_val = CPM(G, source, terminal, target_node, p_i, num_samples)
print(f"조건부 확률 척도 CPM = {CPM_val}")






