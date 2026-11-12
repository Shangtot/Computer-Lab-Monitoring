CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS computers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computer_name VARCHAR(80) NOT NULL UNIQUE,
    location VARCHAR(120),
    is_online BOOLEAN DEFAULT TRUE,
    last_heartbeat DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS student_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computer_id INTEGER,
    username VARCHAR(80) NOT NULL,
    login_time DATETIME NOT NULL,
    logout_time DATETIME,
    session_duration_seconds INTEGER,
    status VARCHAR(20) DEFAULT 'active',
    FOREIGN KEY (computer_id) REFERENCES computers(id)
);

CREATE TABLE IF NOT EXISTS application_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computer_id INTEGER,
    session_id INTEGER,
    app_name VARCHAR(120) NOT NULL,
    start_time DATETIME NOT NULL,
    end_time DATETIME,
    duration_seconds INTEGER,
    FOREIGN KEY (computer_id) REFERENCES computers(id),
    FOREIGN KEY (session_id) REFERENCES student_sessions(id)
);

CREATE TABLE IF NOT EXISTS website_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computer_id INTEGER,
    session_id INTEGER,
    domain VARCHAR(150) NOT NULL,
    accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (computer_id) REFERENCES computers(id),
    FOREIGN KEY (session_id) REFERENCES student_sessions(id)
);

CREATE TABLE IF NOT EXISTS heartbeats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    computer_id INTEGER,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'online',
    FOREIGN KEY (computer_id) REFERENCES computers(id)
);

CREATE TABLE IF NOT EXISTS event_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type VARCHAR(50) NOT NULL,
    computer_id INTEGER,
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (computer_id) REFERENCES computers(id)
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_sessions_username ON student_sessions(username);
CREATE INDEX IF NOT EXISTS idx_sessions_computer ON student_sessions(computer_id);
CREATE INDEX IF NOT EXISTS idx_activities_computer ON application_activities(computer_id);
CREATE INDEX IF NOT EXISTS idx_websites_domain ON website_activities(domain);
