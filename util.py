def delete_selected_actions(className, instance, request):
	actions = super(className, instance).get_actions(request)
	del actions['delete_selected']
	return actions