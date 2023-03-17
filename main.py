from tkinter import *
from tkinter import ttk
import backend as back
from sqlite3 import *

#  Главное окно
window = Tk()
window.title('subd')
window.minsize(700, 450)

frame_change = Frame(window, width=150, height=150, bg='white')  # блок для функционала субд
frame_view = Frame(window, width=150, height=150, bg='white')  # блок для просмотра базы данных
frame_change.place(relx=0, rely=0, relwidth=1, relheight=1)
frame_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)



# порядок элементов
heads = ['id', 'name', 'expenses']
table = ttk.Treeview(frame_view, show='headings')  # дерево выполняющее свойство таблицы
table['columns'] = heads  # длина таблицы

# заголовки столбцов и их расположение
for header in heads:
    table.heading(header, text=header, anchor='center')
    table.column(header, anchor='center')

# добавление из бд в таблицу приложения
for row in back.information():
    table.insert('', END, values=row)
table.pack(expand=YES, fill=BOTH, side=LEFT)

# функция добавления новых записей
def form_submit():
    name = f_name.get()
    expenses = f_expenses.get()
    insert_inf = (name, expenses)
    with connect('database.db') as db:
        cursor = db.cursor()
        query = """ INSERT INTO table1(name, expenses) VALUES (?, ?)"""
        cursor.execute(query, insert_inf)
        db.commit()
        refresh()

# функция добавления новых записей


# функция обновления таблицы
def refresh():
    with connect('database.db') as db:
        cursor = db.cursor()
        cursor.execute(''' SELECT * FROM table1 ''')
        [table.delete(i) for i in
        table.get_children()]
        [table.insert('', 'end', values=row) for row in cursor.fetchall()]
# кнопка удалить и её функционал
f_delete = ttk.Entry(frame_change)
f_delete.grid(row=2, column=1, sticky='w', padx=10, pady=10)


def delete():
    with connect('database.db') as db:
        cursor = db.cursor()
        id = id_sel
        cursor.execute('''DELETE FROM  table2 WHERE id = ?''', (id,))
        db.commit()
        refresh()


def delete_user():
    with connect('database.db') as db:
        cursor = db.cursor()
        id = id_sel
        cursor.execute('''DELETE FROM table1 WHERE id = ?''', (id,))
        db.commit()
        refresh()

btn_delete = ttk.Button(frame_change, text="Удалить", command=delete_user)
btn_delete.grid(row=2, column=3, columnspan=2, sticky='w', padx=10, pady=10)



def on_select(event):
    global id_sel
    global set_col
    id_sel = table.item(table.focus())
    id_sel = id_sel.get('values')[0]
    col = table.identify_column(event.x)
    set_col = table.column(col)
    set_col = set_col.get('id')

table.bind('<ButtonRelease-1>', on_select)

def changeDB():
    with connect('database.db') as db:
        cursor = db.cursor()
        id = id_sel
        whatchange = f_change.get()
        if set_col != 'id':
            cursor.execute("""Update table1 set""" + ' ' + set_col + """ = ? where id = ? """, (whatchange, id))
            db.commit()
            refresh()

