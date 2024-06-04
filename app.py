import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

# Função para cadastrar eventuais
def cadastrar_eventual():
    nome = entry_nome_eventual.get()
    cpf = entry_cpf_eventual.get()
    conta = entry_conta_eventual.get()
    agencia = entry_agencia_eventual.get()
    banco = entry_banco_eventual.get()

    eventual = Eventual(nome=nome, cpf=cpf, conta=conta, agencia=agencia, banco=banco)
    session.add(eventual)
    session.commit()
    messagebox.showinfo("Cadastro", "Eventual cadastrado com sucesso!")

def cadastrar_efetivo():
    nome = entry_nome_efetivo.get()
    cpf = entry_cpf_efetivo.get()
    nif = entry_nif_efetivo.get()
    especialidade = entry_especialidade_efetivo.get()

    efetivo = Efetivo(nome=nome, cpf=cpf, nif=nif, especialidade=especialidade)
    session.add(efetivo)
    session.commit()
    messagebox.showinfo("Cadastro", "Efetivo cadastrado com sucesso!")

# Função para cadastrar aulas eventuais
def cadastrar_aula_eventual():
    eventual_id = int(entry_eventual_id.get())
    efetivo_id = int(entry_efetivo_id.get())
    entrada = datetime.strptime(entry_entrada.get(), '%Y-%m-%d %H:%M:%S')
    saida = datetime.strptime(entry_saida.get(), '%Y-%m-%d %H:%M:%S')
    quantidade_aulas = int(entry_quantidade_aulas.get())
    observacoes = entry_observacoes.get()

    aula_eventual = AulaEventual(
        eventual_id=eventual_id,
        efetivo_id=efetivo_id,
        entrada=entrada,
        saida=saida,
        quantidade_aulas=quantidade_aulas,
        observacoes=observacoes
    )
    session.add(aula_eventual)
    session.commit()
    messagebox.showinfo("Cadastro", "Aula eventual cadastrada com sucesso!")

# Criação da janela principal
root = tk.Tk()
root.title("Dashboard Eventuais")

# Seção de cadastro de eventuais
frame_eventual = ttk.LabelFrame(root, text="Cadastro de Eventuais")
frame_eventual.grid(row=0, column=0, padx=10, pady=10)

tk.Label(frame_eventual, text="Nome:").grid(row=0, column=0)
entry_nome_eventual = tk.Entry(frame_eventual)
entry_nome_eventual.grid(row=0, column=1)

tk.Label(frame_eventual, text="CPF:").grid(row=1, column=0)
entry_cpf_eventual = tk.Entry(frame_eventual)
entry_cpf_eventual.grid(row=1, column=1)

tk.Label(frame_eventual, text="Conta:").grid(row=2, column=0)
entry_conta_eventual = tk.Entry(frame_eventual)
entry_conta_eventual.grid(row=2, column=1)

tk.Label(frame_eventual, text="Agência:").grid(row=3, column=0)
entry_agencia_eventual = tk.Entry(frame_eventual)
entry_agencia_eventual.grid(row=3, column=1)

tk.Label(frame_eventual, text="Banco:").grid(row=4, column=0)
entry_banco_eventual = tk.Entry(frame_eventual)
entry_banco_eventual.grid(row=4, column=1)

tk.Button(frame_eventual, text="Cadastrar", command=cadastrar_eventual).grid(row=5, columnspan=2)

# Seção de cadastro de professores efetivos
frame_efetivo = ttk.LabelFrame(root, text="Cadastro de Professores Efetivos")
frame_efetivo.grid(row=1, column=0, padx=10, pady=10)

tk.Label(frame_efetivo, text="Nome:").grid(row=0, column=0)
entry_nome_efetivo = tk.Entry(frame_efetivo)
entry_nome_efetivo.grid(row=0, column=1)

tk.Label(frame_efetivo, text="CPF:").grid(row=1, column=0)
entry_cpf_efetivo = tk.Entry(frame_efetivo)
entry_cpf_efetivo.grid(row=1, column=1)

tk.Label(frame_efetivo, text="NIF:").grid(row=2, column=0)
entry_nif_efetivo = tk.Entry(frame_efetivo)
entry_nif_efetivo.grid(row=2, column=1)

tk.Label(frame_efetivo, text="Especialidade:").grid(row=3, column=0)
entry_especialidade_efetivo = tk.Entry(frame_efetivo)
entry_especialidade_efetivo.grid(row=3, column=1)

tk.Button(frame_efetivo, text="Cadastrar", command=cadastrar_efetivo).grid(row=4, columnspan=2)

# Seção de cadastro de aulas eventuais
frame_aula_eventual = ttk.LabelFrame(root, text="Cadastro de Aulas Eventuais")
frame_aula_eventual.grid(row=2, column=0, padx=10, pady=10)

tk.Label(frame_aula_eventual, text="ID do Eventual:").grid(row=0, column=0)
entry_eventual_id = tk.Entry(frame_aula_eventual)
entry_eventual_id.grid(row=0, column=1)

tk.Label(frame_aula_eventual, text="ID do Efetivo:").grid(row=1, column=0)
entry_efetivo_id = tk.Entry(frame_aula_eventual)
entry_efetivo_id.grid(row=1, column=1)

tk.Label(frame_aula_eventual, text="Entrada:").grid(row=2, column=0)
entry_entrada = tk.Entry(frame_aula_eventual)
entry_entrada.grid(row=2, column=1)

tk.Label(frame_aula_eventual, text="Saída:").grid(row=3, column=0)
entry_saida = tk.Entry(frame_aula_eventual)
entry_saida.grid(row=3, column=1)

tk.Label(frame_aula_eventual, text="Quantidade de Aulas:").grid(row=4, column=0)
entry_quantidade_aulas = tk.Entry(frame_aula_eventual)
entry_quantidade_aulas.grid(row=4, column=1)

tk.Label(frame_aula_eventual, text="Observações:").grid(row=5, column=0)
entry_observacoes = tk.Entry(frame_aula_eventual)
entry_observacoes.grid(row=5, column=1)

tk.Button(frame_aula_eventual, text="Cadastrar", command=cadastrar_aula_eventual).grid(row=6, columnspan=2)

root.mainloop()
