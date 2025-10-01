package main

import (
	"fmt"
	"log"
	"os"

	"github.com/amanswami/fake-degree-backend/internal/config"
	"github.com/amanswami/fake-degree-backend/internal/db"
	"github.com/amanswami/fake-degree-backend/internal/routes"
	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/joho/godotenv"
)

func main() {
	// Load .env file
	if err := godotenv.Load(".env"); err != nil {
		log.Println("No .env file found")
	}

	// Load config
	cfg := config.LoadConfig()
	if cfg == nil {
		log.Fatal("failed to load config")
	}
	fmt.Println("DatabaseURL:", cfg.DatabaseURL)
	// Connect to DB
	dbConn, err := db.Connect(cfg)
	if err != nil {
		log.Fatalf("db connect: %v", err)
	}
	defer dbConn.DB()

	// Create gin engine
	r := gin.Default()

	// Add CORS middleware
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:3000", "http://localhost:3001", "http://localhost:3002"},
		AllowMethods:     []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type", "Authorization"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))

	// Setup routes
	routes.Setup(r, dbConn, cfg)

	// Get port
	port := os.Getenv("PORT")
	if port == "" {
		port = cfg.Port
	}

	// Run server
	if err := r.Run("0.0.0.0:" + port); err != nil {
		log.Fatalf("server error: %v", err)
	}
}
