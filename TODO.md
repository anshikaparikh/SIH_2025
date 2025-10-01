# TODO: Differentiate Institute and Student Frontend

## Backend Changes
- [x] Add InstitutionID to User model in db.go
- [x] Create auth middleware to verify JWT and set user in context
- [x] Update routes to use auth middleware for protected endpoints
- [x] Modify ListCertificatesHandler to filter by user.InstitutionID
- [x] Modify ListDegreesHandler to filter by user.InstitutionID
- [x] Modify UpdateCertificateHandler to handle multipart form for file update
- [x] Modify UpdateDegreeHandler to handle multipart form for file update
- [x] Update CreateCertificateHandler (upload) to set InstitutionID from user
- [x] Update CreateDegreeHandler to set InstitutionID from user

## Frontend Changes
- [x] Modify InstituteDashboard edit certificate form to include file input
- [x] Modify handleUpdateCertificate to send form data if file selected
- [x] Modify InstituteDashboard edit degree form to include file input
- [x] Modify handleUpdateDegree to send form data if file selected

## Testing
- [ ] Test institute login and dashboard
- [ ] Test adding certificate
- [ ] Test updating certificate with file
- [ ] Test filtering certificates by institution
