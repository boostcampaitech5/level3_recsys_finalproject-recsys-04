from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import ReconiUser, GENDER_CHOICES, SCENT_CHOICES

from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError


class MyCustomSignupForm(SignupForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if ReconiUser.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

    def save(self, request):
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)

        # Add your own processing here.
        # For example, you can set additional fields on the user model.
        user.nickname = self.cleaned_data["nickname"]
        user.gender = self.cleaned_data["gender"]
        user.age = self.cleaned_data["age"]
        user.favorite_scent = self.cleaned_data["favorite_scent"]
        user.sweetness = self.cleaned_data["sweetness"]
        user.body_feel = self.cleaned_data["body_feel"]
        user.acidity = self.cleaned_data["acidity"]
        user.roasting_characteristics = self.cleaned_data[
            "roasting_characteristics"
        ]

        # You must save the user model after setting additional fields.
        user.save()

        # You must return the original result.
        return user


class ReconiUserCreationForm(forms.ModelForm):
    class Meta:
        model = ReconiUser
        fields = [
            "email",
            "nickname",
            "gender",
            "age",
            "favorite_scent",
            "sweetness",
            "body_feel",
            "acidity",
            "roasting_characteristics",
        ]

    # 폼에서 사용되는 필드의 라벨을 지정할 수 있습니다.
    labels = {
        "email": "E-mail",
        "nickname": "별명",
        "gender": "성별",
        "age": "나이",
        "favorite_scent": "선호하는 향",
        "sweetness": "단맛",
        "body_feel": "바디감",
        "acidity": "산미",
        "roasting_characteristics": "로스팅 특징",
    }
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    # 성별 필드에 대해 라디오 버튼 형태로 표시되도록 위젯을 설정합니다.
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)

    # 선호하는 향 필드에 대해 셀렉트 박스 형태로 표시되도록 위젯을 설정합니다.
    favorite_scent = forms.ChoiceField(
        choices=SCENT_CHOICES, widget=forms.Select
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ReconiUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = ReconiUser
        fields = (
            "email",
            "nickname",
            "gender",
            "age",
            "favorite_scent",
            "sweetness",
            "body_feel",
            "acidity",
            "roasting_characteristics",
            "is_active",
            "is_staff",
        )

    def clean_password(self):
        return self.initial["password"]
