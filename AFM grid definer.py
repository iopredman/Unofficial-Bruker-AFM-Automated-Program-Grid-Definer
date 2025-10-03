import dearpygui.dearpygui as dpg, os

def update_series():
    x_size, y_size = int(dpg.get_value(x_grid_size)), int(dpg.get_value(y_grid_size))
    x_int, y_int = int(dpg.get_value(x_interval)), int(dpg.get_value(y_interval))
    x_off, y_off = int(dpg.get_value(x_offset)), int(dpg.get_value(y_offset))
    x_dir, y_dir = {'Top Right': (1, 1), 'Top Left': (-1, 1), 
                    'Bottom Left': (-1, -1), 'Bottom Right': (1, -1)}[dpg.get_value('quadrant')]
    newx, newy = zip(*[(x_dir * i, y_dir * j) 
                       for i in range(x_off, x_off + x_size + x_int, x_int) 
                       for j in range(y_off, y_off + y_size + y_int, y_int)])
    dpg.set_value('series_tag', [newx, newy])
    dpg.set_value("num_points_text", f"Number of Sampling Points: {len(newx)}")
    return zip(newx, newy)

def update_value(sender, app_data, user_data):
    dpg.set_value(user_data, app_data)
    update_series()

def output_program(sender, app_data, user_data):
    mode = "x" if not os.path.exists(f'{file_name}.pgm') else "w"
    with open(f'{file_name}.pgm', mode) as f:
        f.write("Version: 1.0")
        f.writelines(f"\\X point: {coord[0]*1000}\n\\Y point: {coord[1]*1000}\n\\Z point: {dpg.get_value(default_z)}\n\\Coordinate System: 0\n" for coord in update_series())

# def save_file_callback(sender, app_data, user_data):
#     if app_data:
#         file_path = app_data['file_path_name']

#         print(f"File saved to: {file_path}")

# def show_save_dialog_callback():
#     dpg.show_item(FILE_DIALOG_TAG)

if __name__ == "__main__":
    dpg.create_context()
    FILE_DIALOG_TAG = "file_dialog_tag"
    TEXT_EDITOR_TAG = "text_editor_tag"
    file_name, quadrants = 'deafult_sampling_grid', ['Top Right', 'Top Left', 'Bottom Left', 'Bottom Right']
    defaults = {'x_size': 100, 'y_size': 100, 'x_int': 10, 'y_int': 10, 'x_off': 0, 'y_off': 0, 'z': -19000}
    newx, newy = zip(*[(i, j) 
                       for i in range(defaults['x_off'], defaults['x_off'] + defaults['x_size'] + defaults['x_int'], defaults['x_int']) 
                       for j in range(defaults['y_off'], defaults['y_off'] + defaults['y_size'] + defaults['y_int'], defaults['y_int'])])

    with dpg.viewport_menu_bar():
        with dpg.menu(label="File"):
            dpg.add_menu_item(label="Save Program", callback=output_program)
            dpg.add_menu_item(label="Save Program As", callback=output_program)
    
    # with dpg.file_dialog(directory_selector=False,show=False,callback=save_file_callback,tag=FILE_DIALOG_TAG,width=700,height=400,default_path=".", file_extensions=[".pgm", ".*"]):
    #     pass

    with dpg.window(label='grid', tag="Primary Window"):
        with dpg.table(header_row=False):
            dpg.add_table_column(), dpg.add_table_column(), dpg.add_table_column()
            with dpg.table_row():
                x_grid_size = dpg.add_slider_float(label="x grid size", default_value=defaults['x_size'], callback=update_series)
                x_grid_size_input = dpg.add_input_int(label='set x grid size', default_value=defaults['x_size'], callback=update_value, on_enter=True, user_data=x_grid_size)
                x_offset = dpg.add_input_int(label='set x offset', default_value=defaults['x_off'], callback=update_series, on_enter=True)
            with dpg.table_row():
                y_grid_size = dpg.add_slider_float(label="y grid size", default_value=defaults['y_size'], callback=update_series)
                y_grid_size_input = dpg.add_input_int(label='set y grid size', default_value=defaults['y_size'], callback=update_value, on_enter=True, user_data=y_grid_size)
                y_offset = dpg.add_input_int(label='set y offset', default_value=defaults['y_off'], callback=update_series, on_enter=True)
            with dpg.table_row():
                x_interval = dpg.add_slider_float(label="x interval", default_value=defaults['x_int'], callback=update_series)
                x_interval_input = dpg.add_input_int(label='set x interval', default_value=defaults['x_int'], callback=update_value, on_enter=True, user_data=x_interval)
                default_z = dpg.add_input_int(label='default z', default_value=-19000)
            with dpg.table_row():
                y_interval = dpg.add_slider_float(label="y interval", default_value=defaults['y_int'], callback=update_series)
                y_interval_input = dpg.add_input_int(label='set y interval', default_value=defaults['y_int'], callback=update_value, on_enter=True, user_data=y_interval)
                quadrant = dpg.add_combo(items=quadrants, label='Sampling quadrant', default_value='Top Right', callback=update_series, tag='quadrant')

        with dpg.group(width=1070, height=1000):
            with dpg.plot(label="Sample Grid"):
                dpg.add_plot_legend()
                dpg.add_plot_axis(dpg.mvXAxis, label="x (mm)")
                dpg.add_plot_axis(dpg.mvYAxis, label="y (mm)", tag="y_axis")
                dpg.add_scatter_series(newx, newy, label="grid", parent="y_axis", tag='series_tag')

        with dpg.group(width=100, height=100):
            dpg.add_text(f"Number of Sampling Points: {len(newx)}", tag="num_points_text")

    dpg.create_viewport(title='AFM grid definer', width=1100, height=1250)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()