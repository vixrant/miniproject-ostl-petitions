from django.db import models
from django.contrib.auth.models import User


class Petition(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    description = models.TextField()
    cover_image = models.ImageField()

    def __str__(self):
        return "{} | {} | {}".format(self.pk, self.poster, self.title)


class Signature(models.Model):
    petition = models.ForeignKey(
        Petition, related_name="signatures", on_delete=models.CASCADE
    )
    signer = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=512, blank=True)

    class Meta:
        unique_together = [("petition", "signer")]

    def __str__(self):
        return "{} | {}".format(self.petition.pk, self.signer.username)
