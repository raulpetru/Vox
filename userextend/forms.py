from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class AuthenticationNewForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update(
            {'type': 'text', 'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update(
            {'type': 'password', 'class': 'form-control', 'id': 'floatingPassword', 'placeholder': 'Password'})


class PasswordChangeNewForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your old password'})
        self.fields['new_password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter your new password'})
        self.fields['new_password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Please enter again your new password'})
