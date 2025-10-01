package services

import (
	"encoding/json"
	"fmt"
	"time"

	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/amanswami/fake-degree-backend/internal/ml"
)

type AIResponse struct {
	Score   float64 `json:"score"`
	Details string  `json:"details"`
}

func VerifyWithAI(filePath string, cert *db.Certificate) (*AIResponse, error) {
	// Call real ML service
	vr, err := ml.SendToMLService(cert.ID, filePath)
	if err != nil {
		return nil, fmt.Errorf("ML service call failed: %w", err)
	}

	// Update certificate with extracted data
	if extracted, ok := vr.ExtractedData["student_name"]; ok {
		cert.StudentName = extracted
	}
	if extracted, ok := vr.ExtractedData["roll_number"]; ok {
		cert.RollNumber = extracted
	}
	if extracted, ok := vr.ExtractedData["course"]; ok {
		cert.Course = extracted
	}
	if extracted, ok := vr.ExtractedData["issued_on"]; ok {
		// Parse date if needed
		cert.IssuedOn = parseDate(extracted)
	}

	// Save updated cert
	// Note: Caller should save cert after this call

	checksJson, _ := json.Marshal(vr.Checks)
	details := fmt.Sprintf("ML verification: score=%.2f, checks=%s, status=%s", vr.Score, string(checksJson), vr.Status)

	return &AIResponse{
		Score:   vr.Score,
		Details: details,
	}, nil
}

func parseDate(dateStr string) time.Time {
	// Simple date parsing, extend as needed
	formats := []string{"2006-01-02", "01/02/2006", "02/01/2006"}
	for _, f := range formats {
		if t, err := time.Parse(f, dateStr); err == nil {
			return t
		}
	}
	return time.Time{}
}
