# Mitigated: MCP server image with explicit `USER root`, but with a
# justification marker on the same line -- should be suppressed.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp
USER root  # justification: needs CAP_NET_RAW to probe the tool network

ENTRYPOINT ["python", "-m", "mcp_server.main"]
