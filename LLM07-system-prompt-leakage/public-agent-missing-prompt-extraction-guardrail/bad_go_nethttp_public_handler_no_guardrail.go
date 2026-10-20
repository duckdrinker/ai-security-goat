package main

import (
	"fmt"
	"net/http"

	"github.com/openai/openai-go"
)

func handler(w http.ResponseWriter, r *http.Request) {
	client := openai.NewClient()
	resp, _ := client.Chat.Completions.New(r.Context(), openai.ChatCompletionNewParams{
		Model:    openai.ChatModelGPT4o,
		Messages: []openai.ChatCompletionMessageParamUnion{openai.UserMessage(r.URL.Query().Get("q"))},
	})
	fmt.Fprint(w, resp.Choices[0].Message.Content)
}

func main() {
	http.HandleFunc("/chat", handler)
	http.ListenAndServe(":8080", nil)
}