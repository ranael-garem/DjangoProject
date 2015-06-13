from main.forms import BookEditForm
from django.views.generic import TemplateView, DeleteView, FormView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from main.models import Library, Book, Notification
from django.forms.models import modelformset_factory
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    """
    A Class For Displaying Index Page
    Author: Rana El-Garem
    """
    template_name = "main/index.html"


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view, login_url='/main/login_required/')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    A Class for User's Profile
    Author: Rana El-Garem

    """
    template_name = "main/profile.html"
    login_required = True

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        if Library.objects.filter(owner_id=self.request.user.id):
            library = Library.objects.get(owner_id=self.request.user.id)
            context['library'] = library

        context['count'] = Notification.objects.exclude(
                           read=1).exclude(
                           owner=self.request.user.id).filter(
                           user=self.request.user).count()

        return context


class RegisterView(FormView):
    """
    A Class that allows User to Register
    Author: Rana El-Garem

    """
    form_class = UserCreationForm
    template_name = 'main/register.html'
    success_url = '/main/profile'

    def form_valid(self, form):
        user = form.save()
        username = self.request.POST.get('username')
        password = self.request.POST.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)


class LoginView(TemplateView):
    """
    A Class for User Login
    Author: Rana El-Garem

    """
    template_name = 'main/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/profile')
            else:
                return HttpResponse("Your account has been disabled")

        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")


class LoginRequiredView(LoginView, TemplateView):
    template_name = "main/login_required.html"


class LogoutView(LoginRequiredMixin, TemplateView):
    """
    A Class that allows User to logout
    Author: Rana El-Garem

    """
    template_name = 'main/index.html'
    login_required = True

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        logout(request)
        return self.render_to_response(context)


class LibraryListView(ListView):
    """
    A class for listing all instances of libraries
    Author: Rana El-Garem

    """
    model = Library
    template_name = 'library_list.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryListView, self).get_context_data(**kwargs)
        # library_list = Library.objects.exclude(owner_id=self.request.user)
        if Library.objects.filter(owner_id=self.request.user.id):
            library = Library.objects.get(owner_id=self.request.user)
            context['library'] = library

        library_list = Library.objects.all()
        paginator = Paginator(library_list, 2)   # Show 25 contacts per page
        page = self.request.GET.get('page')
        try:
            libraries = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            libraries = paginator.page(1)
        except EmptyPage:
            libraries = paginator.page(paginator.num_pages)
        context['libraries'] = libraries
        context['page_obj'] = paginator.page(int(page) if page else 1)
        return context


class LibraryCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    A class for creating an instance of a library
    User must be logged in to add a library
    Author: Rana El-Garem

    """
    model = Library
    fields = ['name', 'location', 'owner']
    success_message = "%(name)s was created successfully"
    template_name = 'main/library_form.html'

    def get_success_url(self):
        """
        Redirects to the library page
        """
        library = Library.objects.get(owner=self.request.user).id
        return reverse('library-detail', args=(library,))


class LibraryDetailView(DetailView):
    """
    A class for listing all detail of an instance of a Library
    Author: Rana El-Garem

    """
    model = Library
    template_name = 'main/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super(LibraryDetailView, self).get_context_data(**kwargs)
        book_list = Book.objects.filter(library_id=self.object.id)
        paginator = Paginator(book_list, 5)   # Show 25 contacts per page

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

        if Library.objects.filter(owner_id=self.request.user.id):
            library = Library.objects.get(owner_id=self.request.user)
            context['library'] = library

        return context


class BookDetailView(DetailView):
    """
    A class for listing all details of an instance of a book
    Author: Rana El-Garem
    """
    model = Book
    template_name = "main/book_detail.html"
    login_required = True

    def get_context_data(self, **kwargs):
        context = super(BookDetailView, self).get_context_data(**kwargs)
        book = Book.objects.get(id=self.object.id)
        context['book'] = book
        library = Library.objects.get(id=book.library_id)
        context['library'] = library
        return context


