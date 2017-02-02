from . import api_restful
from .resource import *


# All aggregate queries.
# - Get all queries
# - Post query by user-id
api_restful.add_resource(AggregateQueriesAllResource,
    "/aggregate_queries",
    endpoint="aggregate_queries_all")

# Aggregate query by user-id and query-id.
# - Get query by user-id and query-id
# - Patch query by user-id and query-id
# - Delete by user-id and query-id
api_restful.add_resource(AggregateQueryResource,
    "/aggregate_queries/<uuid:user_id>/<uuid:query_id>",
    endpoint="aggregate_query")

# Aggregate queries by user-id.
# - Get queries by user-id
api_restful.add_resource(AggregateQueriesResource,
    "/aggregate_queries/<uuid:user_id>",
    endpoint="aggregate_queries")
