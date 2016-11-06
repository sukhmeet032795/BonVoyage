from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from bonvoyage import views as bon

urlpatterns = [

	url(r'^admin/', include(admin.site.urls)),
	url(r'^$', bon.home, name = 'home' ),
	url(r'^dashboardTraveller/bid', bon.bid, name = 'bid'),
	url(r'^dashboardAgent/bid', bon.bid_agent, name = 'bid_agent'),	
	url(r'^userRequirement/$', bon.userRequirement, name = 'userRequirement'),	
	url(r'^submitReq/$', bon.submitReq, name = 'submitReq'),
	url(r'^submitBid/$', bon.submitBid, name = 'submitBid'),
	url(r'^getPackageDetails/$', bon.packageDetails, name = 'packageDetails'),
	url(r'^makePackage/$', bon.makePackage, name = 'makePackage'),
	url(r'^getAirports/$', bon.getAirports, name = 'getAirports'),
	url(r'^submitPackage/$', bon.submitPackage, name = 'submitPackage'),
	url(r'^viewPackage/$',bon.viewPackage, name = 'viewPackage'),
	url(r'^viewAgentPackage/$',bon.viewAgentPackage, name = 'viewAgentPackage'),
	url(r'^viewAgentPackage1/$',bon.viewAgentPackage1, name = 'viewAgentPackage1'),
	url(r'^getConditions/$', bon.getConditions, name = 'getConditions'),
	url(r'^dashboardTraveller/$', bon.dashboardTraveller, name = 'dashboardTraveller'),
	url(r'^dashboardTraveller/select/$', bon.dashboardTravellerSelect, name = 'dashboardTravellerSelect'),
	url(r'^dashboardAgent/$', bon.dashboardAgent, name = 'dashboardAgent'),
	url(r'^checkPackage/$', bon.checkPackage, name = 'checkPackage'),
	url(r'upload/', bon.upload, name = 'jfu_upload'),
	url(r'^feedback/$', bon.feedback_render, name = 'feedback_render'),	
	url(r'^agentVerification.html/$', bon.agentVerification, name = 'agentVerification'),	
	url(r'uploadVerify/', bon.uploadVerify, name = 'uploadVerify'),
	url(r'imageProcessing/', bon.imageProcessing, name = 'imageProcessing'),
	url(r'imageProcessingPan/', bon.imageProcessingPan, name = 'imageProcessingPan'),
	url(r'submitFeedback/', bon.submitFeedback, name = 'submitFeedback'),
	url(r'submitAgentDetails/', bon.submitAgentDetails, name = 'submitAgentDetails'),
	url(r'destinations/', bon.destinations, name = 'destinations'),
	url(r'adminVerification.html/', bon.adminVerification, name = 'adminVerification'),
	url(r'adminVerificationPan/', bon.adminVerificationPan, name = 'adminVerificationPan'),
	url(r'allAgents.html/', bon.allAgents, name = 'allAgents'),
	url(r'login/', bon.login, name = 'login'),
	url(r'loginCustom/', bon.loginCustom, name = 'loginCustom'),
	url(r'approve/', bon.approve, name = 'approve'),
	url(r'logout', bon.logout, name = 'logout'),
	url(r'chromeExtGetPackage', bon.chromeExtGetPackage, name = 'chromeExtGetPackage'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    

