# -*- coding: utf-8 -*-
from pyvis.network import Network
import streamlit.components.v1 as components
import tempfile
import os

def plot_interactive_network(currencies, path=None):
    """
    Creates an interactive, draggable network graph using Pyvis.
    Avoids the "hairball" effect by simplifying edges unless a path is found.
    """
    # Initialize dynamic network
    net = Network(height='500px', width='100%', bgcolor='#ffffff', font_color='black', directed=True)

    # Add nodes
    for curr in currencies:
        if path and curr in path:
            # Highlight nodes in the arbitrage path
            net.add_node(curr, label=curr, color='#ff4b4b', size=25, title=f"{curr} (Arbitrage Path)")
        else:
            # Fade out other nodes if a path exists, otherwise default blue
            node_color = '#d3d3d3' if path else '#1f77b4'
            net.add_node(curr, label=curr, color=node_color, size=15)

    # Add edges
    if path:
        # Only draw the exact arbitrage path to make it extremely clear
        for i in range(len(path) - 1):
            net.add_edge(path[i], path[i+1], color='#ff4b4b', width=3, arrows='to')
    else:
        # Draw simplified connections for aesthetics without lagging the browser
        base_currencies = ['USD', 'EUR', 'GBP', 'JPY']
        for curr in base_currencies:
            if curr in currencies:
                for other in base_currencies:
                    if curr != other and other in currencies:
                        net.add_edge(curr, other, color='#e0e0e0', width=1, arrows='to')

    # Configure physics for smooth draggable interactions
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
            "gravitationalConstant": -50,
            "centralGravity": 0.01,
            "springLength": 100,
            "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    # Save to a temporary HTML file and read it back for Streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp_file:
        net.save_graph(tmp_file.name)
        html_file_path = tmp_file.name

    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_data = f.read()

    os.remove(html_file_path) # Clean up
    
    # Render in Streamlit
    components.html(html_data, height=510)