CREATE TABLE IF NOT EXISTS samples (
  id SERIAL PRIMARY KEY,
  value DOUBLE PRECISION NOT NULL
);

-- seed a few rows:
INSERT INTO samples(value)
SELECT generate_series(1, 10)
ON CONFLICT DO NOTHING;
