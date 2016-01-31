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

def dashboardTravellerSelect(request):
	
	user=request.user;
	id=request.GET.get("q");
	package=travelPackage.objects.filter(travelReqId=id,selectedForBid=0).order_by('price');
	packages=[];
	for p in package:
		obj={

			'id':p.id,
			'name':p.name,
			'price':p.price
		}	
		packages.append(obj);

	return render(request,'DashboardTravellerSelect.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'packages':packages 
});	


def dashboardTraveller(request):
	
	print(request.user)
	user=User.objects.filter(id=request.user.id)[0];
	userReq=travelReq.objects.filter(userId=user.id).order_by('-startDate');
	date=datetime.date.today();
	reqobj=[];
	count1 = -1
	if (userReq.count() == 0):
		count1 = 0
		return  HttpResponseRedirect('/userRequirement')
	
	else:
		for u in userReq:
			end=0
			
			print(u.endDate)
			if(u.endDate == "14 October,2015" or u.endDate == "16 October,2015" or u.endDate == "17 October,2015"):
				end=1;
			count= travelPackage.objects.filter(travelReqId=u.id).count();
			id=u.id;	
			obj={

				'startDate':u.startDate,
				'endDate':u.endDate,
				'budget':u.budget,
				'name':u.reqName,
				'status':u.status,
				'count':count,
				'end':end,
				'id':id
			}
			reqobj.append(obj)

	return render(request,'DashboardTraveller.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'reqobj' :reqobj,
		'count': count1
	});

def dashboardAgent(request):

	user=request.user;
	requirementObj=travelReq.objects.filter(status=0).order_by('-startDate');
	reqobj=[];
	for u in requirementObj:
		packageExist=0;
		packageSelected=0;
		userPackage=travelPackage.objects.filter(travelReqId=u.id, userId=user.id);
		if(len(userPackage)!=0):
			packageExist=1;
			userPackage=userPackage[0];
			if(userPackage.selectedForBid ==1 ):
				packageSelected=1;

		count= travelPackage.objects.filter(travelReqId=u.id).count();
		id=u.id;	
		obj={

			'startDate':u.startDate,
			'endDate':u.endDate,
			'budget':u.budget,
			'name':u.reqName,
			'count':count,
			'package':packageExist,
			'packageSelect':packageSelected,
			'places': u.placeToVisit,
			'id':id
		}
		reqobj.append(obj)
	print(reqobj);	
	return render(request,'DashboardAgent.html',{

		'firstName':user.first_name,
		'lastName':user.last_name,
		'reqobj' :reqobj 
	});	

def bid(request):
	userId=request.user.id;
	id=request.GET.get("q");
	traveller= travelReq.objects.filter(id=id)[0];
	packages=travelPackage.objects.filter(travelReqId=traveller.id).order_by('price');
	place=traveller.placeToVisit;
	places=place.split( );
	user_Traveller= User.objects.filter(id=traveller.userId.id)[0];
	name= user_Traveller.username;
	travellerObj={

		'name' : name,
		'startDate': traveller.startDate,
		'endDate' : traveller.endDate,
		'cities':places
	}
	packageArray=[];
	count=0;
	for p in packages:
		count+=1;
		discount=0;
		savings=0;
		user_Agent= User.objects.filter(id=p.userId.id)[0];
		name= user_Agent.first_name + " " + user_Agent.last_name;
		# if(int(p.bidPrice)!=0):
		discount=int(100-((int(p.price)-int(p.bidPrice))/int(p.price))*100);
		savings=(int(p.price)-int(p.bidPrice));
		newPrice=(int(p.price)-int(p.bidPrice));
		obj={
			'Id':p.id,
			'Username':name,
			'Packagename':p.name,
			'Price':p.price,
			'BidPrice':p.bidPrice,
			'Discount':discount,
			'Savings':savings
		}
		packageArray.append(obj);
	packageArray.sort(key=lambda x: x['Savings'], reverse=False)
	print(packageArray)
	return render(request,'biddingViewTraveller.html',{

			'firstName':request.user.first_name,
			'lastName':request.user.last_name,
			'travelAgents':packageArray,
			'traveller': travellerObj,
			'agentCount':count	
		});	

def userRequirement(request):
	return render(request,'userRequirement.html');

