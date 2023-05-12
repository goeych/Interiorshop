from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models

from vendor.models import Vendor

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering']

    def __str__(self):
        return self.title
    
class Product(models.Model):
    category = models.ForeignKey(Category,related_name = 'products',on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor,related_name = 'products',on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField(null=True, blank = True)
    price = models.DecimalField(max_digits=6,decimal_places = 2)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/',blank = True,null = True)
    thumbnail = models.ImageField(upload_to='uploads/',blank = True,null = True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x180.jpg'
        
    def make_thumbnail(self,image,size=(300,200)):
        img = Image.open(image)
        img= img.convert('RGB')# Convert to RGB color mode
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io,'JPEG',quality=85)

        thumbnail = File(thumb_io,name=image.name)

        return thumbnail
    
'''
This is a method defined in a class that returns a thumbnail URL for an image. It takes in a parameter self which refers to the instance of the class itself.

The method first checks if self.thumbnail exists, which would mean that a thumbnail has already been generated for the image and saved. If it does, the URL of the thumbnail is returned.

If self.thumbnail does not exist, the method checks if self.image exists. If it does, the make_thumbnail method is called with self.image as the argument, and the resulting thumbnail is saved as self.thumbnail using the save() method. The URL of the thumbnail is then returned.

If self.thumbnail and self.image do not exist, a placeholder image URL is returned.

The make_thumbnail method takes in an image parameter which is the original image file. It opens the image using the PIL library's Image.open() method, converts it to the RGB format using the convert() method, and creates a thumbnail of size (300, 200) using the thumbnail() method. The resulting thumbnail is then saved as a JPEG file in memory using a BytesIO object and returned as a File object.
'''


