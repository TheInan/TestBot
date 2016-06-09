from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Tracker(models.Model):
	message_num = models.IntegerField(default=0)
	user_id = models.IntegerField(default=0)

	def __str__(self):
		return str(self.id)