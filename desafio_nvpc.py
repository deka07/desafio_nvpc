import requests
from tkinter import*
from customtkinter import*
from tkinter.ttk import Treeview, Combobox

set_appearance_mode('system')
set_default_color_theme('green')

win = CTk()
win.geometry('640x420')
win.title('DESAFIO NVPC')

lbl = CTkLabel(win, text='Usuario:')
lbl.place(x=15, y=20)

e = CTkEntry(win, width=130)
e.place(x=110, y=20)

colunas = ('num', 'nome','commit')
tabela = Treeview(win, columns=colunas, show='headings')
tabela.heading('num', text='Nº')
tabela.heading('nome', text='NOME')
tabela.heading('commit', text='Commit')
tabela.column('num', width=100, anchor=CENTER)
tabela.column('nome', width=350)
tabela.column('commit', width=150, anchor=CENTER)

tabela.place(x=20, y=120)


def buscar():
    #Limpar tabela
    for i in tabela.get_children():
        tabela.delete(i)

    usuario = e.get()
    resposta = requests.get('https://api.github.com/users/{}/repos'.format(usuario))
    dados = resposta.json()
    for i in range(len(dados)):
        tabela.insert('', END, values=(i, dados[i]['name']))

def callbackFunc(event):
    #Limpar tabela
    for i in tabela.get_children():
        tabela.delete(i)

    f = flt.get()
    usuario = e.get()
    resposta = requests.get('https://api.github.com/users/{}/repos'.format(usuario))
    dados = resposta.json()
    
    for i in range(len(dados)):
        if f == '':
            tabela.insert('', END, values=(i, dados[i]['name']))

        if f == 'nome':
            tabela.insert('', END, values=(i, dados[i]['name']))
            
        if f == 'arquivado':
            if dados[i]['archived'] == False:
                tabela.insert('', END, values='Nenhum arquivo arquivado!')
                break
            else:
                tabela.insert('', END, values=(i, dados[i]['archived']))
        
        if f == 'forks':
            if dados[i]['forks'] != 0:
                tabela.insert('', END, values=(i, dados[i]['name']))

        if f == 'publico':
            if dados[i]['visibility'] != 'visibility':
                tabela.insert('', END, values=(i, dados[i]['name']))

def search(event):
    #Limpar tabela
    for i in tabela.get_children():
        tabela.delete(i)

    valor = e2.get()
    usuario = e.get()
    resposta = requests.get('https://api.github.com/users/{}/repos'.format(usuario))
    dados = resposta.json()

    for i in range(len(dados)):
        if valor.lower() in dados[i]['name']:
            tabela.insert('', END, values=(i, dados[i]['name']))

lbl3 = CTkLabel(win, text='Pesquisa:')
lbl3.place(x=-5, y=75)

e2 = CTkEntry(win, width=130)
e2.place(x=90, y=75)
e2.bind('<KeyRelease>', search)

lbl2 = CTkLabel(win, text='Filtar:')
lbl2.place(x=390, y=70)

flt = Combobox(win, values=['nome', 'arquivado', 'forks', 'publico'])
flt.place(x=470, y=70)
flt.bind("<<ComboboxSelected>>", callbackFunc)

btn = CTkButton(win, text='Buscar', command=buscar)
btn.place(x=250, y=20)


win.mainloop()