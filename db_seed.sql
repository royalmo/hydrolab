-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 3, 'ca', 0),
    (2, 'user', 'user@user', '{0}', 1, 1, 'en', 0)
;

INSERT INTO sensor (eui, name, location, last_watered_at) VALUES
    ('eui-70b3d57ed8001cab', 'HydroLab OTAA 1', '{{"latitude": 41.72, "longitude": 1.81}}', 'N.A.'),
    ('eui-70b3d57ed80024ae', 'HydroLab OTAA 2', '{{"latitude": 41.72, "longitude": 1.81045}}', 'N.A.')
;

-- INSERT INTO uplink (sensor_id, humidity, temperature, battery, errors) VALUES
--     ('1', '50', '20', '10', '123')
-- ;