# INNER JOIN - возвращает только те строки, которые имеют совпадения в обеих таблицах.
def menu_inner_join():
    def inner_join():
        label_info.config(text="")

        # Установим соединение с базой данных
        with connect('database.db') as db:
            # Создание курсора
            cursor = db.cursor()

            if comboExample.get() == 'Имя':
                # SELECT-запрос с INNER JOIN
                query = """SELECT name
                           FROM table1
                           INNER JOIN table2 ON table1.name = table2.names"""

            elif comboExample.get() == 'Расходы':
                # SELECT-запрос с INNER JOIN
                query = """SELECT expenses
                           FROM table1
                           INNER JOIN table2 ON table1.expenses = table2.paid"""
            else:
                print('Пока для программы не корректный запрос')
            # Выполняем запрос
            cursor.execute(query)

            # Получаем результат запроса
            result = cursor.fetchall()

            # распаковка кортежа и запись его в список
            lst = []
            for item in result:
                lst.append(*item,)

            # пустой список для проверки существующих данных о расходах
            isp = []
            for i in range(len(lst)):
                if lst[i] in isp:
                    continue
                else:
                    isp.append(lst[i])
                    new_text = (f' Число вхождений {lst[i] if lst[i-1] != lst[i] else lst[i-1]}: {lst.count(lst[i])}')
                    label_info.config(text=label_info.cget('text') + '\n'+ new_text)


            # Показываем все на Label


    newWindow = Toplevel(window)
    newWindow.minsize(300, 200)

    #Комбобокс с выбором вхождений из заголовков первой таблицы
    comboExample = ttk.Combobox(newWindow,
                                values=[
                                    "Имя",
                                    "Расходы",])
    comboExample.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=10)
    comboExample.current(1)

    # Кнопка проверки вхождения
    btn_new_table = ttk.Button(newWindow, text='Проверка', command=inner_join)
    btn_new_table.grid(row=10, column=0, columnspan=2, sticky='w', padx=10, pady=10)

    #Лейбл с информацией
    label_info = Label(newWindow, text= 'Что входит из table1 И table2:')
    label_info.grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=10)


