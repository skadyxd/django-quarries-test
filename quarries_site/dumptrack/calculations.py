from shapely.wkt import loads
from shapely.geometry import Point


def is_point_in_polygon(x, y, polygon_wkt) -> bool:
    """
    Функция для определения, попали ли координаты точки разгрузки внутрь полигона.

    :param x: Координата разгрузки x
    :param y: Координата разгрузки y
    :param polygon_wkt: Полигон в представлении WKT.
    :return: Возвращает True, если точка находится внутри полигона, иначе False
    """

    polygon = loads(polygon_wkt)
    point = Point(x, y)

    return polygon.contains(point)


def overload_calculation(max_capacity, current_capacity):
    """
    Функция рассчитывает на основе максимальной грузоподъемности и текущей, имеется ли перегруз

    :param max_capacity: Максимальная грузоподъемность
    :param current_capacity: Текущая грузоподъемность
    :return: Значение перегруза в процентах (%)
    """

    if max_capacity >= current_capacity:
        return 0
    else:
        return ((current_capacity - max_capacity) / max_capacity) * 100


def calculate_new_stock_concentration(
        current_stock,
        new_unloading_list: list,
        new_list_of_sio2_contents: list,
        new_list_of_fe_contents: list
) -> tuple[float, float]:
    """
    Функция для расчета нового значения качественной характеристики после разгрузки, на основе разгруженной руды и её содержаний SiO2 и Fe

    :param current_stock: Склад, на который прибыла разгрузка
    :param new_unloading_list: Список прибывших разгрузок (тонн)
    :param new_list_of_sio2_contents: Список содержаний SiO2
    :param new_list_of_fe_contents:   Список содержаний Fe
    :return:
    """
    pre_unloading_volume = current_stock.pre_unloading_volume  # Объем руды до пополнения руды
    stock_sio2_content_before_unloading = current_stock.sio2_content  # Содержание SiO2 до пополнения руды
    stock_fe_content_before_unloading = current_stock.fe_content      # Содержание Fe до пополнения руды

    sum_of_unloading = sum(new_unloading_list)  # сумма в тоннах привезенного

    after_unloading_volume = pre_unloading_volume + sum_of_unloading  # Сумма руды в тоннах после разгрузки

    sum_of_products_sio2 = 0  # сумма произведений привезенной руды на процент SiO2
    sum_of_products_fe = 0  # сумма произведений привезенной руды на процент Fe

    # Рассчитываем суммы произведений руды на процент (SiO2 и Fe)
    for i, current_unloading in enumerate(new_unloading_list):
        sum_of_products_sio2 += current_unloading * new_list_of_sio2_contents[i]
        sum_of_products_fe += current_unloading * new_list_of_fe_contents[i]

    # Характеристика SiO2
    stock_sio2_content_after_unloading = (pre_unloading_volume * stock_sio2_content_before_unloading + sum_of_products_sio2) / after_unloading_volume

    # Характеристика Fe
    stock_fe_content_after_unloading = (pre_unloading_volume * stock_fe_content_before_unloading + sum_of_products_fe) / after_unloading_volume

    return stock_sio2_content_after_unloading, stock_fe_content_after_unloading

