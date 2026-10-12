-- AI-Health360 — Phase 1 database schema
-- Run: mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS ai_health360
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE ai_health360;

-- ============================================================
-- USERS  (patient / doctor / admin)
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(120) NOT NULL,
    email         VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role          ENUM('patient', 'doctor', 'admin') NOT NULL DEFAULT 'patient',
    age           INT,
    gender        ENUM('Male', 'Female', 'Other'),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ============================================================
-- PREDICTIONS  (one row per disease-prediction run)
-- ============================================================
CREATE TABLE IF NOT EXISTS predictions (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    user_id       INT NOT NULL,
    disease_type  VARCHAR(50) NOT NULL,        -- diabetes / heart / liver / kidney
    input_data    JSON NOT NULL,               -- raw form values submitted
    risk_level    VARCHAR(20),                 -- Low / Moderate / High
    confidence    FLOAT,                       -- model confidence %
    model_used    VARCHAR(50),                 -- e.g. RandomForest, XGBoost
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- HEALTH RECORDS  (time-series metrics -> trend charts + risk score)
-- ============================================================
CREATE TABLE IF NOT EXISTS health_records (
    id                        INT AUTO_INCREMENT PRIMARY KEY,
    user_id                   INT NOT NULL,
    bmi                       FLOAT,
    blood_pressure_systolic   INT,
    blood_pressure_diastolic  INT,
    glucose                   FLOAT,
    cholesterol               FLOAT,
    weight                    FLOAT,
    health_risk_score         INT,             -- 0-100
    recorded_at               TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- ============================================================
-- REPORTS  (generated PDF report log, for Phase 10)
-- ============================================================
CREATE TABLE IF NOT EXISTS reports (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    file_path    VARCHAR(255) NOT NULL,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Helpful indexes for common lookups
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_health_records_user ON health_records(user_id);
CREATE INDEX idx_reports_user ON reports(user_id);
