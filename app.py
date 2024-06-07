import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QLineEdit, QFormLayout, QComboBox, QDateTimeEdit, QTextEdit, QSpinBox,
    QGroupBox, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URI = 'sqlite:///database.db'

# Remove o banco de dados existente (somente para fins de desenvolvimento)
if os.path.exists("database.db"):
    os.remove("database.db")

# Criar uma instância do SQLAlchemy Engine
engine = create_engine(DATABASE_URI)

# Criar uma instância do declarative base
Base = declarative_base()

# Definir a classe da tabela Professor Eventual
class ProfessorEventual(Base):
    __tablename__ = 'professores_eventuais'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    conta = Column(String)
    agencia = Column(String)
    banco = Column(String)

# Definir a classe da tabela Professor Efetivo
class ProfessorEfetivo(Base):
    __tablename__ = 'professores_efetivos'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    conta = Column(String)
    agencia = Column(String)
    banco = Column(String)

# Criar o esquema
Base.metadata.create_all(engine)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Professores")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Botões de Cadastro
        self.btnCadastroEventuais = QPushButton("Cadastro de Eventuais")
        self.btnCadastroEventuais.clicked.connect(self.cadastroEventuais)
        layout.addWidget(self.btnCadastroEventuais)

        self.btnCadastroEfetivos = QPushButton("Cadastro de Professores Efetivos")
        self.btnCadastroEfetivos.clicked.connect(self.cadastroEfetivos)
        layout.addWidget(self.btnCadastroEfetivos)

        self.btnCadastroAulasEventuais = QPushButton("Cadastro de Aulas Eventuais")
        self.btnCadastroAulasEventuais.clicked.connect(self.cadastroAulasEventuais)
        layout.addWidget(self.btnCadastroAulasEventuais)

        self.btnListarEventuais = QPushButton("Listar Eventuais")
        self.btnListarEventuais.clicked.connect(self.listarEventuais)
        layout.addWidget(self.btnListarEventuais)

        self.btnListarEfetivos = QPushButton("Listar Efetivos")
        self.btnListarEfetivos.clicked.connect(self.listarEfetivos)
        layout.addWidget(self.btnListarEfetivos)

        # Criando grupo para os botões de geração de gráficos e relatórios
        groupbox = QGroupBox("Relatórios e Gráficos")
        groupbox_layout = QVBoxLayout()

        self.btnGerarGraficoMensal = QPushButton("Gerar Gráfico Mensal")
        groupbox_layout.addWidget(self.btnGerarGraficoMensal)

        self.btnGerarGraficoAnual = QPushButton("Gerar Gráfico Anual")
        groupbox_layout.addWidget(self.btnGerarGraficoAnual)

        self.btnGerarRelatorioDiario = QPushButton("Gerar Relatório Diário")
        groupbox_layout.addWidget(self.btnGerarRelatorioDiario)

        groupbox.setLayout(groupbox_layout)
        layout.addWidget(groupbox)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def cadastroEventuais(self):
        self.formWindow = CadastroWindow("Cadastro de Eventuais", ProfessorEventual)
        self.formWindow.show()

    def cadastroEfetivos(self):
        self.formWindow = CadastroWindow("Cadastro de Professores Efetivos", ProfessorEfetivo)
        self.formWindow.show()

    def cadastroAulasEventuais(self):
        self.formWindow = CadastroAulasEventuaisWindow()
        self.formWindow.show()

    def listarEventuais(self):
        self.listWindow = ListarProfessoresWindow("Listar Professores Eventuais", ProfessorEventual)
        self.listWindow.show()

    def listarEfetivos(self):
        self.listWindow = ListarProfessoresWindow("Listar Professores Efetivos", ProfessorEfetivo)
        self.listWindow.show()

