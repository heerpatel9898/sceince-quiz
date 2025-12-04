import tkinter as tk
from tkinter import ttk, messagebox
import random
import math

# ==========================================
#  🎨 PUNCHY NEON PALETTE
# ==========================================
BG_COLOR = "#0f172a"        # Deep Navy (Background)
CARD_COLOR = "#1e293b"      # Card Background
BTN_NORMAL = "#334155"      # Option Button (Visible Grey)
BTN_HOVER = "#475569"       # Option Hover
TEXT_MAIN = "#f8fafc"       # White Text
TEXT_DIM = "#94a3b8"        # Grey Text

# Neon Accents
NEON_CYAN = "#22d3ee"       # Primary
NEON_PINK = "#fb7185"       # Exit / Wrong
NEON_GREEN = "#4ade80"      # Success / Correct
NEON_PURPLE = "#a78bfa"     # Header
NEON_ORANGE = "#fbbf24"     # Warning

# Fonts
FONT_TITLE = ("Segoe UI", 32, "bold")
FONT_Q = ("Segoe UI", 18, "bold")
FONT_OPT = ("Segoe UI", 14, "bold")

# ==========================================
#  🧠 LOGIC: UNLIMITED GENERATORS
# ==========================================
class LogicEngine:
    @staticmethod
    def gen_chemistry(diff):
        # Generates: A + B -> Product (Balance it)
        cations = [("Na", 1), ("K", 1), ("Mg", 2), ("Ca", 2), ("Al", 3), ("Fe", 3)]
        anions = [("Cl", 1), ("O", 2), ("S", 2), ("F", 1)]
        
        if diff == "Hard":
            cations.extend([("Zn", 2), ("Cu", 2)])
            anions.extend([("Br", 1), ("N", 3)])

        cat, cat_chg = random.choice(cations)
        an, an_chg = random.choice(anions)
        
        def gcd(a, b): return a if b == 0 else gcd(b, a % b)
        common = gcd(cat_chg, an_chg)
        sub_cat = an_chg // common
        sub_an = cat_chg // common
        
        # Formula String
        p_form = f"{cat}" + (str(sub_cat) if sub_cat > 1 else "") + \
                 f"{an}" + (str(sub_an) if sub_an > 1 else "")
        
        diatomic = ["O", "N", "F", "Cl", "Br", "I"]
        r_an = f"{an}2" if an in diatomic else an
        
        # Solver
        correct = "1, 1, 1"
        for c in range(1, 10):
            req_an = c * sub_an
            per_mol = 2 if an in diatomic else 1
            if req_an % per_mol == 0:
                b = req_an // per_mol
                a = c * sub_cat
                correct = f"{a}, {b}, {c}"
                break
        
        q = f"Balance:  _ {cat} + _ {r_an}  →  _ {p_form}"
        
        # Options
        opts = [correct]
        while len(opts) < 4:
            fake = f"{random.randint(1,5)}, {random.randint(1,5)}, {random.randint(1,5)}"
            if fake not in opts: opts.append(fake)
        random.shuffle(opts)
        return {"q": q, "options": opts, "correct": correct}

    @staticmethod
    def gen_math(diff):
        mode = "calc" if (diff == "Hard" and random.random() > 0.3) else "alg"
        
        if mode == "alg":
            # ax + b = c
            x = random.randint(-10, 10)
            a = random.randint(2, 9)
            b = random.randint(-15, 15)
            c = a*x + b
            q = f"Solve for x:\n{a}x {'+' if b>=0 else ''}{b} = {c}"
            ans = str(x)
            opts = {ans, str(x+1), str(x-1), str(-x)}
        else:
            # Derivative
            n = random.randint(2, 6)
            a = random.randint(1, 5)
            q = f"Find d/dx ( {a}x^{n} )"
            ans = f"{a*n}x^{n-1}"
            opts = {ans, f"{a}x^{n-1}", f"{n}x^{n}", f"{a*n}x^{n}"}

        opts = list(opts)
        while len(opts) < 4: opts.append(str(random.randint(100,200)))
        random.shuffle(opts)
        return {"q": q, "options": opts, "correct": ans}

    @staticmethod
    def gen_physics(diff):
        formulas = [
            ("F = ma", lambda m, a: m*a, ["m (kg)", "a (m/s²)"], "Force (N)"),
            ("V = IR", lambda i, r: i*r, ["I (A)", "R (Ω)"], "Voltage (V)"),
            ("K = 0.5mv²", lambda m, v: 0.5*m*v*v, ["m (kg)", "v (m/s)"], "Energy (J)"),
        ]
        if diff == "Hard":
            formulas.append(("F = Gm1m2/r²", lambda m, r: round(6.67*m*m/(r*r),2), ["m (x10¹¹)", "r (m)"], "F (N)"))

        _, eqn, func, vars, unit = random.choice(formulas)
        vals = [random.randint(2, 10) for _ in vars]
        ans = func(*vals)
        ans = int(ans) if ans == int(ans) else round(ans, 1)
        
        q = f"Using {eqn}, find {unit}\ngiven: " + ", ".join([f"{v}={x}" for v, x in zip(vars, vals)])
        
        opts = {str(ans)}
        while len(opts) < 4:
            off = random.choice([-2, -1, 1, 2, 10])
            opts.add(str(ans + off))
        
        opts = list(opts)
        random.shuffle(opts)
        return {"q": q, "options": opts, "correct": str(ans)}

