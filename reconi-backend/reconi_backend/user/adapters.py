from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field, user_email
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

ReconiUser = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `ReconiUser` instance during registration.
        """
        data = form.cleaned_data
        email = data.get("email")
        nickname = data.get("nickname")
        gender = data.get("gender")
        age = data.get("age")
        favorite_scent = data.get("favorite_scent")
        sweetness = data.get("sweetness")
        body_feel = data.get("body_feel")
        acidity = data.get("acidity")
        roasting_characteristics = data.get("roasting_characteristics")

        if email:
            user_email(user, email)

        if nickname:
            user.nickname = nickname

        if gender:
            user.gender = gender

        if age:
            user.age = age

        if favorite_scent:
            user.favorite_scent = favorite_scent

        if sweetness:
            user.sweetness = sweetness

        if body_feel:
            user.body_feel = body_feel

        if acidity:
            user.acidity = acidity

        if roasting_characteristics:
            user.roasting_characteristics = roasting_characteristics

        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()

        # self.populate_username(request, user)

        if commit:
            user.save()
        return user

    def clean_email(self, email):
        """
        Checks if the given email is unique during registration.
        """
        users = ReconiUser.objects.filter(email=email)
        if users.exists():
            raise ValidationError("This email is already in use.")
        return email
