
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope



@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass

class RelationshipInlineFormset(BaseInlineFormSet):
    def clean(self):
        if len(self.forms) == 0:
            raise ValidationError('Не указаны теги!')
        count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                count += 1
            if count < 1:
                raise ValidationError('Не указан главный тег')
            if count > 1:
                raise ValidationError('главный тег должен быть 1')
        return super().clean()





class Scopeinline(admin.TabularInline):
    model = Scope
    formset = RelationshipInlineFormset
    extra = 0



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [Scopeinline]
