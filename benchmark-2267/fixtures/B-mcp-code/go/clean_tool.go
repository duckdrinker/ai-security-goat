package main

import (
	"github.com/mark3labs/mcp-go/mcp"
	"github.com/mark3labs/mcp-go/server"
)

func register(s *server.MCPServer) {
	tool := mcp.NewTool("add",
		mcp.WithDescription("Adds two numbers and returns the sum."),
		mcp.WithNumber("a", mcp.Required()),
		mcp.WithNumber("b", mcp.Required()),
	)
	s.AddTool(tool, nil)
}
