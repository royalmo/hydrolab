-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 2, 'en', 0),
    (2, 'user', 'user@user', '{0}', 1, 1, 'en', 0)
;

INSERT INTO sensor (eui, name, location) VALUES
    ('eui-70b3d57ed8001cab', 'HydroLab OTAA 1', '{{"latitude": 41.72, "longitude": 1.81}}'),
    ('eui-70b3d57ed80024ae', 'HydroLab OTAA 2', '{{"latitude": 41.72, "longitude": 1.81045}}')
;

INSERT INTO uplink (sensor_id, humidity, temperature, battery, errors) VALUES
    ('1', '50', '20', '10', '123')
;
