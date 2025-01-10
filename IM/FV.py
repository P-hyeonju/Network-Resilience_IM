import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
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

p_i = 0.01



# 모든 min-cutsets

def min_cutsets(G, source, terminal):
    all_nodes = [node for node in G.nodes if node != source and node != terminal]   # 소스와 터미널 노드 제외
    min_cutsets = []
    
    # 노드 집합 생성
    for r in range(1, len(all_nodes)+1):
        for nodes in itertools.combinations(all_nodes, r):
            G_copy = G.copy()
            G_copy.remove_nodes_from(nodes)    # 생성한 노드 집합을 G_copy에서 제거
            
            # 노드 집합을 제거한 G_copy에서 소스 노드와 터미널 노드의 연결 여부 확인
            if not nx.has_path(G_copy, source, terminal):
                
                # 새로 발견된 cutset이 기존 min_cutsets의 진부분집합인지 확인
                if not any(set(existing_cutset).issubset(set(nodes)) for existing_cutset in min_cutsets):
                    
                    # 기존 min_cutsets 중 새로 발견된 cutset의 상위 집합이 존재하면 제거
                    min_cutsets = [
                       existing_cutset
                       for existing_cutset in min_cutsets
                       if not set(nodes).issubset(set(existing_cutset))
                   ]
                    min_cutsets.append(nodes)
                    
    return min_cutsets
            
min_cutsets = min_cutsets(G, source, terminal)



# 구성 요소 i가 포함된 min_cutsets

def min_cutsets_containing_i(cutsets, target_node):
    return [cutset for cutset in cutsets if target_node in cutset]



# 각 cutset의 확률 계산

def Pr_cutsets(cutset, p_i):
    return np.prod([p_i for _ in cutset])



# cutsets 합집합의 확률 계산

def Pr_union(cutsets, p_i):
    total_prob = 0
    n = len(cutsets)
    
    for r in range(1, n+1):
        for subset in itertools.combinations(cutsets, r):
            pr_intersection = 1
            for cutset in subset:
                pr_intersection *= Pr_cutsets(cutset, p_i)
            total_prob += (-1) ** (r + 1) * pr_intersection
            
    return total_prob



# Fussel-Vesely 척도

def FV(G, min_cutsets, target_node, p_i):
    
    # 분자 = i가 포함된 min_cutsets의 합집합의 확률
    cutsets_i = [cutset for cutset in min_cutsets if target_node in cutset]
    numerator = Pr_union(cutsets_i, p_i)
    
    
    # 분모 = 모든 min_cutsets의 합집합의 확률
    denominator = Pr_union(min_cutsets, p_i)
    
    # 분모가 0이 되는 경우
    if denominator == 0:
        raise ValueError
        
    return numerator / denominator


target_node = int(input("노드 i(2~5): "))
FV_val = FV(G, min_cutsets, target_node, p_i)
print(f"Fussel-Vesely 척도 FV = {FV_val}")
    
    


