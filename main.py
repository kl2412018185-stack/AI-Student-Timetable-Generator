# ==========================================================
# AI STUDENT TIMETABLE GENERATOR
# MODERN GUI APPLICATION
# ==========================================================

import tkinter as tk
from tkinter import messagebox

from csp_solver import solve_timetable


# ==========================================================
# THEME
# ==========================================================

BG = "#F4F7FB"
NAVY = "#102A43"
BLUE = "#1F6FEB"
LIGHT_BLUE = "#EAF2FF"
WHITE = "#FFFFFF"
TEXT = "#243B53"
MUTED = "#627D98"
BORDER = "#D9E2EC"
GREEN = "#16855B"
LIGHT_GREEN = "#E8F7F0"
RED = "#C0392B"
LIGHT_RED = "#FDECEC"

FONT = "Segoe UI"


# ==========================================================
# MAIN WINDOW
# ==========================================================

window = tk.Tk()
window.title("AI Student Timetable Generator")
window.geometry("1100x650")
window.resizable(False, False)
window.configure(bg=BG)


# ==========================================================
# GLOBAL DATA
# ==========================================================

subjects_data = []
time_data = []

subject_count = 3

preferences_data = {
    "preferred_day": "Any",
    "preferred_period": "Any",
    "avoid_friday": False
}


TIME_SLOTS = [
    "Monday 8:00 AM - 10:00 AM",
    "Monday 10:00 AM - 12:00 PM",
    "Monday 2:00 PM - 4:00 PM",
    "Tuesday 8:00 AM - 10:00 AM",
    "Tuesday 10:00 AM - 12:00 PM",
    "Tuesday 2:00 PM - 4:00 PM",
    "Wednesday 8:00 AM - 10:00 AM",
    "Wednesday 10:00 AM - 12:00 PM",
    "Wednesday 2:00 PM - 4:00 PM",
    "Thursday 8:00 AM - 10:00 AM",
    "Thursday 10:00 AM - 12:00 PM",
    "Thursday 2:00 PM - 4:00 PM",
    "Friday 8:00 AM - 10:00 AM",
    "Friday 10:00 AM - 12:00 PM",
    "Friday 2:00 PM - 4:00 PM"
]


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def clear_window():
    for widget in window.winfo_children():
        widget.destroy()


def make_button(parent, text, command, primary=True, width=18):
    bg = BLUE if primary else WHITE
    fg = WHITE if primary else NAVY
    active = "#1558B0" if primary else LIGHT_BLUE

    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=(FONT, 10, "bold"),
        width=width,
        height=2,
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg if primary else NAVY,
        relief="flat",
        bd=0,
        cursor="hand2"
    )
    return button


