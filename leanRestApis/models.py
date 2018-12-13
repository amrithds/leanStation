from django.db import models
from django.db import connection

# Create your models here.
class Projects(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class Activities(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name

class ProjectActivity(models.Model):
    project_id = models.IntegerField()
    activity = models.ForeignKey(Activities, on_delete = models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    parent_project_activity = models.ForeignKey("self", on_delete = models.CASCADE, null=True)
    depth=models.IntegerField(null=True)
    sequence=models.IntegerField(null=True)
    wbs_number=models.CharField(max_length=255,null=True, db_index=True)
    def create_wbs_sequence(self, project_id):
        # create a cursor  
        cur = connection.cursor()  
        # execute the stored procedure passing in   
        # search_string as a parameter  
        ret = cur.callproc('createWbsNumber', [project_id,])   
        cur.close()  
        return ret
    def __str__(self):
        return u'%s %s' % (self.project_id, self.activity)