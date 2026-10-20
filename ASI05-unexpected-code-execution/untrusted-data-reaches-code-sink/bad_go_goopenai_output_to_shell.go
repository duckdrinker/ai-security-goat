package main

import (
	"context"
	"os/exec"

	"github.com/sashabaranov/go-openai"
)

func run(question string) error {
	client := openai.NewClient("key")
	resp, err := client.CreateChatCompletion(context.Background(), openai.ChatCompletionRequest{
		Model:    openai.GPT4o,
		Messages: []openai.ChatCompletionMessage{{Role: "user", Content: "Shell command for: " + question}},
	})
	if err != nil {
		return err
	}
	return exec.Command("sh", "-c", resp.Choices[0].Message.Content).Run()
}