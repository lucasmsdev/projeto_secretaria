import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, Eventual, Efetivo, AulaEventual

Base.metadata.create_all(bind=engine)

class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")

        self.session = SessionLocal()

        self.create_widgets()

    def create_widgets(self):
        self.tab_control = ttk.Notebook(self.root)

        self.tab_eventuais = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_eventuais, text='Cadastro de Eventuais')
        self.create_eventuais_tab()

        self.tab_efetivos = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_efetivos, text='Cadastro de Professores Efetivos')
        self.create_efetivos_tab()

        self.tab_aulas = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_aulas, text='Cadastro de Aulas Eventuais')
        self.create_aulas_tab()

        self.tab_graficos = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_graficos, text='Gerar Gráficos')
        self.create_graficos_tab()

        self.tab_relatorio = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_relatorio, text='Gerar Relatório Diário')
        self.create_relatorio_tab()

        self.tab_control.pack(expand=1, fill='both')

    def create_eventuais_tab(self):
        self.eventuais_nome = tk.StringVar()
        self.eventuais_cpf = tk.StringVar()
        self.eventuais_conta = tk.StringVar()
        self.eventuais_agencia = tk.StringVar()
        self.eventuais_banco = tk.StringVar()

        tk.Label(self.tab_eventuais, text="Nome").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.tab_eventuais, textvariable=self.eventuais_nome).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.tab_eventuais, text="CPF").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.tab_eventuais, textvariable=self.eventuais_cpf).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.tab_eventuais, text="Conta").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.tab_eventuais, textvariable=self.eventuais_conta).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.tab_eventuais, text="Agência").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.tab_eventuais, textvariable=self.eventuais_agencia).grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.tab_eventuais, text="Banco").grid(row=4, column=0, padx=10, pady=5)
        tk.Entry(self.tab_eventuais, textvariable=self.eventuais_banco).grid(row=4, column=1, padx=10, pady=5)

        tk.Button(self.tab_eventuais, text="Cadastrar", command=self.cadastrar_eventual).grid(row=5, column=0, columnspan=2, pady=10)

    def cadastrar_eventual(self):
        nome = self.eventuais_nome.get()
        cpf = self.eventuais_cpf.get()
        conta = self.eventuais_conta.get()
        agencia = self.eventuais_agencia.get()
        banco = self.eventuais_banco.get()

        if not nome or not cpf or not conta or not agencia or not banco:
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios")
            return

        novo_eventual = Eventual(nome=nome, cpf=cpf, conta=conta, agencia=agencia, banco=banco)
        self.session.add(novo_eventual)
        self.session.commit()
        messagebox.showinfo("Sucesso", "Eventual cadastrado com sucesso")

    def create_efetivos_tab(self):
        self.efetivos_nome = tk.StringVar()
        self.efetivos_cpf = tk.StringVar()
        self.efetivos_nif = tk.StringVar()
        self.efetivos_especialidade = tk.StringVar()

        tk.Label(self.tab_efetivos, text="Nome").grid(row=0, column=0, padx=10, pady=5)
        tk.Entry(self.tab_efetivos, textvariable=self.efetivos_nome).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.tab_efetivos, text="CPF").grid(row=1, column=0, padx=10, pady=5)
        tk.Entry(self.tab_efetivos, textvariable=self.efetivos_cpf).grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.tab_efetivos, text="NIF").grid(row=2, column=0, padx=10, pady=5)
        tk.Entry(self.tab_efetivos, textvariable=self.efetivos_nif).grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.tab_efetivos, text="Especialidade").grid(row=3, column=0, padx=10, pady=5)
        tk.Entry(self.tab_efetivos, textvariable=self.efetivos_especialidade).grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.tab_efetivos, text="Cadastrar", command=self.cadastrar_efetivo).grid(row=4, column=0, columnspan=2, pady=10)

    def
