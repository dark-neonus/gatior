import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from accounts.models import Comment, Account, Post, Like


class PostConsumer(WebsocketConsumer):
    def connect(self):
        self.post_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.post_group_name = f"post_{self.post_pk}"

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.post_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.post_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        json_data = json.loads(text_data)


        comment_obj = None

        # Create comment
        if len(json_data["comment"]["body"]) > 0:
            comment_obj = Comment()
            comment_obj.body = json_data["comment"]["body"]
            comment_obj.post = Post.objects.get(pk=int(json_data["post_pk"]))
            comment_obj.user = Account.objects.get(pk=int(json_data["user_pk"]))
            comment_obj.save()
        
        # Delete comment
        if len(json_data["delete_pk"]) > 0:
            comment_to_delete = Comment.objects.filter(pk=json_data["delete_pk"])

            if comment_to_delete.exists():
                comment_to_delete.delete()
            

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.post_group_name, {"type": "post.message", "message": self.create_responce(json_data, comment_obj)}
        )

        if json_data["delete_post"]:
            post_to_delete = Post.objects.filter(pk=json_data["post_pk"])

            if post_to_delete.exists():
                post_to_delete.delete()

    # Receive message from room group
    def post_message(self, event):

        # Send message to WebSocket
        self.send(text_data=event["message"])


    def create_responce(self, json_data, comment_obj):
        post = Post.objects.get(pk=int(json_data["post_pk"]))

        if comment_obj is not None:
            # Here comment date parses
            json_data["comment"]["created_at"] = comment_obj.created_at.strftime("%B %d, %Y, %H:%M")   
            json_data["comment"]["pk"] = comment_obj.pk
        
        responce = {
            "like_count": Like.objects.filter(post=post).count(),
            "comment": json_data["comment"],
            "delete_pk": json_data["delete_pk"],
            "delete_post": json_data["delete_post"],
        }

        return json.dumps(responce)
        


        
    