class CadastroWindow(QWidget):
    def __init__(self, title, professor_class, professor=None):
        super().__init__()
        self.setWindowTitle(title)
        self.layout = QFormLayout()

        self.professor_class = professor_class
        self.professor = professor

        self.nome = QLineEdit()
        self.cpf = QLineEdit()
        self.conta = QLineEdit()
        self.agencia = QLineEdit()
        self.banco = QLineEdit()

        if professor:
            self.nome.setText(professor.nome)
            self.cpf.setText(professor.cpf)
            self.conta.setText(professor.conta)
            self.agencia.setText(professor.agencia)
            self.banco.setText(professor.banco)

        self.layout.addRow("Nome:", self.nome)
        self.layout.addRow("CPF:", self.cpf)
        self.layout.addRow("Conta:", self.conta)
        self.layout.addRow("Agência:", self.agencia)
        self.layout.addRow("Banco:", self.banco)

        self.btnSalvar = QPushButton("Salvar")
        self.btnSalvar.clicked.connect(self.salvar)
        self.layout.addRow("", self.btnSalvar)

        self.setLayout(self.layout)

    def salvar(self):
        nome = self.nome.text()
        cpf = self.cpf.text()
        conta = self.conta.text()
        agencia = self.agencia.text()
        banco = self.banco.text()

        if self.professor:
            # Atualizar o professor existente
            self.professor.nome = nome
            self.professor.cpf = cpf
            self.professor.conta = conta
            self.professor.agencia = agencia
            self.professor.banco = banco
        else:
            # Criar um novo professor
            novo_professor = self.professor_class(nome=nome, cpf=cpf, conta=conta, agencia=agencia, banco=banco)
            session.add(novo_professor)
        
        session.commit()
        self.close()

class ListarProfessoresWindow(QWidget):
    def __init__(self, title, professor_class):
        super().__init__()
        self.setWindowTitle(title)
        self.professor_class = professor_class
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Conta", "Agência", "Banco", "Ações"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.table)

        self.atualizarTabela()

        self.setLayout(self.layout)

    def atualizarTabela(self):
        professores = session.query(self.professor_class).all()
        self.table.setRowCount(len(professores))

        for row, professor in enumerate(professores):
            self.table.setItem(row, 0, QTableWidgetItem(str(professor.id)))
            self.table.setItem(row, 1, QTableWidgetItem(professor.nome))
            self.table.setItem(row, 2, QTableWidgetItem(professor.cpf))
            self.table.setItem(row, 3, QTableWidgetItem(professor.conta))
            self.table.setItem(row, 4, QTableWidgetItem(professor.agencia))
            self.table.setItem(row, 5, QTableWidgetItem(professor.banco))
            
            btnEditar = QPushButton("Editar")
            btnEditar.clicked.connect(lambda ch, prof=professor: self.editarProfessor(prof))
            self.table.setCellWidget(row, 6, btnEditar)

            btnExcluir = QPushButton("Excluir")
            btnExcluir.clicked.connect(lambda ch, prof=professor: self.excluirProfessor(prof))
            self.table.setCellWidget(row, 6, btnExcluir)
    
    def editarProfessor(self, professor):
        self.editWindow = CadastroWindow("Editar Professor", self.professor_class, professor)
        self.editWindow.show()

    def excluirProfessor(self, professor):
        resposta = QMessageBox.question(self, "Confirmação", f"Tem certeza que deseja excluir o professor {professor.nome}?", QMessageBox.Yes | QMessageBox.No)
        if resposta == QMessageBox.Yes:
            session.delete(professor)
            session.commit()
            self.atualizarTabela()

class CadastroAulasEventuaisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Aulas Eventuais")
        self.layout = QFormLayout()

        self.professor_eventual = QComboBox()
        self.professor_efetivo = QComboBox()
        self.horario_entrada = QDateTimeEdit()
        self.horario_saida = QDateTimeEdit()
        self.quantidade_aulas = QSpinBox()
        self.observacoes = QTextEdit()

        # Aqui você pode preencher os comboboxes com dados do banco

        self.layout.addRow("Professor Eventual:", self.professor_eventual)
        self.layout.addRow("Professor Efetivo:", self.professor_efetivo)
        self.layout.addRow("Horário de Entrada:", self.horario_entrada)
        self.layout.addRow("Horário de Saída:", self.horario_saida)
        self.layout.addRow("Quantidade de Aulas:", self.quantidade_aulas)
        self.layout.addRow("Observações:", self.observacoes)

        self.setLayout(self.layout)

    def atualizarCombos(self):
        # Atualizar os comboboxes com dados do banco de dados
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
