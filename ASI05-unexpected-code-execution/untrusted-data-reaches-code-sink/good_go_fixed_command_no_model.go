package main

import (
	"fmt"
	"net/http"
	"os/exec"
)

func main() {
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprint(w, "ok")
	})
	_ = exec.Command("ls", "-l").Run()
	http.ListenAndServe(":8080", nil)
}