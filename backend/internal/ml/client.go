package ml

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
)

type VerificationResponse struct {
	CertificateID string                   `json:"certificate_id"`
	ExtractedData map[string]string        `json:"extracted_data"`
	Checks        []map[string]interface{} `json:"checks"`
	Score         float64                  `json:"score"`
	Status        string                   `json:"status"`
}

func SendToMLService(certID, filePath string) (*VerificationResponse, error) {
	// Open file
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("open file: %w", err)
	}
	defer file.Close()

	// Create multipart form
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)
	part, err := writer.CreateFormFile("file", filePath)
	if err != nil {
		return nil, fmt.Errorf("create form file: %w", err)
	}
	io.Copy(part, file)

	// Add cert ID
	writer.WriteField("certificate_id", certID)

	err = writer.Close()
	if err != nil {
		return nil, fmt.Errorf("close writer: %w", err)
	}

	// Send POST to Python service
	req, err := http.NewRequest("POST", "http://localhost:8000/upload", body)
	if err != nil {
		return nil, fmt.Errorf("new request: %w", err)
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("http post: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("ml service error: %d", resp.StatusCode)
	}

	var vr VerificationResponse
	if err := json.NewDecoder(resp.Body).Decode(&vr); err != nil {
		return nil, fmt.Errorf("decode response: %w", err)
	}
	return &vr, nil
}
