
from tortoise import fields
from tortoise.models import Model
from tortoise.signals import pre_save

from app.utils.enums import TestTuri


class Admin(Model):
    id = fields.IntField(primary_key=True)
    username = fields.CharField(max_length=255, unique=True)
    hash_password = fields.CharField(max_length=255)
    is_superuser = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=False)

    def __str__(self):
        return self.username


class User(Model):
    id = fields.BigIntField(pk=True)
    ism = fields.CharField(null=True, max_length=255)

    def __str__(self) -> str:
        return f"{self.id} - {self.ism}"

    class Meta:
        table = 'users'


class Fan(Model):
    id = fields.IntField(pk=True)
    tur = fields.CharEnumField(TestTuri, max_length=10)
    nom = fields.TextField()

    class Meta:
        table = 'fanlar'

    def __str__(self) -> str:
        return self.nom


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
    ball = fields.DecimalField(max_digits=6, decimal_places=2)
    test = fields.ForeignKeyField('models.Test')
    fan = fields.ForeignKeyField('models.Fan')
    
    class Meta:
        table = 'natijalar'
        unique_together = (('user', 'test'),)


class Status(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User')
    test = fields.ForeignKeyField('models.Test')
    fan = fields.ForeignKeyField('models.Fan')
    finish_time = fields.DatetimeField()

    class Meta:
        table = 'statuslar'
