import networkx as nx
import matplotlib.pyplot as plt

# =====================================================
# FOOD SUPPLY CHAIN CONTAMINATION - GRAPH SETUP
# =====================================================

# 1. Directed Graph (Unweighted)
DG = nx.DiGraph()
nodes = [
    "Farm",
    "Collection",
    "Processing",
    "Warehouse",
    "Distributor",
    "Supermarket",
    "Restaurant",
    "Consumer"
]
DG.add_nodes_from(nodes)
DG.add_edges_from([
    ("Farm", "Collection"),
    ("Collection", "Processing"),
    ("Processing", "Warehouse"),
    ("Warehouse", "Distributor"),
    ("Distributor", "Supermarket"),
    ("Supermarket", "Consumer"),
    ("Processing", "Restaurant"),
    ("Restaurant", "Consumer"),
    ("Distributor", "Processing")
])

# 2. Undirected Graph (NOW WITH WEIGHTS MATCHING THE MST)
UG = nx.Graph()
UG.add_nodes_from(nodes)
UG.add_weighted_edges_from([
    ("Farm", "Collection", 2),
    ("Collection", "Processing", 3),
    ("Processing", "Warehouse", 4),
    ("Warehouse", "Distributor", 2),
    ("Distributor", "Supermarket", 1),
    ("Supermarket", "Consumer", 2),
    ("Processing", "Restaurant", 3),
    ("Restaurant", "Consumer", 2),
    ("Distributor", "Processing", 3)
])


# =====================================================
# VISUALIZATION 1: DIRECTED vs. WEIGHTED UNDIRECTED
# =====================================================
plt.figure(figsize=(14, 6))
pos = nx.spring_layout(UG, seed=42)  # Shared layout for consistency

# Subplot 1: Directed Graph (Unweighted)
plt.subplot(121)
nx.draw(
    DG,
    pos,
    with_labels=True,
    node_color='lightblue',
    node_size=2500,
    arrows=True,
    arrowsize=20
)
plt.title("Directed Graph (Unweighted)", fontsize=12, fontweight='bold')

# Subplot 2: Undirected Graph (Weighted)
plt.subplot(122)
nx.draw(
    UG,
    pos,
    with_labels=True,
    node_color='lightgreen',
    node_size=2500
)
ug_labels = nx.get_edge_attributes(UG, 'weight')
nx.draw_networkx_edge_labels(UG, pos, edge_labels=ug_labels)
plt.title("Weighted Undirected Graph", fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()


# =====================================================
# ALGORITHM ANALYSIS & CALCULATIONS
# =====================================================

print("\n" + "="*50)
print(" 2. SHORTEST PATH (Directed Graph)")
print("="*50)
path = nx.shortest_path(DG, "Farm", "Consumer")
print(f"Shortest Path from Farm to Consumer:\n -> {path}\n")

print("All Pairs Shortest Paths:")
for source, paths in nx.all_pairs_shortest_path(DG):
    print(f" {source:<12} -> {paths}")


print("\n" + "="*50)
print(" 3. CYCLES (Directed Graph)")
print("="*50)
cycles = list(nx.simple_cycles(DG))
if cycles:
    print("Graph contains cycles. Simple Cycles found:")
    for c in cycles:
        print(f" -> {c}")
else:
    print("No cycles found.")


print("\n" + "="*50)
print(" 4. EULERIAN PATH / CIRCUIT (Undirected Graph)")
print("="*50)
print(f"Eulerian Path Exists:    {nx.has_eulerian_path(UG)}")
print(f"Eulerian Circuit Exists: {nx.is_eulerian(UG)}")


print("\n" + "="*50)
print(" 5. CONNECTED COMPONENTS (Undirected Graph)")
print("="*50)
components = list(nx.connected_components(UG))
print(f"Number of Connected Components: {len(components)}")
for i, c in enumerate(components, 1):
    print(f" Component {i}: {c}")


print("\n" + "="*50)
print(" 6. MINIMUM SPANNING TREE (From Weighted Undirected)")
print("="*50)
mst = nx.minimum_spanning_tree(UG)
print("MST Edges and Weights:")
for edge in mst.edges(data=True):
    print(f" -> {edge[0]} --({edge[2]['weight']})-- {edge[1]}")

# Visualize MST
plt.figure(figsize=(8, 6))
nx.draw(
    mst,
    pos,
    with_labels=True,
    node_color='orange',
    node_size=2500
)
mst_labels = nx.get_edge_attributes(mst, 'weight')
nx.draw_networkx_edge_labels(mst, pos, edge_labels=mst_labels)
plt.title("Minimum Spanning Tree (MST)", fontsize=12, fontweight='bold')
plt.show()


print("\n" + "="*50)
print(" 7. CUT VERTICES & CUT EDGES (Undirected Graph)")
print("="*50)
print("Articulation Points (Cut Vertices):")
for p in nx.articulation_points(UG):
    print(f" -> {p}")

print("\nBridges (Cut Edges):")
for b in nx.bridges(UG):
    print(f" -> {b[0]} - {b[1]}")


print("\n" + "="*50)
print(" 8. PLANARITY (Undirected Graph)")
print("="*50)
is_planar, _ = nx.check_planarity(UG)
print(f"Graph is Planar: {is_planar}")


print("\n" + "="*50)
print(" 9. GRAPH COLORING (Undirected Graph)")
print("="*50)
colors = nx.coloring.greedy_color(UG, strategy="largest_first")
for node, color in sorted(colors.items()):
    print(f" {node:<12} -> Color {color}")

# Visualize Graph Coloring
color_map = [colors[node] for node in UG.nodes()]
plt.figure(figsize=(8, 6))
nx.draw(
    UG,
    pos,
    with_labels=True,
    node_color=color_map,
    cmap=plt.cm.Set3,
    node_size=2500
)
plt.title("Graph Coloring", fontsize=12, fontweight='bold')
plt.show()