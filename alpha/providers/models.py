from django.db import models

fakeaddress = """146-148 Fake Street
FakeTown
United Kingdom
FA1 8KE"""


class Provider(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    covers_england = models.BooleanField(null=True)

    @property
    def formatted_address(self):
        if not self.address:
            return fakeaddress
        return "\n".join([x.strip() for x in self.address.split(",")])
