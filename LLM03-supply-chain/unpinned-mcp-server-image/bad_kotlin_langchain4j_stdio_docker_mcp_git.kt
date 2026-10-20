package demo

import dev.langchain4j.mcp.client.DefaultMcpClient
import dev.langchain4j.mcp.client.transport.stdio.StdioMcpTransport

fun main() {
    val transport = StdioMcpTransport.Builder()
        .command(listOf("/usr/local/bin/docker", "run", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "-i", "mcp/git"))
        .logEvents(true)
        .build()
    val client = DefaultMcpClient.Builder().transport(transport).build()
    client.close()
}