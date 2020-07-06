from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from user_account.models import User


class UserAccountRegistrationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birth_date', 'image')

        def clean_email(self):
            email = self.cleaned_data['email']

            if User.objects.all().filter(email=email).exists():
                raise ValidationError('Email already exists')

            return email


class UserAccountProfileForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'image')

    def clean_email(self):

        email = self.cleaned_data['email']

        if User.objects.all()\
                .filter(email=email)\
                .exclude(id=self.instance.id)\
                .exists():
            raise ValidationError('Email already exists')

        return email
