import dearpygui.dearpygui as dpg
import math as m

# This code will define a samlpe grid for a bruker AFM automation file

dpg.create_context()

default_x_grid_size = 100
default_y_grid_size = 100
default_x_interval = 10
default_y_interval = 10
default_x_offset = 0
default_y_offset = 0

seriesx = []
seriesy = []
for i in range(default_x_offset, default_x_offset+default_x_grid_size+default_x_interval, default_x_interval):
    for j in range(default_y_offset, default_y_offset+default_y_grid_size+default_y_interval, default_y_interval):
        seriesx.append(i)
        seriesy.append(j)

def update_series():

    # Retrieve the current values of the sliders
    x_grid_size_value = int(dpg.get_value(x_grid_size))
    y_grid_size_value = int(dpg.get_value(y_grid_size))
    x_interval_value = int(dpg.get_value(x_interval))
    y_interval_value = int(dpg.get_value(y_interval))
    x_offset_value = int(dpg.get_value(x_offset))
    y_offset_value = int(dpg.get_value(y_offset))

    newx = []
    newy = []
    for i in range(x_offset_value, x_offset_value+x_grid_size_value+x_interval_value, x_interval_value):
        for j in range(y_offset_value, y_offset_value+y_grid_size_value+y_interval_value, y_interval_value):
            newx.append(i)
            newy.append(j)
    dpg.set_value('series_tag', [newx, newy])

    # Update the number of sampling points dynamically
    num_points = len(range(0, x_grid_size_value, x_interval_value)) * len(range(0, y_grid_size_value, y_interval_value))
    dpg.set_value("num_points_text", f"Number of Sampling Points: {num_points}")

    return zip(newx, newy)


# Callback functions to update sliders from input fields
def update_x_grid_size(sender, app_data):
    dpg.set_value(x_grid_size, app_data)
    update_series()

def update_y_grid_size(sender, app_data):
    dpg.set_value(y_grid_size, app_data)
    update_series()

def update_x_interval(sender, app_data):
    dpg.set_value(x_interval, app_data)
    update_series()

def update_y_interval(sender, app_data):
    dpg.set_value(y_interval, app_data)
    update_series()

def output_program():
    try:
        with open("Sampling Grid.pgm", "x") as f:
            f.write("Version: 1.0")
            for coord in update_series():
                f.write(f"\\X point: {coord[0]*1000}\n")
                f.write(f"\\Y point: {coord[1]*1000}\n")
                f.write(f"\\Z point: {dpg.get_value(default_z)}\n")
                f.write(f"\\Coordinate System: 0\n")
    except:
        with open("Sampling Grid.pgm", "w") as f:
            f.write("Version: 1.0")
            for coord in update_series():
                f.write(f"\\X point: {coord[0]*1000}\n")
                f.write(f"\\Y point: {coord[1]*1000}\n")
                f.write(f"\\Z point: {dpg.get_value(default_z)}\n")
                f.write(f"\\Coordinate System: 0\n")

with dpg.window(label='grid', tag="Primary Window"):
    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            x_grid_size = dpg.add_slider_float(label="x grid size", default_value=default_x_grid_size, callback=update_series)
            x_grid_size_input = dpg.add_input_int(label='set x grid size', default_value=default_x_grid_size, callback=update_x_grid_size, on_enter=True)
            x_offset = dpg.add_input_int(label='set x offset', default_value=default_x_offset, callback=update_series, on_enter=True)
        with dpg.table_row():
            y_grid_size = dpg.add_slider_float(label="y grid size", default_value=default_y_grid_size, callback=update_series)
            y_grid_size_input = dpg.add_input_int(label='set y grid size', default_value=default_y_grid_size, callback=update_y_grid_size, on_enter=True)
            y_offset = dpg.add_input_int(label='set y offset', default_value=default_y_offset, callback=update_series, on_enter=True)
        with dpg.table_row():
            x_interval = dpg.add_slider_float(label="x interval", default_value=default_x_interval, callback=update_series)
            x_interval_input = dpg.add_input_int(label='set x interval', default_value=default_x_interval, callback=update_x_interval, on_enter=True)
            default_z = dpg.add_input_int(label='default z', default_value=-19000)
        with dpg.table_row():
            y_interval = dpg.add_slider_float(label="y interval", default_value=default_y_interval, callback=update_series)
            y_interval_input = dpg.add_input_int(label='set y interval', default_value=default_y_interval, callback=update_y_interval, on_enter=True)
            generate_program = dpg.add_button(label='Generate Program', callback=output_program)

    with dpg.group(width=1000, height=1000):
        with dpg.plot(label="Sample Grid"):
            # optionally create legend
            dpg.add_plot_legend()

            # REQUIRED: create x and y axes
            dpg.add_plot_axis(dpg.mvXAxis, label="x (mm)")
            dpg.add_plot_axis(dpg.mvYAxis, label="y (mm)", tag="y_axis")

            # series belong to a y axis
            dpg.add_scatter_series(seriesx, seriesy, label="grid", parent="y_axis", tag='series_tag')

    with dpg.group(width=100, height=100):
        dpg.add_text(f"Number of Sampling Points: {len(seriesx) * len(seriesy)}", tag="num_points_text")

    print(dpg.get_value(x_grid_size))
    print(dpg.get_value(y_grid_size))
    print(dpg.get_value(x_interval))
    print(dpg.get_value(y_interval))


dpg.create_viewport(title='AFM grid definer', width=1100, height=1200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()