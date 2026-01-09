# importing all libraries
import tkinter as T
from tkinter import messagebox as Mb
from matplotlib.figure import Figure as M
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as F
import json as J
import os as o
import time as Tm
import threading as Th
from tkinter import filedialog as Fd
from PIL import Image as I, ImageTk as It
import shutil as S
from datetime import datetime as D
import scipy.constants as Sc

# initializing root GUI
root = T.Tk()
root.title('    Quizzer')
root.geometry('900x600')
root.resizable(False, False)
root.iconbitmap('./assets/ico_converted.ico')

# initializing widgets container and global question state
widgets = []
q_no = 1

# function to save results and new quizes
def save(data, file):
    with open(file, 'w') as file:
        J.dump(data, file, indent=4)

# function to add results into loaded results
def add(new_result):
    results = load('./data/results.json')
    results.append(new_result)
    save(results, './data/results.json')

# function to add new quizes into loaded quizes
def addq(new_quiz):
    results = load('./data/quizes.json')
    results.append(new_quiz)
    save(results, './data/quizes.json')

# function to load saved files
def load(file):
    if not o.path.exists(file):
        with open(file, 'w') as f:
            J.dump([], f)
            return []
    with open(file, 'r') as file:
        return J.load(file)

def select_image():
    file_path =  Fd.askopenfilename(
        filetypes=[('Image Files', '*.png *.jpg *.jpeg *.gif' )]
    )
    if file_path:
        filename = o.path.basename(file_path)
        dest_path = o.path.join('./assets', filename)
        S.copy(file_path, dest_path)
        return dest_path

quizes =  load('./data/quizes.json')

to_use = []

for q in quizes:
    to_use.append(
        {
         'title':q['title'],
         't': q['t'],
         'questions':[]   
        }
    )
    for idx, qs in enumerate(q['questions']):
        to_use[-1]['questions'].append({
            'q':qs['q'],
            'images':qs['image'],
            'options':qs['options'],
            'selected_option':T.StringVar(value='z')
        })

results = load('./data/results.json')

def unpack(widgets:list):
    for w in widgets:
        if len(w) == 1:
            w[0].pack()

        elif len(w) > 3:
            w[0].pack(side=w[3], padx=w[1], pady=w[2])

        else:
            w[0].pack(padx=w[1], pady=w[2])

        w[0].pack_propagate(False)

def clear(widgets:list):
    for w in widgets:
        w[0].destroy()
    widgets.clear()

class Timer():
    def __init__(self, mins, on_tick = None, on_finish = None):
        self.total = int(mins * 60)
        self.remaining = self.total
        self.running = False
        self._thread = None
        self.start_time = None
        self.end_time = None
        self.on_tick = on_tick
        self.on_finish = on_finish        

    def start(self):
        if not self.running:
            self.running = True
            self.start_time = Tm.time()
            self._thread = Th.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()
        
    def _run(self):
        while self.running and self.remaining > 0:
            Tm.sleep(1)
            self.remaining -= 1
            if self.on_tick:
                minutes = self.remaining//60
                seconds = self.remaining % 60
                tick = f'{minutes:02}:{seconds:02}'
                self.on_tick(tick)
        if  self.on_finish:
            self.end_time = Tm.time()
            self.on_finish(self.elapsed())
            self.running = False

    def stop(self):
        self.running = False
        self.end_time = Tm.time()

    def elapsed(self):
        minutes = self.total//60
        seconds = self.total % 60
        return f'{minutes:02}:{seconds:02}'
    
    def get_time(self):
        used = self.total - self.remaining
        minutes = used//60
        seconds = used % 60
        return f'{minutes:02}:{seconds:02}'

