from django.db import models


# Create your models here.
class OrganisationQuerySet(models.query.QuerySet):
	def get_by_user(self, user):
		return user.staffmember_set.organisation


class OrganisationManager(models.Manager):
	def get_queryset(self):
		return OrganisationQuerySet(self.model, using=self._db)

	def search(self, user):
		return self.get_queryset().get_by_user(user)


class Organisation(models.Model):
	name = models.CharField(max_length=120)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = OrganisationManager()

	def __str__(self):
		return self.name
