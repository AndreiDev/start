from django.views.generic import ListView
from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.core.urlresolvers import reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

import forms

from contacts.models import Contact


class LoggedInMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(*args, **kwargs)

class ContactOwnerMixin(object):
    def get_object(self):
        try:
            return Contact.objects.get(
                                       pk=self.kwargs['pk'],
                                       owner=self.request.user,
                                       )
        except Contact.DoesNotExist:
            raise PermissionDenied


class ListContactView(LoggedInMixin,ContactOwnerMixin,ListView):
    model = Contact
    template_name = 'contact_list.html'
    
    def get_queryset(self):
        return Contact.objects.filter(owner=self.request.user)

class CreateContactView(LoggedInMixin,ContactOwnerMixin,CreateView):
    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm
    
    def get_success_url(self):
        return reverse('contacts-list')
    
    def get_context_date(self, **kwargs):
        context = super(CreateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-new')
        return context
    
class UpdateContactView(LoggedInMixin,ContactOwnerMixin,UpdateView):
    model = Contact
    template_name = 'edit_contact.html'
    form_class = forms.ContactForm    
    
    def get_success_url(self):
        return reverse('contacts-list')

    def get_context_data(self, **kwargs):
        context = super(UpdateContactView, self).get_context_data(**kwargs)
        context['action'] = reverse('contacts-edit',
                                    kwargs={'pk': self.get_object().id})
        return context

class DeleteContactView(LoggedInMixin,ContactOwnerMixin,DeleteView):
    model = Contact
    template_name = 'delete_contact.html'
    
    def get_success_url(self):
        return reverse('contacts-list')
    
class ContactView(LoggedInMixin,ContactOwnerMixin,DetailView):
    model = Contact
    template_name = 'contact.html'
    
class EditContactAddressView(LoggedInMixin,ContactOwnerMixin,UpdateView):
    model = Contact
    template_name = 'edit_addresses.html'
    form_class = forms.ContactAddressFormSet

    def get_success_url(self):

        # redirect to the Contact view.
        return self.get_object().get_absolute_url()
