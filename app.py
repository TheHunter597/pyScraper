import tkinter as tk
from tkinter import font as tkFont
from utils.create_overlay import create_overlay
from utils.submit_data import submit_data


# Initialize main root
root = tk.Tk()


############
def setup_grid():
    # Create labels for each cell in a 3x3 grid
    for row in range(3):
        for col in range(3):
            label = tk.Label(root, borderwidth=1)
            label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    # Configure row and column weights to make the grid cells expand with the window
    for i in range(3):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)


# Setup the grid with widgets
setup_grid()
############
# Amazon link group
amazon_link_group = tk.Frame(root)

amazon_link_label = tk.Label(
    amazon_link_group,
    text="Amazon link",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
amazon_link_entry = tk.Entry(
    amazon_link_group, width=50, font=("Roboto", 12, tkFont.NORMAL)
)
amazon_link_entry.insert(0, "https://www.amazon.com/s?k=laptop&ref=nb_sb_noss")

amazon_link_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
amazon_link_entry.grid(row=0, column=1, padx=5, pady=5)

############
# Products count group
products_count_group = tk.Frame(root)

products_count_label = tk.Label(
    products_count_group,
    text="Count",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
products_count_entry = tk.Entry(
    products_count_group, width=20, font=("Roboto", 12, tkFont.NORMAL)
)
products_count_entry.insert(0, "10")

products_count_label.grid(row=0, column=0, padx=5, sticky="w")
products_count_entry.grid(row=0, column=1, padx=5)

############
seconds_per_product_group = tk.Frame()
seconds_per_product_label = tk.Label(
    seconds_per_product_group,
    text="Delay",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
seconds_per_product_entry = tk.Entry(
    seconds_per_product_group, width=20, font=("Roboto", 12, tkFont.NORMAL)
)
seconds_per_product_entry.insert(0, "5")
seconds_per_product_label.grid(row=0, column=0, padx=5, sticky="w")
seconds_per_product_entry.grid(row=0, column=1, padx=5)

############
output_file_group = tk.Frame()
output_file_label = tk.Label(
    output_file_group,
    text="Output file",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
output_file_entry = tk.Entry(
    output_file_group, width=20, font=("Roboto", 12, tkFont.NORMAL)
)
output_file_entry.insert(0, "output.json")
output_file_label.grid(row=0, column=0, padx=5, sticky="w")
output_file_entry.grid(row=0, column=1, padx=5)
############
accumulate_and_write_once_group = tk.Frame()
accumulate_and_write_once_label = tk.Label(
    accumulate_and_write_once_group,
    text="AccumulateAndWriteOnce",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
checkbox_var = tk.BooleanVar()
accumulate_and_write_once_entry = tk.Checkbutton(
    accumulate_and_write_once_group,
    width=2,
    font=("Roboto", 12, tkFont.NORMAL),
    variable=checkbox_var,
)

accumulate_and_write_once_label.grid(row=0, column=0, padx=5, sticky="w")
accumulate_and_write_once_entry.grid(row=0, column=1, padx=5)
############
product_must_have_features_group = tk.Frame()
product_must_have_features_label = tk.Label(
    product_must_have_features_group,
    text="Product must have features",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
product_must_have_features_checkbox_var = tk.BooleanVar()
product_must_have_features_entry = tk.Checkbutton(
    product_must_have_features_group,
    width=2,
    font=("Roboto", 12, tkFont.NORMAL),
    variable=product_must_have_features_checkbox_var,
)

product_must_have_features_label.grid(row=0, column=0, padx=5, sticky="w")
product_must_have_features_entry.grid(row=0, column=1, padx=5)

############
product_must_have_reviews_group = tk.Frame()
product_must_have_reviews_label = tk.Label(
    product_must_have_reviews_group,
    text="Product must have reviews",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
product_must_have_reviews_checkbox_var = tk.BooleanVar()
product_must_have_reviews_entry = tk.Checkbutton(
    product_must_have_reviews_group,
    width=2,
    font=("Roboto", 12, tkFont.NORMAL),
    variable=product_must_have_reviews_checkbox_var,
)

product_must_have_reviews_label.grid(row=0, column=0, padx=5, sticky="w")
product_must_have_reviews_entry.grid(row=0, column=1, padx=5)
############
threads_group = tk.Frame()
threads_label = tk.Label(
    threads_group,
    text="How many threads",
    foreground="#022B3A",
    font=("Roboto", 14, "bold"),
)
threads_entry = tk.Entry(threads_group, width=20, font=("Roboto", 12, tkFont.NORMAL))
threads_entry.insert(0, "2")
threads_label.grid(row=0, column=0, padx=5, sticky="w")
threads_entry.grid(row=0, column=1, padx=5)
############
buttons_group = tk.Frame(root)
buttons_group.grid(row=4, column=1, sticky="e")
error_widgets = []
submit_button = tk.Button(
    buttons_group,
    text="Submit",
    font=("Arial", 12),
    command=submit_data(
        root,
        amazon_link_entry,
        products_count_entry,
        seconds_per_product_entry,
        output_file_entry,
        threads_entry,
        checkbox_var,
        product_must_have_features_checkbox_var,
        product_must_have_reviews_checkbox_var,
        error_widgets,
    ),
)
open_overlay_button = tk.Button(
    buttons_group, text="Help", command=create_overlay(root), font=("Arial", 12)
)
############
# Place groups in the main root
amazon_link_group.grid(pady=5, row=1, column=1, sticky="w")
products_count_group.grid(pady=5, row=2, column=1, sticky="w")
seconds_per_product_group.grid(pady=5, row=3, column=1, sticky="w")
output_file_group.grid(pady=5, row=4, column=1, sticky="w")
accumulate_and_write_once_group.grid(pady=5, row=5, column=1, sticky="w")
product_must_have_features_group.grid(pady=5, row=6, column=1, sticky="w")
product_must_have_reviews_group.grid(pady=5, row=7, column=1, sticky="w")
threads_group.grid(pady=5, row=8, column=1, sticky="w")

buttons_group.grid(row=8, column=1, padx=5, pady=5)

submit_button.grid(row=0, column=0, padx=5)
open_overlay_button.grid(row=0, column=1, padx=5)
############
# Run the Tkinter event loop
root.mainloop()
