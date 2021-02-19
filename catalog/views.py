from django.shortcuts import render, get_object_or_404
from  catalog.models import Book, BookInstance, Author, Genre
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author

@login_required
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_avaialable = BookInstance.objects.filter(status__exact = 'a').count()
    num_authors = Author.objects.count()
    # Challenge
    books_genre_adventures = Book.objects.filter(genre__name__exact = 'Adventures').count()
    books_genre_fantazy = Book.objects.filter(genre__name__exact = 'Fantasy').count()
    books_genre_fiction = Book.objects.filter(genre__name__exact = 'Science Fiction').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_avaialable,
        'num_authors': num_authors,
        'books_genre_adventures':books_genre_adventures,
        'books_genre_fantazy':books_genre_fantazy,
        'books_genre_fiction':books_genre_fiction,


    }

    return render(request, 'index.html', context)

class BookListView(LoginRequiredMixin,ListView):
    model = Book
    paginate_by = 4


class BookDetailView(DetailView):
    model = Book
  

class AuthorListView(ListView):
    model = Author

class AuthorDetailView(DetailView):
    model = Author


class LoanedBooksByUserListView(LoginRequiredMixin,ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed.html'
    # paginate_by = 3

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedListView(PermissionRequiredMixin,ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance =get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        
        if form.is_valid():
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    success_url = reverse_lazy('authors')

class AuthorUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    fields = '__all__'
    success_url = reverse_lazy('authors')

class AuthorDelete(PermissionRequiredMixin,DeleteView):
    permission_required = 'catalog.can_mark_returned'
    model = Author
    success_url = reverse_lazy('authors')

## CRUD BOOK

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', 'genre', 'language']
    success_url = reverse_lazy('books')

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'
    success_url =reverse_lazy('books')

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')