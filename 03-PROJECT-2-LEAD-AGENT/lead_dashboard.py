import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, timedelta
import json
import os


# ============================================================
# CONFIG
# ============================================================

DATA_FILE = "lead_data.json"


# ============================================================
# COLORS
# ============================================================

BG = "#F4F7FB"
CARD = "#FFFFFF"
TEXT = "#172033"
MUTED = "#6B7280"
BORDER = "#DDE3EC"

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1D4ED8"

HOT = "#DC2626"
WARM = "#D97706"
COLD = "#64748B"

SUCCESS = "#16A34A"
WARNING = "#D97706"
DANGER = "#DC2626"


# ============================================================
# LOAD / SAVE DATA
# ============================================================

def load_leads():

    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except Exception:
        return []


leads = load_leads()


def save_leads():

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                leads,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as error:

        messagebox.showerror(
            "Save Error",
            f"Could not save lead data.\n\n{error}"
        )


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(value):

    return " ".join(
        str(value).strip().lower().split()
    )


# ============================================================
# CATEGORY NORMALIZATION
# ============================================================

def clean_category(category):

    normalized = normalize_text(category)

    category_map = {

        "ai engineering": "AI Engineering",
        "artificial intelligence": "AI Engineering",

        "python ai course": "Python AI Course",
        "python": "Python AI Course",

        "data science": "Data Science",

        "machine learning": "Machine Learning",
        "ml": "Machine Learning",

        "generative ai": "Generative AI",
        "gen ai": "Generative AI",

        "cyber security": "Cyber Security",
        "cybersecurity": "Cyber Security"
    }

    return category_map.get(
        normalized,
        str(category).strip().title()
    )


# ============================================================
# PRIORITY
# ============================================================

def calculate_priority(message, timeline):

    text = normalize_text(
        f"{message} {timeline}"
    )

    hot_words = [
        "today",
        "immediately",
        "this week",
        "urgent",
        "join today",
        "start soon",
        "as soon as possible"
    ]

    warm_words = [
        "2 weeks",
        "two weeks",
        "1 month",
        "one month",
        "this month",
        "next month",
        "2 months",
        "two months"
    ]

    for word in hot_words:

        if word in text:
            return "Hot"

    for word in warm_words:

        if word in text:
            return "Warm"

    return "Cold"


# ============================================================
# FOLLOW-UP STATUS
# ============================================================

def get_followup_status(next_followup):

    if not next_followup:
        return "NO DATE"

    try:

        today = date.today()

        followup_date = date.fromisoformat(
            next_followup
        )

        if followup_date < today:

            days = (
                today - followup_date
            ).days

            return (
                f"OVERDUE {days}D"
            )

        if followup_date == today:

            return "DUE TODAY"

        days = (
            followup_date - today
        ).days

        return f"IN {days}D"

    except Exception:

        return "UNKNOWN"


# ============================================================
# NEEDS ATTENTION
# ============================================================

def needs_attention(lead):

    status = get_followup_status(
        lead.get(
            "next_followup_date",
            ""
        )
    )

    # IMPORTANT:
    # Priority does NOT decide this.
    # Follow-up date decides this.

    return (
        status == "DUE TODAY"
        or status.startswith("OVERDUE")
    )


# ============================================================
# NEXT LEAD ID
# ============================================================

def next_lead_id():

    numbers = []

    for lead in leads:

        lead_id = str(
            lead.get("id", "")
        )

        if lead_id.startswith("L"):

            try:

                numbers.append(
                    int(lead_id[1:])
                )

            except ValueError:
                pass

    if not numbers:
        return "L001"

    return f"L{max(numbers) + 1:03d}"


# ============================================================
# DUPLICATE CHECK
# ============================================================

def is_duplicate(
    name,
    course,
    city
):

    new_name = normalize_text(name)
    new_course = normalize_text(course)
    new_city = normalize_text(city)

    for lead in leads:

        old_name = normalize_text(
            lead.get("name", "")
        )

        old_course = normalize_text(
            lead.get(
                "course_interest",
                ""
            )
        )

        old_city = normalize_text(
            lead.get("city", "")
        )

        if (
            old_name == new_name
            and old_course == new_course
            and old_city == new_city
        ):

            return True

    return False


# ============================================================
# WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "AI Lead Agent — Business Dashboard"
)

root.geometry(
    "1550x950"
)

root.minsize(
    1150,
    750
)

