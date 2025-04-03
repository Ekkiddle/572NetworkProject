import pandas as pd
import networkx as nx
import os
import numpy as np

# This script formats the node and edge lists in the networks folder to allow for visualization in d3. It also
# calculates the betweenness centrality for each node and adds it to the node list.
# link to Observable notebook containing visualizations: https://observablehq.com/d/2771aea511c0615e

names = ['blues', 'classical','country','disco','hiphop','jazz','metal','pop','reggae','rock']

for x in names:
    # Read in node and edge lists from networks folder
    base_path = os.getcwd()
    read_path_edge = base_path + "/networks/'{a}'_edge_list.csv".format(a=x)
    read_path_node = base_path + "/networks/'{a}'_node_list.csv".format(a=x)
    edge_list = pd.read_csv(read_path_edge).rename(columns={"Node1": "source", "Node2": "target"})
    node_list = pd.read_csv(read_path_node).rename(columns={"Node": "node_id"})

    # Keeping only the top 500 edges with the highest correlation
    edge_list = edge_list.sort_values(by='Correlation', ascending=False).iloc[:500,:]

    region_names = pd.read_csv(base_path + "/visualization-data/region_names.csv")

    # make the graph using edge list and node list data
    graph = nx.from_pandas_edgelist(edge_list, source="source", target="target", edge_attr=True, create_using=nx.Graph)
    graph.add_nodes_from([(dict(d)['node_id'], dict(d)) for _, d in node_list.iterrows()])

    #calculate betweenness centrality for each node and add it to the node list
    centrality = nx.betweenness_centrality(graph)
    node_list['betweenness'] = 0.
    node_list['region_name'] = ''
    for i, row in node_list.iterrows():
        node_list.loc[node_list['node_id'] == row['node_id'], 'betweenness'] = centrality[row['node_id']]
        # Add column to nodes that has more descriptive region names
        node_list.loc[i, 'region_name'] = region_names.loc[region_names['Region'] == row['Region'], 'region_name'].values[0]

    nodes_side = node_list.copy(deep=True)

    # rename columns, the force simulation functions in d3 will only work if it can find columns that have these names
    # renaming betweenness as r because betweenness centrality will be used to determine the size of the circle
    # in the visualization. Also, the force simulations in d3 need a column called r to determine the radius of the
    # collision force for each node.
    node_list = node_list.rename(columns={'X': 'x', 'Y': 'y', 'node_id': 'id', 'betweenness' : 'r'}).drop(columns=['Z'])
    # using X and Y columns gives us a top down view of the brain, so using Y and Z as the horizontal and vertical positions, 
    # respectively, in d3 should give us the side view
    nodes_side = nodes_side.rename(columns={'Y': 'x', 'Z': 'y', 'node_id': 'id', 'betweenness' : 'r'}).drop(columns=['X'])

    # making a folder for each genre and writing the updated node and edge lists there.
    # os.mkdir(base_path + "/visualization-data/{a}".format(a=x))

    write_path_node = base_path + "/visualization-data/{a}/{a}_nodes_viz.csv".format(a=x)
    write_path_side = base_path + "/visualization-data/{a}/{a}_nodes_side_view_viz.csv".format(a=x)
    write_path_edges = base_path + "/visualization-data/{a}/{a}_edges_viz.csv".format(a=x)

    node_list.to_csv(write_path_node, index=False)
    nodes_side.to_csv(write_path_side, index=False)
    edge_list.to_csv(write_path_edges, index=False)
