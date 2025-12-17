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

# WIP graphs: NetworkX
import networkx as nx
graph = nx.Graph()
graph.add_edges_from([(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)])
list(nx.dfs_edges(graph, source=1))   # DFS ; list() to force generator object
dfs_tree: nx.DiGraph = nx.dfs_tree(G, source=1) ; list(dfs_tree)
graph.degree[2]       # 2 is node id ; .degree, .in_degree, .out_degree are all dict-like objects

# TODO: rem notebooks