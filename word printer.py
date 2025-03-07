import os
import re
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
import win32api
import win32print
from tkinter import Toplevel
import zipfile
from xml.dom import minidom
from idlelib.tooltip import Hovertip
import time
from tkinter import messagebox
import ttkbootstrap.tableview as tv
from tkinter import messagebox
from tkinter import Toplevel

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]


def get_word_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".docx")]


def sort_files(files):
    sorted_files = sorted(
        files, key=lambda x: natural_sort_key(os.path.basename(x)))
    return sorted_files


def count_word_pages(doc_path):
    if not os.path.exists(doc_path):
        return None
    document = zipfile.ZipFile(doc_path)
    dxml = document.read('docProps/app.xml')
    try:
        uglyXml = minidom.parseString(dxml)
        page = uglyXml.getElementsByTagName('Pages')[0].childNodes[0].nodeValue
        return int(page)
    except (IndexError, ValueError):
        return None


class PrintQueueApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  
        self.title("Print Queue Preview")
        self.geometry("800x600")
        self.directory = ""
        self.files = []
        self.checkboxes = []
        self.select_all_state = False
        self.create_widgets()

    def create_widgets(self):
        # Directory selection
        self.dir_frame = ttk.Frame(self)
        self.dir_frame.pack(pady=5, fill=tk.X)
        self.dir_entry = ttk.Entry(self.dir_frame, font=("Arial", 12))
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady = 5)
        self.dir_button = ttk.Button(self.dir_frame, text="Browse", command=self.browse_directory, style="primary", cursor="hand2")
        self.dir_button.pack(side=tk.LEFT)
        self.select_all_button = ttk.Button(self.dir_frame, text="View Print Queue", command=self.view_print_queue, cursor="hand2")
        self.select_all_button.pack(side=tk.LEFT, padx=5, pady = 5)
        # File selection
        self.files_frame = ttk.Frame(self, relief=tk.SOLID, borderwidth=2)
        self.files_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.files_canvas = tk.Canvas(self.files_frame)
        self.files_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.files_scrollbar = ttk.Scrollbar(self.files_frame, orient=tk.VERTICAL, command=self.files_canvas.yview)
        self.files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_canvas.configure(yscrollcommand=self.files_scrollbar.set)
        self.files_canvas.bind('<Configure>', lambda e: self.files_canvas.configure(scrollregion=self.files_canvas.bbox("all")))
        self.files_inner_frame = ttk.Frame(self.files_canvas)
        self.files_canvas.create_window((0, 0), window=self.files_inner_frame, anchor="nw")
        self.files_label = ttk.Label(self.files_inner_frame, text="окно выбора файлов для печати", font=("Arial", 12, "bold"), foreground="red")
        self.files_label.grid(row=0, column=0, columnspan=6, pady=5, sticky="ew", padx = 20)
        # Printing options
        self.bottom_frame = ttk.Frame(self)
        self.bottom_frame.pack(pady=10, fill=tk.X)
        self.print_button = ttk.Button(self.bottom_frame, text="Print Selected Files", command=self.print_selected_files, style="primary", cursor="hand2")
        self.print_button.pack(side=tk.LEFT, padx=5)
        self.view_queue_button = ttk.Button(self.bottom_frame, text="Select All", command=self.toggle_select_all, cursor="hand2")
        self.view_queue_button.pack(side=tk.LEFT, padx=5)
        self.printer_label = ttk.Label(self.bottom_frame, text="Printer:", font=("Arial", 12))
        self.printer_label.pack(side=tk.LEFT, padx=5)
        printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL)
        printer_names = [printer[2] for printer in printers]
        self.printer_var = tk.StringVar(value=win32print.GetDefaultPrinter())
        self.printer_menu = tk.Menu(self.bottom_frame, tearoff=0)
        for printer_name in printer_names:
            self.printer_menu.add_radiobutton(label=printer_name, variable=self.printer_var, value=printer_name)
        self.printer_menubutton = ttk.Menubutton(self.bottom_frame, textvariable=self.printer_var, menu=self.printer_menu, style="outline")
        self.printer_menubutton.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.strict_priority = tk.BooleanVar(value=True)
        self.checkbox = ttk.Checkbutton(self.bottom_frame, variable=self.strict_priority)
        self.checkbox.pack(side=tk.LEFT, ipadx=5, ipady=5)
        Hovertip(self.checkbox, text='строгая очередность\nпри отправке на печать\nработает не везде')
    def browse_directory(self):
        self.directory = filedialog.askdirectory()
        if self.directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, self.directory)
            self.update_files_frame()

    def update_files_frame(self):
        # Clear existing checkboxes and labels
        for widget in self.files_inner_frame.winfo_children():
            widget.destroy()
        # Clear the checkboxes list
        self.checkboxes = []
        self.get_and_sort_files()


    def get_and_sort_files(self):
        self.files = sort_files(get_word_files(self.directory))
        self.insert_files_to_frame()

    def insert_files_to_frame(self):
        # Clear existing checkboxes and labels
        for widget in self.files_inner_frame.winfo_children():
            widget.destroy()

        self.checkboxes = []

        for i, file in enumerate(self.files):
            page_count = count_word_pages(file)
            if page_count is not None:
                text = os.path.splitext(os.path.basename(file))[0]
                pages_text = str(page_count)
            else:
                text = f"{os.path.splitext(os.path.basename(file))[0]} (Unknown number of pages)"
                pages_text = ""
            var = tk.BooleanVar()
            checkbox = ttk.Checkbutton(
                self.files_inner_frame, text=text, variable=var, cursor="hand2", width=50)
            Hovertip(checkbox, text="имя файла")
            pages_label = ttk.Label(self.files_inner_frame, text=pages_text, style="inverse")
            Hovertip(pages_label, text="количество страниц в файле")
            up_button = ttk.Button(self.files_inner_frame, text="↑", command=lambda idx=i: self.move_up(idx), cursor="hand2")
            Hovertip(up_button, text="сдвинуть вверх")
            down_button = ttk.Button(self.files_inner_frame, text="↓", command=lambda idx=i: self.move_down(idx), cursor="hand2")
            Hovertip(down_button, text="сдвинуть вниз")
            view_button = ttk.Button(self.files_inner_frame, text="открыть", command=lambda file_path=file: self.open_file(file_path), cursor="hand2")
            Hovertip(view_button, text="открыть файл")
            copies_entry = ttk.Entry(self.files_inner_frame, width=5)
            Hovertip(copies_entry, text="количество копий")
            copies_entry.insert(0, "1")
            checkbox.grid(row=i+1, column=0, sticky="w")
            pages_label.grid(row=i+1, column=1, sticky="e")
            copies_entry.grid(row=i+1, column=2, sticky="e")
            up_button.grid(row=i+1, column=3, sticky="e")
            down_button.grid(row=i+1, column=4, sticky="e")
            view_button.grid(row=i+1, column=5, sticky="e")
            self.checkboxes.append((checkbox, var, pages_label, up_button, down_button, view_button, copies_entry))

    def open_file(self, file_path):
        os.startfile(file_path)

    def move_up(self, index):
        if index > 0:
            self.files[index], self.files[index - 1] = self.files[index - 1], self.files[index]
            self.checkboxes[index], self.checkboxes[index - 1] = self.checkboxes[index - 1], self.checkboxes[index]
            self.update_file_row(index)
            self.update_file_row(index - 1)

    def move_down(self, index):
        if index < len(self.files) - 1:
            self.files[index], self.files[index + 1] = self.files[index + 1], self.files[index]
            self.checkboxes[index], self.checkboxes[index + 1] = self.checkboxes[index + 1], self.checkboxes[index]
            self.update_file_row(index)
            self.update_file_row(index + 1)

    def update_file_row(self, index):
        # text = os.path.splitext(os.path.basename(self.files[index]))[0]
        # page_count = count_word_pages(self.files[index])
        # if page_count is not None:
        #     pages_text = str(page_count)
        # else:
        #     text += " (Unknown number of pages)"
        #     pages_text = ""

        checkbox, _, pages_label, up_button, down_button, view_button, copies_entry = self.checkboxes[index]
        # checkbox.config(text=text, width=40)  # Set the width of the checkbox to 30 characters
        # pages_label.config(text=pages_text)

        checkbox.grid(row=index + 1, column=0, sticky="w")
        pages_label.grid(row=index + 1, column=1, sticky="e")
        copies_entry.grid(row=index + 1, column=2, sticky="e")
        up_button.config(command=lambda idx=index: self.move_up(idx))
        down_button.config(command=lambda idx=index: self.move_down(idx))
        view_button.config(command=lambda file_path=self.files[index]: self.open_file(file_path))
        up_button.grid(row=index + 1, column=3, sticky="e")
        down_button.grid(row=index + 1, column=4, sticky="e")
        view_button.grid(row=index + 1, column=5, sticky="e")


    def toggle_select_all(self):
        self.select_all_state = not self.select_all_state
        for _, var, _, _, _, _, _ in self.checkboxes:
            var.set(self.select_all_state)

    def get_last_job_id(self, printer=win32print.GetDefaultPrinter()):
        printer_handle = win32print.OpenPrinter(printer)
        job_id = win32print.StartDocPrinter(printer_handle, 1, ("Blank Page", '', "RAW"))
        win32print.ClosePrinter(printer_handle)
        self.clear_print_queue(job_id)
        return job_id

    def print_doc(self, file_path, printer):
        f = '"' + file_path + '"'
        win32api.ShellExecute(0, "printto", f, '"%s"' % printer, ".", 0)

    def print_selected_files(self):
        selected_files = [(self.files[i], int(copies_entry.get())) for i, (
            _, var, _, _, _, _, copies_entry) in enumerate(self.checkboxes) if var.get()]
        if selected_files:
            printer = self.printer_var.get()
            files_info = []
            total_pages = 0
            document_counter = self.get_last_job_id(printer)
            for file, copies in selected_files:
                page_count = count_word_pages(file)
                if page_count is not None:
                    files_info.append((os.path.basename(file), page_count, copies))
                    total_pages += page_count * copies
                else:
                    files_info.append((os.path.basename(file), "Unknown", copies))
                for _ in range(copies):
                    self.print_doc(file, printer)
                    if self.strict_priority.get():
                        document_counter += 1
                        while True:
                            jobs = win32print.EnumJobs(win32print.OpenPrinter(printer), 0, -1, 1)
                            if jobs and jobs[-1]['JobId'] == document_counter:
                                break
                            time.sleep(0.1)
            self.show_notification(files_info, total_files=len(selected_files), total_pages=total_pages)
        else:
            messagebox.showerror("Error", "Please select files to print.")

    def show_notification(self, files_info, total_files, total_pages):
        notification = Toplevel(self)
        notification.title("Printing Completed")
        notification.geometry(f"{self.winfo_width()}x{self.winfo_height() // 2}")

        # Create a Treeview widget
        columns = ("No.", "File Name", "Page Count", "Copies")
        tree = ttk.Treeview(notification, columns=columns, show="headings")

        # Define headings
        for col in columns:
            tree.heading(col, text=col)

        # Insert data into Treeview
        for i, file_info in enumerate(files_info, start=1):
            tree.insert("", "end", values=(i, *file_info))

        # Insert total summary row
        tree.insert("", "end", values=("Всего", "", total_pages, ""), tags=('summary',))
        # tree.tag_configure('summary', background='lightgray')

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        summary_label = ttk.Label(notification, text=f"Total files: {total_files}\nTotal pages: {total_pages}", font=("Arial", 12, "bold"))
        summary_label.pack(pady=10)

        close_button = ttk.Button(notification, text="Close", command=notification.destroy, style="success", cursor="hand2")
        close_button.pack(pady=5)

        notification.grab_set()

        # notification.after(5000, notification.destroy)
    def view_print_queue(self):
        queue_window = Toplevel(self)
        queue_window.title("Print Queue")
        queue_window.geometry(f"{self.winfo_width()}x{self.winfo_height() // 2}")

        # Create a new frame for the buttons
        buttons_frame = ttk.Frame(queue_window)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        clear_button = ttk.Button(buttons_frame, text="Clear Print Queue", command=self.clear_print_queue, cursor="hand2")
        clear_button.pack(side=tk.LEFT, padx=5)

        refresh_button = ttk.Button(buttons_frame, text="Refresh", command=self.update_print_queue, cursor="hand2")
        refresh_button.pack(side=tk.LEFT, padx=5)

        self.queue_listbox = tk.Listbox(queue_window, font=("Arial", 10))
        self.queue_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.queue_listbox.bind("<Double-Button-1>", self.on_double_click)

        self.update_print_queue()



    def on_double_click(self, event):
        selected_index = self.queue_listbox.curselection()
        if selected_index:
            selected_job = self.queue_listbox.get(selected_index)
            if "Job ID:" in selected_job:
                job_id = int(selected_job.split(",")[0].split(":")[1].strip())
                self.clear_print_queue(job_id)
                self.update_print_queue()

    def update_print_queue(self):
        self.queue_listbox.delete(0, tk.END)
        default_printer = win32print.GetDefaultPrinter()
        jobs = win32print.EnumJobs(win32print.OpenPrinter(default_printer), 0, -1, 1)
        if jobs:
            for job in jobs:
                document = job.get('pDocument', 'Unknown')
                self.queue_listbox.insert(tk.END, f"Job ID: {job['JobId']}, Document: {document}")
                # self.queue_listbox.insert(tk.END, "")
        else:
            self.queue_listbox.insert(tk.END, "No jobs in the print queue.")

    def clear_print_queue(self, job_id=None):
        default_printer = win32print.GetDefaultPrinter()
        jobs = win32print.EnumJobs(win32print.OpenPrinter(default_printer), 0, -1, 1)
        if jobs:
            if job_id is None:
                # Clear the entire print queue
                for job in jobs:
                    win32print.SetJob(win32print.OpenPrinter(default_printer), job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)
                self.queue_listbox.delete(0, tk.END)
                self.queue_listbox.insert(tk.END, "Print queue cleared.")
            else:
                # print(job_id, jobs)
                # Delete the specified job from the print queue
                for job in jobs:
                    if job['JobId'] == job_id:
                        win32print.SetJob(win32print.OpenPrinter(default_printer), job['JobId'], 0, None, win32print.JOB_CONTROL_DELETE)
                        return
                else:
                    self.queue_listbox.insert(tk.END, f"Job with ID {job_id} not found in print queue.")
        else:
            self.queue_listbox.insert(tk.END, "No jobs in the print queue.")

if __name__ == "__main__":
    app = PrintQueueApp()
    app.mainloop()