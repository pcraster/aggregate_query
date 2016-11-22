import os
from aggregate_query import create_app


app = create_app(os.getenv("AGGREGATE_QUERY_CONFIGURATION"))
