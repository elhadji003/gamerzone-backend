from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenRefreshView
from .serializers import RegisterSerializer

User = get_user_model()

# ✅ Expiration du token
class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            access_token = token.access_token
            return Response({"access": str(access_token)}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)

# ✅ Serializer pour GetMe et GetUserByID
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'pseudo', 'username', 'email', 'gender', 'phone', 'pays', 'bio', 'birthday', 'avatar', 'role', 'is_online']

# ✅ Pagination personnalisée
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# ✅ Register
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data["password"])
            user.save()
            return Response({"message": "Compte créé avec succès."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ✅ Login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            user.is_online = True
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        return Response({"detail": "Email ou mot de passe incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

# ✅ getMe
class GetMe(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ✅ Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Token manquant."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            user = token.user

            user.is_online = False
            user.save()

            token.blacklist()

            return Response({"detail": "Déconnecté avec succès."}, status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)


# ✅ Delete Account
class DeleteAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        user = request.user
        password = request.data.get('password')
        if not user.check_password(password):
            return Response({"detail": "Mot de passe incorrect."}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
        return Response({"detail": "Compte supprimé."}, status=status.HTTP_204_NO_CONTENT)

# ✅ Récupérer tous les utilisateurs avec pagination
class UserListView(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        users = User.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

# ✅ Récupérer un utilisateur par ID
class GetUserByIDView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != user_id and not request.user.is_staff:
            return Response({"detail": "Vous n'êtes pas autorisé à voir ces informations."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

# ✅ Modifier le profil utilisateur
class UpdateProfileUser(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_id):
        if request.user.id != user_id:
            return Response({"detail": "Vous n'êtes pas autorisé à modifier ce profil."}, status=status.HTTP_403_FORBIDDEN)

        user = get_object_or_404(User, id=user_id)
        serializer = RegisterSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            if 'is_staff' in serializer.validated_data or 'is_superuser' in serializer.validated_data:
                return Response({"detail": "Modification non autorisée."}, status=status.HTTP_403_FORBIDDEN)
            
            if 'role' in serializer.validated_data and not request.user.is_staff:
                return Response({"detail": "Vous ne pouvez pas modifier votre rôle."}, status=status.HTTP_403_FORBIDDEN)
            
            serializer.save()
            return Response({
                'detail': 'Profil mis à jour avec succès.',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
