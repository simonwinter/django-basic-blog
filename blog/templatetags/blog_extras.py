from django import template
from django.template import Context

from blog.models import Entry, Category, Tag

register = template.Library()

def get_slug(token):
	try:
		tag_name, entry = token.split_contents()
	except ValueError:
		return None
# 		raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
		
	return entry

class TaggingNode(template.Node):
	def __init__(self, entry, mode):
		if entry:
			self.entry = template.Variable(entry)
		else:
			self.entry = None
		self.mode = mode
		
		if mode == 'categories':
			self.mode_objects = Category.objects.all()
		else:
			self.mode_objects = Tag.objects.all()

	def render(self, context):
		t = template.loader.get_template('fragments/categories_tags_fragment.html')
		data = {self.mode: self.mode_objects}

		if self.entry:
			entry = self.entry.resolve(context)
			data = dict(data.items() + {'entry': entry or None}.items())

		if 'category' in context:
			data = dict(data.items() + {'category': context['category']}.items())
		elif 'tag' in context:
			pass
			data = dict(data.items() + {'tag': context['tag']}.items())

		return t.render(Context(data, 
								autoescape=context.autoescape))


def list_categories(parser, token):
	return TaggingNode(get_slug(token), 'categories')
	
def list_tags(parser, token):
	return TaggingNode(get_slug(token), 'tags')

register.tag('list_categories', list_categories)
register.tag('list_tags', list_tags)
