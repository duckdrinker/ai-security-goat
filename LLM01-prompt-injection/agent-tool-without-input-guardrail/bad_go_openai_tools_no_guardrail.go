package main

import (
	"fmt"
	"net/http"

	"github.com/openai/openai-go"
)

func sendEmail(args string) string {
	return "sent " + args
}

func chat(w http.ResponseWriter, r *http.Request) {
	client := openai.NewClient()
	tools := []openai.ChatCompletionToolParam{{
		Function: openai.FunctionDefinitionParam{
			Name:        "send_email",
			Description: openai.String("Sends an email to the given address"),
		},
	}}
	resp, err := client.Chat.Completions.New(r.Context(), openai.ChatCompletionNewParams{
		Model:    openai.ChatModelGPT4o,
		Messages: []openai.ChatCompletionMessageParamUnion{openai.UserMessage(r.URL.Query().Get("q"))},
		Tools:    tools,
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