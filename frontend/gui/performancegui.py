import customtkinter as ctk
import tkinter

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

Width = 1024
Height = 768


class PerformanceGui(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("Performance Management System")
        self.geometry(f"{Width}x{Height}")
        self.resizable(True, True)

        def entry_size(entry):
            entry.configure(
                width=400, height=30, font=("Century Gothic", 14), corner_radius=10
            )

        def add_sale(self):
            self.button1_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button1_frame,
                text="Information",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.label1 = ctk.CTkLabel(
                master=self.right_frame,
                text="ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label1.place(relx=0.1, rely=0.15, anchor=tkinter.CENTER)

            self.entry1 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter ID"
            )
            entry_size(self.entry1)
            self.entry1.place(relx=0.325, rely=0.195, anchor=tkinter.CENTER)

            self.label2 = ctk.CTkLabel(
                master=self.right_frame,
                text="Revenue: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label2.place(relx=0.1, rely=0.25, anchor=tkinter.CENTER)

            self.entry2 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter revenue"
            )
            entry_size(self.entry2)
            self.entry2.place(relx=0.325, rely=0.295, anchor=tkinter.CENTER)

            self.label3 = ctk.CTkLabel(
                master=self.right_frame,
                text="Cost: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label3.place(relx=0.1, rely=0.35, anchor=tkinter.CENTER)

            self.entry3 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter cost"
            )
            entry_size(self.entry3)
            self.entry3.place(relx=0.325, rely=0.395, anchor=tkinter.CENTER)

            self.label4 = ctk.CTkLabel(
                master=self.right_frame,
                text="Profit: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label4.place(relx=0.1, rely=0.45, anchor=tkinter.CENTER)

            self.entry4 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter profit"
            )
            entry_size(self.entry4)
            self.entry4.place(relx=0.325, rely=0.495, anchor=tkinter.CENTER)

            self.label5 = ctk.CTkLabel(
                master=self.right_frame,
                text="Client ID: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label5.place(relx=0.1, rely=0.55, anchor=tkinter.CENTER)

            self.entry5 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter client ID"
            )
            entry_size(self.entry5)
            self.entry5.place(relx=0.325, rely=0.595, anchor=tkinter.CENTER)

            self.label6 = ctk.CTkLabel(
                master=self.right_frame,
                text="Client rating: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label6.place(relx=0.1, rely=0.65, anchor=tkinter.CENTER)

            self.entry6 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter client rating"
            )
            entry_size(self.entry6)
            self.entry6.place(relx=0.325, rely=0.695, anchor=tkinter.CENTER)

            self.label7 = ctk.CTkLabel(
                master=self.right_frame,
                text="Client comment: ",
                font=("Century Gothic", 20, "italic"),
            )
            self.label7.place(relx=0.1, rely=0.75, anchor=tkinter.CENTER)

            self.entry7 = ctk.CTkEntry(
                master=self.right_frame, placeholder_text="Enter client comment"
            )
            entry_size(self.entry7)
            self.entry7.place(relx=0.325, rely=0.795, anchor=tkinter.CENTER)

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Confirm",
                command=(lambda: add_successfully(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            self.button1_frame.pack(pady=20)

        def view_sales_performance(self):
            self.button2_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button2_frame,
                text="Sales performance",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="View",
                font=("Century Gothic", 20, "bold"),
                command=(lambda: view_sales_performance(self)),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            self.button2_frame.pack(pady=20)

        def remove_sale(self):
            self.button3_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button3_frame,
                text="Remove sale",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Remove sale",
                font=("Century Gothic", 20, "bold"),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            self.button3_frame.pack(pady=20)

        def get_sale_info(self):
            self.button4_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button4_frame,
                text="Get sale info",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Get sale info",
                font=("Century Gothic", 20, "bold"),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            self.button4_frame.pack(pady=20)

        def find_sale_by(self):
            self.button5_frame = ctk.CTkFrame(master=self.right_frame)

            self.label = ctk.CTkLabel(
                master=self.button5_frame,
                text="Find sale by",
                font=("Century Gothic", 30, "bold"),
            )
            self.label.pack()

            self.button = ctk.CTkButton(
                master=self.right_frame,
                text="Find",
                font=("Century Gothic", 20, "bold"),
            )
            self.button.configure(
                width=100,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
                fg_color="purple",
            )
            self.button.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

            self.button5_frame.pack(pady=20)

        # Destroy all frames
        def destroy_all_frames(self):
            for widget in self.right_frame.winfo_children():
                widget.destroy()

        self.left_frame = ctk.CTkFrame(master=self, corner_radius=10)

        def button_size(button):
            button.configure(
                width=260,
                height=40,
                font=("Century Gothic", 15, "bold"),
                corner_radius=10,
            )

        self.button1 = ctk.CTkButton(
            master=self.left_frame,
            text="Add Sale",
            command=(lambda: [destroy_all_frames(self), add_sale(self)]),
        )
        button_size(self.button1)
        self.button1.place(relx=0.5, rely=0.15, anchor=tkinter.CENTER)

        self.button2 = ctk.CTkButton(
            master=self.left_frame,
            text="View Sales Performance",
            command=(lambda: [destroy_all_frames(self), view_sales_performance(self)]),
        )
        button_size(self.button2)
        self.button2.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)

        self.button3 = ctk.CTkButton(
            master=self.left_frame,
            text="Remove Sale",
            command=(lambda: [destroy_all_frames(self), remove_sale(self)]),
        )
        button_size(self.button3)
        self.button3.place(relx=0.5, rely=0.35, anchor=tkinter.CENTER)

        self.button4 = ctk.CTkButton(
            master=self.left_frame,
            text="Get Sale Info",
            command=(lambda: [destroy_all_frames(self), get_sale_info(self)]),
        )
        button_size(self.button4)
        self.button4.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.button5 = ctk.CTkButton(
            master=self.left_frame,
            text="Find Sale By",
            command=(lambda: [destroy_all_frames(self), find_sale_by(self)]),
        )
        button_size(self.button5)
        self.button5.place(relx=0.5, rely=0.55, anchor=tkinter.CENTER)

        self.button6 = ctk.CTkButton(
            master=self.left_frame,
            text="Back",
            fg_color="red",
            command=(lambda: self.back_to_homepage()),
        )
        self.button6.configure(
            width=100,
            height=40,
            font=("Century Gothic", 15, "bold"),
            corner_radius=10,
            fg_color="red",
        )
        self.button6.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)

        self.left_frame.pack(side=ctk.LEFT)
        self.left_frame.pack_propagate(False)
        self.left_frame.configure(width=320, height=760)

        self.right_frame = ctk.CTkFrame(master=self, border_width=2, corner_radius=10)
        self.right_frame.pack(side=ctk.RIGHT)
        self.right_frame.pack_propagate(False)
        self.right_frame.configure(width=700, height=760)

    def back_to_homepage(self):
        import homepage

        self.destroy()
        homepage.homepage().mainloop()


if __name__ == "__main__":
    app = PerformanceGui()
    app.mainloop()
