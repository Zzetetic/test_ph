from django.db.models import Prefetch, Max, F
from rest_framework import generics

from .serializers import PostWithLastCommentSerializer, PostWithAllCommentsSerializer
from .models import Post, Comment


class PostWithLastCommentList(generics.ListAPIView):
    serializer_class = PostWithLastCommentSerializer
    queryset = Post.objects.all().prefetch_related(
        Prefetch(
            "comments",
            queryset=Comment.objects.all().order_by("-create_date"),
        )
    )
    '''
    def get_queryset(self):
        queryset = Post.objects.raw(
        'SELECT  \
        "left"."id", "left"."title", "left"."text", \
        "left"."views_count", "left"."create_date", \
        "right"."text" as last_comment_text, \
        "right"."id" as last_comment_id \
        FROM \
        (SELECT *, MAX("posts_comment"."create_date") AS "last_comment" \
        FROM "posts_post" LEFT OUTER JOIN "posts_comment" \
        ON ("posts_post"."id" = "posts_comment"."post_id") \
        GROUP BY "posts_post"."id" ) AS "left" \
        LEFT OUTER JOIN "posts_comment" AS "right" \
        ON ("left"."id" = "right"."post_id" \
        AND "left"."last_comment"="right"."create_date")')
        return queryset
    '''
    
    
class PostWithAllComments(generics.RetrieveAPIView):
    queryset = Post.objects.prefetch_related(
      'comments')
    serializer_class = PostWithAllCommentsSerializer

    def retrieve(self, request, *args, **kwargs):
        post_inst = self.get_object()
        Post.objects.filter(id=post_inst.id).update(
          views_count=F('views_count') + 1)
        return super().retrieve(request, *args, **kwargs)
