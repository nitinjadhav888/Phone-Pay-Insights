CREATE DATABASE phonepe;

USE phonepe;

-- Insurance -- 

CREATE TABLE aggregated_insurance_country (
    id SERIAL PRIMARY KEY,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    counts BIGINT,
    amount BIGINT
);

CREATE TABLE aggregated_insurance_state (
    id SERIAL PRIMARY KEY,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    counts BIGINT,
    amount BIGINT,
    state VARCHAR(100)
);

CREATE TABLE map_insurance_hover_country (
    id SERIAL PRIMARY KEY,
    years INT NOT NULL,
    state VARCHAR(100),
    counts BIGINT,
    amount BIGINT
);

CREATE TABLE map_insurance_hover_state (
    id SERIAL PRIMARY KEY,
    years INT NOT NULL,
    state VARCHAR(100),
    district VARCHAR(150),
    counts BIGINT,
    amount BIGINT
);

CREATE TABLE map_insurance_total_country (
    id SERIAL PRIMARY KEY,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    metric BIGINT,
    label VARCHAR(100),
    years INT
);

CREATE TABLE map_insurance_total_state (
    id SERIAL PRIMARY KEY,
    lat DOUBLE PRECISION,
    lng DOUBLE PRECISION,
    metric BIGINT,
    label VARCHAR(150),
    years INT,
    state VARCHAR(100)
);

CREATE TABLE top_insurance_country (
    id SERIAL PRIMARY KEY,
    years INT,
    levels VARCHAR(50),
    entity_name VARCHAR(150),
    counts BIGINT,
    amount BIGINT
);

CREATE TABLE top_insurance_state (
    id SERIAL PRIMARY KEY,
    years INT,
    state VARCHAR(150),
    levels VARCHAR(50),
    entity_name VARCHAR(150),
    counts BIGINT,
    amount BIGINT
);

-- Transaction -- 

CREATE TABLE aggregated_transaction_country (
    id SERIAL PRIMARY KEY,
    from_date DATE,
    to_date DATE,
    transaction_name TEXT,
    counts BIGINT,
    amount NUMERIC
);

CREATE TABLE aggregated_transaction_state (
    id SERIAL PRIMARY KEY,
    from_date DATE,
    to_date DATE,
    transaction_name TEXT,
    counts BIGINT,
    amount NUMERIC,
    state TEXT
);

CREATE TABLE map_transaction_country (
    id SERIAL PRIMARY KEY,
    years INT,
    state TEXT,
    counts BIGINT,
    amount NUMERIC
);

CREATE TABLE map_transaction_state (
    id SERIAL PRIMARY KEY,
    years INT,
    district TEXT,
    counts BIGINT,
    amount NUMERIC,
    state TEXT
);

CREATE TABLE top_transaction_country (
    id SERIAL PRIMARY KEY,
    years INT,
    entity TEXT,
    counts BIGINT,
    amount NUMERIC,
    levels TEXT
);

CREATE TABLE top_transaction_state (
    id SERIAL PRIMARY KEY,
    years INT,
    state TEXT,
    entity TEXT,
    counts BIGINT,
    amount NUMERIC,
    levels TEXT
);

-- User -- 

CREATE TABLE aggregated_user_country (
    id SERIAL PRIMARY KEY,
    years INT,
    brand VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT,
    percentage DECIMAL(10,8)
);

CREATE TABLE aggregated_user_state (
    id SERIAL PRIMARY KEY,
    years INT,
    state VARCHAR(100),
    brand VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT,
    percentage DECIMAL(10,8)
);

CREATE TABLE map_user_country (
    id SERIAL PRIMARY KEY,
    years INT,
    state VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT
);

CREATE TABLE map_user_state (
    id SERIAL PRIMARY KEY,
    years INT,
    state VARCHAR(100),
    district VARCHAR(100),
    registered_users BIGINT,
    app_opens BIGINT
);

CREATE TABLE top_user_country (
    id SERIAL PRIMARY KEY,
    years INT,
    levels VARCHAR(50),
    name VARCHAR(100),
    registered_users BIGINT
);

CREATE TABLE top_user_state (
    id SERIAL PRIMARY KEY,
    years INT,
    state VARCHAR(100),
    levels VARCHAR(50),
    name VARCHAR(100),
    registered_users BIGINT
);