def Home_page():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    home_frame = [T.Frame(root, height=400, width=850, bd=1, relief='solid', bg='light yellow'), 0, 25]
    widgets.append(home_frame)
    credit_frame = [T.Frame(root, height=50, width=900, bg='blue'), 0, 0]
    widgets.append(credit_frame)
    take_btn_frame = [T.Canvas(home_frame[0], bg='light yellow', height=100, width=100), 106.25, (0, 0), 'left']
    take_btn_frame[0].create_oval(5, 5, 95, 95, fill='red', outline='black', width=2)
    widgets.append(take_btn_frame)
    create_btn_frame = [T.Canvas(home_frame[0], bg='light yellow', height=100, width=100), 106.25, (0, 0), 'right']
    create_btn_frame[0].create_oval(5, 5, 95, 95, fill='red', outline='black', width=2)
    widgets.append(create_btn_frame)
    results_btn_frame = [T.Canvas(home_frame[0], bg='light yellow', height=100, width=100), 0, 150, 'top']
    results_btn_frame[0].create_oval(5, 5, 95, 95, fill='red', outline='black', width=2)
    widgets.append(results_btn_frame)
    take_img = I.open('./assets/tae.png')
    take_img = take_img.resize((50, 50))
    t_photo = It.PhotoImage(take_img)
    take_btn = [T.Button(take_btn_frame[0], image=t_photo, command= lambda: Quiz_menu(), highlightthickness=0, cursor='hand2', activebackground='dark red', borderwidth=0, bg='red'), 2.5, (25, 0)]
    take_btn[0].image = t_photo
    widgets.append(take_btn)
    res_img = I.open('./assets/res.png')
    res_img = res_img.resize((50, 50))
    r_photo = It.PhotoImage(res_img)
    results_btn = [T.Button(results_btn_frame[0], image=r_photo, command= lambda: Results_menu(), highlightthickness=0, cursor='hand2', activebackground='dark red', borderwidth=0, bg='red'), 2.5, (25, 0)]
    results_btn[0].image = r_photo
    widgets.append(results_btn)
    cre_img = I.open('./assets/add.png')
    cre_img = cre_img.resize((50, 50))
    c_photo = It.PhotoImage(cre_img)
    create_btn = [T.Button(create_btn_frame[0], image=c_photo, command= lambda: Create_page(), highlightthickness=0, cursor='hand2', activebackground='dark red', borderwidth=0, bg='red'), 2.5, (25, 0)]
    create_btn[0].image = c_photo
    widgets.append(create_btn)
    creators = [T.Label(credit_frame[0], text='Musa Abdulrahman | | Adepoju Habeeb | | Achadu Anibe | | Adekeye Adewale | | Ayanbisi Abdulhaleem | | Adebiyi David | | Lawal Ireoluwa', foreground='white', bg='blue'), 0, 15]
    widgets.append(creators)
    unpack(widgets)

