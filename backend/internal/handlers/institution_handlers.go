package handlers

import (
	"encoding/csv"
	"net/http"
	"time"

	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
	"gorm.io/gorm"
)

func BulkInstitutionUploadHandler(dbConn *gorm.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		file, err := c.FormFile("file")
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "file required"})
			return
		}
		f, _ := file.Open()
		defer f.Close()

		reader := csv.NewReader(f)
		rows, err := reader.ReadAll()
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "invalid csv"})
			return
		}

		for _, r := range rows {
			if len(r) < 2 {
				continue
			}
			inst := db.Institution{
				ID:        uuid.New().String(),
				Name:      r[0],
				Code:      r[1],
				CreatedAt: time.Now(),
			}
			dbConn.Create(&inst)
		}
		c.JSON(http.StatusOK, gin.H{"status": "done"})
	}
}
