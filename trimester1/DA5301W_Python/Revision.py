#region Logging

import logging 
logging.basicConfig(level=logging.DEBUG)

config_dict = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": "app.log",
            "formatter": "default",
        },
    },
    "loggers": {
        "my_app": {
            "level": "WARNING",
            "handlers": ["file"],
            "propagate": False,
        },
        "myapp_database": {
            "level": "WARNING",
            "handlers": ["console"],
        },
    },
}
logging.config.dictConfig(config_dict)

logging.lastResort = None   # lastResort handles any unhandled log events by any else; set to None causes unhandled to be discarded
root_logger = logging.getLogger()
logger = logging.getLogger('example')
logger.propagate = False    # prevent upgrade propogation

stream_handler = logging.StreamHandler()  # console (sys.stderr by default)
stream_handler.setLevel(logging.WARNING)
stream_handler.setFormatter(logging.Formatter("%(astime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(stream_handler)   

# .debug(), .info(), .warning(), .error(), .critical()

class MyLogFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno >= logging.WARNING
    
logger.addFilter(MyLogFilter())
# NOTE: class not necessary, direct function would also work: (record: logging.LogRecord) -> bool

#endregion Logging

#region Debugging&Testing

# custom exception subclass
class MyException(Exception):
    def __init__(self, message: str):
        super().__init__(message)

# Jupyter Notebook commands: 
# %pdb on    # auto-enter pdb if exception raised
# %debug     # enter ipydb for last cell error
# %%writefile /path/to/script.py   # in notebook, save code (under command in rest of cell) to a new script

# pytest test_script.py --tb=no    # disable traceback on failure
import pytest
x = 3.14302
assert pytest.approx(x) == 3.14        # fail: default precision is 1e-6 I think?
assert pytest.approx(x, 2) == 3.14     # pass: 2 is precision
assert 3.14 == pytest.approx(x, 2)     # pass: other way around also works

# Data Validation: generic including pandas
from pydantic import BaseModel, Field
class User(BaseModel):
    age: int = Field(gt=0)
    score: float = Field(ge=0, le=100)
u1 = User(age=25, score=90)   # Satisfies the conditions
u2 = User(age=-5, score=150)  # throws pydantic ValidationError

# Data Validation: df schema (pandas, polar, pyspark etc.)
import pandas as pd
df = pd.DataFrame({
    "age": [25, -5, 30],
    "score": [90, 150, 80],
})

import pandera.pandas as pa
schema = pa.DataFrameSchema({
    "age": pa.Column(int, pa.Check.gt(0), nullable=False),
    "score": pa.Column(int, pa.Check.between(0, 100)),
})
try:
    schema.validate(df, lazy=True)
except pa.errors.SchemaErrors as e:
    print(e.failure_cases) 
    # a pandas df with columns: 
    # schema_context (Column) | 
    # column (age,score) | 
    # check (greater_than(0),in_range(0,100)) | 
    # check_number (0) | 
    # failure_case (column cell value that failed - -5,150) | 
    # index (of failing row - eg. 1)

#endregion Debugging&Testing

#region NetworkX
import networkx as nx
graph = nx.Graph()
graph.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])

# DFS
list(nx.dfs_edges(graph, source=1))   # DFS ; list() to force generator object
dfs_tree: nx.DiGraph = nx.dfs_tree(G, source=1) ; list(dfs_tree)

# BFS: .bfs_edges(), .bfs_tree()

graph.degree[2]       # 2 is node id ; .degree, .in_degree, .out_degree are all dict-like objects
nx.draw_planar(graph)
plt.show()
pos = nx.spring_layout(graph)   # TODO: not sure exactly what it does
nx.draw(graph, pos)
nx.draw_networkx_edge_labels(graph, pos)
nx.draw_sprint(graph, with_labels=True)

print(list(nx.shortest_path(graph, source=1, target=3)))
print(nx.shortest_path_length(graph, source=1, target=3))
distances, path = nx.single_source_dijkstra(graph, source=1)  #,weight=

G = nx.read_adjlist('/path/to/graph_adj.txt') #, create_using=nx.Graph() (undirected) OR nx.DiGraph() (directed)

# TODO: rest of NetworkX notebook

#endregion NetworkX

#region visualization
import matplotlib.pyplot as plt
plt.figure()      # start new
plt.plot(x, y, label="Label 1", linestyle="--")  # line plot
# plt.scatter(x,y,color="red",marker="o")
# plt.bar(categories,values)
# plt.hist(data, bins=20)   # unlike bar, frequencies auto determined
plt.title("Plottitle")
plt.xlabel("Xname")
plt.ylabel("Yname")
plt.legend()      # add box of plot names
plt.show()

#subplots
figure, axes = plt.subplots(2,2,figsize=(8,6))  # usually 2d grid of plots
axes[0,0].plot(...)
axes[0,0].set_title("subplot title 1")
# ... rest
figure.suptitle("Overall title")
plt.show()

import seaborn as sns
sns.set_theme(style="whitegrid", palette="Set 2") # global theme

df = sns.load_dataset('iris')  # famous pre-packaged Iris dataset
sns.scatterplot(df, x="sepal_length", y="sepal_width", hue="species")  # hue=bubble color by col; ,style="species", s=50 # bubble marker size
plt.show()   # since seaborn is just wrapper on top of matplotlib
sns.histplot(df["petal_length"])   # can pass column series directly like this also
sns.boxplot(x=df['species'], y=df['petal_length'])

corr_df = df.select_dtypes("number").corr()
sns.heatmap(corr_df, annot=True, cmap="coolwarm", linewidths=0.5)

import plotly.express as px
df = px.data.iris()
fig = px.scatter()
fig.show(df, x="xcol", y="ycol", color="color_col", symbol="symbol_col", hover_data=["hover_columns"], title="Title")
#endregion visualization