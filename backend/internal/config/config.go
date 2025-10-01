package config

import (
	"fmt"
	"log"
	"os"
)

type Config struct {
	StoragePath     string
	DatabaseURL     string
	Port            string
	BlockchainRPC   string
	PrivateKey      string
	ContractAddress string
	HFToken         string // For future AI
}

func LoadConfig() *Config {
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Construct DATABASE_URL from individual env vars if not set
	databaseURL := os.Getenv("DATABASE_URL")
	if databaseURL == "" {
		host := os.Getenv("DB_HOST")
		user := os.Getenv("DB_USER")
		password := os.Getenv("DB_PASSWORD")
		dbname := os.Getenv("DB_NAME")
		portDB := os.Getenv("DB_PORT")
		if host != "" && user != "" && password != "" && dbname != "" {
			databaseURL = fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable", host, user, password, dbname, portDB)
		} else {
			log.Printf("Warning: Incomplete DB env vars; DATABASE_URL not set")
		}
	}

	return &Config{
		StoragePath:     os.Getenv("STORAGE_PATH"),
		DatabaseURL:     databaseURL,
		Port:            port,
		BlockchainRPC:   os.Getenv("BLOCKCHAIN_RPC"),   // e.g., "https://sepolia.infura.io/v3/YOUR_PROJECT_ID"
		PrivateKey:      os.Getenv("PRIVATE_KEY"),      // Hex private key without 0x
		ContractAddress: os.Getenv("CONTRACT_ADDRESS"), // e.g., "0x..."
		HFToken:         os.Getenv("HF_TOKEN"),         // For Hugging Face
	}
}