# функция создания окна второй таблицы
def create_table2():
    def on_select2(event):
        global id_sel2
        global set_col2
        id_sel2 = table2.item(table2.focus())
        id_sel2 = id_sel2.get('values')[0]
        col = table2.identify_column(event.x)
        set_col2 = table2.column(col)
        set_col2 = set_col2.get('id')

    def delete2():
        with connect('database.db') as db:
            cursor = db.cursor()
            id = id_sel2
            cursor.execute('''DELETE FROM  table2 WHERE id = ?''', (id,))
            db.commit()
            refresh2()

    def refresh2():
        with connect('database.db') as db:
            cursor = db.cursor()
            cursor.execute(''' SELECT * FROM table2 ''')
            [table2.delete(i) for i in
             table2.get_children()]
            [table2.insert('', 'end', values=row) for row in cursor.fetchall()]

    def form_submit2():
        name = f_name.get()
        expenses = f_expenses.get()
        insert_inf = (name, expenses)
        with connect('database.db') as db:
            cursor = db.cursor()
            query = """ INSERT INTO table2(names, paid) VALUES (?, ?)"""
            cursor.execute(query, insert_inf)
            db.commit()
            refresh2()

    def changeDB2():
        with connect('database.db') as db:
            cursor = db.cursor()
            id = id_sel2
            whatchange = f2_change.get()
            if set_col2 != 'id':
                cursor.execute("""Update table2 set""" + ' ' + set_col2 + """ = ? where id = ? """, (whatchange, id))
                db.commit()
                refresh2()

    window = Tk()
    window.title('subd')
    window.minsize(700, 450)

    frame2_change = Frame(window, width=150, height=150, bg='white')  # блок для функционала субд
    frame2_view = Frame(window, width=150, height=150, bg='white')  # блок для просмотра базы данных
    frame2_change.place(relx=0, rely=0, relwidth=1, relheight=1)
    frame2_view.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    # порядок элементов
    heads2 = ['id', 'names', 'paid']
    table2 = ttk.Treeview(frame2_view, show='headings')  # дерево выполняющее свойство таблицы
    table2['columns'] = heads2  # длина таблицы

    table2.bind('<ButtonRelease-1>', on_select2)
    # заголовки столбцов и их расположение
    for header in heads2:
        table2.heading(header, text=header, anchor='center')
        table2.column(header, anchor='center')

    # добавление из бд в таблицу приложения
    for row in back.information2():
        table2.insert('', END, values=row)
    table2.pack(expand=YES, fill=BOTH, side=LEFT)

    # добавления новых имен в бд
    l2_name = ttk.Label(frame2_change, text="Имя")
    f2_name = ttk.Entry(frame2_change)
    l2_name.grid(row=0, column=0, sticky='w', padx=10, pady=10)
    f2_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)

    # добавления новых платежей в бд
    l2_expenses = ttk.Label(frame2_change, text="Платеж")
    f2_expenses = ttk.Entry(frame2_change)
    l2_expenses.grid(row=1, column=0, sticky='w', padx=10, pady=10)
    f2_expenses.grid(row=1, column=1, sticky='w', padx=10, pady=10)

    #  изменения бд
    l2_change = ttk.Label(frame2_change, text="Заменить на:")
    f2_change = ttk.Entry(frame2_change)  # entry на что меняем прошлое имя в бд
    l2_change.grid(row=3, column=0, sticky='w', padx=10, pady=10)
    f2_change.grid(row=3, column=1, sticky='w', padx=10, pady=10)

    #  кнопка добавить
    btn2_submit = ttk.Button(frame2_change, text="Добавить", command=form_submit2)
    btn2_submit.grid(row=0, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка удалить
    btn2_delete = ttk.Button(frame2_change, text="Удалить", command=delete2)
    btn2_delete.grid(row=1, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка изменить
    but2_change = ttk.Button(frame2_change, text='Изменить', command=changeDB2)
    but2_change.grid(row=3, column=3, columnspan=2, sticky='w', padx=10, pady=10)

    #  кнопка вызывающая справку
    btn2_reference = ttk.Button(frame2_change, text="Справка", command=back.show_info)
    btn2_reference.grid(row=4, column=0, sticky='w', padx=10, pady=10)


# контекстное меню
mainmenu = Menu(window)
window.config(menu=mainmenu)



filemenu = Menu(mainmenu, tearoff=0)
mainmenu.add_cascade(label="Вхождение",
                     menu=filemenu)
filemenu.add_command(label='В обе таблицы', command=menu_inner_join)

# кнопки и label добавления новых записей
l_name = ttk.Label(frame_change, text="Имя")
f_name = ttk.Entry(frame_change)
l_index = ttk.Label(frame_change, text="Индекс")
#здесь по идее должен быть f_index но вместо него мы используем f_delete
l_change = ttk.Label(frame_change, text="Заменить на:")
f_change = ttk.Entry(frame_change) #entry на что меняем прошлое имя в бд
l_expenses = ttk.Label(frame_change, text="Платеж")
f_expenses = ttk.Entry(frame_change)
btn_submit = ttk.Button(frame_change, text="Добавить", command=form_submit)

but_change = ttk.Button(frame_change, text='Изменить', command=changeDB)
btn_reference = ttk.Button(frame_change, text="Справка", command=back.show_info)
# расположение кнопок и label добавления новых записей
l_name.grid(row=0, column=0, sticky='w', padx=10, pady=10)
f_name.grid(row=0, column=1, sticky='w', padx=10, pady=10)
l_expenses.grid(row=1, column=0, sticky='w', padx=10, pady=10)
f_expenses.grid(row=1, column=1, sticky='w', padx=10, pady=10)
l_index.grid(row=2, column=0, sticky='w', padx=10, pady=10)
l_change.grid(row=3, column=0, sticky='w', padx=10, pady=10)
f_change.grid(row=3, column=1, sticky='w', padx=10, pady=10)
#здесь по идее должен быть entry index но вместо него используем f_delete
btn_submit.grid(row=0, column=3, columnspan=2, sticky='w', padx=10, pady=10)
but_change.grid(row=3, column=3, columnspan=2, sticky='w', padx=10, pady=10)
btn_reference.grid(row=4, column=0, sticky='w', padx=10, pady=10)
#Кнопка созданиятаблицы
create_new_table=ttk.Button(frame_change, text='Таблица 2', command=create_table2)
create_new_table.grid(row=1, column = 2, columnspan=2,sticky='w', padx=10, pady=10)
#скроллбар
scrollpanel = ttk.Scrollbar(frame_view, command=table.yview)
table.configure(yscrollcommand=scrollpanel.set)
scrollpanel.pack(side=RIGHT, fill=Y)
table.pack(expand=YES, fill=BOTH)





window.mainloop()
