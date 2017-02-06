from . import api_restful
from .resource import *


# All aggregate query messages.
# - Get all messages
# - Post message by query-id
api_restful.add_resource(AggregateQueryMessagesResource,
    "/aggregate_query_messages",
    endpoint="aggregate_query_messages")

# Aggregate query message by query-id.
# - Get query message by query-id
api_restful.add_resource(AggregateQueryMessageResource,
    "/aggregate_query_messages/<uuid:query_id>",
    endpoint="aggregate_query_message")
