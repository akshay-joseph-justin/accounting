from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import JournalEntryForm, JournalEntryLineFormSet
from finsys.models import JournalEntryModel, AccountModel
from finsys.views.delete import DeleteView


class JournelEntryCreateView(generic.CreateView):
    model = JournalEntryModel
    form_class = JournalEntryForm
    formset_class = JournalEntryLineFormSet
    template_name = "entries-upsert.html"

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
            self.account = formset.forms[0].instance.account
            return super().form_valid(form)
        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(f"finsys:ledger-details", kwargs={"pk": self.account.pk})


class JournalEntryUpdateView(generic.UpdateView):
    model = JournalEntryModel
    form_class = JournalEntryForm
    template_name = 'entries-upsert.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = JournalEntryLineFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = JournalEntryLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            self.account = formset.forms[0].instance.account
            return super().form_valid(form)

        return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy("finsys:ledger-details", kwargs={"pk": self.account.pk})


class JournalEntryHistoryView(generic.DetailView):
    model = JournalEntryModel
    template_name = "entris-history.html"
    context_object_name = "entry"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["entries"] = context["entry"].lines.all()
        return context




