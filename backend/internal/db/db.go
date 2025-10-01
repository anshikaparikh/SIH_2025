package db

import (
	"fmt"
	"time"

	"github.com/amanswami/fake-degree-backend/internal/config"
	"github.com/google/uuid"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

// Connect establishes a connection to Postgres using GORM
func Connect(cfg *config.Config) (*gorm.DB, error) {
	// Example: cfg.DatabaseURL = "host=localhost user=postgres password=1234 dbname=fakedegrees port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(cfg.DatabaseURL), &gorm.Config{
		Logger: logger.Default.LogMode(logger.Info), // show SQL queries
	})
	if err != nil {
		return nil, fmt.Errorf("failed to connect to db: %w", err)
	}

	// Run migrations automatically
	if err := migrate(db); err != nil {
		return nil, fmt.Errorf("failed to run migrations: %w", err)
	}

	// Test ping
	sqlDB, _ := db.DB()
	if err := sqlDB.Ping(); err != nil {
		return nil, fmt.Errorf("db ping: %w", err)
	}

	return db, nil
}

// migrate auto-creates tables if they don’t exist
func migrate(db *gorm.DB) error {
	return db.AutoMigrate(
		&Certificate{},
		&Degree{},
		&Institution{},
		&User{},
		&VerificationResult{},
	)
}

// ----------------------- MODELS -----------------------

type Certificate struct {
	ID            string    `gorm:"primaryKey;type:uuid" json:"id"`
	FilePath      string    `json:"file_path"`
	OriginalName  string    `json:"original_name"`
	StudentName   string    `json:"student_name" gorm:"index"`
	RollNumber    string    `json:"roll_number" gorm:"index"`
	InstitutionID string    `json:"institution_id" gorm:"index"`
	Course        string    `json:"course"`
	IssuedOn      time.Time `json:"issued_on"`
	CertificateNo string    `json:"certificate_no" gorm:"uniqueIndex"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

func (c *Certificate) BeforeCreate(tx *gorm.DB) (err error) {
	if c.ID == "" {
		c.ID = uuid.New().String()
	}
	return
}

type Degree struct {
	ID            string    `gorm:"primaryKey;type:uuid" json:"id"`
	FilePath      string    `json:"file_path"`
	OriginalName  string    `json:"original_name"`
	StudentName   string    `json:"student_name" gorm:"index"`
	DegreeType    string    `json:"degree_type"`
	InstitutionID string    `json:"institution_id" gorm:"index"`
	IssuedOn      time.Time `json:"issued_on"`
	DegreeNo      string    `json:"degree_no" gorm:"uniqueIndex"`
	CreatedAt     time.Time
	UpdatedAt     time.Time
}

func (d *Degree) BeforeCreate(tx *gorm.DB) (err error) {
	if d.ID == "" {
		d.ID = uuid.New().String()
	}
	return
}

type Institution struct {
	ID        string `gorm:"primaryKey;type:uuid" json:"id"`
	Name      string `json:"name" gorm:"uniqueIndex"`
	Code      string `json:"code" gorm:"uniqueIndex"`
	Address   string `json:"address"`
	Contact   string `json:"contact"`
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (i *Institution) BeforeCreate(tx *gorm.DB) (err error) {
	if i.ID == "" {
		i.ID = uuid.New().String()
	}
	return
}

type User struct {
	ID            string `gorm:"primaryKey;type:uuid" json:"id"`
	Email         string `json:"email" gorm:"uniqueIndex"`
	Password      string `json:"-"`    // store hashed password
	Role          string `json:"role"` // institute, hr, admin, student
	InstitutionID string `json:"institution_id" gorm:"index"`
	CreatedAt     time.Time
}

func (u *User) BeforeCreate(tx *gorm.DB) (err error) {
	if u.ID == "" {
		u.ID = uuid.New().String()
	}
	return
}

type VerificationResult struct {
	ID            string `gorm:"primaryKey;type:uuid" json:"id"`
	CertificateID string `json:"certificate_id" gorm:"index"`
	Source        string `json:"source"` // ai, ocr, manual
	Passed        bool   `json:"passed"`
	Details       string `json:"details" gorm:"type:text"`
	CreatedAt     time.Time
}

func (vr *VerificationResult) BeforeCreate(tx *gorm.DB) (err error) {
	if vr.ID == "" {
		vr.ID = uuid.New().String()
	}
	return
}
