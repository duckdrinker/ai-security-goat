"""Redis-backed LangGraph checkpointer with no password in the connection string.

Triggers agent-memory-store-without-integrity: network-reachable memory
store, no authentication configured.
"""
from langgraph.checkpoint.redis import RedisSaver

saver = RedisSaver.from_conn_string("redis://cache:6379")
graph = builder.compile(checkpointer=saver)
