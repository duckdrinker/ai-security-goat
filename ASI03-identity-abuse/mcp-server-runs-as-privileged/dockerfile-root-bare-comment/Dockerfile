# Triggers mcp-server-runs-as-privileged: MCP server image with explicit
# `USER root` and a trailing comment that carries no justification marker --
# should still be flagged (regression check: a bare comment must not suppress).
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp
USER root # TODO revisit before release

ENTRYPOINT ["python", "-m", "mcp_server.main"]