# ==========================================
#  💥 POPUP ANIMATION
# ==========================================
class PunchyPopup:
    def __init__(self, parent, title, msg, is_good, callback):
        self.parent = parent
        self.callback = callback
        bg = NEON_GREEN if is_good else NEON_PINK
        fg = BG_COLOR if is_good else "#ffffff"
        
        self.win = tk.Toplevel(parent)
        self.win.overrideredirect(True)
        self.win.configure(bg=bg)
        self.win.attributes('-topmost', True)
        
        # Center
        rw, rh = parent.winfo_width(), parent.winfo_height()
        rx, ry = parent.winfo_rootx(), parent.winfo_rooty()
        w, h = 450, 220
        x, y = rx + (rw-w)//2, ry + (rh-h)//2
        
        self.target = (w, h, x, y)
        self.win.geometry(f"0x0+{x+w//2}+{y+h//2}")
        
        f = tk.Frame(self.win, bg=bg)
        f.pack(expand=True, fill="both", padx=20, pady=20)
        
        icon = "✔" if is_good else "✖"
        tk.Label(f, text=icon, font=("Segoe UI Emoji", 40), bg=bg, fg=fg).pack()
        tk.Label(f, text=title, font=("Segoe UI", 22, "bold"), bg=bg, fg=fg).pack()
        tk.Label(f, text=msg, font=("Segoe UI", 12), bg=bg, fg=fg).pack(pady=5)
        
        self.step = 0
        self.animate()

    def animate(self):
        if self.step <= 10:
            scale = self.step / 10
            tw, th, tx, ty = self.target
            cw, ch = int(tw*scale), int(th*scale)
            cx, cy = tx + (tw-cw)//2, ty + (th-ch)//2
            self.win.geometry(f"{cw}x{ch}+{cx}+{cy}")
            self.step += 1
            self.parent.after(15, self.animate)
        else:
            self.parent.after(1500, self.close)

    def close(self):
        self.win.destroy()
        if self.callback: self.callback()