def Quiz_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    menu_frame = [T.Canvas(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    # canvas = menu_frame[0]
    # scrollbar = [T.Scrollbar(root, orient='vertical', command=canvas.yview)]
    # scrollframe = [T.Frame(canvas)]
    # scrollframe[0].bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    # canvas.create_window((25, 110), window=scrollframe, anchor='nw')
    # canvas.configure(yscrollcommand=scrollbar[0].set)
    # scrollbar[0].pack(side='right', fill='y')
    widgets.append(menu_frame)
    # canvas.pack(side='left', fill='both', expand=True)
    # widgets.append(scrollbar)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', text='🏠', font=32, command=lambda: Home_page()), 10, 10, 'left']
    widgets.append(home_btn)
    header_menu_label = [T.Label(header_menu_frame[0], text='Quiz Menu', justify='center', font=['serif', 14], foreground='white', bg='blue'), 0, 15]
    widgets.append(header_menu_label)
    q = 1
    for quiz in to_use:
        quiz_btn = [T.Button(menu_frame[0], text=f'Quiz {q}Title: {quiz['title']}                         Time allowed: {quiz['t']}{'min' if quiz['t'] == 1 else 'mins'}                         Number of Questions: {len(quiz['questions'])}', foreground='white', bd=1, relief='solid', highlightthickness=0, activebackground='dark blue', height=3, width= 115, cursor='hand2', bg='gray', command=lambda q=q: Quiz_page(q)), 0, (20, 5)]
        widgets.append(quiz_btn)
        q = q + 1
    unpack(widgets)

def Results_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    menu_frame = [T.Canvas(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    # canvas = menu_frame[0]
    # scrollbar = [T.Scrollbar(root, orient='vertical', command=canvas.yview)]
    # scrollframe = [T.Frame(canvas)]
    # scrollframe[0].bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
    # canvas.create_window((25, 110), window=scrollframe, anchor='nw')
    # canvas.configure(yscrollcommand=scrollbar[0].set)
    # scrollbar[0].pack(side='right', fill='y')
    widgets.append(menu_frame)
    # widgets.append(scrollbar)
    # canvas.pack(side='left', fill='both', expand=True)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', text='🏠', font=32, command=lambda: Home_page()), 10, 10, 'left']
    widgets.append(home_btn)
    header_menu_label = [T.Label(header_menu_frame[0], text='Results Menu', justify='center', font=['serif', 14], foreground='white', bg='blue'), 0, 15]
    widgets.append(header_menu_label)
    r = 1
    for result in results:
        result_btn = [T.Button(menu_frame[0], text=f'Result {r} Title: {result['title']}                            Score: {result['result']}                            Time: {result['time']}                            Date: {result['date']}', bd=1, relief='solid', foreground='black', highlightthickness=0, activebackground='dark blue', cursor='hand2', borderwidth=1, bg='yellow', height=3, width= 115, command=lambda result=result: Result_page(result)), 0, (20, 5)]
        widgets.append(result_btn)
        r = r + 1
    unpack(widgets)

def Create_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', text='🏠', font=32, command=lambda: Home_page()), 10, 10, 'left']
    widgets.append(home_btn)
    header_menu_label = [T.Label(header_menu_frame[0], text='Create a Quiz', justify='center', font=['serif', 14], foreground='white', bg='blue'), 0, 15]
    widgets.append(header_menu_label)
    left_menu = [T.Frame(menu_frame[0], height=400, width=400, bg='light yellow', border=5), 20, 10, 'left']
    widgets.append(left_menu)
    header_left_menu = [T.Frame(left_menu[0], height=20, width=400, bg='blue')]
    widgets.append(header_left_menu)
    header_left_label = [T.Label(header_left_menu[0], text='Add to an Existing Title', foreground='white', bg='blue')]
    widgets.append(header_left_label)
    q = 1
    for uiz, quiz in enumerate(to_use):
        quiz_btn = [T.Button(left_menu[0], text=f'Quiz {q}; Title: {quiz['title']}; Number of Questions: {len(quiz['questions'])}', command=lambda uiz=uiz: Create_page(uiz), height=5, width= 50), 0, (20, 5)]
        widgets.append(quiz_btn)
        q = q + 1
    right_add = [T.Button(menu_frame[0], height=200, width=350, text='+ \n Create New Title', font=['serif', 15], command=lambda: Create_page(quizes[-1])), 20, 125, 'right']
    widgets.append(right_add)
    unpack(widgets)

def Quiz_page(quiz_id):
    clear(widgets)
    present_test = []
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    time = [T.Label(header_frame[0], font=('Ariel', 24)), 40, 0, 'right']
    widgets.append(time)
    def tick(remaining):
        if time[0]:
            time[0].config(text=f'{remaining}')

    def finished(elapsed):
        submit = Mb.showinfo('Time Up', 'You are out of time')
        for z in to_use[quiz_id - 1]['questions']:
            z['selected_option'] = T.StringVar(value='z')
        compile_result(quiz_id - 1)
        q_no = 1
        present_test.clear()

    Tmer = Timer(quizes[quiz_id - 1]['t'], tick, finished)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    menu_frame = [T.Frame(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    btn_back = [T.Button(header_menu_frame[0], height=5, width=10, text='Back', foreground='white', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='red', command=lambda: back()), 10, 2.5, 'left']
    widgets.append(btn_back)
    btn_previous = [T.Button(header_menu_frame[0], height=5, width=10, text='⬅', foreground='black', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='light gray', command=lambda: left()), 10, 2.5, 'left']
    widgets.append(btn_previous)
    btn_submit = [T.Button(header_menu_frame[0], height=5, width=10, text='Submit', foreground='white', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='green', command=lambda:submit()), 10, 2.5, 'right']
    widgets.append(btn_submit)
    btn_next = [T.Button(header_menu_frame[0], height=5, width=10, text='➡', foreground='black', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='light gray', command=lambda: right()), 10, 2.5, 'right']
    widgets.append(btn_next)
    def left():
        global q_no
        if q_no == 1:
            confirm = Mb.askyesno('Are you sure you want to leave?')

            if confirm:
                Tmer.stop()
                q_no = 1
                Quiz_menu()

        else:
            q_no = q_no - 1
            question_label[0].config(text=f'{q_no}.) {to_use[quiz_id - 1]['questions'][q_no - 1]['q']}')
            option_label1[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}')
            option_check1[0].config(variable=present_test[q_no - 1])
            option_label2[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}')
            option_check2[0].config(variable=present_test[q_no - 1])
            option_label3[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}')
            option_check3[0].config(variable=present_test[q_no - 1])
            option_label4[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}')
            option_check4[0].config(variable=present_test[q_no - 1])

    def back():
        global q_no
        confirm = Mb.askyesno('Leave?', 'You are about to quit the quiz \n Proceed?')
        if confirm:
            Tmer.stop()
            q_no = 1
            Quiz_menu()

    def submit():
        global q_no
        submit = Mb.askyesno('Submit?', 'You are about to submit \n Proceed?')
        if submit:
            # Tmer.get_time()
            for z in to_use[quiz_id - 1]['questions']:
                z['selected_option'] = T.StringVar(value='z')
            compile_result(quiz_id - 1)
            q_no = 1
            present_test.clear()
            # time.stop()

    def right():
        global q_no
        if q_no == len(to_use[quiz_id - 1]['questions']):
           submit = Mb.askyesno('Submit?')

           if submit:
                for z in to_use[quiz_id - 1]['questions']:
                    z['selected_option'] = T.StringVar(value='z')
                compile_result(quiz_id - 1)
                q_no = 1
                present_test.clear()

        else:
            q_no = q_no + 1    
            question_label[0].config(text=f'{q_no}.) {to_use[quiz_id - 1]['questions'][q_no - 1]['q']}')
            option_label1[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}')
            option_check1[0].config(variable=present_test[q_no - 1])
            option_label2[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}')
            option_check2[0].config(variable=present_test[q_no - 1])
            option_label3[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}')
            option_check3[0].config(variable=present_test[q_no - 1])
            option_label4[0].config(text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}')
            option_check4[0].config(variable=present_test[q_no - 1])

    question_label = [T.Label(menu_frame[0], height=1, text=f'{q_no}.) {to_use[quiz_id - 1]['questions'][q_no - 1]['q']}', font=20, bg='light yellow', anchor='w'), (0, 00), (20, 0), 'top']
    widgets.append(question_label)
    options_frame = [T.Frame(menu_frame[0], bg='light yellow', height=275, width=400), (0, 400), 15, 'bottom']
    widgets.append(options_frame)
    option_frame1 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame1)
    option_frame2 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame2)
    option_frame3 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame3)
    option_frame4 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame4)
    for qsn in to_use[quiz_id - 1]['questions']:
        present_test.append(T.StringVar(value='Z'))
    option_check1 = [T.Radiobutton(option_frame1[0], variable=present_test[q_no - 1], value='A'), 0, 0, 'left']
    widgets.append(option_check1)
    option_check2 = [T.Radiobutton(option_frame2[0], variable=present_test[q_no - 1], value='B'), 0, 0, 'left']
    widgets.append(option_check2)
    option_check3 = [T.Radiobutton(option_frame3[0], variable=present_test[q_no - 1], value='C'), 0, 0, 'left']
    widgets.append(option_check3)
    option_check4 = [T.Radiobutton(option_frame4[0], variable=present_test[q_no - 1], value='D'), 0, 0, 'left']
    widgets.append(option_check4)
    option_label1 = [T.Label(option_frame1[0], bg='light yellow', text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}'), 10, 0, 'left']
    widgets.append(option_label1)
    option_label2 = [T.Label(option_frame2[0], bg='light yellow', text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}'), 10, 0, 'left']
    widgets.append(option_label2)
    option_label3 = [T.Label(option_frame3[0], bg='light yellow', text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}'), 10, 0, 'left']
    widgets.append(option_label3)
    option_label4 = [T.Label(option_frame4[0], bg='light yellow', text=f'{to_use[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}'), 10, 0, 'left']
    widgets.append(option_label4)
    unpack(widgets)

    def compile_result(quiz_id):
        selected_options = []
        correct_answers = []
        check_answers = []
        total_result = 0

        for present in present_test:
            selected_options.append(present.get())

        for q in to_use[quiz_id]['questions']:
            for i, optn in enumerate(q['options']):
                if True in optn:
                    if i == 0:
                        correct_answers.append('A')

                    elif i == 1:
                        correct_answers.append('B')

                    elif i == 2:
                        correct_answers.append('C')

                    elif i == 3:
                        correct_answers.append('D')

        for id, answers in enumerate(correct_answers):
            if answers == selected_options[id]:
                check_answers.append(True)

            else:
                check_answers.append(False)
        for boolean in check_answers:
            if boolean:
                total_result = total_result + 1

        today = D.today()
        formatted = today.strftime("%d/%m/%Y")

        result_percentage =f'{int(total_result/len(to_use[quiz_id]['questions']) * 100)}%'
        new_results =  {
            'title': to_use[quiz_id]['title'],
            'result': result_percentage,
            'time': Tmer.get_time(),
            'date': formatted,
            'options': check_answers
        }

        results.append(new_results)
        add(new_results)
        Result_page(results[-1])
    Tmer.start()
    # time.start()

def Result_page(result):
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    menu_frame = [T.Frame(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    questions_frame = [T.Frame(menu_frame[0], height=455, width=300, bg='white'), (0, 5), 10, 'right']
    widgets.append(questions_frame)
    history_frame = [T.Frame(menu_frame[0], height=75, width=450, bg='white', border=10, borderwidth=15), (0, 50), (0, 10), 'bottom']
    widgets.append(history_frame)
    header_history_frame = [T.Frame(history_frame[0], height=15, width=450, bg='blue')]
    widgets.append(header_history_frame)
    header_history_label = [T.Label(header_history_frame[0], text='Results Under the Same Title', foreground='white', bg='blue')]
    widgets.append(header_history_label)
    back_btn = [T.Button(header_menu_frame[0], height=30, width=5, text='🏠', bg='red', font=32, command=lambda: Results_menu()), 10, 10, 'left']
    widgets.append(back_btn)
    sizes = [int(result['result'].strip('%')), 100 - int(result['result'].strip('%'))]
    colors = ['green', 'red']
    fig = M(figsize=(4, 4), dpi=100)
    ax = fig.add_subplot(111)
    wedges, texts, autotexts = ax.pie(sizes, startangle=90, colors=colors, autopct='%1.f%%')
    for text in autotexts:
        text.set_color('white')
    ax.axis('equal')
    result_canvas = [F(fig, master=menu_frame[0]).get_tk_widget(), (0, 50), (30, 0)]
    widgets.append(result_canvas)
    time = [T.Label(questions_frame[0], font=('Ariel', 16), text=f'Time used: {result['time']}s'), 0, 0, 'bottom']
    widgets.append(time)
    for ix, answers in enumerate(result['options']):
        text = ''
        color = ''
        if answers:
            text = f'{ix+1}. ✅'
            color = 'green'

        else:
            text = f'{ix+1}. ❌'
            color = 'red'
        answer_label = [T.Label(questions_frame[0], text=text, bg='white', foreground=color), (0, 250), 5]
        widgets.append(answer_label)
    for res in results:
        if res['title'] == result['title']:
            history = [T.Label(history_frame[0], text=f'{res['title']}________{res['result']}_______{res['date']}', bg='white', anchor='w')]
            widgets.append(history)

    unpack(widgets)

def Create_page():
    clear(widgets)
    options = T.StringVar(value='z')
    image_path = ''
    questions = []
    def add():
        global q_no
        questions.append({
            'q':question_label[0].get(),
            'image': image_path,
            'options':[
                [True if options.get() == 'A' else False, option_label1[0].get()],
                [True if options.get() == 'B' else False, option_label2[0].get()],
                [True if options.get() == 'C' else False, option_label3[0].get()],
                [True if options.get() == 'D' else False, option_label4[0].get()],
            ]
        })
        options.set('z')
        question_label[0].delete(0, 'end')
        option_label1[0].delete(0, 'end')
        option_label2[0].delete(0, 'end')
        option_label3[0].delete(0, 'end')
        option_label4[0].delete(0, 'end')
        label[0].config(text=f'Question {len(questions) + 1}:')
        # image_label[0].config(image=None)
        # image_label[0].image = None
        q_no = q_no + 1
    
    def done():
        global q_no
        quiz = {
            'title':title_label[0].get(),
            't': int(time[0].get()),
            'questions':questions
        }
        addq(quiz)
        quizes.append(quiz)
        to_use.append(quiz)
        Quiz_menu()
        q_no = 1
    
    def right():
        global q_no
        if q_no < len(questions):
            q_no = q_no + 1
            question_label[0].delete(0, 'end')
            option_label1[0].delete(0, 'end')
            option_label2[0].delete(0, 'end')
            option_label3[0].delete(0, 'end')
            option_label4[0].delete(0, 'end')
            label[0].config(text=f'Question {q_no}:')
            question_label[0].insert(0, questions[q_no-1]['q'])
            option_label1[0].insert(0, questions[q_no-1]['options'][0][1])
            option_label2[0].insert(0, questions[q_no-1]['options'][1][1])
            option_label3[0].insert(0, questions[q_no-1]['options'][2][1])
            option_label4[0].insert(0, questions[q_no-1]['options'][3][1])
            if option_label1[0].insert(0, questions[q_no-1]['options'][0][0]):
                options.set('A')
            if option_label1[0].insert(0, questions[q_no-1]['options'][1][0]):
                options.set('B')
            if option_label1[0].insert(0, questions[q_no-1]['options'][2][0]):
                options.set('C')
            if option_label1[0].insert(0, questions[q_no-1]['options'][3][0]):
                options.set('D')
            # dspl(questions[q_no-1]['image'])

        if q_no == len(questions):
            q_no = q_no + 1
            question_label[0].delete(0, 'end')
            option_label1[0].delete(0, 'end')
            option_label2[0].delete(0, 'end')
            option_label3[0].delete(0, 'end')
            option_label4[0].delete(0, 'end')
            label[0].config(text=f'Question {q_no}:')
            options.set('Z')
            # image_label[0].config(image=None)
            # image_label[0].image = None

    def left():
        global q_no
        if q_no != 1:
            q_no = q_no - 1
            question_label[0].delete(0, 'end')
            option_label1[0].delete(0, 'end')
            option_label2[0].delete(0, 'end')
            option_label3[0].delete(0, 'end')
            option_label4[0].delete(0, 'end')
            label[0].config(text=f'Question {q_no}:')
            question_label[0].insert(0, questions[q_no-1]['q'])
            option_label1[0].insert(0, questions[q_no-1]['options'][0][1])
            option_label2[0].insert(0, questions[q_no-1]['options'][1][1])
            option_label3[0].insert(0, questions[q_no-1]['options'][2][1])
            option_label4[0].insert(0, questions[q_no-1]['options'][3][1])
            if option_label1[0].insert(0, questions[q_no-1]['options'][0][0]):
                options.set('A')
            if option_label1[0].insert(0, questions[q_no-1]['options'][1][0]):
                options.set('B')
            if option_label1[0].insert(0, questions[q_no-1]['options'][2][0]):
                options.set('C')
            if option_label1[0].insert(0, questions[q_no-1]['options'][3][0]):
                options.set('D')
            # dspl(questions[q_no-1]['image'])

    def remove():
        global q_no
        if len(questions) > 0:
            questions.pop(q_no - 1)
            q_no = q_no - 1
            question_label[0].delete(0, 'end')
            option_label1[0].delete(0, 'end')
            option_label2[0].delete(0, 'end')
            option_label3[0].delete(0, 'end')
            option_label4[0].delete(0, 'end')
            # image_label[0].config(image=None)
            # image_label[0].image = None

    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    time_frame = [T.Frame(header_frame[0], width=300, height=50, bg='light blue'), 40, 0, 'right']
    widgets.append(time_frame)
    time = [T.Entry(time_frame[0], font=('Ariel', 24), width=5), 0, 0, 'right']
    widgets.append(time)
    time_label = [T.Label(time_frame[0], text='Time:', foreground='blue', bg='light blue', font=('Ariel', 24)), 0, 0, 'left']
    widgets.append(time_label)
    time_label1 = [T.Label(time_frame[0], text='(in minutes)', foreground='blue', bg='light blue', font=('Ariel', 14)), 0, 0, 'left']
    widgets.append(time_label1)
    logo_img = I.open('./assets/ico.png')
    logo_img = logo_img.resize((50, 65))
    photo = It.PhotoImage(logo_img)
    logo_label = [T.Label(header_frame[0], image=photo, bg='light blue'), (30, 0), 0, 'left']
    logo_label[0].image = photo
    widgets.append(logo_label)
    menu_frame = [T.Frame(root, height=475, width=850, bd=1, relief='solid', bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    btn_back = [T.Button(header_menu_frame[0], height=5, width=10, text='Back', foreground='white', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='red', command=lambda:Home_page()), 10, 2.5, 'left']
    widgets.append(btn_back)
    btn_remove = [T.Button(header_menu_frame[0], height=5, width=10, text='-', command=lambda:remove()), 10, 2.5, 'left']
    widgets.append(btn_remove)
    btn_previous = [T.Button(header_menu_frame[0], height=5, width=10, text='<', foreground='black', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='light gray', command=lambda:left()), 10, 2.5, 'left']
    widgets.append(btn_previous)
    btn_done = [T.Button(header_menu_frame[0], height=5, width=10, text='Done', foreground='white', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='green', command=lambda:done()), 10, 2.5, 'right']
    widgets.append(btn_done)
    btn_add = [T.Button(header_menu_frame[0], height=5, width=10, text='+', command=lambda:add()), 10, 2.5, 'right']
    widgets.append(btn_add)
    btn_next = [T.Button(header_menu_frame[0], height=5, width=10, text='>', foreground='black', highlightthickness=0, activebackground='dark blue', borderwidth=0, bg='light gray', command=lambda:right()), 10, 2.5, 'right']
    widgets.append(btn_next)
    title_frame = [T.Frame(header_menu_frame[0], width=250, height=50, bg='blue'), 10, 15, 'right']
    widgets.append(title_frame)
    title_label = [T.Entry(title_frame[0], width=30), 0, 0, 'right']
    widgets.append(title_label)
    title_entry = [T.Label(title_frame[0], bg='blue', fg='white', text='Quiz Title:'), 5, 0, 'left']
    widgets.append(title_entry)
    label = [T.Label(menu_frame[0], text=f'Question {q_no}:', bg='light yellow', font=15), 0, (5, 0)]
    widgets.append(label)
    question_label = [T.Entry(menu_frame[0], width=100, bg='light yellow'), (0, 00), (20, 0), 'top']
    widgets.append(question_label)
    options_frame = [T.Frame(menu_frame[0], bg='light yellow', height=275, width=400), (0, 400), 15, 'bottom']
    widgets.append(options_frame)
    option_frame1 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame1)
    option_frame2 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame2)
    option_frame3 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame3)
    option_frame4 = [T.Frame(options_frame[0], bg='light yellow' ,height=40, width=400), 0, 7.5]
    widgets.append(option_frame4)
    option_check1 = [T.Radiobutton(option_frame1[0], variable=options, value='A'), 0, 0, 'left']
    widgets.append(option_check1)
    option_check2 = [T.Radiobutton(option_frame2[0], variable=options, value='B'), 0, 0, 'left']
    widgets.append(option_check2)
    option_check3 = [T.Radiobutton(option_frame3[0], variable=options, value='C'), 0, 0, 'left']
    widgets.append(option_check3)
    option_check4 = [T.Radiobutton(option_frame4[0], variable=options, value='D'), 0, 0, 'left']
    widgets.append(option_check4)
    option_label1 = [T.Entry(option_frame1[0], width=40, bg='light yellow'), 10, 0, 'left']
    widgets.append(option_label1)
    option_label2 = [T.Entry(option_frame2[0], width=40, bg='light yellow'), 10, 0, 'left']
    widgets.append(option_label2)
    option_label3 = [T.Entry(option_frame3[0], width=40, bg='light yellow'), 10, 0, 'left']
    widgets.append(option_label3)
    option_label4 = [T.Entry(option_frame4[0], width=40, bg='light yellow'), 10, 0, 'left']
    widgets.append(option_label4)
    image_frame = [T.Frame(menu_frame[0])]
    # image_frame[0].place(x=425, y=150, width=400, height=275, in_=menu_frame[0])
    # # widgets.append(image_frame)
    image_label = [T.Label(image_frame[0], height=275, width=400)]
    # widgets.append(image_label)
    image_btn = [T.Button(menu_frame[0], command=lambda: dspl(image_path, t=1), text=' Add Image')]
    # # widgets.append(image_btn)
    # image_btn[0].place(x=425, y=425)

    def dspl(fu, t=0):
        if t == 0:
            img = I.open(fu)
            img = img.resize((400, 250))
            photo = It.PhotoImage(img)
            image_label[0].config(image=photo)
            image_label[0].image = photo
        if t == 1:
            img = I.open(select_image())
            img = img.resize((400, 250))
            photo = It.PhotoImage(img)
            image_label[0].config(image=photo)
            image_label[0].image = photo
    unpack(widgets)

Home_page()

root.mainloop()