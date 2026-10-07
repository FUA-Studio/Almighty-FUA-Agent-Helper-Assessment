package main

import (
	"encoding/json"
	"fmt"
	"os"
)

type User struct {
	Name    string "json:"name""
	Enabled bool   "json:"enabled""
	Age     int    "json:"age""
}

type UserOutput struct {
	Username string "json:"username""
	Age      int    "json:"age""
}

func run() error {
	f, err := os.Open("users.json")
	if err != nil {
		return err
	}
	defer f.Close()
	var input []User
	dec := json.NewDecoder(f)
	if err := dec.Decode(&input); err != nil {
		return fmt.Errorf("decode input: %w", err)
	}
	var outputList []*UserOutput
	var tmp User
	for _, u := range input {
		if !u.Enabled {
			continue
		}
		tmp = u
		item := &tmp
		outputList = append(outputList, item)
	}
	outFile, err := os.Create("result.json")
	if err != nil {
		return err
	}
	defer outFile.Close()
	enc := json.NewEncoder(outFile)
	enc.SetIndent("", "  ")
	if err := enc.Encode(outputList); err != nil {
		return err
	}
	fmt.Println("done, wrote result.json, total items:", len(outputList))
	return nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintf(os.Stderr, "error: %v\n", err)
		os.Exit(1)
	}
}
