CREATE TABLE NBA(
    client_id INT,
    dlum_id INT,
    initial_wps FLOAT,
    current_wps FLOAT,
    best_action_path NVARCHAR(MAX),
    is_action_performed NVARCHAR(2),
    is_active NVARCHAR(2),
    PRIMARY KEY (client_id, dlum_id)
)


INSERT INTO NBA(client_id, dlum_id, initial_wps, current_wps, is_action_performed, is_active)
VALUES(1,1,1000, 1000, 'N', 'T')

INSERT INTO NBA(client_id, dlum_id, initial_wps, current_wps, is_action_performed, is_active)
VALUES(1,2,2000, 2000, 'N', 'T')