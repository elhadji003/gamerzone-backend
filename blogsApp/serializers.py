from rest_framework import serializers
from .models import PostGaming

class PostGamingSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="user.full_name", read_only=True)  # 🔥 Retirer la virgule
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = PostGaming
        fields = ['id', 'user', 'image', 'title', 'description', 'created_at', 'updated_at', 'views', 'likes_count', 'author_name']
        read_only_fields = ['user', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()   # 🔥 Assure-toi que `LikeGaming` est bien défini avec une relation ManyToMany
