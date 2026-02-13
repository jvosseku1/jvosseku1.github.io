import os
from supabase import create_client, Client
import tkinter as tk
from tkinter import *
from tkinter import font, messagebox

#--------Import The Database---------#
url = "https://vefblsnxsxgymoamadfg.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZlZmJsc254c3hneW1vYW1hZGZnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzA5MzQxNTQsImV4cCI6MjA4NjUxMDE1NH0.IveWmZDdJS0NawZJMQD2HtR7amr6hepM0HP4urRrVnE"
supabase = create_client(url, key)

#------Basic Info of Root-------#
root = tk.Tk()
root.geometry("1920x1080")
root.title("RDL Tracker")

#---------Database Functionality for Leaderboard---------#
def LBClicked():
    LeaderboardOption = radvar.get()
    output_box.delete("1.0", tk.END)

    if LeaderboardOption == "Games_Played":
        response = supabase.table("Beer_Die").select("Roll_Num, First_Name, Last_Name, Games_Played").order("Games_Played", desc=True).execute()
        headers = ["Roll", "First", "Last", "Games"]
    elif LeaderboardOption == "Num_Catches":
        response = supabase.table("Beer_Die").select("Roll_Num, First_Name, Last_Name, Num_Catches").order("Num_Catches", desc=True).execute()
        headers = ["Roll", "First", "Last", "Catches"]
    elif LeaderboardOption == "Num_Hits":
        response = supabase.table("Beer_Die").select("Roll_Num, First_Name, Last_Name, Num_Hits").order("Num_Hits", desc=True).execute()
        headers = ["Roll", "First", "Last", "Hits"]
    elif LeaderboardOption == "Num_Cups":
        response = supabase.table("Beer_Die").select("Roll_Num, First_Name, Last_Name, Num_Cups").order("Num_Cups", desc=True).execute()
        headers = ["Roll", "First", "Last", "Cups"]
    elif LeaderboardOption == "Num_Field_Goals":
        response = supabase.table("Beer_Die").select("Roll_Num, First_Name, Last_Name, Num_Field_Goals").order("Num_Field_Goals", desc=True).execute()
        headers = ["Roll", "First", "Last", "FG"]
    elif LeaderboardOption == "All_Stats":
        response = supabase.table("Beer_Die").select("*").order("Roll_Num").execute()
        headers = ["Roll", "First", "Last", "Games", "Catches", "Hits", "Cups", "FG"]
    else:
        return

    results = response.data

    output_box.insert(tk.END, " ".join(headers) + "\n")
    output_box.insert(tk.END, "-" * 70 + "\n")

    for row in results:
        output_box.insert(tk.END,
            f"{row['Roll_Num']:<8}{row['First_Name']:<12}{row['Last_Name']:<15}"
            f"{row.get('Games_Played',''):<8}{row.get('Num_Catches',''):<8}"
            f"{row.get('Num_Hits',''):<8}{row.get('Num_Cups',''):<8}"
            f"{row.get('Num_Field_Goals',''):<8}\n"
        )

#------------------------New Player-----------------------------#
def validateNewPlayer(*args):
    First_Name = fnamebox.get().strip()
    Last_Name = lnamebox.get().strip()
    Roll_Num = numbox.get().strip() or "Pledge"

    if First_Name.isalpha() and Last_Name.isalpha():
        response = supabase.table("Beer_Die").insert({
            "Roll_Num": Roll_Num,
            "First_Name": First_Name,
            "Last_Name": Last_Name
        }).execute()
        messagebox.showinfo("Success", "Player added")
    else:
        messagebox.showerror("Invalid Entry", "Names must be text and not empty")