root.configure(
    bg=BG
)


# ============================================================
# STYLE
# ============================================================

style = ttk.Style()

try:
    style.theme_use("clam")
except Exception:
    pass


style.configure(
    "TFrame",
    background=BG
)

style.configure(
    "Card.TFrame",
    background=CARD
)

style.configure(
    "TLabel",
    background=BG,
    foreground=TEXT,
    font=("Segoe UI", 10)
)

style.configure(
    "Title.TLabel",
    background=BG,
    foreground=TEXT,
    font=("Segoe UI", 26, "bold")
)

style.configure(
    "Subtitle.TLabel",
    background=BG,
    foreground=MUTED,
    font=("Segoe UI", 11)
)

style.configure(
    "CardTitle.TLabel",
    background=CARD,
    foreground=MUTED,
    font=("Segoe UI", 10, "bold")
)

style.configure(
    "CardValue.TLabel",
    background=CARD,
    foreground=TEXT,
    font=("Segoe UI", 25, "bold")
)

style.configure(
    "Section.TLabelframe",
    background=CARD,
    foreground=TEXT,
    bordercolor=BORDER,
    relief="solid"
)

style.configure(
    "Section.TLabelframe.Label",
    background=CARD,
    foreground=TEXT,
    font=("Segoe UI", 11, "bold")
)

style.configure(
    "TButton",
    font=("Segoe UI", 10, "bold"),
    padding=(12, 8)
)

style.configure(
    "Primary.TButton",
    background=PRIMARY,
    foreground="white"
)

style.map(
    "Primary.TButton",
    background=[
        ("active", PRIMARY_DARK)
    ]
)

style.configure(
    "Treeview",
    background=CARD,
    fieldbackground=CARD,
    foreground=TEXT,
    rowheight=32,
    font=("Segoe UI", 9)
)

style.configure(
    "Treeview.Heading",
    background="#E9EEF7",
    foreground=TEXT,
    font=("Segoe UI", 9, "bold"),
    padding=8
)

style.map(
    "Treeview",
    background=[
        ("selected", "#DBEAFE")
    ],
    foreground=[
        ("selected", TEXT)
    ]
)


# ============================================================
# MAIN SCROLLABLE WINDOW
# ============================================================

outer = tk.Frame(
    root,
    bg=BG
)

outer.pack(
    fill="both",
    expand=True
)


canvas = tk.Canvas(
    outer,
    bg=BG,
    highlightthickness=0
)

scrollbar = ttk.Scrollbar(
    outer,
    orient="vertical",
    command=canvas.yview
)

canvas.configure(
    yscrollcommand=scrollbar.set
)

scrollbar.pack(
    side="right",
    fill="y"
)

canvas.pack(
    side="left",
    fill="both",
    expand=True
)


content = tk.Frame(
    canvas,
    bg=BG
)

window_id = canvas.create_window(
    (0, 0),
    window=content,
    anchor="nw"
)


def update_scroll_region(event=None):

    canvas.configure(
        scrollregion=canvas.bbox("all")
    )


def resize_content(event):

    canvas.itemconfigure(
        window_id,
        width=event.width
    )


content.bind(
    "<Configure>",
    update_scroll_region
)

canvas.bind(
    "<Configure>",
    resize_content
)


# ============================================================
# HEADER
# ============================================================

header = tk.Frame(
    content,
    bg=BG
)

header.pack(
    fill="x",
    padx=25,
    pady=(25, 15)
)


title_frame = tk.Frame(
    header,
    bg=BG
)

title_frame.pack(
    side="left"
)


tk.Label(
    title_frame,
    text="🤖 AI Lead Agent",
    bg=BG,
    fg=TEXT,
    font=("Segoe UI", 26, "bold")
).pack(
    anchor="w"
)


tk.Label(
    title_frame,
    text="Lead management • Follow-ups • Business insights",
    bg=BG,
    fg=MUTED,
    font=("Segoe UI", 11)
).pack(
    anchor="w",
    pady=(2, 0)
)


day_badge = tk.Label(
    header,
    text="DAY 15 • LEAD DASHBOARD",
    bg=PRIMARY,
    fg="white",
    font=("Segoe UI", 10, "bold"),
    padx=15,
    pady=8
)

day_badge.pack(
    side="right",
    pady=8
)


# ============================================================
# METRIC CARDS
# ============================================================

metrics = tk.Frame(
    content,
    bg=BG
)

