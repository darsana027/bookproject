from django.db import models
from owner.models import Books
from django.contrib.auth.models import User


# Create your models here.
class Carts(models.Model):
    product=models.ForeignKey(Books,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)

    options=(
        ("incart","incart"),
        ("orderplaced","orderplaced"),
        ("ordercancelled","ordercancelled")
    )
    status=models.CharField(max_length=15,choices=options,default="incart")