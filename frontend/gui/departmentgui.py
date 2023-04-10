# Department GUI: implement add department, remove department, update department, view department, view all departments and back

class DepartmentGUI:
    def __init__(self, company: Company, frame: Frame):
        self.__company = company
        self.__frame = frame
        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__input_fields = [
            ("Enter department name: ", self.__set_name),
            ("Enter department ID: ", self.__set_id),
        ]

        self.__input_entries = []
        for prompt, _ in self.__input_fields:
            entry = Entry(self.__frame)
            entry.pack(fill=X, expand=True)
            self.__input_entries.append(entry)

        self.__buttons = []
        for text, command in [
            ("Add", self.__add_department),
            ("Remove", self.__remove_department),
            ("Update", self.__update_department),
            ("View", self.__view_department),
            ("View All", self.__view_all_departments),
            ("Back", self.__back),
        ]:
            button = Button(self.__frame, text=text, command=command)
            button.pack(fill=X, expand=True)
            self.__buttons.append(button)

    def __set_name(self, name: str) -> None:
        self.__name = name

    def __set_id(self, id: str) -> None:
        self.__id = id

    def __add_department(self) -> None:
        for entry, (prompt, setter) in zip(self.__input_entries, self.__input_fields):
            try:
                setter(entry.get())
            except ValueError:
                self.__last_msg = f"Invalid input for {prompt}"
                self.__last_msg_label["text"] = self.__last_msg
                return

        department = Department()
        department.set_name(self.__name)
        department.set_id(self.__id)
        self.__company.departments.append(department)

        self.__last_msg = "Department added!"
        self.__last_msg_label["text"] = self.__last_msg

    def __remove_department(self) -> None:
        pass

    def __update_department(self) -> None:
        pass

    def __view_department(self) -> None:
        pass

    def __view_all_departments(self) -> None:
        pass

    def __back(self) -> None:
        pass

    def __apply(self) -> None:
        pass