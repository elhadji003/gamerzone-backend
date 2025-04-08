from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PostGaming, LikeGaming

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like_post(request, post_id):
    """Ajoute ou enlève un like sur un post."""
    try:
        post = PostGaming.objects.get(id=post_id)
        like, created = LikeGaming.objects.get_or_create(user=request.user, post=post)

        if not created:
            like.delete()
            message = "Like supprimé"
        else:
            message = "Post liké"

        return Response({
            "message": message,
            "likes_count": post.likes.count()
        }, status=200)
    
    except PostGaming.DoesNotExist:
        return Response({"error": "Post introuvable"}, status=404)
