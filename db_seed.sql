-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 2, 'en', 0),
    (2, 'user', 'user@user', '{0}', 1, 1, 'en', 0)
;

INSERT INTO sensor (eui, name) VALUES
    ('123456789', 'Test S1'),
    ('987654321', 'Test S1')
;


-- INSERT INTO monitor (key, title, label, min_value, max_value) VALUES
--     ('humidity', 'Humidity Graph', '%', '0', '100'),
--     ('temperature', 'Temperature Graph', 'C', '0', '30'),
--     ('battery', 'Battery Graph', '%', '0', '100'),
--     ('snr', 'SNR Graph', '', '0', '10')
-- ;
