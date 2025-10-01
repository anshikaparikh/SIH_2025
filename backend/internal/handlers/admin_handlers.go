package handlers

import (
	"net/http"

	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func ListVerificationsHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		var list []db.VerificationResult
		if err := dbConn.Limit(100).Order("created_at desc").Find(&list).Error; err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "db error"})
			return
		}
		c.JSON(http.StatusOK, list)
	}
}
