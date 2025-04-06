import pandas as pd
import networkx as nx
import os
import numpy as np

# This script formats the node and edge lists in the networks folder to allow for visualization in d3. It also
# calculates the betweenness centrality for each node and adds it to the node list.
# link to Observable notebook containing visualizations: https://observablehq.com/d/2771aea511c0615e

genres = ['blues', 'classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

network_names = {
'Vis' : 'Visual',
'SomMot' : 'Somatomotor',
'DorsAttn' : 'Dorsal Attention',
'SalVentAttn' : 'Salience/Ventral Attention',
'Limbic' : 'Limbic',
'Cont' : 'Frontoparietal Control',
'Default' : 'Default'
}

def getNetworkName(s:str):
    for substr in network_names:
        if substr in s:
            return network_names[substr]
    raise ValueError('Network name not found')

vis_edges = pd.DataFrame(columns=['source', 'target', 'Correlation', 'genre'])
vis_nodes_top_view = pd.DataFrame(columns=['id','Label','Network','Hemisphere','Region','Parcel ID','x','y','degree_centrality','r','eigenvector_centrality','closeness_centrality','region_name','network_name', 'genre'])
vis_nodes_side_view = pd.DataFrame(columns=['id','Label','Network','Hemisphere','Region','Parcel ID','x','y','degree_centrality','r','eigenvector_centrality','closeness_centrality','region_name','network_name', 'genre'])
region_names = pd.read_csv("./region_names.csv")

for genre in genres:
    # Read in node and edge lists from networks folder
    # base_path = os.getcwd()
    read_path_edge = f"../networks/{genre}_edge_list.csv"
    read_path_node = f"../networks/{genre}_node_list.csv"
    edge_list = pd.read_csv(read_path_edge).rename(columns={"Node1": "source", "Node2": "target"})
    node_list = pd.read_csv(read_path_node).rename(columns={"Node": "node_id"})

    # Keeping all edges now to allow visualizing whole network
    # edge_list = edge_list.sort_values(by='Correlation', ascending=False).iloc[:500,:]


    # make the graph using edge list and node list data
    # graph = nx.from_pandas_edgelist(edge_list, source="source", target="target", edge_attr=True, create_using=nx.Graph)
    # graph.add_nodes_from([(dict(d)['node_id'], dict(d)) for _, d in node_list.iterrows()])

    #calculate betweenness centrality for each node and add it to the node list
    # centrality = nx.betweenness_centrality(graph)
    # node_list['betweenness'] = 0.
    node_list['region_name'] = ''
    node_list['network_name'] = ''
    for i, row in node_list.iterrows():
        # node_list.loc[node_list['node_id'] == row['node_id'], 'betweenness'] = centrality[row['node_id']]
        # Add column to nodes that has more descriptive region names
        node_list.loc[i, 'region_name'] = region_names.loc[region_names['Region'] == row['Region'], 'region_name'].values[0]
        node_list.loc[i, 'network_name'] = getNetworkName(row['Label'])

    nodes_side = node_list.copy(deep=True)

    # rename columns, the force simulation functions in d3 will only work if it can find columns that have these names
    # renaming betweenness as r because betweenness centrality will be used to determine the size of the circle
    # in the visualization. Also, the force simulations in d3 need a column called r to determine the radius of the
    # collision force for each node.
    node_list = node_list.rename(columns={'X': 'x', 'Y': 'y', 'node_id': 'id', 'betweenness_centrality' : 'r'}).drop(columns=['Z'])
    # using X and Y columns gives us a top down view of the brain, so using Y and Z as the horizontal and vertical positions, 
    # respectively, in d3 should give us the side view
    nodes_side = nodes_side.rename(columns={'Y': 'x', 'Z': 'y', 'node_id': 'id', 'betweenness_centrality' : 'r'}).drop(columns=['X'])

    # Uncomment these lines if you want a seperate file for each genre
    # making a folder for each genre and writing the updated node and edge lists there.
    # os.mkdir(base_path + "/visualization-data/{a}".format(a=x))
    # write_path_node = f"./{genre}/{genre}_nodes_viz.csv"
    # write_path_side = f"./{genre}/{genre}_nodes_side_view_viz.csv"
    # write_path_edges =f"./{genre}/{genre}_edges_viz.csv"
    #
    # node_list.to_csv(write_path_node, index=False)
    # nodes_side.to_csv(write_path_side, index=False)
    # edge_list.to_csv(write_path_edges, index=False)

    node_list['genre'] = genre
    nodes_side['genre'] = genre
    edge_list['genre'] = genre

    vis_edges = pd.concat([vis_edges, edge_list], ignore_index=True)
    vis_nodes_top_view = pd.concat([vis_nodes_top_view, node_list], ignore_index=True)
    vis_nodes_side_view = pd.concat([vis_nodes_side_view, nodes_side], ignore_index=True)

vis_edges.to_csv('vis_edges.csv', index=False)
vis_nodes_top_view.to_csv('vis_nodes_top_view.csv', index=False)
vis_nodes_side_view.to_csv('vis_nodes_side_view.csv', index=False)