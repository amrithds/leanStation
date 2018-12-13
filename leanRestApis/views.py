from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view
from leanRestApis.utils import getMasterPlanHierarchy
from leanRestApis.models import Projects,ProjectActivity
from rest_framework import exceptions

@api_view(['GET'])
def downloadMasterPlan(request):
    if request.method == 'GET':
        project_id = request.query_params.get('project_id')

        allowed_sort_fields = {'wbs_number':1 , 'start_date': 1, '-wbs_number': 1, '-start_date':1}
        order_by = request.query_params.get('sort', 'wbs_number')

        order = order_by.split(',')
        #validate request
        for order_filter in order:
            if order_filter not in allowed_sort_fields:
                raise exceptions.NotFound(detail="Invalid sort paramter")
        
        try: 
            obj = Projects.objects.get(id=1)
        except Projects.DoesNotExist:
            raise exceptions.NotFound(detail="Invalid project_id")

        results = getMasterPlanHierarchy(project_id, order_filter)

        csvContent = ''
        csvContent = '"SI No", "Activity", "Start date", "End date"\n'
        for result in results:
            csvContent += '"%s","%s","%s","%s"\n' % (result.wbs_number,result.activity.name,result.start_date,result.end_date)

        response = HttpResponse(csvContent,content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

        return response
    elif request.method == 'POST':
        #out of scope 
        project_id = request.POST['project_id']
        #validate parameters
        #add node
        #invoke stored procedure after insert
        ProjectActivity.create_wbs_sequence(project_id)

        #return
        #404