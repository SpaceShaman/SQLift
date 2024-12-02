--UP
ALTER TABLE test
DROP COLUMN column_to_delete;

--DOWN
ALTER TABLE test
ADD COLUMN column_to_delete TEXT NOT NULL;