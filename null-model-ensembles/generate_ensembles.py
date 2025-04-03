import pandas as pd
import networkx as nx
import numpy as np
import copy
from tqdm import tqdm

def generate_geometric_graph(n, r, dim):
    #Generates a 2D random geometric graph with threshold r
    positions = {i: np.random.rand(dim) for i in range(n)}
    return nx.random_geometric_graph(n=n, radius=r, pos=positions)

def generate_rgg_ensemble(G, num_iterations, name):
    dim = 2  # 2D space
    n= G.number_of_nodes()
    l = G.number_of_edges()
    k_avg = (2 * l) / n

    # Estimate an initial threshold using theory; this will give us a random network
    # with about the same average degree as the actual network
    # r = np.pow((3*k_avg)/(4 * np.pi * n), 1/3) # r for 3 dimensions
    r = np.sqrt(k_avg/(np.pi * n))

    # dataframe that will store the edges for all network iterations, network_no
    # will tell you which iteraion it came from
    ensemble_df = pd.DataFrame(columns=['source', 'target', 'network_no'])

    for i in tqdm(range(num_iterations), desc='RGG creation', unit=' graph'):
        RGG = generate_geometric_graph(n, r, dim)
        network_df = nx.to_pandas_edgelist(RGG)
        network_df['network_no'] = i+1
        # Append edges for current network iteration to dataframe
        ensemble_df = pd.concat([ensemble_df, network_df])

    ensemble_df.to_csv(f'./networks/random_geometric/{name}_rgg.csv', index=False)

def generate_dp_random_network(G: nx.Graph, num_swaps):
    G_null = copy.deepcopy(G)
    # Create random degree-preserving network through double edge swaps
    nx.double_edge_swap(G_null, num_swaps, max_tries =  10 * num_swaps)
    return G_null

def generate_dp_ensemble(G: nx.Graph, num_iterations, name):
    num_edges = G.number_of_edges()
    # each edge will be swapped on average 10 times
    num_swaps = 10 * num_edges
    # dataframe that will store the edges for all network iterations, network_no
    # will tell you which iteraion it came from
    ensemble_df = pd.DataFrame(columns = ['source', 'target', 'network_no'])

    for i in tqdm(range(num_iterations), desc = 'DP graph creation'):
        G_null = generate_dp_random_network(G, num_swaps)
        network_df = nx.to_pandas_edgelist(G_null)
        network_df['network_no'] = i+1
        # Append edges for current network iteration to dataframe
        ensemble_df = pd.concat([ensemble_df, network_df])

    ensemble_df.to_csv(f'./networks/degree_preserving/{name}_dp.csv', index=False)

def generate_ba_ensemble(G: nx.Graph, num_iterations, name):
    k_average = np.mean([d for (_, d) in G.degree])
    m = round(k_average / 2) # formula gotten from summary of W7L11 notes
    n = G.number_of_nodes()

    ensemble_df = pd.DataFrame(columns=['source', 'target', 'network_no'])
    g_init = nx.complete_graph(m)
    for i in tqdm(range(num_iterations), desc = 'BA graph creation'):
        G_null = nx.barabasi_albert_graph(n=n, m=m, initial_graph=g_init)
        network_df = nx.to_pandas_edgelist(G_null)
        network_df['network_no'] = i + 1
        # Append edges for current network iteration to dataframe
        ensemble_df = pd.concat([ensemble_df, network_df])

    ensemble_df.to_csv(f'./networks/barabasi-albert/{name}_ba.csv', index=False)


if __name__ == '__main__':
    names = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    num_iterations = 100
    for i in tqdm(range(len(names)), desc='Total progress'):
        name = names[i]
        print(f"\nGenerating random networks for {name} genre")
        node_list = pd.read_csv(f"../networks/{name}_node_list.csv").rename(columns={"Node": "node_id"})
        edge_list = pd.read_csv(f"../networks/{name}_edge_list.csv").rename(columns={"Node1": "source", "Node2": "target"})

        # Create network for each genre using the node and edge list from the networks folder
        graph = nx.from_pandas_edgelist(edge_list, source="source", target="target", edge_attr=True, create_using=nx.Graph)
        graph.add_nodes_from([(dict(d)['node_id'], dict(d)) for _, d in node_list.iterrows()])

        generate_rgg_ensemble(graph, num_iterations, name)
        generate_dp_ensemble(graph, num_iterations, name)
        print("\n")