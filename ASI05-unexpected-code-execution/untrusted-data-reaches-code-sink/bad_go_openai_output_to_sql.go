package main

import (
	"context"
	"database/sql"

	"github.com/openai/openai-go"
)

func lookup(db *sql.DB, question string) error {
	client := openai.NewClient()
	resp, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
		Model:    openai.ChatModelGPT4o,
		Messages: []openai.ChatCompletionMessageParamUnion{openai.UserMessage("SQL for: " + question)},
	})
	if err != nil {
		return err
	}
	_, err = db.Query(resp.Choices[0].Message.Content)
	return err
}