from django.contrib import admin
from .models import Author, Book, BookInstance, Genre, Language



class BookInline(admin.TabularInline):
    model = Book
    exclude = ['isbn', 'genre', 'language']
# admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BookInline]
admin.site.register(Author, AuthorAdmin)

# admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')

admin.site.register(Book, BookAdmin)

#admin.site.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','imprint', 'status','borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(BookInstance, BookInstanceAdmin)


admin.site.register(Genre)
admin.site.register(Language)


