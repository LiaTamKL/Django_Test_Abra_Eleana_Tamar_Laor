from pickle import TRUE
from django.db.models import *
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
        
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not username:
            raise ValueError("User must have an username")

        account = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        account.set_password(password)
        account.save(using=self._db)
        return account

    def create_superuser(self, email,username, password):
        account = self.create_user(
        email=self.normalize_email(email),
        password=password,
        username=username,
        )
        account.is_admin = True
        account.is_staff = True
        account.is_superuser = True
        account.save(using=self._db)
        return account

class Account(AbstractBaseUser):
    email = EmailField(verbose_name='email', max_length=60, unique=True)
    username = CharField(max_length=30, unique=True)
    date_joined = DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = BooleanField(default=False)
    is_active = BooleanField(default=True)
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

class Message(Model):
    link = "Edit"
    content = TextField(max_length=100, null=False)
    by_user = ForeignKey(Account, null=False, related_name="by", on_delete=PROTECT)
    to_user = ForeignKey(Account, null=False, related_name="to", on_delete=CASCADE)
    creation_data = DateTimeField(verbose_name='date created', auto_now_add=True)
    read = BooleanField(default=False)

    class Meta:
        ordering = ['creation_data']
    def __str__(self) -> str:
        return (f'By: {self.by_user}, sent to: {self.to_user}. Message id: {self.pk}')