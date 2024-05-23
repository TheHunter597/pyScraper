import tkinter as tk
from tkinter import ttk


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

        overlay.geometry(f"800x400+{overlay_x}+{overlay_y}")

        # Make the overlay resizable
        overlay.resizable(True, True)

        # Create a canvas and a vertical scrollbar for scrolling it
        canvas = tk.Canvas(overlay)
        scrollbar = ttk.Scrollbar(overlay, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configure the scrollbar
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Add a label with your text to the scrollable frame
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
        -----------------------------------------------------
        Product must have reviews --> would make sure the products retreived must have reviews property (would make the search slower if multiple products dont have reviews)
        -----------------------------------------------------
        Threads --> how many threads to use for scraping (the more threads the faster the scraping would be)
        -----------------------------------------------------
        currently you cant use AccumulateAndWriteOnce and more than 1 
        """

        label = tk.Label(
            scrollable_frame,
            text=label_text,
            font=("Arial", 12),
            wraplength=700,  # Wrap text at 700 pixels
            justify="left",  # Left-align the text
        )
        label.pack(pady=20, padx=20)

        # Add a button to close the overlay
        close_button = tk.Button(
            scrollable_frame, text="Close", command=overlay.destroy
        )
        close_button.pack(pady=10)

    return create
