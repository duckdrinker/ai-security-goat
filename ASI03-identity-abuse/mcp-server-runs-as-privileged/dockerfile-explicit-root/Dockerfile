# Triggers mcp-server-runs-as-privileged: MCP server image with an explicit
# `USER root` -- privilege is declared, not just defaulted.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp
USER root

ENTRYPOINT ["python", "-m", "mcp_server.main"]
