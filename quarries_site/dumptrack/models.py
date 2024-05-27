from django.db import models


class DumpTruck(models.Model):
    board_number = models.CharField(max_length=10, unique=True, verbose_name='Бортовой номер')
    model = models.CharField(max_length=50, verbose_name='Модель самосвала')
    max_capacity = models.FloatField(verbose_name='Максимальная грузоподъемность (тонн)')
    current_load = models.FloatField(verbose_name='Текущая нагрузка (тонн)')
    sio2_content = models.FloatField(verbose_name='Содержание SiO2 (%)')
    fe_content = models.FloatField(verbose_name='Содержание Fe (%)')

    class Meta:
        verbose_name = "Самосвал"
        verbose_name_plural = "Самосвалы"


class Stock(models.Model):
    total_volume = models.FloatField(verbose_name='Текущий объем руды (тонн)')
    sio2_content = models.FloatField(verbose_name='Содержание SiO2 (%)')
    fe_content = models.FloatField(verbose_name='Содержание Fe (%)')
    polygon_wkt = models.TextField(verbose_name="Полигон склада (WKT)")

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"


class UnloadingEvent(models.Model):
    dumptruck = models.ForeignKey(DumpTruck, on_delete=models.CASCADE, verbose_name="Самосвал")
    volume = models.IntegerField(verbose_name="Объем разгрузки (тонн)")
    x = models.FloatField(verbose_name="Координата X")
    y = models.FloatField(verbose_name="Координата Y")
    inside_polygon = models.BooleanField(verbose_name="Попал в полигон")

    class Meta:
        verbose_name = "Событие разгрузки"
        verbose_name_plural = "События разгрузки"
