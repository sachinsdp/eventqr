from django.contrib import admin
from .models import Participant, MealScan

admin.site.register(Participant)
admin.site.register(MealScan)


from .models import Panel, Panelist, Question

admin.site.register(Panel)
admin.site.register(Panelist)
admin.site.register(Question)