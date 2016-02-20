from django.db import models

# Create your models here.

class Author(models.Model):
	"""docstring for Author"""
	name = models.CharField(max_length=30)
	email = models.EmailField(blank=True)
	password = models.CharField(max_length=30,blank=True)

	def __unicode__(self):
		return self.name

class Tag(models.Model):
	"""tag of book"""
	tag_name = models.CharField(max_length = 30)
	create_time = models.DateTimeField(auto_now_add =True )
	
	def __unicode__(self):
		return self.tag_name

class Blog(models.Model):
	title = models.CharField(max_length=50)
	author = models.ForeignKey(Author)
	tags = models.ManyToManyField(Tag, blank=True)
	content = models.TextField()
	date_time = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-date_time']


	
