# DA5301W - Python & Data Structures for Data Science

Faculty:
- Prof Satya Jayadev pappu &lt;ps.jayadev@gmail.com&gt;
- Prof Chitra Babu &lt;chitrababu@iitm.ac.in&gt;

DA5301 Course group email: &Lt;da5301w@code.iitm.ac.in&gt;

Midsem question paper with all public & private tests downloaded from https://seek.onlinedegree.iitm.ac.in/courses/ns_25t3iai_daxxxxw?id=83 at [Exams dir](./exams/).

## Notes based on Lectures

**TODO: THEORY DONE, NOTEBOOKS REMAIN!**

### Visualization

libs: 
- matplotlib: figure, axes, plt, ticks, colors, grids, fonts
- plotly (supports interactive  plots (hover, zoom, filter), web dashboards with Dash): figure, plotly.express, graph_objects
- seaborn (built on top of matplotlib)

TODO: practise code in all 3, esp plotly & seaborn (never used before)

variables:
• Numerical : Continous / Discrete
• Categorical : Ordinal (ordered but cant be measured. eg. temp: cold,warm,hot) / Nominal (unordered eg. Gender)

bar plot is discrete, histogram is continous ranges? TODO check

Histogram, Box Plot, Violin Plot (shows both spread, shape of numerical variable) - image above - smooth curve estimation of distribution around box plot:
- using kernel density  estimation estimate continous probability density function from finite sample. kernel function (usually Gaussian) places smooth "bump" on each data point
- so in addition to box plot (median, IQR) info, also shows data frequencies, esp peaks (multi modes)
- shows shape: unimodal / bimodal / skewed / heavy-tailed / tightly clustered

Multi-variate plots show pattern/correlation/trend over time:
- scatter plot
- line plot (eg. stock prices)
- bubble plot: each dot/bubble size indicates external var (numerical), color (categorical)
- heatmap: colored matrix plot. numerical var (x) against 2 categorical: y axis, and color. eg. process/sensor data -> spectral/temporal plot
- parallel numerical plot: superimposed (ie on same X axis) line plots (called polylines), each colored to identify (so color is category of y)

Cmp categorical variables and/or summary plots: Bar plot (optional: grouped, stacked bars), Count plot (subtype of bar - y = frequencies), Pie Chart (prefer bar chart when categories are many or close in size)

### Graphs

lib: networkx - **TODO**: revise `networkx`, `heapq`
• Neighbours of a vertex ?
• shortest path ?
• which vertices reachable from a start vertex ?
• is graph connected - ie all vertices reachable from any vertex?
• map coloring (example of graph problem) - states that share border should have different color. particular example of graph coloring problem
    Four Color Theorem: for planar graphs derived from geographical maps, 4 colors suffice
• Vertex Cover : marking a vertec covers all its edges - find min vertex subset covering all edges. eg. hotel CCTV cameras covering all corridors
• Independent Subset: subset of vertices such that no 2 are connected by an edge
• Matching is mutually disjoint set of edges, ie no 2 edges share any vertex. Find maximal matching

Graph G = (V,E) vertices & edges, E is subset of V x V
• Directed Graph: (v1, v2) in E does not imply (v2, v1) in E
• Undirected Graph: implies

Degree of vertex = Number of edges. For directed, out-degree & in-degree
Path is sequence of vertices v1..vn connected by edges (vi, v(i+1)) in E
Normally path does not re-visit a vertex, if it does it's called a walk
Vertex v is reachable from u if exists path frok u to v

Graph Representations:
• Adjacency Matrix (sparse) of vertices - 1 at (i,j) if (vi,vj) is edge, else 0 - usually we assume no self loops. In Directed Graph, rows are outgoing edges, columns are incoming edges.
• Adjacency List (less space): foreach vertex, store list of outgoing neighbours

Breadth First search:
- FIFO queue of curr level, ie visited vertices whose neighbours yet to be explored
- n = no of vertices, m (no of edges) - if connected graph, n-1 <= m <= n(n-1)/2
- each reachable vertex visited exactly once. max n vertices visited.
- Sum of degrees of all vertices = 2 m
- Complexity: Adjacency Matris has O(n^2), Adjacency List has O(m + n)
- enhanced BFS: 
    * track all shortest paths from start to end, so track parents
    * track vertex distances - save level(i) instead of visited(i)
- in weighted graphs, minimize total cost of edges not number of edges

Depth First Search:
- Backtracking, stack of suspended vertices
- like BFS, each vertex is visited once
- complexity same as BFS: Adjacency Matrix: O(n^2), Adjacency List: O(m + n)
- DFS Paths are NOT shortest paths, unlike BFS

### selection sort, searching in a list, exception handling, debugging & testing

SELECTION SORT
Recurrence means T(n) of an algo

find 1st min put in ans list, 2nd min ... (or inplace: swap 1st min with 1st elem, 2nd min with 2nd elem..)

T(n) = n + (n-1) + .. + 1 = n(n+1)/2 = O(n^2) -- always this much even for almost sorted list

**TODO**: Briefly revise all sort methods' complexity & behaviour with almost-sorted - NOT IN NOTES, but came in assignment 4

-----

SEARCH IN ARRAY
* Linear Search: T(n) = n =O(n)
* Binary Search: (only for sorted list)
   * T(0) = 1, T(n) = T(n//2) + 1 => T(n) = 2 + log n

------

DEBUGGING
Error types: Syntax, Runtime, Logic, Data (eg. missing val, extra category etc.), Performance

Validation: Pydantic (inherit BaseClassModel, Field()), Pandera (schema validation of Pandas / Polars / Pyspark df, integrates with pytest, on fail shows row, column, failing rule)

* Notebook: `%pdb on` (auto enter pdb on error), `%debug` (inspect after error)
* VS Code: Debug and Run, put breakpoints

Tests: Unit, Integration, Performance, End to End

Pytest: Fixture, Parameterized Test, pytest.raises(), 
float approx equal -->
 assert x == pytest.approx(3.14, [OPTIONAL precision: 0.2])

### NOTE: (pytorch & tensorflow, AI assisted coding) lecture slides but not in endsem
