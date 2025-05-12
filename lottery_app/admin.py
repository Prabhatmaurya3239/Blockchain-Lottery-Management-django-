from django.contrib import admin
from .models import User,Lottery,Participant,solidity


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_number', 'date_of_birth', 'is_active', 'is_staff')
    search_fields = ('email', 'name')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-date_of_birth',)
class LotteryAdmin(admin.ModelAdmin):
    list_display = ('lottery_name', 'organizer', 'amount', 'is_active', 'created_at')
    search_fields = ('lottery_name', 'organizer__email')
    list_filter = ('is_active',)
    ordering = ('-created_at',)

    
# Register your models here
admin.site.register(User, UserAdmin)
admin.site.register(Lottery, LotteryAdmin)
admin.site.register(Participant)
admin.site.register(solidity)



