import tkinter as tk


def create_overlay(root):

    def create():
        # Create a new top-level root (overlay)
        overlay = tk.Toplevel(root)
        overlay.title("Overlay root")

        # Make the overlay root appear in the center of the main root
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        overlay_x = root_x + (root_width // 2) - (600 // 2)
        overlay_y = root_y + (root_height // 2) - (400 // 2)

        overlay.geometry(f"600x500+{overlay_x}+{overlay_y}")

        # Make the overlay non-resizable (optional)
        overlay.resizable(True, True)

        # Add a label to the overlay
        label_text = """

    Amazon url --> result url you want scraped ,for instance, go to amazon search for a laptop ,here I did it and this is the url --> https://www.amazon.com/s?k=laptop&ref=nb_sb_noss, copy the result url, and paste it in the amazon link field.
    -----------------------------------------------------
    Count --> how many products do you want to scrape
    -----------------------------------------------------
    Delay --> how many seconds to wait before scraping the next product (if 10 then 6 products would be scraped per minute , the more delay the less likely amazon would suspect this is a robot)
    -----------------------------------------------------
    AccumulateAndWriteOnce --> if True then the data will be written to a file once all the products have been scraped (faster performance, but if unexpected problem happened data would be lost).
    if False then the data will be written to a file after each product has been scraped (slower performance, if unexpected error happened already written data woulndt be lost).
    -----------------------------------------------------
    Output file --> the file name in which the data will be stored the file would be in json format. All the data exists in the data folder in the same directory.
    -----------------------------------------------------
    Product must have features --> would make sure the products retreived must have features property (would make the search slower if multiple products dont have features)
    """

        label = tk.Label(
            overlay,
            text=label_text,
            font=("Arial", 12),
            wraplength=560,  # Wrap text at 560 pixels
            justify="left",  # Left-align the text
        )
        label.pack(pady=20, padx=20)

        # Add a button to close the overlay
        close_button = tk.Button(overlay, text="Close", command=overlay.destroy)
        close_button.pack(pady=10)

    return create