def add_header(title, subtitle, step):
    header = tk.Frame(window, bg=NAVY, height=105)
    header.pack(fill="x")
    header.pack_propagate(False)

    left = tk.Frame(header, bg=NAVY)
    left.pack(side="left", padx=38, pady=20)

    tk.Label(
        left,
        text="AI TIMETABLE",
        font=(FONT, 9, "bold"),
        fg="#9CC4FF",
        bg=NAVY
    ).pack(anchor="w")

    tk.Label(
        left,
        text=title,
        font=(FONT, 23, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(anchor="w")

    tk.Label(
        left,
        text=subtitle,
        font=(FONT, 9),
        fg="#D9E8FA",
        bg=NAVY
    ).pack(anchor="w", pady=(2, 0))

    tk.Label(
        header,
        text=f"STEP {step} / 4",
        font=(FONT, 10, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(side="right", padx=40)


def add_footer():
    tk.Label(
        window,
        text="CSP  •  Backtracking  •  Preference Optimization  •  Logical Reasoning",
        font=(FONT, 8),
        fg=MUTED,
        bg=BG
    ).pack(side="bottom", pady=12)


def card(parent, padx=22, pady=18):
    frame = tk.Frame(
        parent,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    frame.pack(padx=padx, pady=pady, fill="x")
    return frame


# ==========================================================
# HOME PAGE
# ==========================================================

def show_home_page():
    clear_window()
    window.geometry("1100x650")

    top = tk.Frame(window, bg=NAVY, height=185)
    top.pack(fill="x")
    top.pack_propagate(False)

    tk.Label(
        top,
        text="✦  AI STUDENT TIMETABLE GENERATOR",
        font=(FONT, 24, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(pady=(42, 8))

    tk.Label(
        top,
        text="Smart scheduling powered by Constraint Satisfaction & Backtracking",
        font=(FONT, 11),
        fg="#D9E8FA",
        bg=NAVY
    ).pack()

    body = tk.Frame(window, bg=BG)
    body.pack(fill="both", expand=True)

    intro = tk.Frame(body, bg=BG)
    intro.pack(pady=(35, 10))

    tk.Label(
        intro,
        text="Build your timetable smarter.",
        font=(FONT, 20, "bold"),
        fg=TEXT,
        bg=BG
    ).pack()

    tk.Label(
        intro,
        text="Enter your subjects and preferences. The AI will search for the best valid schedule.",
        font=(FONT, 10),
        fg=MUTED,
        bg=BG
    ).pack(pady=6)

    selection = card(body, padx=260, pady=18)

    tk.Label(
        selection,
        text="NUMBER OF SUBJECTS",
        font=(FONT, 9, "bold"),
        fg=MUTED,
        bg=WHITE
    ).pack(anchor="w")

    row = tk.Frame(selection, bg=WHITE)
    row.pack(fill="x", pady=(7, 0))

    subject_count_variable = tk.StringVar(value="3")

    menu = tk.OptionMenu(
        row,
        subject_count_variable,
        "3", "4", "5"
    )
    menu.config(
        font=(FONT, 11, "bold"),
        bg=LIGHT_BLUE,
        fg=NAVY,
        activebackground=LIGHT_BLUE,
        activeforeground=NAVY,
        relief="flat",
        bd=0,
        width=12
    )
    menu["menu"].config(font=(FONT, 10))
    menu.pack(side="left")

    def start_system():
        global subject_count
        subject_count = int(subject_count_variable.get())
        show_subject_page()

    make_button(
        row,
        "GET STARTED  →",
        start_system,
        primary=True,
        width=18
    ).pack(side="right")

    features = tk.Frame(body, bg=BG)
    features.pack(pady=10)

    items = [
        ("01", "Define Subjects", "Add subject, lecturer, room and class type."),
        ("02", "Set Time Slots", "Choose three possible slots for each subject."),
        ("03", "Set Preferences", "Tell the AI your preferred scheduling options.")
    ]

    for number, title, desc in items:
        f = tk.Frame(features, bg=WHITE, width=250, height=105,
                     highlightbackground=BORDER, highlightthickness=1)
        f.pack_propagate(False)
        f.pack(side="left", padx=7)

        tk.Label(
            f, text=number, font=(FONT, 9, "bold"),
            fg=BLUE, bg=WHITE
        ).pack(anchor="w", padx=16, pady=(12, 2))

        tk.Label(
            f, text=title, font=(FONT, 10, "bold"),
            fg=TEXT, bg=WHITE
        ).pack(anchor="w", padx=16)

        tk.Label(
            f, text=desc, font=(FONT, 8),
            fg=MUTED, bg=WHITE,
            wraplength=215, justify="left"
        ).pack(anchor="w", padx=16, pady=3)

    add_footer()


# ==========================================================
# SUBJECT PAGE
# ==========================================================

def show_subject_page():
    clear_window()
    window.geometry("1100x650")

    add_header(
        "Subject Information",
        f"Enter the details for your {subject_count} subjects.",
        1
    )

    # ======================================================
    # FULL-WIDTH SUBJECT TABLE
    # ======================================================

    content = tk.Frame(window, bg=BG)
    content.pack(fill="x", padx=45, pady=(20, 5))

    table = tk.Frame(
        content,
        bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table.pack(fill="x")

    # Use proportional grid columns so the table fills the
    # entire available width instead of leaving empty space.
    column_weights = [5, 30, 25, 20, 20]
    headers = ["#", "SUBJECT", "LECTURER", "ROOM", "CLASS TYPE"]

    for col, weight in enumerate(column_weights):
        table.grid_columnconfigure(col, weight=weight)

    # Header
    for col, title in enumerate(headers):
        tk.Label(
            table,
            text=title,
            font=(FONT, 9, "bold"),
            fg=WHITE,
            bg=NAVY,
            anchor="w" if col != 0 else "center"
        ).grid(
            row=0,
            column=col,
            sticky="ew",
            padx=(5 if col == 0 else 8, 5),
            pady=(8, 5),
            ipady=7
        )

    subject_entries = []
    lecturer_entries = []
    room_entries = []
    type_variables = []

    # Five subject rows are kept compact and evenly distributed.
    for i in range(subject_count):
        row_bg = WHITE if i % 2 == 0 else "#F7F9FC"

        # Number
        tk.Label(
            table,
            text=f"{i + 1:02d}",
            font=(FONT, 9, "bold"),
            fg=BLUE,
            bg=row_bg,
            anchor="center"
        ).grid(
            row=i + 1,
            column=0,
            sticky="ew",
            padx=5,
            pady=4,
            ipady=5
        )

        # Subject
        subject_entry = tk.Entry(
            table,
            font=(FONT, 9),
            relief="flat",
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        subject_entry.grid(
            row=i + 1,
            column=1,
            sticky="ew",
            padx=8,
            pady=4,
            ipady=5
        )

        # Lecturer
        lecturer_entry = tk.Entry(
            table,
            font=(FONT, 9),
            relief="flat",
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        lecturer_entry.grid(
            row=i + 1,
            column=2,
            sticky="ew",
            padx=8,
            pady=4,
            ipady=5
        )

        # Room
        room_entry = tk.Entry(
            table,
            font=(FONT, 9),
            relief="flat",
            bg=WHITE,
            fg=TEXT,
            insertbackground=TEXT,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        room_entry.grid(
            row=i + 1,
            column=3,
            sticky="ew",
            padx=8,
            pady=4,
            ipady=5
        )

        # Class Type
        type_variable = tk.StringVar(value="Lecture")

        type_menu = tk.OptionMenu(
            table,
            type_variable,
            "Lecture",
            "Lab"
        )
        type_menu.config(
            font=(FONT, 9),
            bg=LIGHT_BLUE,
            fg=NAVY,
            activebackground="#D8E8FF",
            activeforeground=NAVY,
            relief="flat",
            bd=0,
            highlightthickness=0,
            anchor="w"
        )
        type_menu["menu"].config(
            font=(FONT, 9),
            bg=WHITE,
            fg=TEXT
        )
        type_menu.grid(
            row=i + 1,
            column=4,
            sticky="ew",
            padx=(8, 10),
            pady=4,
            ipady=2
        )

        subject_entries.append(subject_entry)
        lecturer_entries.append(lecturer_entry)
        room_entries.append(room_entry)
        type_variables.append(type_variable)

    # Short instruction directly below the table.
    tk.Label(
        window,
        text="Enter subject, lecturer and room details. Select Lecture or Lab for each subject.",
        font=(FONT, 8),
        fg=MUTED,
        bg=BG
    ).pack(pady=(5, 4))

    def save_subject_information():
        global subjects_data

        new_subjects = []

        for i in range(subject_count):
            name = subject_entries[i].get().strip()
            lecturer = lecturer_entries[i].get().strip()
            room = room_entries[i].get().strip()
            class_type = type_variables[i].get()

            if name == "" or lecturer == "" or room == "":
                messagebox.showwarning(
                    "Missing Information",
                    f"Please complete Subject {i + 1}."
                )
                return

            new_subjects.append({
                "name": name,
                "lecturer": lecturer,
                "room": room,
                "type": class_type
            })

        names = [subject["name"].lower() for subject in new_subjects]

        if len(names) != len(set(names)):
            messagebox.showerror(
                "Duplicate Subjects",
                "All subject names must be different."
            )
            return

        subjects_data = new_subjects
        show_time_page()

    # Buttons stay immediately below the table.
    buttons = tk.Frame(window, bg=BG)
    buttons.pack(pady=(6, 0))

    make_button(
        buttons,
        "← BACK",
        show_home_page,
        primary=False,
        width=15
    ).pack(side="left", padx=7)

    make_button(
        buttons,
        "NEXT  →",
        save_subject_information,
        primary=True,
        width=18
    ).pack(side="left", padx=7)


# ==========================================================
# TIME PAGE
# ==========================================================

def show_time_page():
    clear_window()
    window.geometry("1100x700")

    global time_data
    time_data = []

    add_header(
        "Available Time Options",
        "Choose three possible time slots for every subject.",
        2
    )

    content = tk.Frame(window, bg=BG)
    content.pack(fill="both", expand=True, padx=35, pady=18)

    option_variables = []

    for i in range(subject_count):
        subject_name = subjects_data[i]["name"]

        subject_card = tk.Frame(
            content, bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        subject_card.pack(fill="x", pady=6)

        label_frame = tk.Frame(subject_card, bg=WHITE, width=220)
        label_frame.pack(side="left", fill="y")
        label_frame.pack_propagate(False)

        tk.Label(
            label_frame,
            text=f"SUBJECT {i + 1}",
            font=(FONT, 8, "bold"),
            fg=BLUE,
            bg=WHITE
        ).pack(anchor="w", padx=16, pady=(12, 2))

        tk.Label(
            label_frame,
            text=subject_name,
            font=(FONT, 10, "bold"),
            fg=TEXT,
            bg=WHITE,
            wraplength=185,
            justify="left"
        ).pack(anchor="w", padx=16)

        row_variables = []

        for column in range(3):
            variable = tk.StringVar(value=TIME_SLOTS[column])

            menu = tk.OptionMenu(
                subject_card,
                variable,
                *TIME_SLOTS
            )
            menu.config(
                font=(FONT, 8),
                bg=LIGHT_BLUE,
                fg=NAVY,
                activebackground="#D8E8FF",
                relief="flat",
                bd=0,
                width=22
            )
            menu["menu"].config(font=(FONT, 8))
            menu.pack(side="left", padx=5, pady=16)

            row_variables.append(variable)

        option_variables.append(row_variables)

    def save_time_information():
        global time_data

        new_time_data = []

        for row in option_variables:
            times = [variable.get() for variable in row]

            if len(set(times)) != 3:
                messagebox.showwarning(
                    "Invalid Time Options",
                    "Each subject must have three different time options."
                )
                return

            new_time_data.append(times)

        time_data = new_time_data
        show_preferences_page()

    buttons = tk.Frame(window, bg=BG)
    buttons.pack(pady=10)

    make_button(
        buttons, "← BACK", show_subject_page,
        primary=False, width=15
    ).pack(side="left", padx=8)

    make_button(
        buttons, "NEXT  →", save_time_information,
        primary=True, width=18
    ).pack(side="left", padx=8)


# ==========================================================
# PREFERENCES PAGE
# ==========================================================

def show_preferences_page():
    clear_window()
    window.geometry("1100x650")

    add_header(
        "Student Preferences",
        "The AI will use these preferences to rank valid timetables.",
        3
    )

    body = tk.Frame(window, bg=BG)
    body.pack(fill="both", expand=True)

    main_card = tk.Frame(
        body, bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    main_card.pack(padx=250, pady=30, fill="x")

    # Preferred day
    tk.Label(
        main_card,
        text="PREFERRED DAY",
        font=(FONT, 9, "bold"),
        fg=MUTED,
        bg=WHITE
    ).pack(anchor="w", padx=25, pady=(22, 4))

    day_variable = tk.StringVar(
        value=preferences_data["preferred_day"]
    )

    day_menu = tk.OptionMenu(
        main_card,
        day_variable,
        "Any", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    )
    day_menu.config(
        font=(FONT, 10),
        bg=LIGHT_BLUE,
        fg=NAVY,
        activebackground="#D8E8FF",
        relief="flat",
        bd=0,
        width=28
    )
    day_menu.pack(anchor="w", padx=25)

    # Preferred period
    tk.Label(
        main_card,
        text="PREFERRED PERIOD",
        font=(FONT, 9, "bold"),
        fg=MUTED,
        bg=WHITE
    ).pack(anchor="w", padx=25, pady=(20, 4))

    period_variable = tk.StringVar(
        value=preferences_data["preferred_period"]
    )

    period_menu = tk.OptionMenu(
        main_card,
        period_variable,
        "Any", "Morning", "Afternoon"
    )
    period_menu.config(
        font=(FONT, 10),
        bg=LIGHT_BLUE,
        fg=NAVY,
        activebackground="#D8E8FF",
        relief="flat",
        bd=0,
        width=28
    )
    period_menu.pack(anchor="w", padx=25)

    # Friday
    friday_variable = tk.BooleanVar(
        value=preferences_data["avoid_friday"]
    )

    friday_frame = tk.Frame(main_card, bg=WHITE)
    friday_frame.pack(fill="x", padx=25, pady=(22, 25))

    tk.Checkbutton(
        friday_frame,
        text="Avoid Friday classes",
        variable=friday_variable,
        font=(FONT, 10, "bold"),
        fg=TEXT,
        bg=WHITE,
        activebackground=WHITE,
        selectcolor=LIGHT_BLUE
    ).pack(anchor="w")

    tk.Label(
        friday_frame,
        text="Friday receives a lower preference score when this option is enabled.",
        font=(FONT, 8),
        fg=MUTED,
        bg=WHITE
    ).pack(anchor="w", padx=25, pady=(2, 0))

    def start_generation():
        global preferences_data

        preferences_data = {
            "preferred_day": day_variable.get(),
            "preferred_period": period_variable.get(),
            "avoid_friday": friday_variable.get()
        }

        show_processing_page()
        window.update()

        subjects_for_solver = []

        for i in range(subject_count):
            subject = subjects_data[i].copy()
            subject["times"] = time_data[i]
            subjects_for_solver.append(subject)

        solution, score = solve_timetable(
            subjects_for_solver,
            preferences_data
        )

        if solution is not None:
            show_result_page(solution, score)
        else:
            show_no_solution_page()

    buttons = tk.Frame(window, bg=BG)
    buttons.pack(pady=10)

    make_button(
        buttons, "← BACK", show_time_page,
        primary=False, width=15
    ).pack(side="left", padx=8)

    make_button(
        buttons, "✦ GENERATE TIMETABLE",
        start_generation,
        primary=True, width=23
    ).pack(side="left", padx=8)


# ==========================================================
# PROCESSING PAGE
# ==========================================================

def show_processing_page():
    clear_window()
    window.geometry("1100x700")

    add_header(
        "AI is Working",
        "Searching possible assignments and evaluating constraints...",
        4
    )

    body = tk.Frame(window, bg=BG)
    body.pack(fill="both", expand=True)

    tk.Label(
        body,
        text="✦",
        font=(FONT, 38, "bold"),
        fg=BLUE,
        bg=BG
    ).pack(pady=(40, 4))

    tk.Label(
        body,
        text="Generating your timetable...",
        font=(FONT, 20, "bold"),
        fg=TEXT,
        bg=BG
    ).pack()

    tk.Label(
        body,
        text="The AI is checking constraints and searching for the best valid solution.",
        font=(FONT, 9),
        fg=MUTED,
        bg=BG
    ).pack(pady=5)

    steps_frame = tk.Frame(
        body, bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    steps_frame.pack(padx=270, pady=20, fill="x")

    steps = [
        "Reading subject information",
        "Creating CSP variables and domains",
        "Checking time conflicts",
        "Checking lecturer conflicts",
        "Checking room conflicts",
        "Checking laboratory requirements",
        "Applying logical constraints",
        "Searching using backtracking",
        "Evaluating student preferences"
    ]

    for step in steps:
        row = tk.Frame(steps_frame, bg=WHITE)
        row.pack(fill="x", padx=18, pady=3)

        tk.Label(
            row,
            text="✓",
            font=(FONT, 9, "bold"),
            fg=GREEN,
            bg=WHITE
        ).pack(side="left")

        tk.Label(
            row,
            text=step,
            font=(FONT, 9),
            fg=TEXT,
            bg=WHITE
        ).pack(side="left", padx=8)


# ==========================================================
# RESULT PAGE
# ==========================================================

def show_result_page(solution, score):
    clear_window()
    window.geometry("1100x700")

    top = tk.Frame(window, bg=NAVY, height=105)
    top.pack(fill="x")
    top.pack_propagate(False)

    left = tk.Frame(top, bg=NAVY)
    left.pack(side="left", padx=38, pady=18)

    tk.Label(
        left,
        text="✓  TIMETABLE GENERATED SUCCESSFULLY",
        font=(FONT, 20, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(anchor="w")

    tk.Label(
        left,
        text="A valid timetable was found using CSP and backtracking.",
        font=(FONT, 9),
        fg="#D9E8FA",
        bg=NAVY
    ).pack(anchor="w", pady=3)

    score_box = tk.Frame(top, bg=BLUE)
    score_box.pack(side="right", padx=38, pady=18)

    tk.Label(
        score_box,
        text="PREFERENCE SCORE",
        font=(FONT, 7, "bold"),
        fg="#D9E8FA",
        bg=BLUE
    ).pack(padx=20, pady=(7, 0))

    tk.Label(
        score_box,
        text=str(score),
        font=(FONT, 18, "bold"),
        fg=WHITE,
        bg=BLUE
    ).pack(padx=20, pady=(0, 7))

    body = tk.Frame(window, bg=BG)
    body.pack(fill="both", expand=True, padx=28, pady=18)

    # Table
    table = tk.Frame(
        body, bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    table.pack(fill="x")

    headers = ["#", "SUBJECT", "TIME", "LECTURER", "ROOM", "TYPE"]
    widths = [5, 24, 30, 20, 15, 10]

    head = tk.Frame(table, bg=NAVY)
    head.pack(fill="x")

    for i, h in enumerate(headers):
        tk.Label(
            head,
            text=h,
            font=(FONT, 8, "bold"),
            fg=WHITE,
            bg=NAVY,
            width=widths[i],
            anchor="w"
        ).grid(row=0, column=i, padx=5, pady=8)

    sorted_solution = sorted(
        solution.items(),
        key=lambda item: item[1]["time"]
    )

    for number, (subject, data) in enumerate(sorted_solution, start=1):
        bg = WHITE if number % 2 else "#F8FAFD"

        row = tk.Frame(table, bg=bg)
        row.pack(fill="x")

        values = [
            number,
            subject,
            data["time"],
            data["lecturer"],
            data["room"],
            data["type"]
        ]

        for i, value in enumerate(values):
            tk.Label(
                row,
                text=str(value),
                font=(FONT, 8),
                fg=TEXT,
                bg=bg,
                width=widths[i],
                anchor="w"
            ).grid(row=0, column=i, padx=5, pady=7)

    # Validation
    validation = tk.Frame(body, bg=BG)
    validation.pack(fill="x", pady=12)

    checks = [
        ("✓", "No Time Conflicts"),
        ("✓", "No Lecturer Conflicts"),
        ("✓", "No Room Conflicts"),
        ("✓", "All Hard Constraints Satisfied")
    ]

    for symbol, text in checks:
        f = tk.Frame(
            validation, bg=LIGHT_GREEN,
            highlightbackground="#C6E8D8",
            highlightthickness=1
        )
        f.pack(side="left", expand=True, fill="x", padx=4)

        tk.Label(
            f, text=symbol, font=(FONT, 10, "bold"),
            fg=GREEN, bg=LIGHT_GREEN
        ).pack(side="left", padx=(9, 4), pady=8)

        tk.Label(
            f, text=text, font=(FONT, 8, "bold"),
            fg=TEXT, bg=LIGHT_GREEN
        ).pack(side="left", pady=8)

    buttons = tk.Frame(body, bg=BG)
    buttons.pack(pady=3)

    make_button(
        buttons, "CREATE NEW", show_home_page,
        primary=False, width=17
    ).pack(side="left", padx=7)

    make_button(
        buttons, "BACK TO HOME", show_home_page,
        primary=True, width=17
    ).pack(side="left", padx=7)


# ==========================================================
# NO SOLUTION PAGE
# ==========================================================

def show_no_solution_page():
    clear_window()
    window.geometry("1100x650")

    top = tk.Frame(window, bg=NAVY, height=105)
    top.pack(fill="x")
    top.pack_propagate(False)

    tk.Label(
        top,
        text="NO VALID TIMETABLE FOUND",
        font=(FONT, 22, "bold"),
        fg=WHITE,
        bg=NAVY
    ).pack(pady=(30, 4))

    tk.Label(
        top,
        text="The current constraints cannot be satisfied simultaneously.",
        font=(FONT, 9),
        fg="#D9E8FA",
        bg=NAVY
    ).pack()

    body = tk.Frame(window, bg=BG)
    body.pack(fill="both", expand=True)

    card_frame = tk.Frame(
        body, bg=WHITE,
        highlightbackground=BORDER,
        highlightthickness=1
    )
    card_frame.pack(padx=300, pady=80, fill="x")

    tk.Label(
        card_frame,
        text="⚠",
        font=(FONT, 35, "bold"),
        fg=RED,
        bg=WHITE
    ).pack(pady=(25, 8))

    tk.Label(
        card_frame,
        text="No solution exists for the current input.",
        font=(FONT, 15, "bold"),
        fg=TEXT,
        bg=WHITE
    ).pack()

    tk.Label(
        card_frame,
        text="Try changing the available time options, lecturer, or room information.",
        font=(FONT, 9),
        fg=MUTED,
        bg=WHITE,
        wraplength=420
    ).pack(pady=8)

    make_button(
        card_frame,
        "MODIFY INPUT",
        show_home_page,
        primary=True,
        width=20
    ).pack(pady=(10, 25))


# ==========================================================
# START APPLICATION
# ==========================================================

show_home_page()
window.mainloop()
