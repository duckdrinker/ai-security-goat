"""Every turn is pushed onto a Redis list with no TTL and no trim.

Triggers unbounded-agent-memory: there is no key expiry (`expire`) and
no cap on list length (`ltrim`) anywhere, so the memory store grows
forever for long-lived sessions.
"""
import json

import redis

r = redis.Redis(host="localhost", port=6379)


def remember_turn(session_id: str, role: str, content: str):
    r.rpush(f"memory:{session_id}", json.dumps({"role": role, "content": content}))
    # no r.expire(...) and no r.ltrim(...) anywhere
