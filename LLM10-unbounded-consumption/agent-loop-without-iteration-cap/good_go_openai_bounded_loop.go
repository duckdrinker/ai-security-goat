package main

import (
	"context"

	"github.com/openai/openai-go"
)

func main() {
	client := openai.NewClient()
	goal := "keep improving the report"
	for i := 0; i < 5; i++ {
		resp, _ := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
			Model:     openai.ChatModelGPT4o,
			MaxTokens: openai.Int(256),
			Messages:  []openai.ChatCompletionMessageParamUnion{openai.UserMessage(goal)},
		})
		goal = resp.Choices[0].Message.Content
	}
}