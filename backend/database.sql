CREATE TABLE documents (
    document_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    file_type VARCHAR(10),
    file_path TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng embeddings
CREATE TABLE embeddings (
    embedding_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    embedding_vector JSONB NOT NULL,
    text_segment TEXT,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

-- Bảng search_history
CREATE TABLE search_history (
    history_id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bảng conversations
CREATE TABLE conversations (
    conversation_id SERIAL PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP
);

-- Bảng messages
CREATE TABLE messages (
    message_id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL,
    sender VARCHAR(10) NOT NULL,
    message_content TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id) ON DELETE CASCADE
);

-- Bảng recommendations
CREATE TABLE recommendations (
    recommendation_id SERIAL PRIMARY KEY,
    document_id INT NOT NULL,
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (document_id) REFERENCES documents(document_id) ON DELETE CASCADE
);

-- Bảng uploaded_files
CREATE TABLE uploaded_files (
    file_id SERIAL PRIMARY KEY,
    file_name VARCHAR(100) NOT NULL,
    file_type VARCHAR(10),
    file_path TEXT NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);