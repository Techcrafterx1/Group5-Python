import tkinter as T
from tkinter import messagebox as Mb

root = T.Tk()
root.title('Quizzer')
root.geometry('900x600')
root.resizable(False, False)

widgets = []
q_no = 1
present_test = ['Z']

quizes = [
    {
    'title': 'English Studies',
    'questions': [
        {
            'q':'A is for?',
            'images':None,
            'options': [
                [False, 'Ball'],
                [True, 'Apple'],
                [False, 'Carrot'],
                [False, 'Banana']
            ],
            'selected_option':T.StringVar(value='Z')
        },
        {
            'q':'B is for?',
            'images':None,
            'options':[
                [False, 'Plantain'],
                [False, 'Watermelon'],
                [False, 'Zebra'],
                [True, 'Basket']
            ],
            'selected_option':T.StringVar(value='Z')
        }
    ]
    },
    {
    'title': 'Mathematics',
    'questions': [
        {
            'q':'1 + 1 =',
            'images':None,
            'options':[
                [False, '3'],
                [False, '9'],
                [False, '1'],
                [True, '2']
            ],
            'selected_option':T.StringVar(value='Z')
        },
        {
            'q':'Round up {pi} to the nearest 2 D.P',
            'images':None,
            'options':[
                [True, '3.14'],
                [False, '3.1'],
                [False, '3'],
                [False, '3.143']
            ],
            'selected_option':T.StringVar(value='Z')
        },
        {
            'q':'What determines an Even function in sinusoidal fourier series? When ...',
            'images':None,
            'options':[
                [False, 'f(x) = 0'],
                [True, 'f(x) = f(-x)'],
                [False, 'f(x) = -g(x)'],
                [False, 'The derivatives are discontinuous']
            ],
            'selected_option':T.StringVar(value='Z')
        }
    ]
    }
]

results = [
    {
        'title':'Mathematics',
        'result': '67%',
        'date': '24/12/2025',
        'options':[True, True, False]
    },
    {
        'title':'English Studies',
        'result': '0%',
        'date': '23/12/2025',
        'options':[False, False, False]
    },
]

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

def Home_page():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    home_frame = [T.Frame(root, height=400, width=850,  bg='light yellow'), 0, 25]
    widgets.append(home_frame)
    credit_frame = [T.Frame(root, height=50, width=900, bg='blue'), 0, 0]
    widgets.append(credit_frame)
    take_btn_frame = [T.Frame(home_frame[0], bg='red', height=100, width=100), 106.25, (0, 0), 'left']
    widgets.append(take_btn_frame)
    create_btn_frame = [T.Frame(home_frame[0], bg='red', height=100, width=100), 106.25, (0, 0), 'right']
    widgets.append(create_btn_frame)
    results_btn_frame = [T.Frame(home_frame[0], bg='red', height=100, width=100), 0, 150, 'top']
    widgets.append(results_btn_frame)
    take_btn = [T.Button(take_btn_frame[0], text='Take a Quiz', command= lambda: Quiz_menu()), 2.5, 40]
    widgets.append(take_btn)
    results_btn = [T.Button(results_btn_frame[0], text='View Past Results', command= lambda: Results_menu()), 2.5, 40]
    widgets.append(results_btn)
    create_btn = [T.Button(create_btn_frame[0], text='Create New Quiz', command= lambda: Create_menu()), 2.5, 40]
    widgets.append(create_btn)
    unpack(widgets)

def Quiz_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', command=lambda: Home_page()), 10, 10, 'left']
    widgets.append(home_btn)
    header_menu_label = [T.Label(header_menu_frame[0], text='Quiz Menu', justify='center', font=['serif', 14], foreground='white', bg='blue'), 0, 15]
    widgets.append(header_menu_label)
    q = 1
    for quiz in quizes:
        quiz_btn = [T.Button(menu_frame[0], text=f'Quiz {q}; Title: {quiz['title']}; Number of Questions: {len(quiz['questions'])}', height=5, width= 115, command=lambda q=q: Quiz_page(q)), 0, (20, 5)]
        widgets.append(quiz_btn)
        q = q + 1
    unpack(widgets)

def Results_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', command=lambda: Home_page()), 10, 10, 'left']
    widgets.append(home_btn)
    header_menu_label = [T.Label(header_menu_frame[0], text='Results Menu', justify='center', font=['serif', 14], foreground='white', bg='blue'), 0, 15]
    widgets.append(header_menu_label)
    r = 1
    for result in results:
        result_btn = [T.Button(menu_frame[0], text=f'Result {r} Title: {result['title']}; Score: {result['result']}; Date: {result['date']}', height=5, width=115, command=lambda result=result: Result_page(result)), 0, (20, 5)]
        widgets.append(result_btn)
        r = r + 1
    unpack(widgets)

