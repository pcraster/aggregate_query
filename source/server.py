import os
from emis_aggregate_query import create_app


app = create_app(os.getenv("EMIS_AGGREGATE_QUERY_CONFIGURATION"))
