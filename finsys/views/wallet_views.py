from django.views import generic


class WalletView(generic.TemplateView):
    template_name = 'wallet.html'
