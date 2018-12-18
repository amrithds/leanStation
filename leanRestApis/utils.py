
from leanRestApis.models import ProjectActivity

def getMasterPlanHierarchy(project_id, sortFilters=['wbs_number']):
    if not project_id:
        raise ValueError('Project id is not provided.')
    
    return ProjectActivity.objects.filter(project_id=project_id).select_related('activity').order_by(sortFilters)
