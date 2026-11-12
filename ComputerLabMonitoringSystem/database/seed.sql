INSERT INTO users (username, password_hash, role) VALUES
('admin', 'pbkdf2_sha256$100000$0$placeholder', 'admin'),
('viewer', 'pbkdf2_sha256$100000$0$placeholder', 'viewer');

INSERT INTO computers (computer_name, location, is_online, last_heartbeat) VALUES
('PC-01', 'Lab A', TRUE, CURRENT_TIMESTAMP),
('PC-02', 'Lab A', TRUE, CURRENT_TIMESTAMP),
('PC-03', 'Lab B', FALSE, CURRENT_TIMESTAMP);

INSERT INTO student_sessions (computer_id, username, login_time, logout_time, session_duration_seconds, status) VALUES
(1, 'student01', DATETIME('now', '-2 hours'), DATETIME('now', '-1 hour'), 3600, 'completed'),
(2, 'student02', DATETIME('now', '-3 hours'), DATETIME('now', '-2 hours'), 3600, 'completed');

INSERT INTO application_activities (computer_id, session_id, app_name, start_time, end_time, duration_seconds) VALUES
(1, 1, 'Google Chrome', DATETIME('now', '-2 hours'), DATETIME('now', '-1 hours'), 3600),
(2, 2, 'Visual Studio Code', DATETIME('now', '-3 hours'), DATETIME('now', '-2 hours'), 3600);

INSERT INTO website_activities (computer_id, session_id, domain, accessed_at) VALUES
(1, 1, 'youtube.com', DATETIME('now', '-90 minutes')),
(1, 1, 'github.com', DATETIME('now', '-60 minutes')),
(2, 2, 'google.com', DATETIME('now', '-120 minutes'));
