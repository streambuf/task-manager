from django.db import models
from datetime import datetime

class Task(models.Model):
	title = models.CharField(max_length=255)
	expiration_date = models.DateTimeField()
	is_deleted = models.BooleanField(default=False)
	is_completed = models.BooleanField(default=False)
	is_expired = models.BooleanField(default=False)

	@property
	def is_past_due(self):
	    if datetime.now() > self.expiration_date:
	        return True
	    return False
