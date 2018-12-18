# leanStation

This stored procedure is created in an assumption that sequence of activity under parent is an input from frontend. If sequence isto be generated based on start date then add procedure 2
Add a strored procedure 1

DROP PROCEDURE IF EXISTS createWbsNumber;
DELIMITER $$
CREATE  PROCEDURE  createWbsNumber(IN proj_id INT)
	BEGIN
        #re-initialize wbs_number and depth
        UPDATE leanRestApis_projectactivity SET depth = NULL, wbs_number = NULL WHERE project_id = proj_id;

        #set root to depth 1
        UPDATE leanRestApis_projectactivity SET depth = 1 WHERE parent_project_activity_id IS NULL and project_id = proj_id;

        #calculate depth of other nodes
        WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE depth IS NULL AND project_id = proj_id) DO
            UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON (T.parent_project_activity_id = P.id)  SET T.depth = P.depth + 1  
            WHERE T.project_id = proj_id
            AND T.depth IS NULL;
        END WHILE;
    
    #set root to wbs_number to 1
    UPDATE leanRestApis_projectactivity SET  wbs_number = '1'
    WHERE parent_project_activity_id IS NULL AND project_id = proj_id;

    #set other nodes wbs_number
	WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE wbs_number Is Null AND project_id = proj_id) DO
        UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON       (T.parent_project_activity_id = P.Id)  SET T.wbs_number =   CONCAT(P.wbs_number ,'.', T.sequence)  
        WHERE P.sequence >= 0 
        AND T.wbs_number IS NULL
        AND T.project_id = proj_id; 
    END WHILE;
	END$$
	
	
Add a strored procedure 2

DROP PROCEDURE IF EXISTS createWbsNumber;
DELIMITER $$
CREATE  PROCEDURE  createWbsNumber(IN proj_id INT)
	BEGIN
        #re-initialize wbs_number and depth
        UPDATE leanRestApis_projectactivity SET depth = NULL, wbs_number = NULL WHERE project_id = proj_id;

        #set root to depth 1
        UPDATE leanRestApis_projectactivity SET depth = 1 WHERE parent_project_activity_id IS NULL and project_id = proj_id;

        #calculate depth of other nodes
        WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE depth IS NULL AND project_id = proj_id) DO
            UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON (T.parent_project_activity_id = P.id)  SET T.depth = P.depth + 1  
            WHERE T.project_id = proj_id
            AND T.depth IS NULL;
        END WHILE;
        
    WITH 
    x AS (
    SELECT
    id,
    project_id,
    ROW_NUMBER() OVER (PARTITION BY parent_project_activity_id ORDER BY start_date)  AS seq,
    start_date,
    sequence,
    parent_project_activity_id
	FROM 
	leanRestApis_projectactivity 
	where project_id = proj_id 
	AND parent_project_activity_id is NOT NULL 
	ORDER BY parent_project_activity_id)

	UPDATE leanRestApis_projectactivity 
	SET sequence = x.seq WHERE leanRestApis_projectactivity.id = x.id AND project_id = proj_id
    
    #set root to wbs_number to 1
    UPDATE leanRestApis_projectactivity SET  wbs_number = '1'
    WHERE parent_project_activity_id IS NULL AND project_id = proj_id;

    #set other nodes wbs_number
	WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE wbs_number Is Null AND project_id = proj_id) DO
        UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON       (T.parent_project_activity_id = P.Id)  SET T.wbs_number =   CONCAT(P.wbs_number ,'.', T.sequence)  
        WHERE P.sequence >= 0 
        AND T.wbs_number IS NULL
        AND T.project_id = proj_id; 
    END WHILE;
	END$$	
	
	