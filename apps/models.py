import time
from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey, Model, CharField, CASCADE, DateTimeField, ManyToManyField, ImageField, \
    FloatField, PositiveIntegerField
from django_resized import ResizedImageField

from apps.tasks import task_send_email


class CreatedBaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    image = ResizedImageField(size=[200, 200], crop=['middle', 'center'], upload_to='users/images',
                              default='users/default.jpg')


class Category(Model):
    name = CharField(max_length=255)

    def count_blogs(self) -> int:
        return self.blog_set.count()


class Teg(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Blog(CreatedBaseModel):
    name = CharField(max_length=255)
    author = ForeignKey('apps.User', CASCADE, 'blogs')
    category = ForeignKey('apps.Category', CASCADE)
    image = ImageField(default='blog/default.png', upload_to='blog/images/')
    tags = ManyToManyField('apps.Teg')
    text = RichTextField(blank=True, null=True, config_name='extends')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        emails: list = Emails.objects.values_list('email', flat=True)
        print(emails)
        start = time.time()
        task_send_email.delay("New blog" , self.name, list(emails))
        end = time.time()
        print(f"Time taken: {end - start}")

    def count_comments(self):
        return self.comment_set.count()


class Comment(Model):
    text = CharField(max_length=255)
    blog = ForeignKey('apps.Blog', CASCADE)
    author = ForeignKey('apps.User', CASCADE, 'comments')


class Product(CreatedBaseModel):
    name = CharField(max_length=255)
    price = FloatField()
    description = RichTextField(blank=True, null=True, config_name='extends')
    quantity = PositiveIntegerField(default=0)


class ProductImage(Model):
    image = ImageField(upload_to='products/images/')
    product = ForeignKey('apps.Product', CASCADE)


class Emails(Model):
    email = CharField(max_length=255)
