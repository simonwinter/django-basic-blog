from django import template
from django.template import Context

from blog.models import Entry, Category, Tag

register = template.Library()

def get_slug(token):
	try:
		tag_name, entry_slug = token.split_contents()
	except ValueError:
		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
		
	return entry_slug

class TaggingNode(template.Node):
	def __init__(self, entry_slug, mode):
		self.entry_slug = template.Variable(entry_slug)
		self.mode = mode
		
		if mode == 'categories':
			self.mode_objects = Category.objects.all()
		else:
			self.mode_objects = Tag.objects.all()

	def render(self, context):
		slug = self.entry_slug.resolve(context)
		t = template.loader.get_template('fragments/%s_fragment.html' % self.mode)
		return t.render(Context({self.mode: self.mode_objects, 
								'entry': Entry.objects.get(slug=slug)}, 
								autoescape=context.autoescape))


def list_categories(parser, token):
	return TaggingNode(get_slug(token), 'categories')
	
def list_tags(parser, token):
	return TaggingNode(get_slug(token), 'tags')

register.tag('list_categories', list_categories)
register.tag('list_tags', list_tags)
