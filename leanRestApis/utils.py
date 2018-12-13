
from leanRestApis.models import ProjectActivity

def getMasterPlanHierarchy(project_id, sortFilters=['wbs_number']):
    if not project_id:
        raise ValueError('Project id is not provided.')
    
    return ProjectActivity.objects.filter(project_id=project_id).select_related('activity').order_by(sortFilters)


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
                
                
                
