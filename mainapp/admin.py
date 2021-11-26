from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import *
from django.utils.safestring import mark_safe
from django.forms import ModelChoiceField, ModelForm
from PIL import Image


    


class NotebookAdmin(admin.ModelAdmin):

    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class SmartPhoneAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name=='category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(SmartPhone, SmartPhoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Customer)
