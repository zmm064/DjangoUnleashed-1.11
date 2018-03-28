from django.conf import settings
from django.contrib.auth import get_user, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.contrib.messages import error, success
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.debug import sensitive_post_parameters

from .forms import UserCreationForm
from .utils import MailContextViewMixin



class DisableAccount(View):
    success_url = settings.LOGIN_REDIRECT_URL
    template_name = 'user/user_confirm_delete.html'

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def get(self, request):
        # a replacement for the HttpResponse object
        return TemplateResponse(request, self.template_name)

    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def post(self, request):
        #The get_user() function takes an HttpRequest object 
        #and returns the User (or AnonymousUser) instance.
        user = get_user(request)
        # Disable the user
        user.set_unusable_password()
        user.is_active = False
        user.save()
        # destroy the current user’s session to log the user out
        logout(request)
        return redirect(self.success_url)



class CreateAccount(MailContextViewMixin, View):
    form_class = UserCreationForm
    success_url = reverse_lazy('dj-auth:create_done')
    template_name = 'user/user_create.html'

    @method_decorator(csrf_protect)
    def get(self, request):
        return TemplateResponse(request, self.template_name, {'form': self.form_class()})

    @method_decorator(csrf_protect)  # marks specific data as sensitive
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            # not catching returned user
            bound_form.save(**self.get_save_kwargs(request))
            if bound_form.mail_sent:  # mail sent?
                return redirect(self.success_url)
            else:
                errs = bound_form.non_field_errors()
                for err in errs:
                    error(request, err)
                # TODO: redirect to email resend
        return TemplateResponse(request, self.template_name, {'form': bound_form})



class ActivateAccount(View):
    success_url = reverse_lazy('dj-auth:login')
    template_name = 'user/user_activate.html'

    @method_decorator(never_cache)
    def get(self, request, uidb64, token):
        User = get_user_model()
        try:
            # turn the base-64 uidb64 number into a base-10 number
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user is not None and token_generator.check_token(user, token)):
            user.is_active = True
            user.save()
            success(request, 'User Activated! You may now login.')
            return redirect(self.success_url)
        else:
            return TemplateResponse(request, self.template_name)