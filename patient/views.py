from django.shortcuts import render, redirect
from rest_framework import viewsets
from patient.models import Patient
from patient import serializers 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Create your views here.

class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Patient.objects.all()
    serializer_class = serializers.PatientSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient_id')
        if patient_id:
            queryset = queryset.filter(id = patient_id)
        return queryset

class RegistrationView(APIView):
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data) # serializer form ta ke neya aslam

        if serializer.is_valid():
            user = serializer.save()
            
            # confirmation link ta ke strong korar jonno token r uid ta use kortaci
            token = default_token_generator.make_token(user)
            # print('token', token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            # print('uid', uid)
            confirmation_link = f"https://hospital-0851.onrender.com/patient/active/{uid}/{token}"

            # email part
            email_subject ="Confirm Your Email"
            email_body = render_to_string('confirmation_mail.html', {'confirmation_link': confirmation_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Form Submission Done")
        return Response(serializer.errors)
    
def is_active(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode() # encode kora sei uid ta ke decode kortaci
        user = User._default_manager.get(pk=uid) # ei uid ta kon user seta janar jonno ei code ta
    except (User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        print(default_token_generator.check_token(user, token))
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class LoginView(APIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        # serializer = serializers.LoginSerializer(data= self.request.data)
        serializer = self.serializer_class(data= self.request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "user_id": user.id})
            else:
                return Response({"Invalid Credential"})
        return Response(serializer.errors)
    
class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
