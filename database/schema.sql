-- SQLite schema reference. Flask-SQLAlchemy creates the live schema on startup.
CREATE TABLE product (
  id INTEGER PRIMARY KEY,
  slug VARCHAR(120) UNIQUE NOT NULL,
  name VARCHAR(160) NOT NULL,
  description TEXT NOT NULL,
  short_description VARCHAR(280),
  category VARCHAR(80) NOT NULL,
  price_ars INTEGER NOT NULL,
  cover_class VARCHAR(40) NOT NULL,
  accent VARCHAR(20) NOT NULL,
  featured BOOLEAN DEFAULT 0,
  file_name VARCHAR(255),
  cover_image VARCHAR(255),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_record (
  id INTEGER PRIMARY KEY,
  buyer_name VARCHAR(120) NOT NULL,
  buyer_email VARCHAR(255) NOT NULL,
  total_ars INTEGER NOT NULL,
  payment_method VARCHAR(30) NOT NULL,
  status VARCHAR(30) DEFAULT 'pending',
  download_token VARCHAR(120) UNIQUE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE order_item (
  id INTEGER PRIMARY KEY,
  order_id INTEGER NOT NULL,
  product_id INTEGER NOT NULL,
  product_name VARCHAR(160) NOT NULL,
  unit_price_ars INTEGER NOT NULL
);
