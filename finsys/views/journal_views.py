from django.urls import reverse_lazy
from django.views import generic

from finsys.forms import JournalForm
from finsys.models import JournalModel


class JournalListView(generic.ListView):
    model = JournalModel
    context_object_name = 'entries'
    template_name = 'journal.html'


class JournalDetailView(generic.DetailView):
    pass


class JournalCreateView(generic.CreateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'account-transaction.html'
    success_url = reverse_lazy('finsys:journal')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class JournalUpdateView(generic.UpdateView):
    model = JournalModel
    form_class = JournalForm
    template_name = 'account-transaction.html'
    success_url = reverse_lazy('finsys:journal')
