from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import JournalEntryForm, JournalEntryLineFormSet
from finsys.models import JournalEntry
from finsys.views.delete import DeleteView


class JournelEntryListView(generic.ListView):
    model = JournalEntry
    context_object_name = 'entries'
    template_name = "entries_list.html"
    ordering = ['-date']


class JournelEntryDetailView(generic.DetailView):
    model = JournalEntry
    context_object_name = 'entry'
    template_name = "entries_details.html"


class JournelEntryCreateView(generic.CreateView):
    model = JournalEntry
    form_class = JournalEntryForm
    formset_class = JournalEntryLineFormSet
    template_name = "entries_upsert.html"
    success_url = reverse_lazy("finsys:entries-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            formset = self.formset_class(self.request.POST, instance=self.object)
        else:
            formset = self.formset_class()
        context['formset'] = formset
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save(commit=False)
        formset = self.formset_class(self.request.POST, instance=self.object)

        if formset.is_valid():
            self.object.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        return self.form_invalid(form)


class JournelEntryUpdateView(generic.UpdateView):
    model = JournalEntry
    form_class = JournalEntryForm
    formset_class = JournalEntryLineFormSet
    template_name = "entries_upsert.html"
    success_url = reverse_lazy("finsys:entries-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formset = JournalEntryLineFormSet(instance=self.get_object())
        context['formset'] = formset
        return context


class JournelEntryDeleteView(DeleteView):
    model = JournalEntry
    success_url = reverse_lazy("finsys:entries-list")
