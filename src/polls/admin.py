from django.contrib import admin

# Register your models here.

from .models import Question, Choice, PollUser

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    #fields = ["pub_date", "question_text"]
    fieldsets = [
        (None, {"fields": ["question_text"]}),
        ("Date information", {"fields": ["pub_date"]}),
    ]
    list_display = ["question_text", "pub_date", "was_published_recently", "f"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]

    def f(self, obj):
        return obj.question_text + str(obj.pub_date)
    f.short_description = "New Info"

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(PollUser)
