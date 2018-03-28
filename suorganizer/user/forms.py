from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .utils import ActivationMailFormMixin


class UserCreationForm(ActivationMailFormMixin, BaseUserCreationForm):

    mail_validation_error = 'User created. Could not send activation email. Please try again later. (Sorry!)'

    class Meta(BaseUserCreationForm.Meta):
        model = get_user_model()  # overriding the model
        fields = ('username', 'email')  # adding the email form to the field

    def save(self, **kwargs):
        user = super().save(commit=False)
        if not user.pk:  # 数据库中尚不存在该用户
            user.is_active = False
            send_mail = True
        else:
            send_mail = False
        user.save()
        # save any many-to-many relations using the save_m2m() method
        self.save_m2m()
        if send_mail:
            self.send_mail(user=user, **kwargs)
        return user