from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Book
from .models import SelectedBook

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, pa   ssword=password)
        if user is not None:
            login(request, user)
            return redirect('book_list')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
@login_required
def book_list(request):
    # Fetch all available books
    books = Book.objects.all()

    # Fetch selected books for the current user in the session
    selected_books = SelectedBook.objects.filter(user=request.user)

    # Get the IDs of the selected books
    selected_book_ids = [selected_book.book_id for selected_book in selected_books]

    return render(request, 'book_list.html', {'books': books, 'selected_books': selected_book_ids})

@login_required
# def select_books(request):
#     if request.method == 'POST':
#         selected_books = request.POST.getlist('selected_books')
#         user = request.user
#         for book_id in selected_books:
#             selected_book = SelectedBook.objects.create(user=user, book_id=book_id)
#         return redirect('selected_books')
#     else:
#         return redirect('book_list')
def select_books(request):
    if request.method == 'POST':
        selected_books = request.POST.getlist('selected_books')
        user = request.user
        # Delete existing selections of the user
        SelectedBook.objects.filter(user=user).delete()
        # Create new selections
        for book_id in selected_books:
            selected_book = SelectedBook.objects.create(user=user, book_id=book_id)
        return redirect('selected_books')
    else:
        return redirect('book_list')

@login_required
# def selected_books(request):
#     selected_books = request.session.get('SelectedBook', [])
#     return render(request, 'book_list.html', {'selected_books': selected_books})
def selected_books(request):
    user = request.user
    selected_books = SelectedBook.objects.filter(user=user)
    return render(request, 'selected_books.html', {'selected_books': selected_books})
@login_required
def deselect_books(request):
    if request.method == 'POST':
        deselected_books = request.POST.getlist('deselected_books')
        print("Deselected Books:", deselected_books)  # Debug statement
        user = request.user
        print("User:", user)  # Debug statement
        
        # Remove empty strings from the list
        deselected_books = [book_id for book_id in deselected_books if book_id]
        print("Filtered Deselected Books:", deselected_books)  # Debug statement
        
        # Delete deselected books for the user
        SelectedBook.objects.filter(user=user, book_id__in=deselected_books).delete()
        return redirect('selected_books')
    else:
        return redirect('book_list')


@login_required
def user_logout(request):
    logout(request)
    return redirect('user_login')

