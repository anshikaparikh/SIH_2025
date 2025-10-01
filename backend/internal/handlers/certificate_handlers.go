package handlers

import (
	"encoding/json"
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

func GetCertificateHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		var cert db.Certificate
		if err := dbConn.First(&cert, "id = ?", id).Error; err != nil {
			if err == gorm.ErrRecordNotFound {
				c.JSON(http.StatusNotFound, gin.H{"error": "not found"})
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}
		c.JSON(http.StatusOK, cert)
	}
}

// ✅ Trigger AI-based verification
func TriggerVerifyHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")

		// Check if certificate exists
		var cert db.Certificate
		if err := dbConn.First(&cert, "id = ?", id).Error; err != nil {
			if err == gorm.ErrRecordNotFound {
				c.JSON(http.StatusNotFound, gin.H{"error": "certificate not found"})
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		// Use saved file path
		filePath := cert.FilePath

		// Call AI Service
		result, err := services.VerifyWithAI(filePath, &cert)
		if err != nil {
			vr := db.VerificationResult{
				ID:            uuid.New().String(),
				CertificateID: id,
				Source:        "ai",
				Passed:        false,
				Details:       "AI service error: " + err.Error(),
				CreatedAt:     time.Now(),
			}
			dbConn.Create(&vr)

			c.JSON(http.StatusInternalServerError, gin.H{"error": "AI service failed"})
			return
		}

		// Convert AIResponse struct to JSON string for storage
		resultBytes, _ := json.Marshal(result)

		vr := db.VerificationResult{
			ID:            uuid.New().String(),
			CertificateID: id,
			Source:        "ai",
			Passed:        result.Score > 0.8, // example threshold
			Details:       string(resultBytes),
			CreatedAt:     time.Now(),
		}
		if err := dbConn.Create(&vr).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"status":          "completed",
			"verification_id": vr.ID,
			"ai_score":        result.Score,
			"ai_details":      result.Details,
		})
	}
}

// ListCertificatesHandler lists certificates for the user's institution
func ListCertificatesHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		user, exists := c.Get("user")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "user not found in context"})
			return
		}
		u := user.(db.User)

		var certificates []db.Certificate
		if err := dbConn.Where("institution_id = ?", u.InstitutionID).Find(&certificates).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}
		c.JSON(http.StatusOK, certificates)
	}
}

// UpdateCertificateHandler updates a certificate
func UpdateCertificateHandler(dbConn *gorm.DB, cfg *config.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")

		var cert db.Certificate
		if err := dbConn.First(&cert, "id = ?", id).Error; err != nil {
			if err == gorm.ErrRecordNotFound {
				c.JSON(http.StatusNotFound, gin.H{"error": "certificate not found"})
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		// Check if multipart form
		if c.ContentType() == "multipart/form-data" {
			// Handle multipart form
			form, err := c.MultipartForm()
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": "invalid form data"})
				return
			}

			// Update fields from form
			if values := form.Value["student_name"]; len(values) > 0 && values[0] != "" {
				cert.StudentName = values[0]
			}
			if values := form.Value["roll_number"]; len(values) > 0 && values[0] != "" {
				cert.RollNumber = values[0]
			}
			if values := form.Value["course"]; len(values) > 0 && values[0] != "" {
				cert.Course = values[0]
			}
			if values := form.Value["issued_on"]; len(values) > 0 && values[0] != "" {
				if parsedTime, err := time.Parse("2006-01-02", values[0]); err == nil {
					cert.IssuedOn = parsedTime
				}
			}

			// Handle file upload
			if files := form.File["file"]; len(files) > 0 {
				file := files[0]
				// Save new file
				newID := uuid.New().String()
				os.MkdirAll(cfg.StoragePath, 0700)
				ext := filepath.Ext(file.Filename)
				newOutPath := filepath.Join(cfg.StoragePath, fmt.Sprintf("%s%s", newID, ext))

				inFile, err := file.Open()
				if err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot open uploaded file"})
					return
				}
				defer inFile.Close()

				out, err := os.Create(newOutPath)
				if err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot save file"})
					return
				}
				defer out.Close()
				io.Copy(out, inFile)

				// Delete old file if exists
				if cert.FilePath != "" {
					os.Remove(cert.FilePath)
				}

				cert.FilePath = newOutPath
				cert.OriginalName = file.Filename
			}
		} else {
			// Handle JSON
			var updateData struct {
				StudentName string `json:"student_name"`
				RollNumber  string `json:"roll_number"`
				Course      string `json:"course"`
				IssuedOn    string `json:"issued_on"`
			}
			if err := c.ShouldBindJSON(&updateData); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}

			if updateData.StudentName != "" {
				cert.StudentName = updateData.StudentName
			}
			if updateData.RollNumber != "" {
				cert.RollNumber = updateData.RollNumber
			}
			if updateData.Course != "" {
				cert.Course = updateData.Course
			}
			if updateData.IssuedOn != "" {
				if parsedTime, err := time.Parse("2006-01-02", updateData.IssuedOn); err == nil {
					cert.IssuedOn = parsedTime
				}
			}
		}

		cert.UpdatedAt = time.Now()
		if err := dbConn.Save(&cert).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		c.JSON(http.StatusOK, cert)
	}
}

