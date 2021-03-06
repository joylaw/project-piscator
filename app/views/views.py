## Application Objects
from app import db, logger

## Flask
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, url_for

## WTForms
from wtforms import StringField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Email

class GlobalIndexView(AdminIndexView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

class BaseView(ModelView):
	def scaffold_filters(self, name):
		filters = super().scaffold_filters(name)
		if hasattr(self, 'column_filter_labels') \
		and name in self.column_filter_labels:
			for f in filters:
				f.name = self.column_filter_labels[name]
		return filters

class AdminBaseView(BaseView):
	def is_accessible(self):
		return current_user.is_authenticated and current_user.is_admin

	def inaccessible_callback(self, name, **kwargs):
		return redirect(url_for('login'))

## User table view
class AdminUserView(AdminBaseView):
	### Display Rules
	# Page set allowed
	# PK displayed, selected columns relabelled and displayed
	can_set_page_size = True
	column_display_pk = True
	column_list = ['user_id', 'username', 'created_at', 'last_logged_in'\
	, 'is_active', 'is_admin', 'reset_token']
	column_labels = {
		'user_id' : 'ID',
		'created_at' : 'Created At',
		'last_logged_in' : 'Last Logged In',
		'is_admin' : 'Administrator',
		'is_active' : 'Active',
		'reset_token' : 'Reset Token'
	}

	# Edit columns
	column_editable_list = ['is_active']

	create_modal = True
	edit_modal = True
	# column_searchable_list = ['username', 'user_id']
	column_filters = ['user_id', 'username']

	## Custom View template
	list_template = 'admin/admin_base_list.html'
	create_template = 'admin/admin_base_create.html'
	edit_template = 'admin/admin_base_edit.html'

	# Sortable columns
	column_sortable_list = ['user_id', 'username', 'created_at', 'last_logged_in',\
	 'is_active', 'is_admin']


	### Create / Edit form rules
	# Additional fields not in column_list
	# 'password' for creating new users
	# 'change_password' for editing existing users
	form_extra_fields = {
		'password' : StringField('Password', validators=[DataRequired()]),
		'change_password': StringField('Change Password') }

	# Changes created_at and last_logged_in to be unmodifiable when editing entity
	form_widget_args = {
		'created_at' : {
			'readonly' : True,
			'disabled' : True
		},
		'last_logged_in' : {
			'readonly' : True,
			'disabled' : True
		},
	}

	# Rulesets for creating and editing, these columns will appear in
	# respective pages (create / edit)
	form_create_rules = ['username', 'password', 'is_admin']
	form_edit_rules = ['username', 'change_password', 'created_at',\
	'last_logged_in', 'is_active', 'is_admin']

	column_default_sort = 'user_id'

	# Date formatters for created_at and last_logged_in columns
	def create_date_format(view, context, model, name):
		return model.created_at.strftime('%d-%m-%Y %H:%M:%S')

	def last_login_format(view, context, model, name):
		return model.last_logged_in.strftime('%d-%m-%Y %H:%M:%S') \
		if model.last_logged_in else None

	column_formatters = {
		'created_at' : create_date_format,
		'last_logged_in' : last_login_format
	}

	# Function on creating a new user or editing password of user
	def on_model_change(self, form, model, is_created):
		logger.info("User form submitted")
		# If new user is created
		if is_created:
			logger.info("New user created: {}".format(model.get_username()))
			model.set_password(form.password.data)
		else:
			# If change_password field has data.
			# If edit and field is empty does not do anything
			# hasattr is a check for if edit is done via Modal or inline in list
			if hasattr(form, 'change_password') and form.change_password.data:
				logger.info("User {}'s password is changed"\
				.format(model.get_username()))
				# Password hashing is automatically done on Model level
				model.set_password(form.change_password.data)

	# Function on deleting user - handling of deleting currently logged in user
	def on_model_delete(self, model):
		if model == current_user:
			logger.error("Attempted to delete {} as {}. Throwing error"\
			.format(model.get_username(), current_user.get_username()))
			raise ValidationError('Cannot delete currently logged in account')

	# Function to prefill edit forms - called when edit_view is invoked
	# During editing of entries, username is set to readonly so it cannot be modified
	def on_form_prefill(self, form, model):
		form.username.render_kw = {
			'readonly':True
		}

class AdminEmailView(AdminBaseView):
	### Display Rules
	# Page set allowed
	# PK displayed, selected columns relabelled and displayed
	can_set_page_size = True
	column_display_pk = True
	column_list = ['email_id', 'email_address', 'owner_id',
	 'phishing_mail_detected', 'total_mails_checked', 'created_at', 'last_updated'\
	 , 'active', 'notification_preference']
	column_labels = {
		'email_id' : 'ID',
		'email_address' : 'Email Address',
		'owner_id' : 'Owner ID',
		'phishing_mail_detected' : 'Detections',
		'total_mails_checked' : 'Mails Checked',
		'created_at' : 'Created At',
		'last_updated' : 'Last Updated',
		'active' : 'Active',
		'notification_preference' : 'Notifications'
	}

	# Edit columns
	column_editable_list = ['active', 'notification_preference']

	create_modal = True
	edit_modal = True
	column_filters = ['owner_id', 'email_address', 'email_id', 'active'\
	, 'notification_preference']

	list_template = 'admin/admin_base_list.html'
	create_template = 'admin/admin_base_create.html'
	edit_template = 'admin/admin_base_edit.html'

	# Sortable columns
	columns_sortable_list = ['email_id', 'owner_id', 'phishing_mail_detected',\
	 'created_at', 'last_updated', 'active']

	column_default_sort = 'email_id'

	### Create / Edit form rules
	# Additional fields not in column_list
	# 'email_password' for creating new addresses
	# 'change_password' for editing existing addresses
	form_extra_fields = {
		'email_password' : StringField('Password', validators=[DataRequired()]),
		'change_password': StringField('Change Password')
	}

	# Read only columns for the following supposedly manually unmodifiable columns
	form_widget_args = {
		'last_mailbox_size' : {
			'readonly' : True,
			'disabled' : True
		},
		'created_at' : {
			'readonly' : True,
			'disabled' : True
		},
		'last_updated' : {
			'readonly' : True,
			'disabled' : True
		}
	}

	# Rulesets for creating and editing, these columns will appear
	# in respective pages (create / edit)
	form_create_rules = ['email_address', 'email_password', 'owner']
	form_edit_rules = ['email_address', 'change_password', 'owner', \
	'created_at', 'last_updated', 'active', 'notification_preference' ]

	# Date formatters for created_at and last_logged_in columns
	def create_date_format(view, context, model, name):
		return model.created_at.strftime('%d-%m-%Y %H:%M:%S')

	def last_updated_format(view, context, model, name):
		return model.last_updated.strftime('%d-%m-%Y %H:%M:%S')\
		if model.last_updated else "Never"

	column_formatters = {
		'created_at' : create_date_format,
		'last_updated' : last_updated_format
	}

	# Function on creating a new address or editing password of an address
	def on_model_change(self, form, model, is_created):
		logger.info("Email form submitted")
		# If new email is created
		if is_created:
			logger.info("New email created: {}".format(model.get_email_address()))
			model.set_email_password(form.email_password.data)
		else:
			if hasattr(form, 'change_password') and form.change_password.data:
				logger.info("Email Addr {}'s password is changed"\
				.format(model.get_email_address()))
				model.set_email_password(form.change_password.data)

	# Function to prefill edit forms - called when edit_view is invoked
	# During editing of entries, email is set to readonly so it cannot be modified
	def on_form_prefill(self, form, model):
		form.email_address.render_kw = {
			'readonly':True
		}

class AdminPhishingView(AdminBaseView):
	### Display Rules
	# Page set allowed
	# PK displayed, selected columns relabelled and displayed
	can_set_page_size = True
	column_display_pk = True
	can_create = False
	column_list = ['mail_id', 'sender_address', 'subject', 'created_at']
	column_labels = {
		'mail_id' : 'ID',
		'sender_address' : 'Sender',
		'subject' : 'Subject',
		'created_at' : 'Detected At'
	}

	create_modal = True
	edit_modal = True
	column_searchable_list = ['subject']

	## Custom View template
	list_template = 'admin/admin_base_list.html'
	create_template = 'admin/admin_base_create.html'
	edit_template = 'admin/admin_base_edit.html'

	# Sortable columns
	column_sortable_list = ['mail_id', 'sender_address', 'created_at']

	form_widget_args = {
		'sender_address' : {
			'readonly' : True
		},
		'subject' : {
			'readonly' : True
		},
		'created_at' : {
			'readonly' : True
		},
		'content' : {
			'rows' : 12,
			'readonly' : True
		}
	}

	column_default_sort = 'mail_id'

	def _content_formatter(view, context, model, name):
		return model.content[:20] + '...' if len(model.content) > 20 else model.content

	def _subject_formatter(view, context, model, name):
		return model.subject[:30] + '...' if len(model.subject) > 100 else model.subject

	column_formatters = {
		'subject' : _subject_formatter,
		'content' : _content_formatter
	}
