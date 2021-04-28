import datetime
from django.shortcuts import render, get_object_or_404
from catalog.models import Book, BookInstance, Author, Genre, Language
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy #dont understand why reverse_lazy needs to be used
from catalog.forms import RenewBookForm, RenewBookModelForm #Use either of these with change in field name
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.

def index(request):
    '''View function for the home page of the site'''
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.all().count()
    num_genres=Genre.objects.all().count()
    num_languages=Language.objects.all().count()
    num_books_with_the=Book.objects.filter(title__icontains='the').count()

    num_visits = request.session.get('num_visits',1)
    request.session['num_visits'] = num_visits + 1

    context={
        'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_genres':num_genres,
        'num_languages':num_languages,
        'num_books_with_the':num_books_with_the,
        'num_visits':num_visits,
    }

    return render(request,'index.html',context=context)

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author

class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book

class BookListView(generic.ListView):
    model = Book 
    paginate_by=5
    # #Everything below this is optional. Would work even without those
    # context_object_name='my_book_list' #default would be book_list
    # # queryset = Book.objects.filter(title__icontains='i')[:5]
    # # Alternately, if I need a more complicated queryset:
    # def get_queryset(self):
    #     return Book.objects.filter(title__icontains='i')[:5]
    # template_name='books/myarbitrary_template_name.html' #default would be book_list.html

    # # To make available additional context data within the template:
    # def get_context_data(self,**kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView,self).get_context_data(**kwargs)
    #     # Creating sample data to add it to the context
    #     context['some_data'] = 'This is some additional sample data'
    #     return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    '''Generic class based view listing all books on loan to the current user'''
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).order_by('due_back').filter(status__exact='o')
    
class AllBorrowedBooksListView(PermissionRequiredMixin, generic.ListView):
    '''Class-based view listing for staff of all books borrowed from library'''
    permission_required = 'catalog.can_renew'
    model = BookInstance
    template_name = 'catalog/bookinstance_list_all_borrowed.html'
    paginate_by = 5
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = 'o').order_by('due_back')

@permission_required('catalog.can_renew')#, raise_exception=True)
def renew_book_librarian(request, pk):
    '''View function for renewing a specific book copy by a librarian'''
    copy = get_object_or_404(BookInstance,pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)
        #form = RenewBookModelForm(request.POST)
        if form.is_valid():
            copy.due_back = form.cleaned_data['renewal_date']
            copy.save()
            return HttpResponseRedirect(reverse('all-borrowed'))
    else:
        default_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': default_renewal_date})

    context = {
        'form': form,
        'book_instance': copy,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required='catalog.can_modify_authors'
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': datetime.date.today()}
    success_url = reverse_lazy('authors') #default is the newly created model item: author detail view

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required='catalog.can_modify_authors'
    fields = '__all__' # All and exclude are not recommended because of potential security issues if some new field added

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required='catalog.can_modify_authors'
    success_url = reverse_lazy('authors') #no default for delete 
    template_name_suffix = '_delete' # default is '_confirm_delete'

class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_modify_books'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', ]
    initial = {'language': 'English'} # check if this works

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_modify_books'
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language', ]

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_modify_books'
    success_url = reverse_lazy('books')
