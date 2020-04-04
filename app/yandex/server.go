package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"strings"
)

/*
Meaning struct to store the meaning
*/
type Meaning struct {
	Word       string `json:"word"`
	POS        string `json:"type"`
	Definition string `json:"definition"`
}

/*
Response JSON respsonse
*/
type Response struct {
	Definitions []Meaning `json:"definitions"`
}

const wordListURL = "../../words_alpha.txt"
const baseURL = "https://owlbot.info/api/v3/dictionary/"
const apiKey = "Token bd08ade0ad1688c0caed2b814cac344deef3751f"

func buildURL(word string, baseURL string) string {
	return fmt.Sprintf("%s%s", baseURL, word)
}

func getMeaning(word string) string {
	var url = buildURL(word, baseURL)
	var jsonResp = makeReq(url, apiKey)
	return jsonResp
}

func makeReq(url string, apiKey string) string {
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Set("Authorization", apiKey)
	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	resp, _ := client.Do(req)
	jsonStr, _ := ioutil.ReadAll(resp.Body)
	return string(jsonStr)
}

func fileOpen(filePath string) string {
	dat, err := ioutil.ReadFile(filePath)
	if err != nil {
		log.Fatal(err)
	}
	return string(dat)
}

func parseResponse(jsonStr string) Response {
	resp := Response{}
	err := json.Unmarshal([]byte(jsonStr), &resp)
	if err != nil {
		log.Println(err)
	}
	return resp
}

func splitWords(wordsRaw string) []string {
	return strings.Split(wordsRaw, "\r\n")
}

func main() {
	var wordsRaw = fileOpen(wordListURL)
	var wordsSplit = splitWords(wordsRaw)
	for index, word := range wordsSplit {
		// var meaning = getMeaning(word)
		fmt.Print((getMeaning(word)))
		// fmt.Println(meaning)
		if index == 100 {
			break
		}
	}

}
