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
        blog_pic= models.TextField(default='http://download.caiyun.feixin.10086.cn/storageWeb/servlet/GetFileByURLServlet?root=/mnt/wfs42&fileid=3Fe77a00d6bdfb5beccfb7295b71133b80.png&ct=1&type=1&code=BD26DD1BC55E13E64925B9D9BE78A129609F6FEBEBD4313F7635307B6FAE5FB8&exp=35026&account=MTM3NjE0MTgzMDc=&p=0&ui=0111Yvkc50I9&ci=0111Yvkc50I906420171210000034xxr&cn=python&oprChannel=10201200&dom=D992')
	author = models.ForeignKey(Author)
	tags = models.ManyToManyField(Tag, blank=True)
	content = models.TextField()
	date_time = models.DateTimeField(auto_now_add = True)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = ['-date_time']