# ==========================================
#  🎮 MAIN APP
# ==========================================
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Science Quiz")
        self.root.geometry("900x700")
        self.root.configure(bg=BG_COLOR)
        self.score = 0
        self.current_q_idx = 0
        self.timer_id = None
        self.show_main_menu()

    def clear(self):
        if self.timer_id: self.root.after_cancel(self.timer_id)
        for w in self.root.winfo_children(): w.destroy()

    # --- MENU SCREEN ---
    def show_main_menu(self):
        self.clear()
        tk.Label(self.root, text="∞ UNLIMITED", font=("Segoe UI", 20), bg=BG_COLOR, fg=NEON_CYAN).pack(pady=(60,0))
        tk.Label(self.root, text="SCIENCE QUIZ", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=(0,30))
        
        bf = tk.Frame(self.root, bg=BG_COLOR)
        bf.pack()
        
        self.btn_menu(bf, "Chemistry", lambda: self.show_settings("Chemistry"), NEON_PURPLE)
        self.btn_menu(bf, "Physics", lambda: self.show_settings("Physics"), NEON_CYAN)
        self.btn_menu(bf, "Maths", lambda: self.show_settings("Maths"), NEON_GREEN)
        self.btn_menu(bf, "Exit", self.root.quit, NEON_PINK)

    def btn_menu(self, p, txt, cmd, col):
        b = tk.Button(p, text=txt, font=("Segoe UI", 14), width=20, bg=col, fg=BG_COLOR,
                      bd=0, cursor="hand2", activebackground=TEXT_MAIN, command=cmd)
        b.pack(pady=8)

    # --- SETTINGS SCREEN ---
    def show_settings(self, cat):
        self.clear()
        self.cat = cat
        tk.Label(self.root, text=f"{cat} Settings", font=FONT_TITLE, bg=BG_COLOR, fg=NEON_CYAN).pack(pady=40)
        
        # Difficulty
        tk.Label(self.root, text="Select Difficulty:", font=("Segoe UI", 14), bg=BG_COLOR, fg=TEXT_DIM).pack()
        self.diff = tk.StringVar(value="Medium")
        f_d = tk.Frame(self.root, bg=BG_COLOR)
        f_d.pack(pady=10)
        for d in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(f_d, text=d, variable=self.diff, value=d, bg=BG_COLOR, fg=TEXT_MAIN, 
                           font=("Segoe UI", 12), selectcolor=CARD_COLOR, activebackground=BG_COLOR).pack(side="left", padx=10)

        # Count
        tk.Label(self.root, text="Number of Questions:", font=("Segoe UI", 14), bg=BG_COLOR, fg=TEXT_DIM).pack(pady=(20,0))
        self.count = tk.IntVar(value=5)
        tk.Scale(self.root, from_=3, to=20, variable=self.count, orient="horizontal", 
                 bg=BG_COLOR, fg=TEXT_MAIN, length=300, highlightthickness=0).pack(pady=10)
        
        tk.Button(self.root, text="START GAME", font=("Segoe UI", 16, "bold"), bg=NEON_GREEN, fg=BG_COLOR,
                  width=20, bd=0, cursor="hand2", command=self.start_game).pack(pady=40)
        tk.Button(self.root, text="Back", bg=BG_COLOR, fg=TEXT_DIM, bd=0, command=self.show_main_menu).pack()

    # --- GAME LOOP ---
    def start_game(self):
        self.total = self.count.get()
        self.diff_val = self.diff.get()
        self.current_q_idx = 0
        self.score = 0
        self.time_limit = 30 if self.diff_val=="Easy" else 20 if self.diff_val=="Medium" else 15
        self.load_question()

    def load_question(self):
        if self.current_q_idx >= self.total:
            self.show_results()
            return
            
        self.clear()
        self.current_q_idx += 1
        
        # Generate
        if self.cat == "Chemistry": data = LogicEngine.gen_chemistry(self.diff_val)
        elif self.cat == "Physics": data = LogicEngine.gen_physics(self.diff_val)
        else: data = LogicEngine.gen_math(self.diff_val)
        self.curr_data = data

        # Header
        h = tk.Frame(self.root, bg=BG_COLOR)
        h.pack(fill="x", padx=40, pady=20)
        tk.Label(h, text=f"Q {self.current_q_idx} / {self.total}", font=("Segoe UI", 14, "bold"), bg=BG_COLOR, fg=NEON_PURPLE).pack(side="left")
        self.lbl_tm = tk.Label(h, text=str(self.time_limit), font=("Segoe UI", 20, "bold"), bg=BG_COLOR, fg=NEON_GREEN)
        self.lbl_tm.pack(side="right")

        # Question Card
        card = tk.Frame(self.root, bg=CARD_COLOR, bd=2)
        card.pack(fill="x", padx=40, pady=10)
        tk.Label(card, text=data['q'], font=FONT_Q, bg=CARD_COLOR, fg=TEXT_MAIN, wraplength=800, pady=30).pack()
        
        tk.Label(self.root, text="Select an option:", font=("Segoe UI", 12), bg=BG_COLOR, fg=TEXT_DIM).pack(pady=(10,5))

        # === RE-ADDED & IMPROVED: OPTIONS GRID ===
        opt_grid = tk.Frame(self.root, bg=BG_COLOR)
        opt_grid.pack(pady=10)
        
        self.btns = []
        labels = ["A", "B", "C", "D"]
        
        for i, opt in enumerate(data['options']):
            # Calculate Grid Position (0,0), (0,1), (1,0), (1,1)
            row = i // 2
            col = i % 2
            
            # Button with Label (A. Answer)
            btn_txt = f"{labels[i]}.  {opt}"
            
            b = tk.Button(opt_grid, text=btn_txt, font=FONT_OPT, bg=BTN_NORMAL, fg=TEXT_MAIN,
                          width=25, height=2, relief="flat", bd=0, cursor="hand2",
                          activebackground=NEON_CYAN, activeforeground=BG_COLOR,
                          command=lambda x=opt: self.check(x))
            
            # Add padding for grid look
            b.grid(row=row, column=col, padx=10, pady=10)
            
            # Hover effect
            b.bind("<Enter>", lambda e, btn=b: btn.config(bg=BTN_HOVER))
            b.bind("<Leave>", lambda e, btn=b: btn.config(bg=BTN_NORMAL))
            
            self.btns.append(b)

        self.time_left = self.time_limit
        self.update_timer()

    def update_timer(self):
        col = NEON_GREEN if self.time_left > 10 else NEON_ORANGE if self.time_left > 5 else NEON_PINK
        self.lbl_tm.config(text=f"⏱ {self.time_left}", fg=col)
        
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.check(None, timeout=True)

    def check(self, user_ans, timeout=False):
        if self.timer_id: self.root.after_cancel(self.timer_id)
        for b in self.btns: b.config(state="disabled")
        
        correct = self.curr_data['correct']
        
        if timeout:
            PunchyPopup(self.root, "TIME'S UP!", f"Answer: {correct}", False, self.load_question)
        elif user_ans == correct:
            self.score += 1
            PunchyPopup(self.root, "CORRECT!", "Excellent work!", True, self.load_question)
        else:
            PunchyPopup(self.root, "WRONG", f"Answer: {correct}", False, self.load_question)

    def show_results(self):
        self.clear()
        pct = (self.score/self.total)*100
        c = NEON_GREEN if pct>70 else NEON_ORANGE if pct>40 else NEON_PINK
        tk.Label(self.root, text="FINISHED", font=FONT_TITLE, bg=BG_COLOR, fg=TEXT_MAIN).pack(pady=50)
        tk.Label(self.root, text=f"{self.score} / {self.total}", font=("Segoe UI", 60, "bold"), bg=BG_COLOR, fg=c).pack()
        tk.Button(self.root, text="Menu", font=("Segoe UI", 16), bg=NEON_CYAN, fg=BG_COLOR, width=20, command=self.show_main_menu).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()