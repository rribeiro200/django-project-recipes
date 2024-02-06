import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.utils.text import slugify

from project import settings

class Category(models.Model):
    name = models.CharField(max_length=65, null=True)
    
    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=65, null=True)
    description = models.CharField(max_length=165, null=True)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField(null=True)
    preparation_time_unit = models.CharField(max_length=65, null=True)
    servings = models.IntegerField(null=True)
    servings_unit = models.CharField(max_length=65, null=True)
    preparation_steps = models.TextField(null=True)
    preparation_steps_is_html = models.BooleanField(default=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_published = models.BooleanField(default=False, null=True)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d', null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    # Redimensionando imagem da receita enviada pelo usuário
    @staticmethod
    def resize_image(original_img, new_width=1280):
        img_full_path = os.path.join(settings.MEDIA_ROOT, original_img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size
        new_height = round((new_width * original_height) / original_width)

        # Se 1280 for maior que a largura da imagem original enviada pelo usuário
        # Ai fazemos o redimensionamento da imagem
        # Pois, 1280 é maior, é sinal que o tamanho original da imagem não atingiu o espaço todo a ser preenchido 
        if not new_width >= original_width:
            img_pil.close()
            return
        new_image = img_pil.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(img_full_path, optime=True, quality=60)
        img_pil.close()

    # Retorna um URL absoluto para visualização detalhada da receita
    def get_absolute_url(self):
        return reverse('recipes:recipe', args=(self.pk,))

    def save(self, *args, **kwargs):
        # Criando slug automático
        if not self.slug:
            slug = f'{slugify(self.title or "", allow_unicode=False)}'
            self.slug = slug # Nova slug

        # Redimensionando imagem antes de salvar a receita
        max_image_size = 1280
        if self.cover:
            self.resize_image(self.cover, max_image_size)
        
        # Salvando definitivamente, depois das modificações necessárias
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title