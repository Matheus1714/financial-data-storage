CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS customers(
    customer_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    first_name VARCHAR(128) NOT NULL,
    last_name VARCHAR(128) NOT NULL,
    email VARCHAR(256) UNIQUE NOT NULL,
    phone VARCHAR(20),
    address VARCHAR(216),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS  accounts (
    account_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    customer_id UUID REFERENCES customers(customer_id),

    account_number VARCHAR(32) UNIQUE NOT NULL,
    balance DECIMAL(15, 2) DEFAULT 0.00,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS  transactions (
    transaction_id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,

    account_id UUID REFERENCES accounts(account_id),

    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    description VARCHAR(64) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
);