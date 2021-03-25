from django.db import models
from organisation.models import Organisation


MEMBER_ROLES = (
	("A", "Admin"),
	("R", "Reader")
)


# Create your models here.
class StaffMember(models.Model):
	user = models.CharField(max_length=120)
	organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
	role = models.CharField(max_length=20, choices=MEMBER_ROLES)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.name