// CreateDegreeHandler creates a new degree
func CreateDegreeHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		user, exists := c.Get("user")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "user not found in context"})
			return
		}
		u := user.(db.User)

		var degreeData struct {
			StudentName string `json:"student_name" binding:"required"`
			DegreeType  string `json:"degree_type" binding:"required"`
			IssuedOn    string `json:"issued_on" binding:"required"`
			File        string `json:"file"` // optional file path
		}
		if err := c.ShouldBindJSON(&degreeData); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		issuedOn, err := time.Parse("2006-01-02", degreeData.IssuedOn)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid date format"})
			return
		}

		degree := db.Degree{
			StudentName:   degreeData.StudentName,
			DegreeType:    degreeData.DegreeType,
			InstitutionID: u.InstitutionID,
			IssuedOn:      issuedOn,
			DegreeNo:      uuid.New().String(),
			CreatedAt:     time.Now(),
			UpdatedAt:     time.Now(),
		}

		if degreeData.File != "" {
			degree.FilePath = degreeData.File
		}

		if err := dbConn.Create(&degree).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		c.JSON(http.StatusCreated, degree)
	}
}

// ListDegreesHandler lists degrees for the user's institution
func ListDegreesHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		user, exists := c.Get("user")
		if !exists {
			c.JSON(http.StatusUnauthorized, gin.H{"error": "user not found in context"})
			return
		}
		u := user.(db.User)

		var degrees []db.Degree
		if err := dbConn.Where("institution_id = ?", u.InstitutionID).Find(&degrees).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}
		c.JSON(http.StatusOK, degrees)
	}
}

// UpdateDegreeHandler updates a degree
func UpdateDegreeHandler(dbConn *gorm.DB, cfg *config.Config) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")

		var degree db.Degree
		if err := dbConn.First(&degree, "id = ?", id).Error; err != nil {
			if err == gorm.ErrRecordNotFound {
				c.JSON(http.StatusNotFound, gin.H{"error": "degree not found"})
				return
			}
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		// Check if multipart form
		if c.ContentType() == "multipart/form-data" {
			// Handle multipart form
			form, err := c.MultipartForm()
			if err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": "invalid form data"})
				return
			}

			// Update fields from form
			if values := form.Value["student_name"]; len(values) > 0 && values[0] != "" {
				degree.StudentName = values[0]
			}
			if values := form.Value["degree_type"]; len(values) > 0 && values[0] != "" {
				degree.DegreeType = values[0]
			}
			if values := form.Value["issued_on"]; len(values) > 0 && values[0] != "" {
				if parsedTime, err := time.Parse("2006-01-02", values[0]); err == nil {
					degree.IssuedOn = parsedTime
				}
			}

			// Handle file upload
			if files := form.File["file"]; len(files) > 0 {
				file := files[0]
				// Save new file
				newID := uuid.New().String()
				os.MkdirAll(cfg.StoragePath, 0700)
				ext := filepath.Ext(file.Filename)
				newOutPath := filepath.Join(cfg.StoragePath, fmt.Sprintf("%s%s", newID, ext))

				inFile, err := file.Open()
				if err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot open uploaded file"})
					return
				}
				defer inFile.Close()

				out, err := os.Create(newOutPath)
				if err != nil {
					c.JSON(http.StatusInternalServerError, gin.H{"error": "cannot save file"})
					return
				}
				defer out.Close()
				io.Copy(out, inFile)

				// Delete old file if exists
				if degree.FilePath != "" {
					os.Remove(degree.FilePath)
				}

				degree.FilePath = newOutPath
				degree.OriginalName = file.Filename
			}
		} else {
			// Handle JSON
			var updateData struct {
				StudentName string `json:"student_name"`
				DegreeType  string `json:"degree_type"`
				IssuedOn    string `json:"issued_on"`
			}
			if err := c.ShouldBindJSON(&updateData); err != nil {
				c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
				return
			}

			if updateData.StudentName != "" {
				degree.StudentName = updateData.StudentName
			}
			if updateData.DegreeType != "" {
				degree.DegreeType = updateData.DegreeType
			}
			if updateData.IssuedOn != "" {
				if parsedTime, err := time.Parse("2006-01-02", updateData.IssuedOn); err == nil {
					degree.IssuedOn = parsedTime
				}
			}
		}

		degree.UpdatedAt = time.Now()
		if err := dbConn.Save(&degree).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}

		c.JSON(http.StatusOK, degree)
	}
}
