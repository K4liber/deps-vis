import cytoscape, { Stylesheet } from 'cytoscape';
import dagre from 'cytoscape-dagre';

cytoscape.use( dagre );

fetch('/src/resources/fastapi.json')
  .then(response => response.json())
  .then(graph_data => {
    const container = document.getElementById('cy');
    const layout = {
        name: 'dagre'
    };

    fetch('/src/resources/style/cytoscape-stylesheet.json')
        .then(response => response.json())
        .then(cytoscapeStylesheet => {
            const cy = cytoscape({
                container,
                elements: graph_data.nodes.concat(graph_data.edges),
                layout,
                style: cytoscapeStylesheet as Stylesheet[]
            });
        })
  })
  .catch(error => {
    console.error('Error loading JSON data:', error);
  });
