from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# Register your models here.

# admin.site.register(BookInstance)
# admin.site.register(Book)
# admin.site.register(Author)

admin.site.register(Genre)
admin.site.register(Language)

class BookInline(admin.TabularInline):
    model=Book
    extra=0

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0

class AuthorAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','date_of_birth','date_of_death')
    fields=['first_name','last_name',('date_of_birth','date_of_death')]
    inlines=[BookInline]
admin.site.register(Author, AuthorAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title','author','display_genre','language')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=('book','status','borrower','due_back','id',)
    list_filter=('status','due_back')
    fieldsets=(
        (None,{
            'fields':('book','imprint','id')
        }),
        ('Availability',{
            'fields':('status','due_back','borrower',)
        }),
    )