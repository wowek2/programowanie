import networkx as nx
import matplotlib.pyplot as plt
import random
import os
from PIL import Image 

# Simulation parameeters
n_nodes = 100              # Nodes count
p_connection = 0.6        # Nodes connection propaility
n_steps = 50              # No. of steps in simulation
output_gif = "random_walk.gif" 


G = nx.gnp_random_graph(n_nodes, p_connection)
while not nx.is_connected(G):
    G = nx.gnp_random_graph(n_nodes, p_connection)

pos = nx.spring_layout(G)
current_node = random.choice(list(G.nodes()))
filenames = []

for step in range(n_steps):
    neighbors = list(G.neighbors(current_node))
    if neighbors:
        current_node = random.choice(neighbors)
    
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.draw_networkx_nodes(G, pos, node_size=300, node_color="lightblue")
    nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_size=500, node_color="red")
    plt.title(f"Krok: {step}")
    filename = f"frame_{step:03d}.png"
    plt.savefig(filename)
    plt.close()
    filenames.append(filename)


images = []
for filename in filenames:
    images.append(Image.open(filename))

images[0].save(
    output_gif,
    save_all=True,
    append_images=images[1:],
    duration=1000, 
    loop=0          
)

for img in images:
    img.close()

for filename in filenames:
    os.remove(filename)

print(f"Animacja została zapisana jako {output_gif}")