from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import PostGaming
from .serializers import PostGamingSerializer


class GetAllPostGamings(generics.ListAPIView):
    """Permet à tout le monde de voir tous les posts."""
    queryset = PostGaming.objects.all().order_by('-created_at')
    serializer_class = PostGamingSerializer
    permission_classes = [permissions.AllowAny]  # Accès public

class PostGamingListCreateView(generics.ListCreateAPIView):
    """Lister et créer des posts (création réservée aux utilisateurs authentifiés)."""
    serializer_class = PostGamingSerializer
    permission_classes = [permissions.IsAuthenticated]  # Seuls les utilisateurs connectés peuvent créer

    def get_queryset(self):
        return PostGaming.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PostGamingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression d'un post (par son auteur uniquement)."""
    serializer_class = PostGamingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PostGaming.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas modifier ce post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("Vous ne pouvez pas supprimer ce post.")
        instance.delete()