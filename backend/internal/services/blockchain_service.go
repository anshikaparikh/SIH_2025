
package services

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

type BlockchainRequest struct {
	CertificateID string `json:"certificate_id"`
	Hash          string `json:"hash"`
}

func ComputeHashFromFile(path string) string {
	f, err := os.Open(path)
	if err != nil {
		return ""
	}
	defer f.Close()

	h := sha256.New()
	io.Copy(h, f)
	return hex.EncodeToString(h.Sum(nil))
}
func StoreHash(certID, hash string) error {
	reqBody := map[string]string{
		"certificate_id": certID,
		"hash":           hash,
	}
	jsonBody, err := json.Marshal(reqBody)
	if err != nil {
		return fmt.Errorf("marshal json: %w", err)
	}

	// Send POST to blockchain service
	resp, err := http.Post("http://localhost:9000/store", "application/json", bytes.NewBuffer(jsonBody))
	if err != nil {
		return fmt.Errorf("http post: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		bodyBytes, _ := io.ReadAll(resp.Body)
		return fmt.Errorf("blockchain store error: %d, %s", resp.StatusCode, string(bodyBytes))
	}

	var regResp map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&regResp)
	fmt.Printf("Blockchain stored: cert %s, status %s\n", certID, regResp["status"])

	return nil
}

func VerifyHash(certID, hash string) (bool, error) {
	req := BlockchainRequest{CertificateID: certID, Hash: hash}
	body, _ := json.Marshal(req)

	resp, err := http.Post("http://localhost:9000/verify", "application/json", bytes.NewBuffer(body))
	if err != nil {
		return false, err
	}
	defer resp.Body.Close()

	var out map[string]bool
	json.NewDecoder(resp.Body).Decode(&out)
	return out["exists"], nil
}
