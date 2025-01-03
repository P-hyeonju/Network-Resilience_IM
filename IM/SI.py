import networkx as nx
import matplotlib.pyplot as plt
import random



# 네트워크 모델링

G = nx.DiGraph()

G.add_nodes_from([1, 2, 3, 4, 5, 6])
G.add_edges_from([(1,2), (2,3), (2,4), (3,5), (4,5), (5,6)])

node_positions = {1: (0,1), 2: (1,1), 3: (2,2), 4: (2,0), 5: (3,1), 6: (4,1)}

plt.figure()
nx.draw(G, pos=node_positions, with_labels=True, node_size=200, node_color="lightblue", arrowsize=10)
plt.show()

adj_matrix = nx.adjacency_matrix(G).todense()

source = 1
terminal = 6



# 네트워크 상태 임의 설정

# 구성 요소 상태
Pi_i = {Pi_i: random.randint(0, 1) for Pi_i in G.nodes}
print("Node States:", Pi_i)
    
# 네트워크 상태 함수 (노드1과 노드6이 연결된 경우에만 네트워크 작동)
def network_function(G, Pi_i):
    
    active_nodes = [i for i, Pi_i in Pi_i.items() if Pi_i == 1]
    active_subgraph = G.subgraph(active_nodes)
    
    if 1 not in active_subgraph or 6 not in active_subgraph:
        return 0
        
    return int(nx.has_path(active_subgraph, 1, 6))

# 네트워크 상태 표현
Pi_network = network_function(G, Pi_i)
print("Network Status:", "1(작동)" if Pi_network == 1 else "0(고장)")

