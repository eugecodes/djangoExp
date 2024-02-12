from django.db import models


class BankDataMixin(models.Model):
    bank_account_holder = models.CharField(max_length=255, null=True)
    bank_account_number = models.CharField(max_length=255, null=True)
    fiscal_address = models.CharField(max_length=255, null=True)

    class Meta:
        abstract = True
