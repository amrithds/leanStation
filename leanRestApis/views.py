from django.shortcuts import render
from rest_framework.response import Response
# Create your views here.
import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view
from leanRestApis.utils import getMasterPlanHierarchy

@api_view(['GET'])
def downloadMasterPlan(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    #create header
    writer.writerow(['SI No', 'Activity', 'Start Date', 'End Date'])
    
    result = getMasterPlanHierarchy(1)
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    #return response