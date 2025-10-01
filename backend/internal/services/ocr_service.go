package services

import (
	"context"
	"errors"
	"os/exec"
)

// Minimal OCR stub: in production, you'd call Tesseract, Google Vision, AWS Textract or a local OCR microservice.
func RunOCR(ctx context.Context, filePath string) (map[string]string, error) {
	// Example: call tesseract and parse. Here we return an error to indicate stub.
	_ = exec.CommandContext(ctx, "tesseract", "--version")
	return nil, errors.New("ocr not implemented: wire in tesseract or cloud ocr")
}
