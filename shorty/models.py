from django.db import models

from hashlib import md5
from graphql import GraphQLError
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

# Create your models here.
class URL(models.Model):
    original_url = models.URLField(unique=True)
    url_hash = models.URLField(unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_accessed_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    # Keeps track of the number of clicks to shortened url.
    def clicked(self):
        self.clicks += 1
        self.save()

    # Validates and saves url.
    def save(self):
        self.validate_url()
        if not self.id:
            self.url_hash = md5(self.original_url.encode()).hexdigest()[:10]
        try:
            return super().save()
        except IntegrityError:
            return URL.objects.get(url_hash=self.url_hash)

    # Validates the url received.
    def validate_url(self):
        validate = URLValidator()
        try:
            validate(self.original_url)
        except ValidationError:
            raise GraphQLError("You entered an invalid url.")
