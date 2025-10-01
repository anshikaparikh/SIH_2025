-- Insert sample data into institutions table
INSERT INTO institutions (id, name, code, address, contact, created_at, updated_at) VALUES
(uuid_generate_v4(), 'Indian Institute of Technology Delhi', 'IITD', 'Hauz Khas, New Delhi, India', 'contact@iitd.ac.in', NOW(), NOW()),
(uuid_generate_v4(), 'Jawaharlal Nehru University', 'JNU', 'New Mehrauli Road, New Delhi, India', 'info@jnu.ac.in', NOW(), NOW()),
(uuid_generate_v4(), 'University of Delhi', 'DU', 'Delhi, India', 'admissions@du.ac.in', NOW(), NOW()),
(uuid_generate_v4(), 'Banaras Hindu University', 'BHU', 'Varanasi, Uttar Pradesh, India', 'registrar@bhu.ac.in', NOW(), NOW()),
(uuid_generate_v4(), 'Anna University', 'AU', 'Chennai, Tamil Nadu, India', 'info@annauniv.edu', NOW(), NOW());

-- Insert sample data into certificates table
INSERT INTO certificates (id, file_path, original_name, student_name, roll_number, institution_id, course, issued_on, certificate_no, created_at, updated_at) VALUES
(uuid_generate_v4(), '/storage/sample1.pdf', 'degree1.pdf', 'Rahul Sharma', 'CS2021001', (SELECT id FROM institutions WHERE code = 'IITD' LIMIT 1), 'Computer Science', '2023-06-15', 'CERT001', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample2.pdf', 'degree2.pdf', 'Priya Singh', 'EE2021002', (SELECT id FROM institutions WHERE code = 'IITD' LIMIT 1), 'Electrical Engineering', '2023-06-15', 'CERT002', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample3.pdf', 'degree3.pdf', 'Amit Kumar', 'ME2021003', (SELECT id FROM institutions WHERE code = 'JNU' LIMIT 1), 'Mechanical Engineering', '2023-06-20', 'CERT003', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample4.pdf', 'degree4.pdf', 'Sneha Patel', 'BT2021004', (SELECT id FROM institutions WHERE code = 'DU' LIMIT 1), 'Biotechnology', '2023-06-25', 'CERT004', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample5.pdf', 'degree5.pdf', 'Vikram Rao', 'CE2021005', (SELECT id FROM institutions WHERE code = 'BHU' LIMIT 1), 'Civil Engineering', '2023-06-30', 'CERT005', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample6.pdf', 'degree6.pdf', 'Kavita Jain', 'IT2021006', (SELECT id FROM institutions WHERE code = 'AU' LIMIT 1), 'Information Technology', '2023-07-05', 'CERT006', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample7.pdf', 'degree7.pdf', 'Rohit Verma', 'CS2021007', (SELECT id FROM institutions WHERE code = 'IITD' LIMIT 1), 'Computer Science', '2023-07-10', 'CERT007', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample8.pdf', 'degree8.pdf', 'Anjali Gupta', 'PH2021008', (SELECT id FROM institutions WHERE code = 'JNU' LIMIT 1), 'Physics', '2023-07-15', 'CERT008', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample9.pdf', 'degree9.pdf', 'Suresh Reddy', 'CH2021009', (SELECT id FROM institutions WHERE code = 'DU' LIMIT 1), 'Chemistry', '2023-07-20', 'CERT009', NOW(), NOW()),
(uuid_generate_v4(), '/storage/sample10.pdf', 'degree10.pdf', 'Meera Iyer', 'MA2021010', (SELECT id FROM institutions WHERE code = 'BHU' LIMIT 1), 'Mathematics', '2023-07-25', 'CERT010', NOW(), NOW());

-- Insert sample data into verification_results table
INSERT INTO verification_results (id, certificate_id, source, passed, details, created_at) VALUES
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT001' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT001' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT002' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT002' LIMIT 1), 'AI_ML', false, 'Potential forgery detected in signature', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT003' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT003' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT004' LIMIT 1), 'OCR', false, 'OCR failed: text extraction issues', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT004' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT005' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT005' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT006' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT006' LIMIT 1), 'AI_ML', false, 'Anomaly detected in text formatting', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT007' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT007' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT008' LIMIT 1), 'OCR', false, 'OCR failed: poor image quality', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT008' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT009' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT009' LIMIT 1), 'AI_ML', true, 'AI/ML anomaly detection passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT010' LIMIT 1), 'OCR', true, 'OCR verification passed', NOW()),
(uuid_generate_v4(), (SELECT id FROM certificates WHERE certificate_no = 'CERT010' LIMIT 1), 'AI_ML', false, 'Potential tampering detected', NOW());
