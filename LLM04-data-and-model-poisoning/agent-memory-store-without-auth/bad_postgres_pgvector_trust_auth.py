"""Postgres-backed LangGraph checkpointer with an empty password.

Triggers agent-memory-store-without-integrity: the connection string uses
an empty password over an open host binding, exposing all persisted
agent memory.
"""
from langgraph.checkpoint.postgres import PostgresSaver

saver = PostgresSaver.from_conn_string("postgresql://postgres:@0.0.0.0:5432/agent_memory")
graph = builder.compile(checkpointer=saver)
