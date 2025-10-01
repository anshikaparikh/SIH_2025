package services

import "github.com/amanswami/fake-degree-backend/internal/db"

type AIResult struct {
	CertificateID string                   `json:"certificate_id"`
	Checks        []map[string]interface{} `json:"checks"`
	Score         float64                  `json:"score"`
	Message       string                   `json:"message,omitempty"`
}

func CallAI(filePath string, cert *db.Certificate) (*AIResult, error) {
	// Basic AI logic based on extracted fields
	var checks []map[string]interface{}
	score := 0.0
	message := "AI verification based on extracted fields"

	// Check if key fields are present
	fieldCount := 0
	if cert.StudentName != "" {
		fieldCount++
		checks = append(checks, map[string]interface{}{"check": "student_name", "result": "extracted"})
	}
	if cert.RollNumber != "" {
		fieldCount++
		checks = append(checks, map[string]interface{}{"check": "roll_number", "result": "extracted"})
	}
	if cert.Course != "" {
		fieldCount++
		checks = append(checks, map[string]interface{}{"check": "course", "result": "extracted"})
	}
	if !cert.IssuedOn.IsZero() {
		fieldCount++
		checks = append(checks, map[string]interface{}{"check": "issued_on", "result": "extracted"})
	}

	// Simple score: 0.25 per field, max 1.0
	score = float64(fieldCount) * 0.25

	if score >= 0.75 {
		message = "High confidence: Most fields extracted successfully"
	} else if score >= 0.5 {
		message = "Medium confidence: Partial fields extracted"
	} else {
		message = "Low confidence: Few or no fields extracted - possible tampering"
		checks = append(checks, map[string]interface{}{"check": "tampering", "result": "suspected"})
	}

	return &AIResult{
		CertificateID: cert.ID,
		Checks:        checks,
		Score:         score,
		Message:       message,
	}, nil
}
