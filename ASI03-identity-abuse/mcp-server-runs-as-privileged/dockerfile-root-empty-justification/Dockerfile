# Triggers mcp-server-runs-as-privileged: MCP server image with explicit
# `USER root` and a justification marker with no text after the colon --
# should still be flagged (an empty marker does not count).
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp
USER root # justification:

ENTRYPOINT ["python", "-m", "mcp_server.main"]
