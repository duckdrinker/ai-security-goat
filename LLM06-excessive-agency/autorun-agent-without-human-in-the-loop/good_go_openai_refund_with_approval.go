package main

import (
	"bufio"
	"context"
	"fmt"
	"os"
	"strings"

	"github.com/openai/openai-go"
)

func approve(prompt string) bool {
	fmt.Print(prompt + " [y/N] ")
	line, _ := bufio.NewReader(os.Stdin).ReadString('\n')
	return strings.EqualFold(strings.TrimSpace(line), "y")
}

func refund(orderID string) string {
	return "refunded " + orderID
}

func main() {
	client := openai.NewClient()
	tools := []openai.ChatCompletionToolParam{{
		Function: openai.FunctionDefinitionParam{
			Name:        "refund",
			Description: openai.String("Refunds an order after a human approves it"),
		},
	}}
	messages := []openai.ChatCompletionMessageParamUnion{
		openai.UserMessage("Process the refund request for order 42."),
	}
	resp, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
		Model:     openai.ChatModelGPT4o,
		MaxTokens: openai.Int(256),
		Messages:  messages,
		Tools:     tools,
	})
	if err != nil {
		return
	}
	for _, call := range resp.Choices[0].Message.ToolCalls {
		if !approve("Run " + call.Function.Name + "?") {
			continue
		}
		fmt.Println(refund(call.Function.Arguments))
	}
}