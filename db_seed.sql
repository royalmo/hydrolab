-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 1, 'en')
;

INSERT INTO sensor (name, description, status, location, eui) VALUES
    ('Test S1', 'Sensor test 1 Hydrolab', 'on', '{{"latitude": 41.72, "longitude": 1.81}}', '70B3D57ED8001CAB')
;

INSERT INTO monitor (key, title, label, min_value, max_value) VALUES
    ('humidity', 'Humidity Graph', '%', '0', '100'),
    ('temperature', 'Temperature Graph', 'C', '0', '30'),
    ('battery', 'Battery Graph', '%', '0', '100'),
    ('snr', 'SNR Graph', '', '0', '10')
;

INSERT INTO sensor_history (eui, timestamp, humidity, temperature, battery, bandwidth, frequency, snr, rssi) VALUES
("70B3D57ED8001CAB", '2023-12-06 00:00:00', 50, 20, 75, 125, 868, 7, -120),
("70B3D57ED8001CAB", '2023-12-06 01:00:00', 52, 21, 74, 125, 868, 6, -118),
("70B3D57ED8001CAB", '2023-12-06 02:00:00', 53, 22, 73, 125, 868, 5, -119),
("70B3D57ED8001CAB", '2023-12-06 03:00:00', 51, 23, 72, 125, 868, 8, -117),
("70B3D57ED8001CAB", '2023-12-06 04:00:00', 55, 20, 71, 125, 868, 9, -115),
("70B3D57ED8001CAB", '2023-12-06 05:00:00', 57, 25, 70, 125, 868, 5, -113),
("70B3D57ED8001CAB", '2023-12-06 06:00:00', 54, 21, 69, 125, 868, 7, -116),
("70B3D57ED8001CAB", '2023-12-06 07:00:00', 56, 24, 68, 125, 868, 8, -112),
("70B3D57ED8001CAB", '2023-12-06 08:00:00', 58, 23, 67, 125, 868, 6, -114),
("70B3D57ED8001CAB", '2023-12-06 09:00:00', 59, 22, 66, 125, 868, 4, -118),
("70B3D57ED8001CAB", '2023-12-06 10:00:00', 49, 26, 65, 125, 868, 9, -119),
("70B3D57ED8001CAB", '2023-12-06 11:00:00', 48, 25, 64, 125, 868, 3, -120),
("70B3D57ED8001CAB", '2023-12-06 12:00:00', 47, 27, 63, 125, 868, 7, -115),
("70B3D57ED8001CAB", '2023-12-06 13:00:00', 46, 28, 62, 125, 868, 8, -116),
("70B3D57ED8001CAB", '2023-12-06 14:00:00', 45, 29, 61, 125, 868, 4, -113),
("70B3D57ED8001CAB", '2023-12-06 15:00:00', 44, 30, 60, 125, 868, 6, -117),
("70B3D57ED8001CAB", '2023-12-06 16:00:00', 43, 31, 59, 125, 868, 5, -111),
("70B3D57ED8001CAB", '2023-12-06 17:00:00', 42, 32, 58, 125, 868, 4, -110),
("70B3D57ED8001CAB", '2023-12-06 18:00:00', 41, 33, 57, 125, 868, 9, -112),
("70B3D57ED8001CAB", '2023-12-06 19:00:00', 40, 34, 56, 125, 868, 10, -114)
;
-- Safety trigger to prevent more than 5000 samples of one single monitor
-- CREATE TRIGGER max_samples AFTER INSERT ON sample
-- FOR EACH ROW
-- WHEN (SELECT COUNT(*) FROM sample WHERE monitor_key = new.monitor_key) >= 5000
-- BEGIN
--     DELETE FROM sample WHERE id = (SELECT id FROM sample WHERE monitor_key = new.monitor_key ORDER BY date ASC LIMIT 1);
-- END;
