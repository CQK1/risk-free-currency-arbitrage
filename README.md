Foreign Exchange Arbitrage Detector

Project Overview

This project is a quantitative analysis tool based on the Bellman-Ford Algorithm from Graph Theory. It automatically identifies and calculates potential risk-free arbitrage paths by analyzing real-time cross-exchange rates of various currencies in the global forex market.

Featuring an interactive web interface, the tool provides a visual representation of exchange rate networks and arbitrage logic. It also incorporates a "Transaction Fee" parameter to ensure the model aligns closely with real-world financial environments.

Core Theory & Algorithmic Logic

In financial markets, an arbitrage opportunity occurs when a sequence of currency exchanges results in a final amount greater than the initial principal.

Suppose we have currencies $A, B,$ and $C$, with exchange rates $R_{AB}, R_{BC},$ and $R_{CA}$. An arbitrage opportunity exists if the product of these rates is greater than 1:

$$R_{AB} \times R_{BC} \times R_{CA} > 1$$

Mathematical Transformation

Traditional shortest-path algorithms in graph theory (like Dijkstra) use addition to calculate path weights, whereas currency exchange involves multiplication. To transform this financial problem into a graph theory model that a computer can process, this project employs logarithmic transformation.

Taking the natural logarithm of both sides of the arbitrage condition:

$$\ln(R_{AB} \times R_{BC} \times R_{CA}) > \ln(1)$$

$$\ln(R_{AB}) + \ln(R_{BC}) + \ln(R_{CA}) > 0$$

Multiplying both sides by -1 reverses the inequality:

$$(-\ln(R_{AB})) + (-\ln(R_{BC})) + (-\ln(R_{CA})) < 0$$

Conclusion:
By treating different currencies as nodes and the negative natural logarithm of the exchange rate ($-\ln(R)$) as the weight of a directed edge, finding a profitable arbitrage path is mathematically equivalent to identifying a negative cycle within a directed graph.

This project utilizes the Bellman-Ford algorithm, which is specifically designed to handle graphs with negative edge weights and accurately detect negative cycles.

Tech Stack

Python: Core algorithm implementation.

Streamlit: Interactive web dashboard for data visualization.

NetworkX & Matplotlib: Graph network construction and visual rendering.

Pandas & NumPy: Matrix data manipulation and mathematical operations.

How to Run Locally

Clone this repository to your local machine.

(Optional but recommended) Create a virtual environment.

Install project dependencies:

pip install -r requirements.txt


Launch the Streamlit application:

streamlit run app.py


Open the local address provided in your browser (usually http://localhost:8501) to start using the tool.

Project Highlights

Interdisciplinary Application: Successfully applies Operations Research and Graph Theory to a practical quantitative finance scenario.

Real-world Accuracy: Unlike purely theoretical models, this tool supports dynamic "Transaction Fee" adjustments to filter out "phantom" arbitrage opportunities that would be unprofitable in practice.

Intuitive Visualization: Replaces dense terminal output with a user-friendly interface and clear network maps, making complex algorithmic results easy to understand at a glance.