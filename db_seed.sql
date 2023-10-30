-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 1, 'en')
;

INSERT INTO sensor (name, description, status, location, eui) VALUES
    ('Test S1', 'Sensor test 1 Hydrolab', 'on', '{{"latitude": 41.72, "longitude": 1.81}}', '8121069293845617835')
;

-- Safety trigger to prevent more than 5000 samples of one single monitor
-- CREATE TRIGGER max_samples AFTER INSERT ON sample
-- FOR EACH ROW
-- WHEN (SELECT COUNT(*) FROM sample WHERE monitor_key = new.monitor_key) >= 5000
-- BEGIN
--     DELETE FROM sample WHERE id = (SELECT id FROM sample WHERE monitor_key = new.monitor_key ORDER BY date ASC LIMIT 1);
-- END;
