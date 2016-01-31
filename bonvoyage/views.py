from django.contrib import auth
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
import json
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import timezone

from django.core import serializers

from travelRequirement.models import *
from urllib.request import urlopen
import base64
import requests
import datetime
import os
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse
import xml.etree.ElementTree
import xmltodict
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def home(request):

	url= settings.STATICFILES_DIRS[0]+ '/js/travelDestinations.json';
	destination = json.loads(open( url ).read())
	length=len(destination)
	categories=['Weekend-Getaways','Romantic','Relax','Cultural','Disappear','Adventure','City','With-Friends','With-Family']
	length_i=len(categories)
	i=0;
	dest=[];

	while(i<length_i):

		j=0;
		individual=[];
		obj={};
		while(j<length):

			if(destination[j]['Type'] == categories[i]):

				url="/static/images/IMAGES/"+destination[j]["Image"]
				obj={

					'name' : destination[j]["Name"],
					'image' : url
				}
				individual.append(obj)

			j+=1;

		objFinal={
		
			'type':categories[i],
			'des': individual
		}

		i=i+1;
		dest.append(objFinal);

	return render(request,'home.html',{

		'data':dest
	});

def checkPackage(request):
	id=request.GET.get("id");
	check=request.GET.get("value");	

	package=travelPackage.objects.filter(id=id)[0];

	print(int(check));
	if(int(check) == 1):
		package.selectedForBid=True;

	if(int(check) == 2):
		package.selectedForBid =False;
		
	package.save();	
	return HttpResponse(json.dumps({"status": 1}), content_type="application/json")