metrics.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)


def create_metric(
    parent,
    title_text,
    icon
):

    card = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    tk.Label(
        card,
        text=f"{icon}  {title_text}",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 10, "bold")
    ).pack(
        anchor="w",
        padx=18,
        pady=(15, 3)
    )

    value = tk.Label(
        card,
        text="0",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 25, "bold")
    )

    value.pack(
        anchor="w",
        padx=18,
        pady=(0, 15)
    )

    return value


total_value = create_metric(
    metrics,
    "TOTAL LEADS",
    "👥"
)

hot_value = create_metric(
    metrics,
    "HOT LEADS",
    "🔥"
)

attention_value = create_metric(
    metrics,
    "NEED ATTENTION",
    "⚠"
)

warm_value = create_metric(
    metrics,
    "WARM LEADS",
    "🟠"
)

cold_value = create_metric(
    metrics,
    "COLD LEADS",
    "🔵"
)


# ============================================================
# ADD LEAD
# ============================================================

form = ttk.LabelFrame(
    content,
    text="➕  Add New Lead",
    style="Section.TLabelframe",
    padding=15
)

form.pack(
    fill="x",
    padx=25,
    pady=(0, 15)
)


name_var = tk.StringVar()
course_var = tk.StringVar()
city_var = tk.StringVar()
timeline_var = tk.StringVar()


# Row 1

tk.Label(
    form,
    text="Name",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=7,
    pady=(0, 4)
)

tk.Label(
    form,
    text="Course Interest",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=7,
    pady=(0, 4)
)

tk.Label(
    form,
    text="City",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
).grid(
    row=0,
    column=2,
    sticky="w",
    padx=7,
    pady=(0, 4)
)

tk.Label(
    form,
    text="Timeline",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
).grid(
    row=0,
    column=3,
    sticky="w",
    padx=7,
    pady=(0, 4)
)


name_entry = ttk.Entry(
    form,
    textvariable=name_var
)

course_entry = ttk.Entry(
    form,
    textvariable=course_var
)

city_entry = ttk.Entry(
    form,
    textvariable=city_var
)

timeline_entry = ttk.Entry(
    form,
    textvariable=timeline_var
)


name_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=7,
    pady=5
)

course_entry.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=7,
    pady=5
)

city_entry.grid(
    row=1,
    column=2,
    sticky="ew",
    padx=7,
    pady=5
)

timeline_entry.grid(
    row=1,
    column=3,
    sticky="ew",
    padx=7,
    pady=5
)


# Row 2

tk.Label(
    form,
    text="Lead Message",
    bg=CARD,
    fg=TEXT,
    font=("Segoe UI", 9, "bold")
).grid(
    row=2,
    column=0,
    sticky="nw",
    padx=7,
    pady=(10, 4)
)


message_text = tk.Text(
    form,
    height=4,
    font=("Segoe UI", 10),
    relief="solid",
    bd=1,
    wrap="word"
)

message_text.grid(
    row=3,
    column=0,
    columnspan=4,
    sticky="ew",
    padx=7,
    pady=5
)


for column in range(4):

    form.columnconfigure(
        column,
        weight=1
    )


# ============================================================
# TABLE CREATION HELPER
# ============================================================

def create_tree(
    parent,
    columns,
    headings,
    widths,
    height=8,
    horizontal=True
):

    frame = tk.Frame(
        parent,
        bg=CARD
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=height
    )

    for column, heading, width in zip(
        columns,
        headings,
        widths
    ):

        tree.heading(
            column,
            text=heading
        )

        tree.column(
            column,
            width=width,
            minwidth=60
        )


    vertical = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=vertical.set
    )


    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical.grid(
        row=0,
        column=1,
        sticky="ns"
    )


    if horizontal:

        horizontal_bar = ttk.Scrollbar(
            frame,
            orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            xscrollcommand=horizontal_bar.set
        )

        horizontal_bar.grid(
            row=1,
            column=0,
            sticky="ew"
        )


    frame.rowconfigure(
        0,
        weight=1
    )

    frame.columnconfigure(
        0,
        weight=1
    )

    return frame, tree


# ============================================================
# TABLES AREA
# ============================================================

tables = tk.Frame(
    content,
    bg=BG
)

tables.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 15)
)


# ============================================================
# ALL LEADS
# ============================================================

all_section = ttk.LabelFrame(
    tables,
    text="👥  All Leads",
    style="Section.TLabelframe",
    padding=10
)

