from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from todo.utils import send_mail


# Model тип котельной
class TypeBoiler(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва котельной")
    year = models.PositiveIntegerField(default=2000, verbose_name="Рiк випуску")

    def __str__(self):
        return self.name


class Board(models.Model):
    name = models.CharField(max_length=30, verbose_name="Назва дошки")

    def __str__(self):
        return self.name


class Profile(models.Model):
    JUN = "J"
    MID = "M"
    SEN = "S"

    LEVEL_OF_OPERATOR = (
        (JUN, "Початковий"),
        (MID, "Середнiй"),
        (SEN, "Старший"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    domain = models.ForeignKey("todo.Domain", related_name="profiles")
    level = models.CharField(max_length=1, choices=LEVEL_OF_OPERATOR, default=JUN)
    is_main_operator = models.BooleanField(default=False)
    type_boiler = models.ManyToManyField(TypeBoiler)

    def __unicode__(self):
        return "%s %s" % (self.user.first_name, self.user.last_name)

    def is_admin(self):
        return self.user == self.domain.admin


class Domain(models.Model):
    name = models.TextField(max_length=140)
    admin = models.ForeignKey(User, null=True, blank=True, related_name="domains")

    def __unicode__(self):
        return self.name


class Todo(models.Model):
    ACTIVE = "A"
    PENDING = "P"
    DONE = "D"
    CANCELLED = "C"

    LOW = "L"
    STANDARD = "S"
    HIGH = "H"

    STATUS = (
        (ACTIVE, "Активна"),
        (PENDING, "Очікує на розгляд"),
        (DONE, "Завершена"),
        (CANCELLED, "Відмінено"),
    )

    PRIORITY = (
        (LOW, "😌 Низький"),
        (STANDARD, "😀 Стандартний"),
        (HIGH, "🔥 Високий"),
    )

    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name="Дошка")
    assignee = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Виконавець",
        related_name='assigned', null=True, blank=True
    )
    assignor = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Створювач",
        related_name='assignor', null=True, blank=True
    )

    title = models.CharField(max_length=140, verbose_name="Титульна завдання")
    task = models.TextField(max_length=255, verbose_name="Умова завдання")
    status = models.CharField(
        max_length=1, choices=STATUS, default=ACTIVE, verbose_name="Статус завдання"
    )
    priority = models.CharField(
        max_length=1, choices=PRIORITY, default=STANDARD, verbose_name="Пріоритет"
    )
    image = models.ImageField(null=True, blank=True, verbose_name="Скрiншот показника")

    # units for dispatcher
    temperature = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Температура котельнi"
    )
    heat_meter = models.IntegerField(
        default=0, null=True, blank=True, verbose_name="Лічильник тепла"
    )
    water_leak = models.BooleanField(default=False, verbose_name="Витік води")
    flooding = models.BooleanField(default=False, verbose_name="Затоплення")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Створена")
    deadline = models.DateField(
        default=timezone.now(), verbose_name="Кінцева дата", blank=True, null=True
    )
    time = models.PositiveSmallIntegerField(
        default=0, verbose_name="Часи на виконання", blank=True, null=True
    )

    def __unicode__(self):
        return self.task


class Review(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    task = models.ForeignKey(Todo, on_delete=models.CASCADE)
    review = models.TextField(max_length=1000)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        domain_name = instance.email.split("@")[1]
        domain, domain_created = Domain.objects.get_or_create(name=domain_name)
        Profile.objects.create(user=instance, domain=domain)

        if domain_created:
            instance.profile.is_approved = True
            instance.profile.save()
            domain.admin = instance
            domain.save()
        else:
            send_mail(
                subject="New registration request",
                body="%s has registered with your domain." % instance.email,
                to=domain.admin.email,
            )


@receiver(post_save, sender=Todo)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        assignor = instance.todo.assignor.email.split("@")[1]
        todo = instance

        if todo:
            body_message = f"""
                   Завдання було виконано співробітником,
                   основна інформація про завдання:
                   пройдено часу: {instance.todo.time};
                   рiзниця мiж пройденим часом та назначеним часом: {instance.todo.time - instance.todo.stock_time};

                   звіт оператора: {instance.todo.report}
                   """

            send_mail(
                subject="New registration request",
                body=body_message,
                to=assignor,
            )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
