# coding:utf-8
"""
PageRank算法優缺點

長處：

是一個與查詢無關的靜態算法，全部網頁的PageRank值通過離線計算獲得；有效降低在線查詢時的計算量，極大降低了查詢響應時間。

缺點：

1）人們的查詢具有主題特徵，PageRank忽略了主題相關性，導致結果的相關性和主題性減少

2）舊的頁面等級會比新頁面高。由於即使是非常好的新頁面也不會有非常多上游連結，除非它是某個網站的子網站。

"""
import pandas as pd
import numpy as np

def read_data(filename):
    graph_dict = {}
    with open(filename, 'r') as fin:
        for line in fin.readlines():
            tmp = line.strip().split(' ')
            if len(tmp) < 2:
                graph_dict[source_link] = {}
                continue
            source_link = tmp[0]
            if source_link not in graph_dict:
                graph_dict[source_link] = {}
            target_list = tmp[1:]
            for target_link in target_list:
                graph_dict[source_link][target_link] = 1
    return graph_dict



def PageRank(M, alpha, root):
    """
    Personal Rank in matrix formation
    :param M: transfer probability matrix
    :param index2node: index2node dictionary
    :param node2index: node2index dictionary
    :return:type of list of tuple, ex.
    [(node1, prob1),(node2, prob2),...]
    """
    result = []
    n = len(M)
    v = np.zeros(n)
    v[node2index[root]] = 1
    while np.sum(abs(v - (alpha*np.matmul(M,v) + (1-alpha)*v))) > 0.0001:
        v = alpha * np.matmul(M, v) + (1-alpha)*v
    for ind, prob in enumerate(v):
        result.append((index2node[ind], prob))
    result = sorted(result, key=lambda x:x[1], reverse=True)[:num_candidates]
    return result

def Generate_Transfer_Matrix(G):
    """generate transfer matrix given graph"""
    index2node = dict()
    node2index = dict()
    for index,node in enumerate(G.keys()):
        node2index[node] = index
        index2node[index] = node
    # num of nodes
    n = len(node2index)
    # generate Transfer probability matrix M, shape of (n,n)
    M = np.zeros([n,n])
    for node1 in G.keys():
        for node2 in G[node1]:
            # FIXME: some nodes not in the Graphs.keys, may incur some errors
            try:
                M[node2index[node2],node2index[node1]] = 1/len(G[node1])
            except:
                continue
    return M, node2index, index2node


if __name__ == '__main__':
    alpha = 0.85
    root = 'WT07-B26-225'
    #root = 'A'
    num_iter = 100
    num_candidates = 10
    G = read_data("page_link.txt")
    print(len(G.keys()))
    """
    G = {'A' : {'a' : 1, 'c' : 1},
         'B' : {'a' : 1, 'b' : 1, 'c':1, 'd':1},
         'C' : {'c' : 1, 'd' : 1},
         'a' : {'A' : 1, 'B': 1, 'c': 1},
         'b' : {'B' : 1},
         'c' : {'A' : 1, 'C':1, 'e': 1},
         'd' : {'c' : 1},
         'e' : {'a' : 1, 'b': 1, 'c': 1, 'd': 1}}
    """
    M, node2index, index2node = Generate_Transfer_Matrix(G)
    # print transfer matrix
    print(pd.DataFrame(M, index=G.keys(), columns=G.keys()))
    result = PageRank(M, alpha, root)
    # print results
    print(result)
