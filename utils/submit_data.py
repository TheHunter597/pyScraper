import json
import subprocess
import tkinter as tk
import os
import json


def is_numeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def submit_data(
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
):

    def submit():
        errors = {}
        amazon_link = amazon_link_entry.get()
        if not amazon_link:
            errors["amazon_link"] = "Amazon link is required"
        elif amazon_link.find("amazon.com") == -1:
            errors["amazon_link"] = "Amazon link is invalid"
        threads = threads_entry.get()
        if not threads:
            errors["threads"] = "Threads is required"
        elif not threads.isdigit():
            errors["threads"] = "Threads must be a number"
        elif os.cpu_count() <= int(threads) + 1:
            errors["threads"] = (
                f"Your system has {os.cpu_count()} threads, you can't use more than {os.cpu_count()-1} threads"
            )
        count = products_count_entry.get()
        if not count:
            errors["count"] = "Count is required"
        elif not count.isdigit():
            errors["count"] = "Count must be a number"
        delay = seconds_per_product_entry.get()
        if not delay:
            errors["delay"] = "Delay is required"
        elif is_numeric(delay) == False:
            errors["delay"] = "Delay must be a number"
        output_file = output_file_entry.get()
        if not output_file:
            errors["output_file"] = "Output file is required"

        for widget in error_widgets:
            widget.destroy()
        error_widgets.clear()

        if errors:
            error_widgets.append(
                tk.Label(
                    root,
                    font=("Arial", 12),
                    text="Please fix the following errors",
                    foreground="red",
                )
            )
            error_widgets[-1].grid(row=10, column=1, padx=5, pady=5)
            for i, (key, value) in enumerate(errors.items()):
                error_widgets.append(
                    tk.Label(
                        root,
                        font=("Arial", 12),
                        text=f"{key}: {value}",
                        foreground="red",
                    )
                )
                error_widgets[-1].grid(row=11 + i, column=1, padx=5, pady=5)
            return
        accumulate_and_write_once = checkbox_var.get()

        with open(
            f"{os.path.dirname(os.path.realpath(__file__))}/http_configs/user_agents.json"
        ) as file:
            user_agents = json.load(file)

        scrapingData = {
            "url": amazon_link,
            "count": int(count),
            "secondsPerProduct": int(delay),
            "outputFile": (
                output_file if output_file.endswith(".json") else output_file + ".json"
            ),
            "accumulateAndWriteOnce": accumulate_and_write_once,
            "mustHaveFeatures": product_must_have_features_checkbox_var.get(),
            "mustHaveReviews": product_must_have_reviews_checkbox_var.get(),
            "threads": int(threads),
            "userAgents": user_agents,
        }
        output_file_dir = f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/scrapingData.json"
        with open(output_file_dir, "w") as file:
            file.write(json.dumps(scrapingData, indent=4))
        output_text_widget = tk.Label(
            root,
            font=("Arial", 12),
            text="Scraping data, result would be saved in data folder",
            foreground="#083D77",
        )
        output_text_widget.grid(row=11, column=1, padx=5, pady=5)

        root.update_idletasks()
        subprocess.run(
            [
                "python",
                "index.py",
            ]
        )
        output_text_widget.destroy()

        done_widget = tk.Label(
            root,
            font=("Arial", 12),
            text="Scraping done, result saved in data folder",
            foreground="green",
        )
        done_widget.grid(row=12, column=1, padx=5, pady=5)

    return submit
