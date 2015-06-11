from django.shortcuts import render
from main.forms import UserForm, BookEditForm
from django.views.generic import TemplateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import Library, Book
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class IndexView(TemplateView):
    template_name = "main/index.html"

    # def get_context_data(self, **kwargs):
    #     context = super(IndexView, self).get_context_data(**kwargs)
    #     library = Library.objects.get(owner_id=self.request.user)
    #     context['library'] = library
    #     return context


class ProfileView(TemplateView):
    template_name = "main/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        library = Library.objects.get(owner_id=self.request.user)
        context['library'] = library
        return context


def register(request):
    """
    Allows user to register
    Author: Rana El-Garem

    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            print user_form.errors
    else:
        user_form = UserForm()

    return render(request, 'main/register.html',
                  {'user_form': user_form, 'registered': registered})


def user_login(request):
    """
    ALlows User to login
    Author: Rana El-Garem

    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                return HttpResponse("Your account has been disabled")

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'main/login.html', {})


@login_required
def user_logout(request):
    """
    Allows user to logout
    Author: Rana El-Garem

    """
    logout(request)
    return HttpResponseRedirect('/main/')


class LibraryListView(ListView):
    """
    A class for listing all instances of libraries
    :model :'ClassBasedApp.Library'
    Author: Rana El-Garem

    """

    model = Library
    template_name = 'library_list.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super(LibraryListView, self).get_context_data(**kwargs)
        library = Library.objects.get(owner_id=self.request.user)
        context['library'] = library
        library_list = Library.objects.exclude(owner_id=self.request.user)
        context['object_list'] = library_list
        return context


class LibraryCreate(CreateView):
    """
    A class for creating an instance of a library
    Author: Rana El-Garem

    """
    model = Library
    fields = ['name', 'location', 'owner']
    success_url = '/main/'
    template_name = 'main/library_form.html'


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'main/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryDetailView, self).get_context_data(**kwargs)
        book_list = Book.objects.filter(library_id=self.object.id)
        paginator = Paginator(book_list, 1)   # Show 25 contacts per page

        page = self.request.GET.get('page')
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context['books'] = books
        context['page_obj'] = paginator.page(int(page) if page else 1)
        library = Library.objects.get(owner_id=self.request.user)
        context['library'] = library
        return context


class BookDetailView(DetailView):
    """
    A class for listing all details of an instance of a book
    :model :'ClassBasedApp.Book'
    Author: Rana El-Garem
    """
    model = Book
    template_name = "main/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = Book.objects.get(id=self.object.id)
        context['book'] = book
        library = Library.objects.get(id=book.library_id)
        context['library'] = library
        return context


class BookCreate(CreateView):
    """
    A class for creating an instance of a book
    Author: Rana El-Garem

    """
    model = Book
    template_name = "main/book_form.html"
    fields = ('name', 'author', 'library')
    # success_url = '/main/'

    def get_context_data(self, **kwargs):
        context = super(BookCreate, self).get_context_data(**kwargs)
        lib_id = self.kwargs['pk']
        context['lib_id'] = lib_id
        return context


class BookDelete(DeleteView):
    """
    A class for deleting an instance of a book :model :'ClassBasedApp.Book'
    Author: Rana El-Garem
    """
    model = Book
    template_name = "main/book_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super(BookDelete, self).get_context_data(**kwargs)
        library = Book.objects.get(id=self.object.id).library_id
        context['library'] = library
        return context

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        library = Book.objects.get(id=self.object.id).library_id
        return reverse('library-detail', args=(library,))


def BookEdit(request):
    BookFormSet = modelformset_factory(Book,
                                       form=BookEditForm, extra=0)

    library = Library.objects.get(owner=request.user)
    queryset = Book.objects.filter(library=library)
    if request.method == "POST":
        formset = BookFormSet(
            request.POST,
            request.FILES,
            queryset=queryset
            )

        if(formset.is_valid()):
            formset.save()
            return HttpResponseRedirect(reverse('library-detail',
                                        args=(library.id,)))

    else:
        formset = BookFormSet(queryset=queryset)

    return render_to_response('main/book_formset.html',
                              {'formset': formset,
                               'library': library, },
                              context_instance=RequestContext(request))

