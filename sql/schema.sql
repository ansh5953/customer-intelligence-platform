CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,

    gender VARCHAR(20),
    senior_citizen SMALLINT,

    partner BOOLEAN,
    dependents BOOLEAN,

    tenure INTEGER CHECK (tenure >= 0),

    phone_service BOOLEAN,
    multiple_lines VARCHAR(30),

    internet_service VARCHAR(30),
    online_security VARCHAR(30),
    online_backup VARCHAR(30),
    device_protection VARCHAR(30),
    tech_support VARCHAR(30),

    streaming_tv VARCHAR(30),
    streaming_movies VARCHAR(30),

    contract VARCHAR(50),
    paperless_billing BOOLEAN,
    payment_method VARCHAR(100),

    monthly_charges NUMERIC(10, 2),
    total_charges NUMERIC(12, 2),

    churn BOOLEAN,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);