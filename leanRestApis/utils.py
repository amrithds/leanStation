
from leanRestApis.models import ProjectActivity

def getMasterPlanHierarchy(project_id):
    if not project_id:
        raise ValueError('Project id is not provided.')
    
    sql = """select  id,parent_project_activity_id, start_date, end_date, activity_id from    
                (select * from leanRestApis_projectactivity
                    order by parent_project_activity_id, id) leanRestApis_projectactivity_temp,
                    (select @pv := '1') initialisation
                where   ( find_in_set(parent_project_activity_id, @pv) > 0
                and     @pv := concat(@pv, ',', id) ) OR id = @pv"""
    return ProjectActivity.objects.raw(sql)


# DELIMITER $$
# DROP FUNCTION IF EXISTS `getDepth` $$
# CREATE FUNCTION `getDepth` (activity_id INT, project_id INT) RETURNS int
# BEGIN
#     DECLARE depth INT;
#     SET depth=1;

#     WHILE activity_id > 0 DO
#         SELECT IFNULL(parent_project_activity_id,-1) 
#         INTO activity_id 
#         FROM ( SELECT parent_project_activity_id FROM leanRestApis_projectactivity WHERE activity_id = activity_id and project_id = project_id) t;

#         IF activity_id > 0 THEN
#             SET depth = depth + 1;
#         END IF;

#     END WHILE;

#     RETURN (depth);

# END $$
# DELIMITER ;


# DELIMITER $$
# DROP FUNCTION IF EXISTS getDepth $$
# CREATE FUNCTION getDepth(activity_id INT, project_id INT) RETURNS int
# BEGIN
#     DECLARE depth INT;
#     SET depth=1;

#     WHILE activity_id > 0 DO
#         SELECT IFNULL(parent_project_activity_id,-1) 
#         INTO activity_id 
#         FROM ( SELECT parent_project_activity_id FROM leanRestApis_projectactivity WHERE activity_id = activity_id and project_id = project_id) t;

#         IF activity_id > 0 THEN
#             SET depth = depth + 1;
#         END IF;

#     END WHILE;

#     RETURN (depth);

# END $$
# DELIMITER ;

# select  id,parent_project_activity_id, start_date, end_date, activity_id,getDepth(activity_id, 1) from    
#                 (select * from leanRestApis_projectactivity where project_id = 1
#                     order by parent_project_activity_id, id) leanRestApis_projectactivity_temp,
#                     (select @pv := '1') initialisation
#                 where   ( find_in_set(parent_project_activity_id, @pv) > 0
#                 and     @pv := concat(@pv, ',', id) ) OR id = @pv
                
                
                
DROP PROCEDURE IF EXISTS createWbsNumber;
DELIMITER $$
CREATE  PROCEDURE  createWbsNumber()
	BEGIN
        UPDATE leanRestApis_projectactivity SET depth = 1 WHERE parent_project_activity_id IS NULL and project_id = 1;

        WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE depth IS NULL AND project_id = 1) DO
            UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON (T.parent_project_activity_id = P.id)  SET T.depth = P.depth + 1  
            WHERE T.project_id = 1
            AND T.depth IS NULL;
        END WHILE;
    
    UPDATE leanRestApis_projectactivity SET  wbs_number = '1'
    WHERE parent_project_activity_id IS NULL AND project_id = 1;

	WHILE EXISTS (SELECT * FROM leanRestApis_projectactivity WHERE wbs_number Is Null AND project_id = 1) DO
        UPDATE leanRestApis_projectactivity AS T INNER JOIN leanRestApis_projectactivity AS P ON       (T.parent_project_activity_id = P.Id)  SET T.wbs_number =   CONCAT(P.wbs_number ,'.', T.sequence)  
        WHERE P.sequence >= 0 
        AND T.wbs_number IS NULL
        AND T.project_id = 1; 
    END WHILE;
	END$$
call createWbsNumber();