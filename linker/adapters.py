from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter

class LinkerAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/"
        return path