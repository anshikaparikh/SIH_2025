package services

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
)

type BlockchainResponse struct {
	Valid   bool   `json:"valid"`
	Message string `json:"message"`
}

func VerifyWithBlockchain(certHash string) (*BlockchainResponse, error) {
	url := "http://localhost:5001/verify" // blockchain_service Flask API

	payload := map[string]string{"hash": certHash}
	body, _ := json.Marshal(payload)

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(body))
	if err != nil {
		return nil, fmt.Errorf("blockchain service error: %w", err)
	}
	defer resp.Body.Close()

	var result BlockchainResponse
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("decode blockchain response: %w", err)
	}

	return &result, nil
}
