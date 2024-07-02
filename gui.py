from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy
from pathlib import Path
import pickle
import json

CONFIG_PATH = Path("config_files/exe_config.json")

def donothing():
    pass

class FingerprintViewerGui:
    def __init__(self) -> None:
        # self.WINDOW_SIZE = (750, 700)
        self.TITLE = "Fingerprint Viewer"
        self.load_config()
        self.construct_gui()
    
    def load_config(self):
        with open(CONFIG_PATH) as f:
            self.config = json.load(f)

    def construct_gui(self) -> None:
        self.root = Tk()
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        self.root.title(self.TITLE)

        # Create the menu
        self.menubar = Menu(self.root)

            # File menu
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Open Fingerprint", command=self.load_fingerprint)
        self.file_menu.add_command(label="Downsample Fingerprint", command=donothing)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

            # Help menu
        self.help_menu = Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="Quick Guide", command=donothing)
        self.help_menu.add_command(label="About", command=donothing)
        self.menubar.add_cascade(label="Help", menu=self.help_menu)

        # Top Frame
        self.top_frame = Frame(self.root, borderwidth=5, relief='ridge')
        self.top_frame.pack(side='top', fill='x')

            # Metadata labels
        self.fingerprint_name_label = Label(self.top_frame, text=f"Name:\t\t\t{"default"}")
        self.date_label = Label(self.top_frame, text=f"Date:\t\t\t{"01/01/2000"}")
        self.machine_label = Label(self.top_frame, text=f"Machine:\t\t{"fjdskafjads"}")
        self.config_label = Label(self.top_frame, text=f"Config:\t\t\t{"NXE:3800"}")

        self.fingerprint_name_label.grid(row=0, sticky="W")
        self.date_label.grid(row=1, sticky="W")
        self.machine_label.grid(row=2, sticky="W")
        self.config_label.grid(row=3, sticky="W")

        # Bottom Frame
        self.bottom_frame = Frame(self.root, borderwidth=5, relief="ridge")
        self.bottom_frame.pack(side="top", fill='both', expand=True)

            # Notebook (Tabs) widget
        self.my_notebook= ttk.Notebook(self.bottom_frame, width=200)
        self.my_notebook.pack(side="left", fill="y", expand=True, anchor="nw")

        tab_labels = ["AUR", "APA", "ALR", "LL1", "LL2", "SUR", "VPA", "SLR"]

        self.tabs = dict.fromkeys(tab_labels)
        for k in self.tabs.keys():
            self.tabs[k] = ttk.Frame(self.my_notebook)
            self.my_notebook.add(self.tabs[k], text=k)

                # Treeview widget
        self.trees = dict.fromkeys(tab_labels)
        for k in self.tabs.keys():
            self.trees[k] = ttk.Treeview(self.tabs[k], selectmode=BROWSE)
            self.trees[k].pack(fill='both', expand=True) 
            self.trees[k].heading("#0", text="Test Cycles & DNDM signals")

            # Right-side Frame
        self.figure_frame = Frame(self.bottom_frame, width=500, borderwidth=5, relief='ridge')
        self.figure_frame.pack(side="left", anchor="nw")

                # Figure widget
        self.fig = Figure(figsize=(5, 4), dpi=100)
        t = numpy.arange(0, 3, .01)
        self.plot = self.fig.add_subplot(111)
        self.plot.plot(t, 2 * numpy.sin(2 * numpy.pi * t))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.figure_frame) # A tk.DrawingArea.
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

                # Controls Frame
        self.controls_frame = Frame(self.figure_frame, height=50, borderwidth=5, relief="ridge")
        self.controls_frame.pack(fill="x")

                    # Cycle Frame
        self.cycle_frame = Frame(self.controls_frame, height=50, borderwidth=5, relief="ridge")
        self.cycle_frame.pack()

                        # Cycle Left
        self.previous_cycle_button = Button(self.cycle_frame, text="<", command=self.show_previous_cycle)
        self.previous_cycle_button.pack(side="left")

                        # Cycle Label
        self.cycle_label = Label(self.cycle_frame, text="Cycle 1")
        self.cycle_label.pack(side="left")

                        # Cycle Right
        self.next_cycle_button = Button(self.cycle_frame, text=">", command=self.show_next_cycle)
        self.next_cycle_button.pack(side="right")

                # Checkbox Hide Other Cycles
        var1 = IntVar()
        self.hide_cycles_checkbox = Checkbutton(self.controls_frame, text="Hide other cycles", variable=var1, command=self.toggle_show_cycles)
        self.hide_cycles_checkbox.pack(side="right")

        self.root.config(menu=self.menubar)
        self.root.mainloop()
    
    def load_fingerprint(self) -> None:
        self.pickle_file = Path(filedialog.askopenfilename())

        with open(self.pickle_file, 'rb') as f:
            self.fingerprint = pickle.load(f)
        
        # Load metadata
        pickle_path_parts = self.pickle_file.stem.split("_")
        self.fingerprint_name = pickle_path_parts[0]
        self.machine = pickle_path_parts[1]
        self.date = "_".join(pickle_path_parts[2:5])

        self.update_gui_to_fingerprint()

    def update_gui_to_fingerprint(self) -> None:
        # Update metadata labels
        self.fingerprint_name_label.config(text=f"Name:\t\t\t{self.fingerprint_name}")
        self.machine_label.config(text=f"Machine:\t\t{self.machine}")
        self.date_label.config(text=f"Date:\t\t\t{self.date}")

        human_dict = {}

        # Update TreeView
        for peripheral in self.fingerprint.keys():

            test_cycle_expandable = dict.fromkeys(self.fingerprint[peripheral])
            for test_cycle in self.fingerprint[peripheral].keys():

                test_cycle_expandable[test_cycle] = self.trees[peripheral].insert("", END, text=test_cycle)
                for signal in self.fingerprint[peripheral][test_cycle]["cycle_1"].columns:

                    # try:
                    #     item_text = f"{self.config[signal]} - {signal}"
                    # except KeyError: # In case human readable name is not found
                    #     item_text = signal
                    item_text=signal
                    
                    self.trees[peripheral].insert(test_cycle_expandable[test_cycle], END, text=item_text)
                    self.trees[peripheral].bind("<<TreeviewSelect>>", lambda event, p=peripheral: self.show_selected_trace(p))
    
    def show_selected_trace(self, p):
        self.selected_peripheral = p

        # Get the missing information: test cycle & the selected signal name
        selected_item = self.trees[p].focus()
        self.selected_test_cycle = self.trees[p].item(self.trees[p].parent(selected_item))["text"]

        # Ignore when not a signal, but a test-cycle is selected
        if not self.selected_test_cycle:
            self.selected_trace = None
            return

        self.selected_trace = self.trees[p].item(selected_item)["text"]
        self.selected_cycle = 1

        self.update_figure(p, self.selected_test_cycle, self.selected_trace, self.selected_cycle)
    
    def update_figure(self, peripheral, test_cycle, trace_name, cycle, show_other_cycles=True):
        # Plot the figure
        self.plot.clear()

        if show_other_cycles:
            for c in [f"cycle_{i}" for i in range(1, 6)]:
                trace = self.fingerprint[peripheral][test_cycle][c][trace_name]
                self.plot.plot(trace, color='0.8')

        trace = self.fingerprint[peripheral][test_cycle][f"cycle_{cycle}"][trace_name]
        self.plot.plot(trace)

        self.plot.set_title(trace_name)
        self.plot.grid()
        self.fig.tight_layout()
        self.canvas.draw()

        self.cycle_label.config(text=f"Cycle {self.selected_cycle}")
    
    def show_previous_cycle(self):
        if self.selected_cycle == 1:
            self.selected_cycle = 5
        else:
            self.selected_cycle = self.selected_cycle - 1
        
        self.update_figure(self.selected_peripheral, self.selected_test_cycle, self.selected_trace, self.selected_cycle)


    def show_next_cycle(self):
        if self.selected_cycle == 5:
            self.selected_cycle = 1
        else:
            self.selected_cycle = self.selected_cycle + 1
        
        self.update_figure(self.selected_peripheral, self.selected_test_cycle, self.selected_trace, self.selected_cycle)
    
    def toggle_show_cycles(self):
        pass


if __name__=="__main__":
    gui = FingerprintViewerGui()
