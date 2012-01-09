def delete_selected_actions(className, instance, request):
	actions = super(className, instance).get_actions(request)
	if 'delete_selected' in actions:
		del actions['delete_selected']
	return actions
