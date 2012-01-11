from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404

from blog.models import Entry


def pagination(request, entries_list, template='category_tags_list.html'):
	paginator = Paginator(entries_list, settings.PAGINATION_NUM_PER_PAGE)

	try:
		page = int(request.GET.get('page', '1'))
	except ValueError:
		page = 1

	try:
		entries = paginator.page(page)
	except (EmptyPage, InvalidPage):
		entries = paginator.page(paginator.num_pages)

	return render_to_response(template, {'entries': entries})


def home(request):
	entries_list = get_list_or_404(Entry.published_objects.accessible_entries(request.user))

	return pagination(request, entries_list, template='home.html')

def entry(request, slug):
	return render_to_response('details.html', {
												'entry': get_object_or_404(Entry.published_objects.accessible_entries(request.user), slug=slug)})

def category_tag_entries(request, slug, mode):
	if mode == 'category':
		entries_list = get_list_or_404(Entry.published_objects.accessible_entries(request.user), category__slug=slug)
	elif mode == 'tag':
		entries_list = get_list_or_404(Entry.published_objects.accessible_entries(request.user), tags__slug__contains=slug)
	else:
		raise Http404

	return pagination(request, entries_list)
