package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/openai/openai-go"
)

func sendEmail(args string) string {
	return "sent " + args
}

// flagged reports whether the moderation model rejects the user input.
func flagged(ctx context.Context, client openai.Client, input string) bool {
	res, err := client.Moderations.New(ctx, openai.ModerationNewParams{
		Input: openai.ModerationNewParamsInputUnion{OfString: openai.String(input)},
	})
	return err != nil || res.Results[0].Flagged
}

func chat(w http.ResponseWriter, r *http.Request) {
	client := openai.NewClient()
	q := r.URL.Query().Get("q")
	if flagged(r.Context(), client, q) {
		http.Error(w, "input rejected by the input guardrail", 400)
		return
	}
	tools := []openai.ChatCompletionToolParam{{
		Function: openai.FunctionDefinitionParam{
			Name:        "send_email",
			Description: openai.String("Sends an email to the given address"),
		},
	}}
	resp, err := client.Chat.Completions.New(r.Context(), openai.ChatCompletionNewParams{
		Model:     openai.ChatModelGPT4o,
		MaxTokens: openai.Int(256),
		Messages:  []openai.ChatCompletionMessageParamUnion{openai.UserMessage(q)},
		Tools:     tools,
	})
	if err != nil {
		http.Error(w, err.Error(), 500)
		return
	}
	for _, call := range resp.Choices[0].Message.ToolCalls {
		fmt.Fprintln(w, sendEmail(call.Function.Arguments))
	}
}

func main() {
	http.HandleFunc("/chat", chat)
	http.ListenAndServe(":8080", nil)
}