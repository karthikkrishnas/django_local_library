from django.db import models
from django.urls import reverse
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Genre(models.Model):
    '''Model representing a book genre'''
    name = models.CharField(max_length=200,help_text='Enter a book genre (e.g. Science Fiction)')

    def __str__(self):
        '''String for representing the Model object'''
        return self.name

class Language(models.Model):
    '''Model representing a book genre'''
    name=models.CharField(max_length=200,help_text='Enter language')

    def __str__(self):
        return self.name

class Book(models.Model):
    '''Model to represent a book IP'''
    title=models.CharField(max_length=200,help_text='Enter title of the book')
    author=models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)
    summary=models.TextField(max_length=1000,help_text='Enter a brief description of the book in a few sentences')
    isbn=models.CharField('ISBN',unique=True,max_length=13,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre=models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language=models.ForeignKey(Language,help_text='Select language for this book',on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering=['title','author']
        permissions=(('can_modify_books','Can add, update and delete books.'),)

    def __str__(self):
        '''String for representing the Model object'''
        return f'{self.title}, by {self.author}'

    def get_absolute_url(self):
        '''Returns the URL to access a detail record for this book'''
        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
        '''Create a string for the genre(s). Required to display in Admin'''
        genre_list=[genre.name for genre in self.genre.all()[:3]]
        genre_list.sort()
        return ', '.join(genre_list[:])
    
    display_genre.short_description='Genre'

class BookInstance(models.Model):
    '''Model to represent a copy of the book'''
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    book=models.ForeignKey(Book,on_delete=models.RESTRICT,null=True)
    imprint=models.CharField(max_length=200,help_text='Enter the version details')

    LOAN_STATUS=(
            ('m','Maintenance'),
            ('o','On loan'),
            ('a','Available'),
            ('r','Reserved'),
    )

    status=models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
        )
    
    borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)

    due_back=models.DateField(null=True,blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today()>self.due_back:
            return True
        return False
    
    class Meta:
        ordering=['due_back']
        permissions = (('can_mark_returned','Can mark book as returned'),('can_renew','Can mark book as renewed'),)
    
    def __str__(self):
        '''String representing the Model object'''
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    '''Model representing an author'''
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    date_of_birth=models.DateField(null=True,blank=True)
    date_of_death=models.DateField('died',null=True,blank=True)

    class Meta():
        ordering=['last_name','first_name']
        permissions=(('can_modify_authors','Can add, delete and change authors'),)

    def __str__(self):
        '''String representing the Model object'''
        return f'{self.last_name}, {self.first_name}'

    def get_absolute_url(self):
        '''Returns the URL to access a detail record for this author'''
        return reverse('author-detail',args=[str(self.id)])