#--------------------------Add Match Info-----------------------------#
def validateMatchInfo():
    First_Name = fnamebox.get().strip()
    Last_Name = lnamebox.get().strip()
    Roll_Num = numbox.get().strip() or "Pledge"

    Num_Catches = catchesbox.get()
    Num_Hits = hitsbox.get()
    Num_Cups = cupsbox.get()
    Field_Goals = fieldgoalbox.get()

    # Fetch current stats
    response = supabase.table("Beer_Die").select("*")\
        .eq("First_Name", First_Name)\
        .eq("Last_Name", Last_Name)\
        .eq("Roll_Num", Roll_Num)\
        .execute()

    if not response.data:
        messagebox.showerror("Error", "Player not found")
        return

    row = response.data[0]

    supabase.table("Beer_Die").update({
        "Games_Played": row["Games_Played"] + 1,
        "Num_Catches": row["Num_Catches"] + Num_Catches,
        "Num_Hits": row["Num_Hits"] + Num_Hits,
        "Num_Cups": row["Num_Cups"] + Num_Cups,
        "Num_Field_Goals": row["Num_Field_Goals"] + Field_Goals
    })\
    .eq("Roll_Num", Roll_Num)\
    .execute()

    messagebox.showinfo("Success", "Match recorded")

#---------IDEK---------#
radvar = StringVar()
radvar.set(" ")

#Default font / size
font1 = font.Font(size=18)
font2 = font.Font(size=14)
font3 = font.Font(size=12)

#Set up each frame
MainMenu = Frame(root)
NewPlayerMenu = Frame(root)
LeaderboardMenu = Frame(root)
AddMatchMenu = Frame(root)

#Grids for each menu
MainMenu.grid(row=0, column=0, sticky="nsew")
NewPlayerMenu.grid(row=0, column=0, sticky="nsew")
LeaderboardMenu.grid(row=0, column=0, sticky="nsew")
AddMatchMenu.grid(row=0,column=0, sticky="nsew") 

#---------------------------------Main Menu Buttons------------------------------------#
#Label for Main Menu
MainMenuHeader = Label(MainMenu, text="RDL Tracker Main Menu", font=font1)
MainMenuHeader.pack(padx=200, pady=10)

#Main Menu -> Add Match
MainAddMatch = Button(MainMenu, text="Add Match", command=lambda: AddMatchMenu.tkraise(), font=font1)
MainAddMatch.pack(pady=10)

#Main Menu -> New Player Button
MainNewPlayer = Button(MainMenu, text="Add New Player", command=lambda: NewPlayerMenu.tkraise(), font = font1)
MainNewPlayer.pack(pady=10)

#Main Menu -> Leaderboard Button
MainLeaderboard = Button(MainMenu, text="View Leaderboards", command=lambda: LeaderboardMenu.tkraise(), font=font1)
MainLeaderboard.pack(pady=10)

#----------------------------------------Back Buttons-----------------------------#

#New Player -> Main Menu Button
NewPlayerMain = Button(NewPlayerMenu, text="Back to Main Menu", command=lambda: MainMenu.tkraise(), font=font1)
NewPlayerMain.pack(side="left", pady=20)

#Leaderboard -> Main Menu Button
LeaderboardMain = Button(LeaderboardMenu, text="Back to Main Menu", command=lambda: MainMenu.tkraise(), font=font1)
LeaderboardMain.pack(side="bottom", pady=20)

#Add Match -> Main Menu Button
AddMatchMain = Button(AddMatchMenu, text="Back to Main Menu", command=lambda: MainMenu.tkraise(), font=font1)
AddMatchMain.pack(side="bottom", pady=20)

#------------Leaderboard Labels & Radio Buttons--------------------#
#Label for Viewing Leaderboard
LeaderboardHeader = Label(LeaderboardMenu, text="RDL Leaderboards", font=font1)
LeaderboardHeader.pack(padx=10, pady=10)

#Sort By Label for Leaderboard
SortByLabel = Label(LeaderboardMenu, text="Sort By: ", font=font2)
SortByLabel.pack(padx=10, pady=10, anchor="w")

# Container for radio buttons and text box
LeaderboardContentFrame = Frame(LeaderboardMenu)
LeaderboardContentFrame.pack(fill="both", expand=True, padx=20, pady=20)

