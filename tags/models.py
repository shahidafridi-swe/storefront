from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label
    


class TaggedItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    
    #product = models.ForeignKey(Product)
    #type (product, article, video)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #ID 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()