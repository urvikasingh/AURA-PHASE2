/* =====================================================
   DROP DATABASE (SAFE RECREATE)
   ===================================================== */
USE master;
GO

IF EXISTS (SELECT 1 FROM sys.databases WHERE name = 'AURA_PHASE2')
BEGIN
    ALTER DATABASE AURA_PHASE2
    SET SINGLE_USER
    WITH ROLLBACK IMMEDIATE;
    DROP DATABASE AURA_PHASE2;
END
GO

/* =====================================================
   CREATE DATABASE
   ===================================================== */
CREATE DATABASE AURA_PHASE2;
GO

USE AURA_PHASE2;
GO

/* =====================================================
   USERS
   ===================================================== */
CREATE TABLE users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255),


    created_at DATETIME DEFAULT GETDATE()
);
GO


/* =====================================================
   USER PREFERENCES (LONG-TERM MEMORY)
   ===================================================== */
-- user_preferences
-- Used for USP long-term human memory:
-- e.g. display_name, tone, relationship preferences

CREATE TABLE user_preferences (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    preference_key VARCHAR(100),
    preference_value VARCHAR(500),
    updated_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_user_preferences
        FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

CREATE INDEX idx_user_preferences_user
ON user_preferences (user_id);
GO

/* =====================================================
   USER BEHAVIOR PROFILE (FUTURE USE)
   ===================================================== */
CREATE TABLE user_behavior_profile (
    user_id INT PRIMARY KEY,
    behavior_summary VARCHAR(MAX),
    updated_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_behavior_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

/* =====================================================
   CONVERSATION CONTEXT (SUMMARY MEMORY)
   ===================================================== */
CREATE TABLE conversation_context (
    user_id INT PRIMARY KEY,
    context_summary VARCHAR(MAX),
    updated_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_context_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

/* =====================================================
   ACADEMIC DOMAIN MEMORY
   ===================================================== */
CREATE TABLE academic_memory (
    id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,

    explanation_style VARCHAR(50) NOT NULL DEFAULT 'step_by_step',
    difficulty_level VARCHAR(50) NOT NULL DEFAULT 'beginner',

    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_academic_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

/* =====================================================
   CONVERSATIONS (CHAT SESSIONS)
   ===================================================== */
CREATE TABLE conversations (
    id INT IDENTITY PRIMARY KEY,
    user_id INT NOT NULL,
    domain VARCHAR(50) NOT NULL,
    has_greeted BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

GO

CREATE INDEX idx_conversations_user_updated
ON conversations (user_id, updated_at DESC);
GO

/* =====================================================
   CHAT MESSAGES (CHAT HISTORY)
   ===================================================== */
CREATE TABLE chat_messages (
    id INT IDENTITY(1,1) PRIMARY KEY,

    conversation_id INT NOT NULL,
    user_id INT NOT NULL,

    role VARCHAR(20) NOT NULL,        -- 'user' | 'assistant'
    content VARCHAR(MAX) NOT NULL,

    created_at DATETIME DEFAULT GETDATE(),

    CONSTRAINT fk_message_conversation
        FOREIGN KEY (conversation_id) REFERENCES conversations(id),

    CONSTRAINT fk_message_user
        FOREIGN KEY (user_id) REFERENCES users(id)
);
GO

CREATE INDEX idx_chat_messages_conversation
ON chat_messages (conversation_id, created_at);
GO

/* =====================================================
   EXPERIMENT LOGS (RESEARCH INSTRUMENTATION)
   -----------------------------------------------------
   This table is used ONLY for empirical evaluation
   and does NOT affect application behavior.
   ===================================================== */

IF NOT EXISTS (
    SELECT 1
    FROM sys.tables
    WHERE name = 'experiment_logs'
)
BEGIN
    CREATE TABLE experiment_logs (
        id INT IDENTITY(1,1) PRIMARY KEY,

        user_id INT NOT NULL,
        conversation_id INT NOT NULL,

        domain VARCHAR(50) NOT NULL,

        memory_triggered BIT DEFAULT 0,

        latency_ms FLOAT NOT NULL,

        input_length INT,
        output_length INT,

        created_at DATETIME DEFAULT GETDATE(),

        CONSTRAINT fk_experiment_user
            FOREIGN KEY (user_id)
            REFERENCES users(id),

        CONSTRAINT fk_experiment_conversation
            FOREIGN KEY (conversation_id)
            REFERENCES conversations(id)
    );

    CREATE INDEX idx_experiment_domain
        ON experiment_logs (domain);
END;
GO
