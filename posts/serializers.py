from rest_framework import serializers

from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields='__all__'


class PostWithLastCommentSerializer(serializers.ModelSerializer):
    last_comment = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields='__all__'

    def get_last_comment(self, obj):
        #return {'pk': obj.last_comment_id, 'text': obj.last_comment_text}
        return {'pk': obj.comments.all()[0].id, 'text': obj.comments.all()[0].text}
        
class PostWithAllCommentsSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(
      many=True)
    
    class Meta:
        model = Post
        fields='__all__'
