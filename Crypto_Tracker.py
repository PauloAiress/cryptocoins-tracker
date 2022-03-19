import tkinter
import tkinter as tk
import requests
from bs4 import BeautifulSoup


# get_data busca os top100 ativos cryptos listados na investing.com
# convert_brl converte o numero recebido no formato usado no Brasil
# track_crypto busca as informacoes de cada ativo selecionado
# move_items move os ativos selecionados entre as list boxs


def move_items(from_list, to_list):
    index_list = from_list.curselection()
    if index_list:
        index = index_list[0]
        symb = from_list.get(index)
        from_list.delete(index)
        to_list.insert(tkinter.END, symb)


def get_data():
    headers = {'User-Agent':
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
    url = 'https://br.investing.com/crypto/currencies'
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    crypto_list = []
    for v in soup.find_all('td', {'class':
                                  "left noWrap elp symb js-currency-symbol"}):
        crypto_list.append("".join(v.find_all(text=True)))
    return crypto_list


def convert_brl(val):
    brl = f'R$ {val:,}'
    brl = str(brl)
    brl = brl.replace(',', '*')
    brl = brl.replace('.', ',')
    brl = brl.replace('*', '.')
    return brl


def track_crypto():
    result_list.delete(0, tkinter.END)
    selected_items = right_list.get(0, tkinter.END)
    for a in selected_items:
        url = f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={a}&tsyms=BRL'
        response = requests.get(url).json()
        for x in response:
            crypto = str(x)
            price = float((response[crypto]['BRL']))
            crypto = f'{crypto}/BRL'
            result_list.insert(0, f'Valor atual {crypto} = {convert_brl(price)}')


canvas_one = tk.Tk()
canvas_one.resizable(width=False, height=False)
canvas_one.title('Rastreador de Cryptos!')
canvas_one.geometry("400x500")
canvas_one.configure(bg='#AAD3F0')


label = tkinter.Label(text="Escolha suas cryptos:",
                    fg='black', font=("Lato", 18), bg='#AAD3F0')
label.place(relx=0.5, y=50, anchor='center')

btn = tkinter.Button(text=">>", fg='black', bg='#AAD3F0', font=("Lato", 10),
                     command=lambda: move_items(left_list, right_list))
btn.place(relx=0.5, y=150, anchor='center')

btn = tkinter.Button(text="<<", fg='black', bg='#AAD3F0', font=("Lato", 10),
                     command=lambda: move_items(right_list, left_list))
btn.place(relx=0.5, y=200, anchor='center')

btn = tkinter.Button(text="     OK     ", fg='black', bg='#AAD3F0', font=("Lato", 12),
                     command=lambda: track_crypto())
btn.place(relx=0.5, y=288, anchor='center')

symbol_list = get_data()
var = tkinter.StringVar()
var.set("")
data = symbol_list


left_list = tkinter.Listbox(height=8, selectmode='single', bg='#AAD3F0',
                            fg='#000', font=("Lato", 12), width=14)
scrollbar = tkinter.Scrollbar(left_list)
for num in data:
    left_list.insert(tkinter.END, num)
left_list.place(x=30, y=100)

right_list = tkinter.Listbox(height=8, selectmode='single', bg='#AAD3F0',
                             fg='#000', font=("Lato", 12), width=14)
right_list.place(x=243, y=100)

result_list = tkinter.Listbox(height=8, selectmode='single', bg='#AAD3F0',
                              fg='#000', font=("Lato", 12), width=37)
result_list.place(x=31, y=317)

footer = tkinter.Label(text=r"Desenvolvido por Paulo Aires",
                    fg='black', font=("Lato", 7), bg='#AAD3F0')
footer.place(relx=0.5, y=490, anchor='center')

canvas_one.mainloop()
