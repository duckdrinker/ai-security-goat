package main

import (
	"context"
	"os/exec"

	"github.com/anthropics/anthropic-sdk-go"
)

func run(question string) error {
	client := anthropic.NewClient()
	msg, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		Model:     anthropic.ModelClaude3_7SonnetLatest,
		MaxTokens: 256,
		Messages:  []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock("Shell command for: " + question))},
	})
	if err != nil {
		return err
	}
	return exec.Command("sh", "-c", msg.Content[0].Text).Run()
}