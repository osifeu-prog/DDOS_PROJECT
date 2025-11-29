-- יצירת טבלת משתמשים (Users)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- יצירת טבלת נתונים שהועלו על ידי משתמשים (UploadedData)
-- כלי מרכזי לפאנל האדמין: לראות את הנתונים שמשתמשים מעלים
CREATE TABLE uploaded_data (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    data_type VARCHAR(50) NOT NULL,
    data_content TEXT, -- יכיל את הנתונים שהועלו (לדוגמה, דירוגים, משוב)
    status VARCHAR(20) DEFAULT 'Pending',
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- יצירת טבלת חיבור לבוט טלגרם (TelegramConnections)
-- מקשרת בין משתמש מערכת ל-Chat ID בטלגרם
CREATE TABLE telegram_connections (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE UNIQUE,
    chat_id BIGINT UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    connected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
