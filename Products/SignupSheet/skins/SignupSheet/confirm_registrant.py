##parameters=id

# change workflow state for a registrant

obj = context[id]
context.portal_workflow.doActionFor(obj, 'accept-unconfirmed')

context.REQUEST.RESPONSE.redirect(context.REQUEST['HTTP_REFERER'])