# Frame for radio buttons inside LeaderboardContentFrame at row=0, column=0
RadioButtonFrame = Frame(LeaderboardContentFrame)
RadioButtonFrame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

# Add radio buttons inside RadioButtonFrame using grid()
SortGamesPlayed = Radiobutton(RadioButtonFrame, text="Games Played", variable=radvar, value="Games_Played", command=LBClicked, font=font2)
SortGamesPlayed.grid(row=0, column=0, sticky="w", pady=2)

#Sort By Catches 
SortNumCatches = Radiobutton(RadioButtonFrame, text="Catches", variable=radvar, value="Num_Catches", command=LBClicked, font=font2)
SortNumCatches.grid(row=1, column=0, sticky="w", pady=2)

#Sort By Cups Hit
SortNumHits = Radiobutton(RadioButtonFrame, text="Cup Hits", variable=radvar, value="Num_Hits", command=LBClicked, font=font2)
SortNumHits.grid(row=2, column=0, sticky="w", pady=2)

#Sort By Cups Made
SortNumCups = Radiobutton(RadioButtonFrame, text="Cups Made", variable=radvar, value="Num_Cups", command=LBClicked, font=font2)
SortNumCups.grid(row=3, column=0, sticky="w", pady=2)

#Sort By Num Field Goals
SortNumGoals = Radiobutton(RadioButtonFrame, text="Field Goals", variable=radvar, value="Num_Field_Goals", command=LBClicked, font=font2)
SortNumGoals.grid(row=4, column=0, sticky="w", pady=2)

#Shows all stats in order by Number
ViewAll = Radiobutton(RadioButtonFrame, text="View All Stats By Number", variable=radvar, value="All_Stats", command=LBClicked, font=font2)
ViewAll.grid(row=5, column=0, sticky="w", pady=2)

# Text box in LeaderboardContentFrame at row=0, column=1
output_box = Text(LeaderboardContentFrame, height=30, width=80)
output_box.grid(row=0, column=1, padx=20, sticky="n")

#---------------------------------------------New Player Items---------------------------------------------------#
#Frame for New Player Items
fnamebox = StringVar()
lnamebox = StringVar()
numbox = StringVar()

#Label for Add New player
NewPlayerHeader = Label(NewPlayerMenu, text="Add New Player Information", font=font1)
NewPlayerHeader.pack(padx=10, pady=10)

NewPlayerLabel = Label(NewPlayerMenu, text="Enter the Following Info: ", font=font2)
NewPlayerLabel.pack(padx=10, pady=10, anchor="w")

NewPlayerContentFrame = Frame(NewPlayerMenu)
NewPlayerContentFrame.pack(fill="both", expand=True, padx=10)

#First Name Label & Button
FirstNameLabel = Label(NewPlayerContentFrame, text="First Name",font=font2)
FirstNameLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")

FirstNameBox = Entry(NewPlayerContentFrame, width=20, textvariable=fnamebox)
FirstNameBox.grid(row=0, column=1, padx=5, pady=5)

#Last Name Label & Button
LastNameLabel = Label(NewPlayerContentFrame, text="Last Name", font=font2)
LastNameLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")

LastNameBox = Entry(NewPlayerContentFrame, width=20, textvariable=lnamebox)
LastNameBox.grid(row=1, column=1, padx=5, pady=5)

#Roll Number Labels & Button
RollNumLabel = Label(NewPlayerContentFrame, text="Roll Number", font=font2)
RollNumLabel.grid(row=2, column=0, padx=5, pady=5, sticky="w")

RollNumBox = Entry(NewPlayerContentFrame, width=20, textvariable=numbox)
RollNumBox.grid(row=2, column=1, padx=5, pady=5)

PledgeLabel = Label(NewPlayerContentFrame, text="*Leave Blank For Pledge", font=font3)
PledgeLabel.grid(row=2, column=2, padx=5, pady=5)

