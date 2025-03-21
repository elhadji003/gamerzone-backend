from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import render


User = get_user_model()

class PasswordResetView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Email non trouvé."}, status=status.HTTP_400_BAD_REQUEST)

        # Générer uidb64
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        # Générer token
        token = default_token_generator.make_token(user)

        # Lien de reset
        reset_url = f"http://127.0.0.1:8000/api/users/reset/{uidb64}/{token}/"

     
        subject = "Réinitialisation de votre mot de passe"
        message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'reset_url': reset_url,
        })

        send_mail(subject, message, 'malickelhadji07@gmail.com', [email])

        return Response({"detail": "Un email de réinitialisation a été envoyé."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({"detail": "Lien de réinitialisation invalide."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier si le token est valide
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Retourner un formulaire de réinitialisation du mot de passe (GET)
        return render(request, 'users/password_reset_form.html', {
            'uidb64': uidb64,
            'token': token
        })

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            return Response({"detail": "Lien de réinitialisation invalide."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérifier si le token est valide
        if not default_token_generator.check_token(user, token):
            return Response({"detail": "Token invalide."}, status=status.HTTP_400_BAD_REQUEST)

        # Réinitialiser le mot de passe
        new_password = request.data.get('new_password')
        user.set_password(new_password)
        user.save()

        return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)
