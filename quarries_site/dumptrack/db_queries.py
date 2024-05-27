def update_stock_fields(
        current_stock,
        new_pre_unloading_volume: float,
        new_after_unloading_volume: float,
        new_sio2_content: float,
        new_fe_content: float,
):

    current_stock.pre_unloading_volume = new_pre_unloading_volume
    current_stock.after_unloading_volume = new_after_unloading_volume
    current_stock.sio2_content = new_sio2_content
    current_stock.fe_content = new_fe_content
    current_stock.save()
