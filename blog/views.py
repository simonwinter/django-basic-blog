from django.conf import settings
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, get_list_or_404, get_object_or_404
from django.template import RequestContext

from blog.models import Entry, Category, Tag

from endless_pagination.decorators import page_template


@page_template("fragments/entry_fragment.html")
def paging(request, template="home.html",
    extra_context=None):
    context = {
        'objects': Entry.published_objects.accessible_entries(request.user),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render_to_response(template, context,
        context_instance=RequestContext(request))


def home(request):
	return paging(request)


def entry(request, slug):
	return render_to_response('details.html', {'entry': get_object_or_404(Entry.published_objects.accessible_entries(request.user), slug=slug)})


def category_tag_entries(request, slug, mode):
	if mode == 'category':
		extra_context = {'objects': get_list_or_404(Entry.published_objects.accessible_entries(request.user), category__slug=slug),
						'category': get_object_or_404(Category, slug=slug)}
	elif mode == 'tag':
		extra_context = {'objects': get_list_or_404(Entry.published_objects.accessible_entries(request.user), tags__slug__contains=slug),
						'tag': get_object_or_404(Tag, slug=slug)}
	else:
		raise Http404
	
	return paging(request, template='category_tags_list.html', extra_context=extra_context)


def user(request, user):
	return paging(request, extra_context={'objects': Entry.published_objects.accessible_entries(request.user).filter(user__username=user)})
