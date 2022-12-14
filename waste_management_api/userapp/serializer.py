
from rest_framework import serializers
from allauth.account.adapter import get_adapter
from main import settings
from .models import User
from phonenumber_field.serializerfields import PhoneNumberField
# from allauth.account.utils import setup_user_email


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=settings.ACCOUNT_EMAIL_REQUIRED)
    first_name = serializers.CharField(required=False, write_only=True)
    last_name = serializers.CharField(required=False, write_only=True)
    address = serializers.CharField(required=False, write_only=True)
    phone = PhoneNumberField()
    password1 = serializers.CharField(required=True, write_only=True,label ="Password")
    password2 = serializers.CharField(required=True, write_only=True,label ="Confirm Password")

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'user_type': self.validated_data.get('user_type', ''),
            'password1': self.validated_data.get('password1', ''),
            'phone': self.validated_data.get('phone', ''),
            'email': self.validated_data.get('email', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        print("****************self.cleaned_data*********************",self.cleaned_data)
        user.phone =self.cleaned_data.get("phone")
        adapter.save_user(request, user, self)
        # setup_user_email(request, user, [])
        return user

        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name',
                  'last_name',"phone")
        read_only_fields = ('email', )
