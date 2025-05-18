import tkinter as tk
import subprocess
import os

DUONG_DAN_THU_MUC_HIEN_HANH = os.path.dirname(__file__)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        CHIEU_RONG_MAN_HINH = self.winfo_screenwidth()
        CHIEU_DAI_MAN_HINH = self.winfo_screenheight()
        CHIEU_RONG_CUA_SO = 1200
        CHIEU_DAI_CUA_SO = 650
        toa_do_x_man_hinh = (CHIEU_RONG_MAN_HINH // 2) - (CHIEU_RONG_CUA_SO // 2)
        toa_do_y_man_hinh = (CHIEU_DAI_MAN_HINH // 2) - (CHIEU_DAI_CUA_SO // 2)
        self.title("Võ Lê Khánh Duy - 23110196")
        self.geometry(f"{CHIEU_RONG_CUA_SO}x{CHIEU_DAI_CUA_SO}+{toa_do_x_man_hinh}+{toa_do_y_man_hinh}")
        self["bg"] = "#99FFCC"
        self.current_frame = None
        self.show_frame(StartFrame)
        
    def show_frame(self, frame_name):
        if self.current_frame:
            self.current_frame.destroy()
            
        self.current_frame = frame_name(self)
        self.current_frame.pack(fill="both", expand=True)
        
class StartFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#99FFCC"
        tk.Label(self, text="Chose algorithm group: ", font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#99FFCC").pack(pady=10)
        tk.Button(self, text="Fully observered environment and reinforcement learning", font=("Times New Roman", 13), command=lambda: show_fully_observered_environment_and_reinforcement_learning_screen(), width= 50).pack(pady=5)
        tk.Button(self, text="Sensorless problem", font=("Times New Roman", 13), command=lambda: parent.show_frame(ComplexEnviromentFrame), width=50).pack(pady=5)
        tk.Button(self, text="Constrain satisfaction problem", font=("Times New Roman", 13), command=lambda: show_constrain_satisfaction_problem(), width=50).pack(pady=5)

class ComplexEnviromentFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self["bg"] = "#99FFCC"
        tk.Label(self, text="Chose algorithm: ", font=("Times New Roman", 15, "bold"), width=30, fg="#008080", bg="#99FFCC").pack(pady=10)
        tk.Button(self, text="AND OR graph search", font=("Times New Roman", 13), command=lambda: show_AND_OR_graph_search_screen(), width=50).pack(pady=5)
        tk.Button(self, text="Search with no observation, search with partial observation", font=("Times New Roman", 13), command=lambda: show_sensorless_problem_screen(), width=50).pack(pady=5)      
        tk.Button(self, text="Back", font=("Times New Roman", 13), command=lambda: parent.show_frame(StartFrame), width=50).pack(pady=5)

def show_fully_observered_environment_and_reinforcement_learning_screen():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/fully_observered_environment_and_reinforcement_learning_screen.py"])
    
def show_AND_OR_graph_search_screen():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/AND_OR_graph_search_screen.py"])
    
def show_sensorless_problem_screen():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/complex_environment_screen.py"])
    
def show_constrain_satisfaction_problem():
    subprocess.run(["python", DUONG_DAN_THU_MUC_HIEN_HANH + "/constrain_satisfaction_problem_screen.py"])
          
app = MainApp()
app.mainloop()