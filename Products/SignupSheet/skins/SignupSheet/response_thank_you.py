## Controller Python Script "response_thank_you"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=signup_sheet=None
##title=Return thanks message
##

return container.thank_you_message(signup_sheet=signup_sheet)