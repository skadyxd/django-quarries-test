from django.shortcuts import render, redirect
from .models import DumpTruck, Stock, UnloadingEvent
from .calculations import is_point_in_polygon, overload_calculation, calculate_new_stock_concentration
from .db_queries import update_stock_fields


def reset_data(request):
    # Удаляем все события разгрузки
    UnloadingEvent.objects.all().delete()

    # Сбрасываем данные склада к значениям по умолчанию
    stock = Stock.objects.first()
    stock.total_volume = 900
    stock.sio2_content = 34.0
    stock.fe_content = 65.0
    stock.save()

    return redirect('index')


def index(request):
    dump_trucks = DumpTruck.objects.all()
    stock = Stock.objects.first()
    unloading_events = UnloadingEvent.objects.all()

    # Список для хранения информации о самосвалах вместе с перегрузом
    dump_trucks_with_overload = []

    unloading_list = []

    list_of_sio2_contents = []
    list_of_fe_contents = []

    for dump_truck in dump_trucks:
        overload = overload_calculation(dump_truck.max_capacity, dump_truck.current_load)

        dump_trucks_with_overload.append({
            'dump_truck': dump_truck,
            'overload': overload
        })

    if request.method == "POST":
        for dump_truck in dump_trucks:
            coord = request.POST.get(f'coord_{dump_truck.id}')
            if coord:

                x, y = map(float, coord.split())
                inside_polygon = is_point_in_polygon(x, y, stock.polygon_wkt)

                if inside_polygon:
                    # Если попали в полигон, тогда сохраняем данные самосвала
                    unloading_list.append(dump_truck.current_load)
                    list_of_sio2_contents.append(dump_truck.sio2_content)
                    list_of_fe_contents.append(dump_truck.fe_content)

                UnloadingEvent.objects.create(
                    dumptruck=dump_truck,
                    stock=stock,  # добавляем ссылку на склад
                    volume=dump_truck.current_load,
                    inside_polygon=inside_polygon,
                    x=x,
                    y=y
                )

        if len(unloading_list) > 0:
            stock_sio2_content_after_unloading, stock_fe_content_after_unloading = (
                calculate_new_stock_concentration(stock, unloading_list, list_of_sio2_contents, list_of_fe_contents))

            update_stock_fields(
                current_stock=stock,
                new_pre_unloading_volume=stock.after_unloading_volume,
                new_after_unloading_volume=stock.after_unloading_volume + sum(unloading_list),
                new_sio2_content=stock_sio2_content_after_unloading,
                new_fe_content=stock_fe_content_after_unloading
            )

        return redirect('index')

    return render(request, 'dumptrack/index.html', {
        'dump_trucks_with_overload': dump_trucks_with_overload,
        'stock': stock,
        'unloading_events': unloading_events
    })
