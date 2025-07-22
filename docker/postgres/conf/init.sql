CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE request_response_log (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER,
    ip VARCHAR(30) NOT NULL,
    port INTEGER NOT NULL,
    agent VARCHAR NOT NULL,
    method VARCHAR(30) NOT NULL,
    path VARCHAR(30) NOT NULL,
    response_status SMALLINT NOT NULL,
    request_id UUID NOT NULL DEFAULT gen_random_uuid(),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);