def Create_menu():
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    home_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', command=lambda: Home_page()), 10, 10, 'left']
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
    for quiz in quizes:
        quiz_btn = [T.Button(left_menu[0], text=f'Quiz {q}; Title: {quiz['title']}; Number of Questions: {len(quiz['questions'])}', height=5, width= 50), 0, (20, 5)]
        widgets.append(quiz_btn)
        q = q + 1
    right_add = [T.Button(menu_frame[0], height=200, width=350, text='+ \n Create New Title', font=['serif', 15]), 20, 125, 'right']
    widgets.append(right_add)
    unpack(widgets)

def Quiz_page(quiz_id):
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bg='light yellow'), 0, 20]
    widgets.append(menu_frame)
    header_menu_frame = [T.Frame(menu_frame[0], height=50, width=850, bg='blue')]
    widgets.append(header_menu_frame)
    # header_menu_label = [T.Label(header_menu_frame[0], text=f'{quizes[quiz_id - 1]['title']}'), 0, 10]
    # widgets.append(header_menu_label)
    btn_previous = [T.Button(header_menu_frame[0], height=5, width=10, text='⬅', command=lambda: left()), 10, 2.5, 'left']
    widgets.append(btn_previous)
    btn_next = [T.Button(header_menu_frame[0], height=5, width=10, text='➡', command=lambda: tfel()), 10, 2.5, 'right']
    widgets.append(btn_next)
    def left():
        global q_no
        if q_no == 1:
            confirm = Mb.askyesno('Are you sure you want to leave?')
            if confirm:
                Quiz_menu()
                q_no = 1
        else:
            q_no = q_no - 1
            question_label[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['q']}')
            option_label1[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}')
            option_check1[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label2[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}')
            option_check2[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label3[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}')
            option_check3[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label4[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}')
            option_check4[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])

    def tfel():
        global q_no
        if q_no == len(quizes[quiz_id - 1]['questions']):
           submit = Mb.askyesno('Submit?')
           if submit:
               compile_result(quiz_id - 1)
               q_no = 1
               for z in quizes[quiz_id - 1]['questions']:
                   z['selected_option'] = T.StringVar(value='z')

        else:
            q_no = q_no + 1    
            question_label[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['q']}')
            option_label1[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}')
            option_check1[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label2[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}')
            option_check2[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label3[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}')
            option_check3[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])
            option_label4[0].config(text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}')
            option_check4[0].config(variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'])

    question_label = [T.Label(menu_frame[0], height=1, text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['q']}', font=20, bg='light yellow', anchor='w'), (0, 00), (20, 0), 'top']
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
    option_check1 = [T.Radiobutton(option_frame1[0], variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'], value='A'), 0, 0, 'left']
    widgets.append(option_check1)
    option_check2 = [T.Radiobutton(option_frame2[0], variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'], value='B'), 0, 0, 'left']
    widgets.append(option_check2)
    option_check3 = [T.Radiobutton(option_frame3[0], variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'], value='C'), 0, 0, 'left']
    widgets.append(option_check3)
    option_check4 = [T.Radiobutton(option_frame4[0], variable=quizes[quiz_id - 1]['questions'][q_no - 1]['selected_option'], value='D'), 0, 0, 'left']
    widgets.append(option_check4)
    option_label1 = [T.Label(option_frame1[0], bg='light yellow', text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][0][1]}'), 10, 0, 'left']
    widgets.append(option_label1)
    option_label2 = [T.Label(option_frame2[0], bg='light yellow', text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][1][1]}'), 10, 0, 'left']
    widgets.append(option_label2)
    option_label3 = [T.Label(option_frame3[0], bg='light yellow', text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][2][1]}'), 10, 0, 'left']
    widgets.append(option_label3)
    option_label4 = [T.Label(option_frame4[0], bg='light yellow', text=f'{quizes[quiz_id - 1]['questions'][q_no - 1]['options'][3][1]}'), 10, 0, 'left']
    widgets.append(option_label4)
    unpack(widgets)

    def compile_result(quiz_id):
        selected_options = []
        correct_answers = []
        check_answers = []
        total_result = 0

        for q in quizes[quiz_id]['questions']:
            selected_options.append(q['selected_option'].get())
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

        result_percentage =f'{int(total_result/len(quizes[quiz_id]['questions']) * 100)}%'
        new_results =  {
            'title': quizes[quiz_id]['title'],
            'result': result_percentage,
            'date': '23/12/2025',
            'options': check_answers
        }
        results.append(new_results)
        Result_page(results[-1])

def Result_page(result):
    clear(widgets)
    header_frame = [T.Frame(root, height=100, width=900, bg='light blue'), 0, 0]
    widgets.append(header_frame)
    menu_frame = [T.Frame(root, height=475, width=850, bg='light yellow'), 0, 20]
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
    back_btn = [T.Button(header_menu_frame[0], height=30, width=5, bg='red', command=lambda: Results_menu()), 10, 10, 'left']
    widgets.append(back_btn)
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
            history = [T.Label(history_frame[0], text=f'{res['title']}________{res['result']}%_______{res['date']}', bg='white', anchor='w')]
            widgets.append(history)
    unpack(widgets)

Home_page()

root.mainloop()