SubmitButton = Button(NewPlayerContentFrame, text="Submit", font=font2, command=validateNewPlayer)
SubmitButton.grid(row=3, column=1, padx=5, pady=5)

#---------------------------------Add Match Labels-----------------------------------#
pledgeORactive = IntVar(value=0)
#fnamebox, lnamebox, numbox are already declared in New Player Items
catchesbox = IntVar()
hitsbox = IntVar()
cupsbox = IntVar()
fieldgoalbox = IntVar()

#Label for Add Match
AddMatchHeader = Label(AddMatchMenu, text="Add Match Info", font=font1)
AddMatchHeader.pack(padx=10, pady=10)

AddMatchContentFrame = Frame(AddMatchMenu)
AddMatchContentFrame.pack(fill="both", expand=True, padx=10)

FirstNameLabel2 = Label(AddMatchContentFrame, text="First Name:", font=font2)
FirstNameLabel2.grid(row=0, column=0, padx=5, pady=5, sticky="w")

LastNameLabel2 = Label(AddMatchContentFrame, text="Last Name:", font=font2)
LastNameLabel2.grid(row=1, column=0, padx=5, pady=5, sticky="w")

RollNumLabel2 = Label(AddMatchContentFrame, text="Roll Number:", font=font2)
RollNumLabel2.grid(row=2, column=0, padx=5, pady=5, sticky="w")

NumCatchesLabel = Label(AddMatchContentFrame, text="Number of Catches:", font=font2)
NumCatchesLabel.grid(row=0, column=2, padx=5, pady=5, sticky="w")

NumHitsLabel = Label(AddMatchContentFrame, text="Number of Cup Hits:", font=font2)
NumHitsLabel.grid(row=1, column=2, padx=5, pady=5, sticky="w")

NumCupsLabel = Label(AddMatchContentFrame, text="Number of Cups Made:", font=font2)
NumCupsLabel.grid(row=2, column=2, padx=5, pady=5, sticky="w")

NumFieldGoalsLabel = Label(AddMatchContentFrame, text="Number of Field Goals:", font=font2)
NumFieldGoalsLabel.grid(row=3, column=2, padx=5, pady=5, sticky="w")

PledgeOrActiveButton = Checkbutton(AddMatchContentFrame, text="*Check If Player is a Pledge", variable=pledgeORactive)
PledgeOrActiveButton.grid(row=3, column=0, padx=5, pady=5)

#-------------------------------Add Match Entry Boxes-----------------------------------#
FirstNameBox2 = Entry(AddMatchContentFrame, width=20, textvariable=fnamebox)
FirstNameBox2.grid(row=0, column=1, padx=5, pady=5)

LastNameBox2 = Entry(AddMatchContentFrame, width=20, textvariable=lnamebox)
LastNameBox2.grid(row=1, column=1, padx=5, pady=5)

RollNumBox2 = Entry(AddMatchContentFrame, width=20, textvariable=numbox)
RollNumBox2.grid(row=2, column=1, padx=5, pady=5)

NumCatchesBox = Entry(AddMatchContentFrame, width=20, textvariable=catchesbox)
NumCatchesBox.grid(row=0, column=3, padx=5, pady=5)

NumHitsBox = Entry(AddMatchContentFrame, width=20, textvariable=hitsbox)
NumHitsBox.grid(row=1, column=3, padx=5, pady=5)

NumCupsBox = Entry(AddMatchContentFrame, width=20, textvariable=cupsbox)
NumCupsBox.grid(row=2, column=3, padx=5, pady=5)

NumFieldGoalsBox = Entry(AddMatchContentFrame, width=20, textvariable=fieldgoalbox)
NumFieldGoalsBox.grid(row=3, column=3, padx=5, pady=5)

SubmitButton = Button(AddMatchContentFrame, text="Submit", font=font2, command=validateMatchInfo)
SubmitButton.grid(row=3, column=1, padx=5, pady=5)

#-----Misc Items-------#
MainMenu.tkraise()
root.mainloop()
