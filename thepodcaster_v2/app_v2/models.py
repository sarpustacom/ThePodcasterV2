import os
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.deconstruct import deconstructible
import uuid as u
from . import extensions
# Create your models here.

languages = {
    "en-us": "English (United States)",
    "en-gb": "English (United Kingdom)",
    "tr-tr": "Turkish (Turkey)",
    "de-de": "German (Germany)",
    "fr-fr": "French (France)",
    "es-es": "Spanish (Spain)",
    "it-it": "Italian (Italy)",
    "ru-ru": "Russian (Russia)",
    "zh-cn": "Chinese (Simplified)",
    "ja-jp": "Japanese (Japan)",
    "ko-kr": "Korean (South Korea)",
    "pt-br": "Portuguese (Brazil)",
    "ar-sa": "Arabic (Saudi Arabia)",
    "hi-in": "Hindi (India)",
    "uk-ua": "Ukrainian (Ukraine)",
    "pl-pl": "Polish (Poland)",
    "nl-nl": "Dutch (Netherlands)",
    "sv-se": "Swedish (Sweden)",
    "fi-fi": "Finnish (Finland)",
    "da-dk": "Danish (Denmark)",
    "no-no": "Norwegian (Norway)",
    "hu-hu": "Hungarian (Hungary)",
    "cs-cz": "Czech (Czech Republic)",
    "sk-sk": "Slovak (Slovakia)",
    "ro-ro": "Romanian (Romania)",
    "bg-bg": "Bulgarian (Bulgaria)",
    "el-gr": "Greek (Greece)"
}

@deconstructible
class AudioFileValidator:
    allowed_extensions = {'mp3', 'wav'}

    def __call__(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(f"Invalid file type: {ext}. Allowed: {self.allowed_extensions}")

@deconstructible
class ImageFileValidator:
    allowed_extensions = {'jpg', 'jpeg', 'png'}

    def __call__(self, value):
        ext = value.name.split('.')[-1].lower()
        if ext not in self.allowed_extensions:
            raise ValidationError(f"Invalid file type: {ext}. Allowed: {self.allowed_extensions}")
        


def upload_audio_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"audio_{u.uuid4()}.{ext}"
    directory = f"sounds/user_{instance.show.author.id}/"
    if os.path.exists(directory):
        os.makedirs(directory)
    return os.path.join(directory, new_filename)


def upload_photos_to(instance, filename):
    ext = filename.split('.')[-1].lower()
    new_filename = f"photo_{u.uuid4()}.{ext}"
    return os.path.join('photos/', new_filename)


class Show(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    cover = models.ImageField(upload_to=upload_photos_to, validators=[ImageFileValidator()])
    keywords = models.CharField(max_length=160)
    copyright = models.CharField(max_length=160)
    language = models.CharField(max_length=30, choices=[(k, v) for k, v in languages.items()], default='en-us')
    explicit = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    pubDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def format_pubdate(self):
        return str(extensions.correct_date(self.pubDate))
    

class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    pubDate = models.DateTimeField(auto_now=True)
    duration = models.CharField(max_length=30)
    guid = models.UUIDField(default=u.uuid4, editable=False)
    explicit = models.BooleanField(default=False)
    audio = models.FileField(upload_to=upload_audio_to, validators=[AudioFileValidator()])

    def __str__(self):
        return self.title
    
    def media_mime_type(self):
        ext = self.audio.name.split('.')[-1].lower()
        if ext == 'mp3':
            return 'audio/mpeg'
        elif ext == 'wav':
            return 'audio/wav'
        return 'application/octet-stream'
    
    def format_pubdate(self):
        return str(extensions.correct_date(self.pubDate))
    