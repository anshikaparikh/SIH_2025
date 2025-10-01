package handlers

import (
	"net/http"
	"time"

	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

func AIWebhookHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		var payload map[string]interface{}
		if err := c.BindJSON(&payload); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid json"})
			return
		}

		certID, _ := payload["certificate_id"].(string)

		vr := db.VerificationResult{
			ID:            uuid.New().String(),
			CertificateID: certID,
			Source:        "ai",
			Passed:        false,
			Details:       "received ai payload",
			CreatedAt:     time.Now(),
		}
		dbConn.Create(&vr)

		c.JSON(http.StatusOK, gin.H{"status": "ok"})
	}
}