all_section.pack(
    fill="both",
    expand=True,
    pady=(0, 15)
)


all_columns = (
    "id",
    "name",
    "course",
    "city",
    "timeline",
    "priority",
    "status",
    "last_contact",
    "next_followup"
)

all_headings = (
    "ID",
    "NAME",
    "COURSE",
    "CITY",
    "TIMELINE",
    "PRIORITY",
    "STATUS",
    "LAST CONTACT",
    "NEXT FOLLOW-UP"
)

all_widths = (
    65,
    130,
    170,
    110,
    120,
    90,
    110,
    120,
    130
)


all_table_frame, all_tree = create_tree(
    all_section,
    all_columns,
    all_headings,
    all_widths,
    height=9,
    horizontal=True
)

all_table_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# LOWER DASHBOARD
# ============================================================

lower = tk.Frame(
    content,
    bg=BG
)

lower.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=(0, 20)
)


# ============================================================
# LEFT: NEED ATTENTION
# ============================================================

attention_section = ttk.LabelFrame(
    lower,
    text="⚠  Leads Needing Attention",
    style="Section.TLabelframe",
    padding=10
)

attention_section.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(0, 7)
)


attention_columns = (
    "name",
    "priority",
    "status",
    "last_contact",
    "next_followup"
)

attention_headings = (
    "LEAD",
    "PRIORITY",
    "FOLLOW-UP",
    "LAST CONTACT",
    "NEXT FOLLOW-UP"
)

attention_widths = (
    120,
    90,
    120,
    120,
    130
)


attention_frame, attention_tree = create_tree(
    attention_section,
    attention_columns,
    attention_headings,
    attention_widths,
    height=7,
    horizontal=True
)

attention_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# MIDDLE: HOT LEADS
# ============================================================

hot_section = ttk.LabelFrame(
    lower,
    text="🔥  Hot Leads",
    style="Section.TLabelframe",
    padding=10
)

hot_section.pack(
    side="left",
    fill="both",
    expand=True,
    padx=7
)


hot_columns = (
    "name",
    "course",
    "city",
    "timeline",
    "followup"
)

hot_headings = (
    "LEAD",
    "COURSE",
    "CITY",
    "TIMELINE",
    "FOLLOW-UP"
)

hot_widths = (
    110,
    140,
    90,
    110,
    110
)


hot_frame, hot_tree = create_tree(
    hot_section,
    hot_columns,
    hot_headings,
    hot_widths,
    height=7,
    horizontal=True
)

hot_frame.pack(
    fill="both",
    expand=True
)


# ============================================================
# RIGHT: CATEGORY CHART
# ============================================================

chart_section = ttk.LabelFrame(
    lower,
    text="📊  Leads By Category",
    style="Section.TLabelframe",
    padding=10
)

chart_section.pack(
    side="left",
    fill="both",
    expand=True,
    padx=(7, 0)
)


chart_canvas = tk.Canvas(
    chart_section,
    bg=CARD,
    highlightthickness=0,
    height=260
)

chart_canvas.pack(
    fill="both",
    expand=True
)


# ============================================================
# CATEGORY CHART
# ============================================================

def draw_category_chart():

    chart_canvas.delete("all")

    categories = {}

    for lead in leads:

        category = clean_category(
            lead.get(
                "course_interest",
                "Other"
            )
        )

        categories[category] = (
            categories.get(category, 0) + 1
        )


    if not categories:

        chart_canvas.create_text(
            200,
            100,
            text="No lead data yet",
            fill=MUTED,
            font=("Segoe UI", 11)
        )

        return


    sorted_categories = sorted(
        categories.items(),
        key=lambda item: item[1],
        reverse=True
    )


    width = max(
        chart_canvas.winfo_width(),
        400
    )

    height = max(
        chart_canvas.winfo_height(),
        250
    )


    max_count = max(
        categories.values()
    )

    left = 145
    right = 25

    usable_width = (
        width - left - right
    )

    bar_height = 25

    gap = 17

    start_y = 25


    for index, (
        category,
        count
    ) in enumerate(sorted_categories):

        y = (
            start_y
            + index * (
                bar_height + gap
            )
        )


        # Category name

        display_name = category

        if len(display_name) > 20:

            display_name = (
                display_name[:18]
                + "..."
            )


        chart_canvas.create_text(
            left - 10,
            y + bar_height / 2,
            text=display_name,
            anchor="e",
            fill=TEXT,
            font=("Segoe UI", 9, "bold")
        )


        # Bar

        bar_width = (
            count / max_count
        ) * usable_width


        chart_canvas.create_rectangle(
            left,
            y,
            left + bar_width,
            y + bar_height,
            fill=PRIMARY,
            outline=""
        )


        # Number

        chart_canvas.create_text(
            left + bar_width + 10,
            y + bar_height / 2,
            text=str(count),
            anchor="w",
            fill=TEXT,
            font=("Segoe UI", 10, "bold")
        )


