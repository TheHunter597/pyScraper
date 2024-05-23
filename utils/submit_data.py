import json
import subprocess
import tkinter as tk
import os


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

        # if int(threads) > 1 and checkbox_var.get() == True:
        #     errors["accumulateAndWriteOnce"] = (
        #         "You can't use accumulate and write once with more than 1 thread"
        #     )

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
            "userAgents": [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Safari/605.1.15",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1 Mobile/15E148 Safari/604.1",
                "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
                "Mozilla/5.0 (Android 10; Mobile; rv:88.0) Gecko/88.0 Firefox/88.0",
            ],
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
        done_widget.grid(row=11, column=1, padx=5, pady=5)

    return submit
