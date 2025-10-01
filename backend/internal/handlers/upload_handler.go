package handlers

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/amanswami/fake-degree-backend/internal/config"
	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/amanswami/fake-degree-backend/internal/services"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

// POST /api/v1/certificates/upload
func UploadCertificateHandler(dbConn *gorm.DB, cfg *config.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		user, exists := c.Get("user")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "user not found in context"})
			return
		}
		u := user.(db.User)

		// --- 1. Get uploaded file
		file, err := c.FormFile("file")
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "file is required"})
			return
		}

		// --- 2. Save file to disk
		id := uuid.New().String()
		os.MkdirAll(cfg.StoragePath, 0700)
		ext := filepath.Ext(file.Filename)
		outPath := filepath.Join(cfg.StoragePath, fmt.Sprintf("%s%s", id, ext))

		inFile, err := file.Open()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot open uploaded file"})
			return
		}
		defer inFile.Close()

		out, err := os.Create(outPath)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot save file"})
			return
		}
		defer out.Close()
		io.Copy(out, inFile)

		// --- 3. Create DB record
		cert := db.Certificate{
			ID:            id,
			FilePath:      outPath,
			OriginalName:  file.Filename,
			InstitutionID: u.InstitutionID,
			CertificateNo: uuid.New().String(),
			CreatedAt:     time.Now(),
			UpdatedAt:     time.Now(),
		}
		if err := dbConn.Create(&cert).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		// --- 3.5 OCR Extraction skipped to avoid C dependencies
		// Fields will be extracted later or manually

		// --- 4. Compute hash + send to blockchain
		hash := services.ComputeHashFromFile(outPath)
		if err := services.StoreHash(cert.ID, hash); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "blockchain error"})
			return
		}

		// --- 5. Call AI service (optional)
		aiResult, err := services.VerifyWithAI(outPath, &cert)
		if err != nil {
			// AI service not available, set default
			aiResult = &services.AIResponse{Score: 0.5, Details: "AI service unavailable"}
		}

		// Save updated certificate with extracted fields
		if err := dbConn.Save(&cert).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db save error"})
			return
		}

		// --- 6. Save verification result
		vr := db.VerificationResult{
			ID:            uuid.New().String(),
			CertificateID: cert.ID,
			Source:        "ai",
			Passed:        aiResult.Score > 0.8,
			Details:       aiResult.Details,
			CreatedAt:     time.Now(),
		}
		dbConn.Create(&vr)

		// --- 7. Response
		c.JSON(http.StatusAccepted, gin.H{
			"certificate_id": cert.ID,
			"blockchain":     "stored",
			"ai_score":       aiResult.Score,
			"verification":   vr.ID,
			"extracted":      cert.StudentName != "" || cert.RollNumber != "" || cert.Course != "",
		})
	}
}

// POST /api/v1/verify/manual
func ManualVerifyHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req struct {
			CertNumber  string `json:"certNumber"`
			StudentName string `json:"studentName"`
		}
		if err := c.ShouldBindJSON(&req); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid request"})
			return
		}

		var cert db.Certificate
		if err := dbConn.Where("certificate_no = ? AND student_name = ?", req.CertNumber, req.StudentName).First(&cert).Error; err != nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "certificate not found"})
			return
		}

		// Always compute score based on fields for manual verification
		fieldCount := 0
		if cert.StudentName != "" {
			fieldCount++
		}
		if cert.RollNumber != "" {
			fieldCount++
		}
		if cert.Course != "" {
			fieldCount++
		}
		if !cert.IssuedOn.IsZero() {
			fieldCount++
		}
		score := float64(fieldCount) * 0.25
		passed := score > 0.8
		message := "Certificate appears fake."
		if passed {
			message = "Yes, your certificate is valid."
		}
		c.JSON(http.StatusOK, gin.H{
			"passed":  passed,
			"score":   score,
			"details": fmt.Sprintf("Fields matched: %d/4", fieldCount),
			"message": message,
		})
	}
}
