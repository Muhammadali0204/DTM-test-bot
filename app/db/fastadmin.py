import bcrypt

from uuid import UUID
from fastadmin import TortoiseModelAdmin, register

from app.db.models import Admin, Fan, Natija, Status, Test, User


@register(Admin)
class UserAdmin(TortoiseModelAdmin):
    list_display = ('id', 'username', 'is_active', 'is_superuser')

    async def authenticate(self, username: str, password: str) -> UUID | int | None:
        admin = await Admin.filter(username=username, is_superuser=True).first()
        if not admin:
            return None
        if not bcrypt.checkpw(password.encode(), admin.hash_password.encode()):
            return None
        return admin.id

    async def change_password(self, user_id, password):
        user = await self.model_cls.filter(id=user_id).first()
        if not user:
            return
        user.hash_password = password
        await user.save()


@register(User)
class UserView(TortoiseModelAdmin):
    list_display = ('id', 'ism')
    search_fields = ('id', 'ism')
    list_filter = ('id', 'ism')
    list_display_links = ('id')


@register(Fan)
class FanView(TortoiseModelAdmin):
    list_display = ('id', 'tur', 'nom')
    list_display_links = ('id',)
    list_filter = ('tur, nom')
    search_fields = ('tur', 'nom')


@register(Test)
class TestView(TortoiseModelAdmin):
    list_display = ('id', 'fan', 'savollar_soni', 'umumiy_ball', 'duration', 'tarif', 'owner')
    list_display_links = ('id',)
    list_filter = ('fan', 'savollar_soni')
    search_fields = ('fan', 'data', 'savollar_soni')


@register(Natija)
class NatijaView(TortoiseModelAdmin):
    list_display = ('id', 'user', 'ball', 'test', 'fan')
    list_display_links = ('id',)
    list_filter = ('id', 'user', 'ball', 'test', 'fan')
    search_fields = ('id', 'user', 'ball', 'test', 'fan')


@register(Status)
class StatusView(TortoiseModelAdmin):
    list_display = ('id', 'user', 'test', 'fan', 'finish_time')
    list_display_links = ('id',)
    list_filter = ('id', 'user', 'test', 'fan', 'finish_time')
    search_fields = ('id', 'user', 'test', 'fan', 'finish_time')
