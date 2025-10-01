CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS institutions (
id uuid PRIMARY KEY,
name text UNIQUE,
code text UNIQUE,
address text,
contact text,
created_at timestamptz,
updated_at timestamptz
);


CREATE TABLE IF NOT EXISTS certificates (
id uuid PRIMARY KEY,
file_path text,
original_name text,
student_name text,
roll_number text,
institution_id uuid,
course text,
issued_on timestamptz,
certificate_no text,
created_at timestamptz,
updated_at timestamptz
);


CREATE TABLE IF NOT EXISTS verification_results (
id uuid PRIMARY KEY,
certificate_id uuid,
source text,
passed boolean,
details text,
created_at timestamptz
);