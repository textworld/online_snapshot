from django.db import models


class ImagePost(models.Model):
    image_path = models.TextField(max_length=65535)
    page_title = models.CharField(max_length=200)
    url = models.TextField(max_length=65535, null=False, default="")
    url_hash = models.CharField(max_length=128, null=True)
    page_content = models.TextField(null=True)
    gmt_create = models.DateTimeField(auto_now_add=True)
    gmt_modify = models.DateTimeField(auto_now=True)
