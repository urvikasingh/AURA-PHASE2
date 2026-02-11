--CREATE DATABASE

CREATE DATABASE AURA_PHASE2;

USE AURA_PHASE2;


--CREATE user TABLE

CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    created_at DATETIME DEFAULT GETDATE()
);

--CREATE user_preferences (LONG-TERM MEMORY)

CREATE TABLE user_preferences (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    preference_key VARCHAR(100),
    preference_value VARCHAR(500),
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_user_preferences
        FOREIGN KEY (user_id) REFERENCES users(id)
);

--CREATE user_behavior_profile

CREATE TABLE user_behavior_profile (
    user_id INT PRIMARY KEY,
    behavior_summary VARCHAR(MAX),
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_behavior_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);

--CREATE conversation_context

CREATE TABLE conversation_context (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    context_summary VARCHAR(MAX),
    updated_at DATETIME DEFAULT GETDATE(),
    CONSTRAINT fk_context_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);

--adding column password in table users

ALTER TABLE users
ADD password_hash VARCHAR(255);