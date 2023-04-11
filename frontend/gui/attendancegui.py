# Attendance GUI: implement check attendance, upadtea attendance, get attendance report and exit

class AttendanceGUI:
    def __init__(self, employee: Employee, frame: Frame):
        self.__employee = employee
        self.__frame = frame  
        self.__last_msg = ""
        self.__last_msg_label = Label(self.__frame, text=self.__last_msg)
        self.__last_msg_label.pack()

        self.__input_fields = [
            ("Enter attendance date: ", self.__set_date),
            ("Enter attendance time: ", self.__set_time),
            ("Enter attendance status: ", self.__set_status),
        ]

        self.__input_entries = []
        for prompt, _ in self.__input_fields:
            entry = Entry(self.__frame)
            entry.pack(fill=X, expand=True)
            self.__input_entries.append(entry)

        self.__buttons = []
        for text, command in [
            ("Check Attendance", self.__check_attendance),
            ("Update Attendance", self.__update_attendance),
            ("Get Attendance Report", self.__get_attendance_report),
            ("Exit", self.__exit),
        ]:
            button = Button(self.__frame, text=text, command=command)
            button.pack(fill=X, expand=True)
            self.__buttons.append(button)

    def __set_date(self, date: str) -> None:
        self.__date = date

    def __set_time(self, time: str) -> None:
        self.__time = time

    def __set_status(self, status: str) -> None:
        self.__status = status

    def __check_attendance(self) -> None:
        self.__employee.check_attendance(self.__date, self.__time, self.__status)
        self.__last_msg = "Attendance checked"
        self.__last_msg_label.config(text=self.__last_msg)

    def __update_attendance(self) -> None:
        self.__employee.update_attendance(self.__date, self.__time, self.__status)
        self.__last_msg = "Attendance updated"
        self.__last_msg_label.config(text=self.__last_msg)

    def __get_attendance_report(self) -> None:
        self.__employee.get_attendance_report(self.__date, self.__time, self.__status)
        self.__last_msg = "Attendance report generated"
        self.__last_msg_label.config(text=self.__last_msg)

    def __exit(self) -> None:
        self.__frame.destroy() 

        
