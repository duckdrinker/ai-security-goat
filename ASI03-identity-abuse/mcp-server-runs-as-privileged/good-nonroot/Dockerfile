# Mitigated: same MCP server image, but with an explicit non-root USER.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp \
    && adduser --system --no-create-home mcp-user
USER mcp-user

ENTRYPOINT ["python", "-m", "mcp_server.main"]
