import bcrypt, json

from uuid import UUID

from tortoise import fields
from tortoise.models import Model
from tortoise.signals import pre_save

from fastadmin import TortoiseModelAdmin, register

from app.utils.enums import TestTuri


        
class Admin(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255, unique=True)
    hash_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return self.username
    
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
        
class User(Model):
    id = fields.BigIntField(pk=True)
    ism = fields.CharField(null=True, max_length=255)
    
    def __str__(self) -> str:
        return f"{self.id} - {self.ism}"
    
    class Meta:
        table = 'users'
        
@register(User)
class UserView(TortoiseModelAdmin):
    list_display = ('id', 'ism')
    search_fields = ('id', 'ism')
    list_filter = ('id', 'ism')
    list_display_links = ('id')
    
class Fan(Model):
    id = fields.IntField(pk=True)
    tur = fields.CharEnumField(TestTuri, max_length=10)
    nom = fields.TextField()
    
    class Meta:
        table = 'fanlar'
        
    def __str__(self) -> str:
        return self.nom
        
@register(Fan)
class FanView(TortoiseModelAdmin):
    list_display = ('id', 'tur', 'nom')
    list_display_links = ('id',)
    list_filter = ('tur, nom')
    search_fields = ('tur', 'nom')
    

    
class Test(Model):
    id = fields.IntField(pk=True)
    file = fields.TextField()
    fan = fields.ForeignKeyField('models.Fan', related_name='tests', null=True)
    data = fields.JSONField()
    savollar_soni = fields.IntField(null=True)
    umumiy_ball = fields.DecimalField(max_digits=6, decimal_places=2, null=True)
    fanlar = fields.JSONField(null=True)
    tarif = fields.TextField(null=True)
    owner = fields.TextField(null=True)
    duration = fields.IntField()
    
    class Meta:
        table = 'testlar'
        
    def __str__(self) -> str:
        return f"{self.id} {self.fanlar}"
        
@register(Test)
class TestView(TortoiseModelAdmin):
    list_display = ('id', 'fan', 'savollar_soni', 'umumiy_ball', 'duration', 'tarif', 'owner')
    list_display_links = ('id',)
    list_filter = ('fan', 'savollar_soni')
    search_fields = ('fan', 'data', 'savollar_soni')
        
@pre_save(Test)
async def test_pre_save(sender, instance, using_db, update_fields):
    if instance._saved_in_db is False:
        savollar_soni = 0
        umumiy_ball = 0
        fanlar = []
        for data in instance.data:
            savollar_soni += len(data['javoblar'])
            umumiy_ball += data['ball']*len(data['javoblar'])
            fanlar.append(data['fan'])
        
        instance.savollar_soni = savollar_soni
        instance.umumiy_ball = umumiy_ball
        instance.fanlar = fanlar
    
class Natija(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User')
    ball = fields.DecimalField(max_digits=4, decimal_places=2)
    test = fields.ForeignKeyField('models.Test')
    fan = fields.ForeignKeyField('models.Fan')
    
    class Meta:
        table = 'natijalar'
        unique_together = (('user', 'test'),)

 
@register(Natija)
class NatijaView(TortoiseModelAdmin):
    list_display = ('id', 'user', 'ball', 'test', 'fan')
    list_display_links = ('id',)
    list_filter = ('id', 'user', 'ball', 'test', 'fan')
    search_fields = ('id', 'user', 'ball', 'test', 'fan')
        

class Status(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User')
    test = fields.ForeignKeyField('models.Test')
    fan = fields.ForeignKeyField('models.Fan')
    finish_time = fields.DatetimeField()
    
    class Meta:
        table = 'statuslar'

        
@register(Status)
class StatusView(TortoiseModelAdmin):
    list_display = ('id', 'user', 'test', 'fan', 'finish_time')
    list_display_links = ('id',)
    list_filter = ('id', 'user', 'test', 'fan', 'finish_time')
    search_fields = ('id', 'user', 'test', 'fan', 'finish_time')
