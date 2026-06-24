CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    email      VARCHAR(255) NOT NULL UNIQUE,
    name       VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(150) NOT NULL,
    price      NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock      INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total      NUMERIC(10, 2) NOT NULL CHECK (total >= 0),
    status     VARCHAR(20) NOT NULL DEFAULT 'pending'
                   CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS order_items (
    id         SERIAL PRIMARY KEY,
    order_id   INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id),
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL
);
