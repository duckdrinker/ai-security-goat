package main

import (
	"context"
	"encoding/json"

	"github.com/openai/openai-go"
)

func extract(text string) (map[string]any, error) {
	client := openai.NewClient()
	resp, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
		Model:    openai.ChatModelGPT4o,
		Messages: []openai.ChatCompletionMessageParamUnion{openai.UserMessage("Extract JSON from: " + text)},
	})
	if err != nil {
		return nil, err
	}
	var out map[string]any
	err = json.Unmarshal([]byte(resp.Choices[0].Message.Content), &out)
	return out, err
}