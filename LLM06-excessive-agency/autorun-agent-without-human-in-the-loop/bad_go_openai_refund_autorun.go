package main

import (
	"context"

	"github.com/openai/openai-go"
)

func refund(orderID string) string {
	// moves real money
	return "refunded " + orderID
}

func main() {
	client := openai.NewClient()
	tools := []openai.ChatCompletionToolParam{{
		Function: openai.FunctionDefinitionParam{
			Name:        "refund",
			Description: openai.String("Refunds an order to the customer"),
		},
	}}
	messages := []openai.ChatCompletionMessageParamUnion{
		openai.UserMessage("Process every pending refund request."),
	}
	for {
		resp, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
			Model:    openai.ChatModelGPT4o,
			Messages: messages,
			Tools:    tools,
		})
		if err != nil {
			return
		}
		for _, call := range resp.Choices[0].Message.ToolCalls {
			out := refund(call.Function.Arguments)
			messages = append(messages, openai.ToolMessage(out, call.ID))
		}
	}
}