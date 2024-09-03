from flask import Flask, render_template, request, send_file
import networkx as nx
import matplotlib.pyplot as plt
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

# Ruta específica para guardar la imagen
img_path = 'C:/Users/Suseth Sandoval/Documents/jafet/verano/static/graph.png'

# Verificar y crear la carpeta si no existe
if not os.path.exists(os.path.dirname(img_path)):
    os.makedirs(os.path.dirname(img_path))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():
    num_nodes = int(request.form['num_nodes'])
    edges = []
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = request.form.get(f'weight_{i}_{j}')
            if weight:
                edges.append((i, j, int(weight)))
    
    G = nx.Graph()
    G.add_weighted_edges_from(edges)
    
    # Crear una figura de matplotlib
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=500, font_size=16, ax=axis)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=axis)
    
    canvas = FigureCanvas(fig)
    if os.path.exists(img_path):
        os.remove(img_path)
    canvas.print_png(img_path)
    
    source = int(request.form['source'])
    target = int(request.form['target'])
    path = nx.shortest_path(G, source=source, target=target, weight='weight')
    path_length = nx.shortest_path_length(G, source=source, target=target, weight='weight')
    
    return render_template('result.html', path=path, path_length=path_length, img_path=img_path)

if __name__ == '__main__':
    app.run(debug=True)
