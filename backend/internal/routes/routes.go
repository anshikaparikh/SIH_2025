package routes

import (
	"github.com/amanswami/fake-degree-backend/internal/config"
	"github.com/amanswami/fake-degree-backend/internal/handlers"
	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func Setup(r *gin.Engine, db *gorm.DB, cfg *config.Config) {
	api := r.Group("/api/v1")
	{
		cert := api.Group("/certificates")
		{
			cert.POST("/upload", handlers.AuthMiddleware(db), handlers.UploadCertificateHandler(db, cfg))
			cert.GET("", handlers.AuthMiddleware(db), handlers.ListCertificatesHandler(db))
			cert.GET("/:id", handlers.AuthMiddleware(db), handlers.GetCertificateHandler(db))
			cert.PUT("/:id", handlers.AuthMiddleware(db), handlers.UpdateCertificateHandler(db, cfg))
			cert.POST("/:id/verify", handlers.AuthMiddleware(db), handlers.TriggerVerifyHandler(db))
		}

		degree := api.Group("/degrees")
		{
			degree.POST("", handlers.AuthMiddleware(db), handlers.CreateDegreeHandler(db))
			degree.GET("", handlers.AuthMiddleware(db), handlers.ListDegreesHandler(db))
			degree.PUT("/:id", handlers.AuthMiddleware(db), handlers.UpdateDegreeHandler(db, cfg))
		}

		instit := api.Group("/institutions")
		{
			instit.POST("/bulk", handlers.BulkInstitutionUploadHandler(db))
		}

		api.POST("/webhooks/ai", handlers.AIWebhookHandler(db))

		admin := api.Group("/admin")
		{
			admin.GET("/verifications", handlers.AuthMiddleware(db), handlers.ListVerificationsHandler(db))
		}

		auth := api.Group("/auth")
		{
			auth.POST("/register", handlers.RegisterHandler(db))
			auth.POST("/login", handlers.LoginHandler(db))
		}

		verify := api.Group("/verify")
		{
			verify.POST("/manual", handlers.ManualVerifyHandler(db))
		}
	}
}
