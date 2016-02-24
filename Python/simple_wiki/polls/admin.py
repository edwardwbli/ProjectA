from django.contrib import admin
from .models import Question, Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 0
class QuestiongAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    fieldsets  = [
                   ('Question', {'fields': ['question_text']}),
                   ('Date information', {'fields': ['pub_date']}),
                  ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']
admin.site.register(Question, QuestiongAdmin)
#admin.site.register(Choice)
admin.site.site_header = 'Poll Admin'
admin.site.site_title = 'Poll Admin'