# ============================================================
# STATUS SUMMARY
# ============================================================

status_section = ttk.LabelFrame(
    content,
    text="📌  Lead Status Summary",
    style="Section.TLabelframe",
    padding=10
)

status_section.pack(
    fill="x",
    padx=25,
    pady=(0, 25)
)


status_labels = {}


for status in [
    "NEW",
    "REVIEWED",
    "CONTACTED",
    "FOLLOW-UP",
    "CONVERTED",
    "LOST"
]:

    card = tk.Frame(
        status_section,
        bg=CARD,
        highlightbackground=BORDER,
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=4
    )


    tk.Label(
        card,
        text=status,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(
        pady=(8, 2)
    )


    value = tk.Label(
        card,
        text="0",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 18, "bold")
    )

    value.pack(
        pady=(0, 8)
    )


    status_labels[status] = value


# ============================================================
# ADD LEAD
# ============================================================

def add_lead():

    name = name_var.get().strip()

    course = course_var.get().strip()

    city = city_var.get().strip()

    timeline = timeline_var.get().strip()

    message = message_text.get(
        "1.0",
        "end"
    ).strip()


    # Validation

    if not name:

        messagebox.showwarning(
            "Missing Information",
            "Please enter the lead name."
        )

        name_entry.focus()

        return


    if not course:

        messagebox.showwarning(
            "Missing Information",
            "Please enter the course interest."
        )

        course_entry.focus()

        return


    if not city:

        messagebox.showwarning(
            "Missing Information",
            "Please enter the city."
        )

        city_entry.focus()

        return


    if not timeline:

        messagebox.showwarning(
            "Missing Information",
            "Please enter the timeline."
        )

        timeline_entry.focus()

        return


    # Duplicate check

    if is_duplicate(
        name,
        course,
        city
    ):

        messagebox.showwarning(
            "Duplicate Lead",
            f"{name} already exists.\n\n"
            "The same lead will not be added again."
        )

        return


    # Normalize category

    category = clean_category(
        course
    )


    # Priority

    priority = calculate_priority(
        message,
        timeline
    )


    # Dates

    today = date.today()

    last_contact = (
        today.isoformat()
    )

    # Day 1 follow-up

    next_followup = (
        today
        + timedelta(days=1)
    ).isoformat()


    # Create lead

    new_lead = {

        "id": next_lead_id(),

        "name": name,

        "course_interest": category,

        "lead_message": message,

        "city": city,

        "timeline": timeline,

        "priority": priority,

        "status": "NEW",

        "last_contact_date":
            last_contact,

        "next_followup_date":
            next_followup
    }


    leads.append(
        new_lead
    )

    save_leads()

    refresh_dashboard()


    # Clear

    name_var.set("")

    course_var.set("")

    city_var.set("")

    timeline_var.set("")

    message_text.delete(
        "1.0",
        "end"
    )


    name_entry.focus()


    messagebox.showinfo(
        "Lead Added Successfully",
        f"Lead: {name}\n"
        f"Category: {category}\n"
        f"Priority: {priority}\n"
        f"Status: NEW\n"
        f"Next Follow-Up: {next_followup}"
    )


# ============================================================
# CLEAR FORM
# ============================================================

def clear_form():

    name_var.set("")

    course_var.set("")

    city_var.set("")

    timeline_var.set("")

    message_text.delete(
        "1.0",
        "end"
    )

    name_entry.focus()


# ============================================================
# BUTTONS
# ============================================================

buttons = tk.Frame(
    form,
    bg=CARD
)

buttons.grid(
    row=4,
    column=0,
    columnspan=4,
    sticky="w",
    padx=7,
    pady=(10, 0)
)


ttk.Button(
    buttons,
    text="➕  ADD LEAD",
    style="Primary.TButton",
    command=add_lead
).pack(
    side="left",
    padx=(0, 8)
)


