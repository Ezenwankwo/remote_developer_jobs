from django.db import models


class Job(models.Model):
    tweet_id = models.CharField(max_length=100)
    created_at = models.DateTimeField()
    text = models.TextField()

    def __str__(self):
        return f"{self.tweet_id} - {self.created_at}"

    class Meta:
        ordering = ["-created_at"]

    @property
    def get_tweet_url(self):
        """returns a url to the job tweet"""
        return f"https://twitter.com/sobrarybooks/status/{self.tweet_id}"

