# Fake Degree Backend (Go + Gin + Postgres)


This scaffold provides the backend API foundation. Key points:


- Upload certificates (files) and persist metadata in Postgres.
- Webhook endpoint to receive AI/ML verification JSON from your friend.
- Basic institution bulk upload.
- Stubs for OCR and blockchain which you must implement/integrate.
- Use GORM migrations or SQL file to bootstrap schema.


## Next steps (recommended)
1. Implement OCR integration (Tesseract, Google Vision, AWS Textract). Use a background worker (Redis + Sidekiq-like) to process uploads asynchronously.
2. Harden authentication (JWT + roles) and add rate limiting.
3. Implement deterministic hashing and optionally push certificate hashes to a permissioned blockchain or ledger.
4. Build institution integration module: offer CSV/JSON bulk ingest, REST/GraphQL API, or SFTP sync from college ERPs.
5. Provide admin UI and public verification endpoints (read-only) that emit minimal PII.


---