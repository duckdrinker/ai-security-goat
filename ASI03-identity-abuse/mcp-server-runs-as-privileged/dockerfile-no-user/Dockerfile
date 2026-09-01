# Triggers mcp-server-runs-as-privileged: MCP server image (RUN pip install
# mcp, entrypoint runs the MCP server) with no USER directive at all -- runs
# as root by default.
#
# NOTE (unconfirmed): the exact "MCP marker" the real detector looks for was
# not specified by the dev -- pending reply on xygeni-product-backlog#1358.
# This fixture guesses "an MCP SDK dependency installed + an entrypoint that
# launches it" as the marker. Revisit once confirmed.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install mcp fastmcp

ENTRYPOINT ["python", "-m", "mcp_server.main"]
