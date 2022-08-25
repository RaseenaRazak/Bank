from django.contrib import admin

# Register your models here.
from test_app.models import Branch,District, Person

admin.site.register(Branch)
admin.site.register(District)
admin.site.register(Person)