"""MongoDB-backed LangGraph checkpointer connected with no credentials.

Triggers agent-memory-store-without-integrity: the connection string carries
no username/password, so the memory backend is a network-reachable store
with no authentication or integrity controls.
"""
from langgraph.checkpoint.mongodb import MongoDBSaver

saver = MongoDBSaver.from_conn_string("mongodb://0.0.0.0:27017/")
graph = builder.compile(checkpointer=saver)
