# leanStation

Add a strored procedure

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