ttk.Button(
    buttons,
    text="✕  CLEAR",
    command=clear_form
).pack(
    side="left",
    padx=8
)


ttk.Button(
    buttons,
    text="🔄  REFRESH",
    command=lambda: refresh_dashboard()
).pack(
    side="left",
    padx=8
)


# ============================================================
# REFRESH DASHBOARD
# ============================================================

def refresh_dashboard():

    # -----------------------------------------
    # Clear tables
    # -----------------------------------------

    for item in all_tree.get_children():
        all_tree.delete(item)

    for item in hot_tree.get_children():
        hot_tree.delete(item)

    for item in attention_tree.get_children():
        attention_tree.delete(item)


    # -----------------------------------------
    # Counts
    # -----------------------------------------

    total = len(leads)

    hot = 0
    warm = 0
    cold = 0

    attention = 0


    for lead in leads:

        priority = normalize_text(
            lead.get(
                "priority",
                ""
            )
        )

        if priority == "hot":
            hot += 1

        elif priority == "warm":
            warm += 1

        else:
            cold += 1


        if needs_attention(lead):
            attention += 1


    total_value.config(
        text=str(total)
    )

    hot_value.config(
        text=str(hot)
    )

    attention_value.config(
        text=str(attention)
    )

    warm_value.config(
        text=str(warm)
    )

    cold_value.config(
        text=str(cold)
    )


    # -----------------------------------------
    # Status counts
    # -----------------------------------------

    status_counts = {
        status: 0
        for status in status_labels
    }


    # -----------------------------------------
    # All Leads
    # -----------------------------------------

    for lead in leads:

        status = lead.get(
            "status",
            "NEW"
        )

        if status not in status_counts:
            status_counts[status] = 0

        status_counts[status] += 1


        all_tree.insert(
            "",
            "end",
            values=(

                lead.get(
                    "id",
                    ""
                ),

                lead.get(
                    "name",
                    ""
                ),

                clean_category(
                    lead.get(
                        "course_interest",
                        ""
                    )
                ),

                lead.get(
                    "city",
                    ""
                ),

                lead.get(
                    "timeline",
                    ""
                ),

                lead.get(
                    "priority",
                    ""
                ),

                status,

                lead.get(
                    "last_contact_date",
                    ""
                ),

                lead.get(
                    "next_followup_date",
                    ""
                )
            )
        )


    # -----------------------------------------
    # Hot Leads
    # -----------------------------------------

    for lead in leads:

        if normalize_text(
            lead.get(
                "priority",
                ""
            )
        ) != "hot":

            continue


        hot_tree.insert(
            "",
            "end",
            values=(

                lead.get(
                    "name",
                    ""
                ),

                clean_category(
                    lead.get(
                        "course_interest",
                        ""
                    )
                ),

                lead.get(
                    "city",
                    ""
                ),

                lead.get(
                    "timeline",
                    ""
                ),

                get_followup_status(
                    lead.get(
                        "next_followup_date",
                        ""
                    )
                )
            )
        )


    # -----------------------------------------
    # Needs Attention
    # -----------------------------------------

    for lead in leads:

        if not needs_attention(lead):
            continue


        attention_tree.insert(
            "",
            "end",
            values=(

                lead.get(
                    "name",
                    ""
                ),

                lead.get(
                    "priority",
                    ""
                ),

                get_followup_status(
                    lead.get(
                        "next_followup_date",
                        ""
                    )
                ),

                lead.get(
                    "last_contact_date",
                    ""
                ),

                lead.get(
                    "next_followup_date",
                    ""
                )
            )
        )


    # -----------------------------------------
    # Status cards
    # -----------------------------------------

    for status, value in status_labels.items():

        value.config(
            text=str(
                status_counts.get(
                    status,
                    0
                )
            )
        )


    # -----------------------------------------
    # Chart
    # -----------------------------------------

    draw_category_chart()


# ============================================================
# KEYBOARD SHORTCUT
# ============================================================

root.bind(
    "<Control-Return>",
    lambda event: add_lead()
)


# ============================================================
# MOUSE WHEEL
# ============================================================

def mouse_wheel(event):

    canvas.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units"
    )


canvas.bind_all(
    "<MouseWheel>",
    mouse_wheel
)


# ============================================================
# START
# ============================================================

refresh_dashboard()

name_entry.focus()

root.mainloop()