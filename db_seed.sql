-- Data to seed the database

INSERT INTO user VALUES
    (1, 'root', 'root@root', '{0}', 1, 2, 'en', 0),
    (2, 'user', 'user@user', '{0}', 1, 1, 'en', 0)
;

INSERT INTO sensor (eui, name) VALUES
    ('eui-70b3d57ed8001cab', 'HydroLab OTAA 1')
    ('eui-70b3d57ed80024ae', 'HydroLab OTAA 2')
;
