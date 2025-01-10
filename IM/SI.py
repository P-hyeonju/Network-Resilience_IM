import networkx as nx
import matplotlib.pyplot as plt
import itertools



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



# 네트워크 상태 임의 설정

# 구성 요소 상태
Pi_i = {1: 1, 2: 1, 3: 0, 4: 1, 5: 1, 6: 1}
    
# 네트워크 상태 함수 (노드1과 노드6이 연결된 경우에만 네트워크 작동)
def network_function(G, Pi_i):
    
    # 구성 요소 상태가 1인 노드만 활성화
    active_nodes = [i for i, Pi_i in Pi_i.items() if Pi_i == 1]
    active_subgraph = G.subgraph(active_nodes)
    
    # 소스 노드와 터미널 노드가 서브 그래프에 포함되는지 확인
    if 1 not in active_subgraph or 6 not in active_subgraph:
        return 0
    
    # 서브 그래프에서 소스 노드와 터미널 노드의 연결 여부 확인    
    return int(nx.has_path(active_subgraph, 1, 6))

# 네트워크 상태 표현
Pi_network = network_function(G, Pi_i)
print("Network Status:", "1(작동)" if Pi_network == 1 else "0(고장)")



# 구성 요소가 네트워크 상태에 영향을 미치는 변수 정의

def del_i(G, Pi_i, i):
    
    # 기존 상태 저장
    original_state = Pi_i[i]
    
    # 구성 요소의 상태가 1일 때 네트워크 상태
    Pi_i[i] = 1
    Pi_net_1 = network_function(G, Pi_i)
    
    # 구성 요소의 상태가 0일 때 네트워크 상태
    Pi_i[i] = 0
    Pi_net_0 = network_function(G, Pi_i)
    
    # 구성 요소 i의 상태를 기존 상태로 복원
    Pi_i[i] = original_state
    
    return Pi_net_1 - Pi_net_0



# 구조적 중요도 척도 SI
N = G.number_of_nodes()

def SI_i(G, N, i):
    
    # 모든 상태 조합 생성
    state_combinations = itertools.product([0,1], repeat = N-1)
    
    # 상태 조합에 따른 SI의 합
    SI_sum = 0
    for combination in state_combinations:
        
        # 값 초기화
        Pi_i = {node: 0 for node in G.nodes}
        index = 0
        
        # i 노드를 제외한 모든 노드에 대한 delta_i 값의 합
        for node in G.nodes:
            if node != i:
                Pi_i[node] = combination[index]
                index += 1
        SI_sum += del_i(G, Pi_i, i)
        
    SI_val = SI_sum / (2**(N-1))
    return SI_val


i = int(input("노드 i:"))
del_i_value = del_i(G, Pi_i, i)
SI_value = SI_i(G, N, i)
print(f"delta_{i}:", "1(영향을 미침)" if del_i_value == 1 else "0(영향을 미치지 않음)")
print(f"구조적 중요도 척도 SI = {SI_value}")