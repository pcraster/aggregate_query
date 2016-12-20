from . import api_restful
from .resource import *


# All aggregate query results.
# - Get all results
# - Post result by query-id
api_restful.add_resource(AggregateQueryResultsResource,
    "/aggregate_query_results",
    endpoint="aggregate_query_results")

# Aggregate query result by query-id.
# - Get query result by query-id
api_restful.add_resource(AggregateQueryResultResource,
    "/aggregate_query_results/<uuid:query_id>",
    endpoint="aggregate_query_result")