class BookCreate(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    A class for creating an instance of a book
    User must be logged in to add a book
    Author: Rana El-Garem

    """
    model = Book
    template_name = "main/book_form.html"
    fields = ('name', 'author', 'library')
    success_message = "%(name)s was added successfully"

    def get_context_data(self, **kwargs):
        context = super(BookCreate, self).get_context_data(**kwargs)
        lib_id = self.kwargs['pk']
        context['lib_id'] = lib_id
        return context


class BookDelete(LoginRequiredMixin, DeleteView):
    """
    A class for deleting an instance of a book :model :'ClassBasedApp.Book'
    User must be logged in to delete a book
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
        messages.add_message(request,
                             messages.INFO,
                             "" + self.object.name +
                             " was deleted successfully")
        self.object.delete()
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        """
        Redirects to the library page
        """
        library = Book.objects.get(id=self.object.id).library_id
        return reverse('library-detail', args=(library,))


class BookUpdate(LoginRequiredMixin, TemplateView):
    """
    A class for updating all instances of books
    User must be logged instances
    Author: Rana El-Garem

    """
    template_name = 'main/book_formset'

    def post(self, request, *args, **kwargs):
        BookFormSet = modelformset_factory(Book,
                                           form=BookEditForm, extra=0)

        library = Library.objects.get(owner=request.user)
        queryset = Book.objects.filter(library=library)
        formset = BookFormSet(
            request.POST,
            request.FILES,
            queryset=queryset)

        if(formset.is_valid()):
            formset.save()
            messages.add_message(request, messages.INFO,
                                 "Books were updated successfully")
            return HttpResponseRedirect(reverse('library-detail',
                                        args=(library.id,)))

    def get(self, request, *args, **kwargs):
        BookFormSet = modelformset_factory(Book,
                                           form=BookEditForm, extra=0)

        library = Library.objects.get(owner=request.user)
        queryset = Book.objects.filter(library=library)
        formset = BookFormSet(queryset=queryset)
        return render_to_response('main/book_formset.html',
                                  {'formset': formset,
                                   'library': library, },
                                  context_instance=RequestContext(request))


@receiver(post_save, sender=Book)
def notify_book_create(sender, **kwargs):
    """
    Creates notification for every user when a book is created
    Author: Rana El-Garem

    """

    if kwargs.get('created', False):
        book = kwargs.get('instance')
        if book.library_id:
            library = Library.objects.get(id=book.library_id)
            user_list = User.objects.all()
            for user in user_list:
                Notification.objects.get_or_create(
                 message="" + library.name +
                 " added a new book '" + book.name+"'",
                 book=book, library=library,
                 owner=library.owner, slug=book.slug,
                 user=user)


class NotificationListView(LoginRequiredMixin, ListView):
    """
    A class for listing all instances of Notification
    belonging to a certain user
    User must be logged in
    Author: Rana El-Garem

    """
    model = Notification
    template_name = 'notification_list.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationListView,
                        self).get_context_data(**kwargs)
        if Library.objects.filter(owner_id=self.request.user.id):
            library = Library.objects.get(owner_id=self.request.user)
            context['library'] = library

        notification_list = Notification.objects.exclude(
                            read=1).exclude(
                            owner=self.request.user.id).filter(
                            user=self.request.user)

        paginator = Paginator(notification_list, 2)
        page = self.request.GET.get('page')
        try:
            notifications = paginator.page(page)
            for notification in notifications:
                notification.read = 1
                notification.save()
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            notifications = paginator.page(1)
            for notification in notifications:
                notification.read = 1
                notification.save()
        except EmptyPage:
            notifications = paginator.page(paginator.num_pages)

        context['object_list'] = notifications
        context['page_obj'] = paginator.page(int(page) if page else 1)
        context['unread_list'] = Notification.objects.exclude(
                                read=0).exclude(
                                owner=self.request.user.id).filter(
                                user=self.request.user)
        return context
