from django.contrib.auth.mixins import UserPassesTestMixin
import news.models

class LikeMixin():
    def like(self):
        self.rating += 1
        self.save()
    
    def dislike(self):
        self.rating -= 1
        self.save()


class UserIsAuthorOfPostMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_author_id = news.models.Author.objects.get(user__pk=self.request.user.pk).id
        post_author_id = news.models.Post.objects.get(pk=self.kwargs['pk']).author_id
        return user_author_id == post_author_id


class UserIsOwnerOfProfileMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        user_id = news.models.User.objects.get(pk=self.request.user.pk).id
        profile_user_id = news.models.User.objects.get(pk=self.kwargs['pk']).id
        return user_id == profile_user_id