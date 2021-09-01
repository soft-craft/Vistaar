from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from products.models import Products
from suppliers.models import Supplier


ACCOUNTS = ( ('Supplier','Supplier'),
             ('Retailer','Retailer'),
            )


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    linked = models.BooleanField(default=False)
    account_type = models.CharField(max_length=50,choices=ACCOUNTS)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
        


class Primary_leads(models.Model):
    seller = models.ForeignKey(Supplier, related_name='seller', on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='buyer', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True)
    quantity_required = models.CharField(max_length=500)
    request_description = models.CharField(max_length=999)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order by ' + str(self.buyer.profile) + ' to ' + str(self.seller) + ' for ' + str(self.product)

    def get_message(self):
        return 'I would like to buy ' + str(self.product) + ' in Quantity : "' + self.quantity_required + '" from you.'



class Message_box(models.Model):
    lead = models.OneToOneField(Primary_leads, on_delete=models.CASCADE, related_name='all_mboxes')
    title = models.CharField(max_length=100)
    initiated = models.DateTimeField(editable=False)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mboxseller', on_delete=models.CASCADE, null=True)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='mboxbuyer', on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ('initiated',)
    
    def __str__(self):
        return self.title

class Lead_messages(models.Model):
    m_box = models.ForeignKey(Message_box, on_delete=models.CASCADE, null=True)
    content = models.CharField(max_length=500)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_sender')
    reciever = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='message_reciever')
    time = models.DateTimeField(editable=False)

    class Meta:
        ordering = ('time',)