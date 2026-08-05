"""Mitigated: the LangGraph checkpointer connection requires authentication.

The credential comes from an environment variable (not hardcoded) and is
part of the connection string passed to the saver.
"""
import os

from langgraph.checkpoint.redis import RedisSaver

saver = RedisSaver.from_conn_string(f"redis://:{os.environ['REDIS_PASSWORD']}@cache:6379")
graph = builder.compile(checkpointer=saver)
