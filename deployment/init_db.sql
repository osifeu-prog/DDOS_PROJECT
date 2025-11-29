-- קובץ init_db.sql
-- פקודות SQL ליצירת מסד נתונים PostgreSQL

-- טבלת משתמשים רשומים (כולל PII - מספר טלפון)
CREATE TABLE registered_users (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    registration_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- טבלת פניות לאדמין (דרך טופס יצירת קשר)
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    sender_name VARCHAR(255),
    sender_email VARCHAR(255),
    content TEXT NOT NULL,
    access_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET -- נשמר לצורך אימות וזיהוי שולח
);

-- טבלת לוגים מפורטת (נדרש לחוק 13)
CREATE TABLE access_logs (
    id SERIAL PRIMARY KEY,
    ip_address INET NOT NULL, -- שומר כתובת IP
    access_time TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT, -- לוג מפורט (סוג מכשיר/דפדפן)
    page_viewed VARCHAR(255),
    session_data JSONB -- נתונים נוספים על המשתמש
);

-- יצירת אינדקסים לשיפור ביצועים
CREATE INDEX idx_access_time ON access_logs (access_time);
CREATE INDEX idx_phone_number ON registered_users (phone_number);
