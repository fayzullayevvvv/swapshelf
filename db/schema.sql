CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    telegram_id BIGINT NOT NULL UNIQUE,
    rating INTEGER NOT NULL DEFAULT 0,
    phone_number VARCHAR(20),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS genres (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    genre_id INTEGER REFERENCES genres(id) ON DELETE SET NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('New', 'Good', 'Fair', 'Worn')) DEFAULT 'New',
    type VARCHAR(50) NOT NULL CHECK (type IN ('Borrow', 'Permanent', 'Both')) DEFAULT 'Borrow',
    rating INTEGER NOT NULL DEFAULT 0,

    added_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    added_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS swap_requests (
    id SERIAL PRIMARY KEY,
    requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Pending', 'Accepted', 'Rejected')) DEFAULT 'Pending',
    requested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    responded_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS swaps (
    id SERIAL PRIMARY KEY,
    swap_request_id INTEGER UNIQUE REFERENCES swap_requests(id) ON DELETE CASCADE,
    requester_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    responder_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    book_id INTEGER REFERENCES books(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Active', 'Completed', 'Cancelled')) DEFAULT 'Active',
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS reviews (
    id SERIAL PRIMARY KEY,
    reviewer_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    reviewee_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

ALTER TABLE books
ADD COLUMN IF NOT EXISTS available BOOLEAN DEFAULT TRUE;

ALTER TABLE books
ADD COLUMN IF NOT EXISTS channel_message_id BIGINT;