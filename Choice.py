import tkinter as tk
from random import randint


class LuckyDrawApp:
    def __init__(self, master):
        self.master = master
        self.master.title("特典抽选工具")

        self.prizes = []
        self.history = []
        self.probabilities = {}
        self.no_repeat = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        self.entry_label = tk.Label(self.master, text="请输入奖池内含物（逗号分隔）:")
        self.entry_label.pack()

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.master, textvariable=self.entry_var, width=30)
        self.entry.pack()

        self.add_button = tk.Button(self.master, text="添加内容", command=self.add_prize)
        self.add_button.pack()

        self.prize_var = tk.StringVar()
        self.prize_label = tk.Label(self.master, textvariable=self.prize_var, font=("Helvetica", 16), pady=20)
        self.prize_label.pack()

        self.pool_var = tk.StringVar()
        self.pool_label = tk.Label(self.master, textvariable=self.pool_var, font=("Helvetica", 12), pady=10)
        self.pool_label.pack()

        self.history_text = tk.Text(self.master, height=5, width=40, wrap=tk.WORD, state=tk.DISABLED)
        self.history_text.pack()

        self.creator_label = tk.Label(self.master, text="制作人: Siren")
        self.creator_label.pack()

        self.prob_label = tk.Label(self.master, text="当前概率:")
        self.prob_label.pack()

        self.no_repeat_check = tk.Checkbutton(self.master, text="不重复抽取", variable=self.no_repeat)
        self.no_repeat_check.pack()

        self.spin_button = tk.Button(self.master, text="开始抽取", command=self.spin)
        self.spin_button.pack()

    def add_prize(self):
        new_prizes = self.entry_var.get().replace('，', ',').split(',')

        new_prizes = [prize.strip() for prize in new_prizes]

        new_prizes = list(filter(None, new_prizes))

        self.prizes.extend(new_prizes)

        for prize in new_prizes:
            self.probabilities[prize] = 0

        self.entry_var.set("")

        self.update_pool()

        self.update_probability()

    def spin(self):
        if not self.prizes:
            self.prize_var.set("请先添加内容")
            return

        if self.no_repeat.get():
            remaining_prizes = list(set(self.prizes) - set(self.history))
            if not remaining_prizes:
                self.prize_var.set("所有内容已经抽取完毕")
                return
            selected_prize = remaining_prizes[randint(0, len(remaining_prizes) - 1)]
        else:
            selected_prize = self.prizes[randint(0, len(self.prizes) - 1)]

        self.prize_var.set(selected_prize)

        self.history.append(selected_prize)

        self.update_history()

        self.update_probability()

    def update_pool(self):
        if self.prizes:
            self.pool_var.set("当前池中内容：" + ', '.join(self.prizes))
        else:
            self.pool_var.set("无内容")

    def update_history(self):
        history_str = ', '.join(self.history)

        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)

        self.history_text.insert(tk.END, history_str)

        self.history_text.config(state=tk.DISABLED)

    def update_probability(self):
        total_spins = len(self.history)
        for prize in self.prizes:
            prize_count = self.history.count(prize)
            probability = (prize_count / total_spins) * 100 if total_spins > 0 else 0
            self.probabilities[prize] = probability

        prob_str = ', '.join(f"{prize}: {prob:.2f}%" for prize, prob in self.probabilities.items())

        self.prob_label.config(text="概率: " + prob_str)


if __name__ == "__main__":
    root = tk.Tk()
    app = LuckyDrawApp(root)
    root.mainloop()
