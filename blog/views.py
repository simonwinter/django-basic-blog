from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response

from blog.models import Entry


def home(request):
	pass

def entry(request, slug):
	try:
		entry = Entry.objects.get(slug=slug)
	except:
		raise Http404
		
	return render_to_response('blog/details.html', {'entry': entry})