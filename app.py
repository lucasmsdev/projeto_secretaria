import sys
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, 
    QLineEdit, QFormLayout, QComboBox, QDateTimeEdit, QTextEdit, QSpinBox,
    QGroupBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QDateEdit,
    QDialog, QGridLayout
)
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

DATABASE_URI = 'sqlite:///database.db'

# Criar uma instância do SQLAlchemy Engine
engine = create_engine(DATABASE_URI)

# Criar uma instância do declarative base
Base = declarative_base()

# Definir a classe da tabela ProfessorEventual
class ProfessorEventual(Base):
    __tablename__ = 'professores_eventuais'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    conta = Column(String)
    agencia = Column(String)
    banco = Column(String)

# Definir a classe da tabela ProfessorEfetivo
class ProfessorEfetivo(Base):
    __tablename__ = 'professores_efetivos'

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    conta = Column(String)
    agencia = Column(String)
    banco = Column(String)

# Definir a classe da tabela AulaEventual
class AulaEventual(Base):
    __tablename__ = 'aulas_eventuais'

    id = Column(Integer, primary_key=True)
    professor_eventual_id = Column(Integer, ForeignKey('professores_eventuais.id')) # Adicionando a chave estrangeira
    professor_efetivo_id = Column(Integer)
    data_aula = Column(DateTime)
    horario_entrada = Column(DateTime)
    horario_saida = Column(DateTime)
    quantidade_aulas = Column(Integer)
    observacoes = Column(String)


# Criar o esquema
Base.metadata.create_all(engine)

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Eventuais")
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

        # Botões de Listagem
        self.btnListarEventuais = QPushButton("Listar Professores Eventuais")
        self.btnListarEventuais.clicked.connect(self.listarEventuais)
        layout.addWidget(self.btnListarEventuais)

        self.btnListarEfetivos = QPushButton("Listar Professores Efetivos")
        self.btnListarEfetivos.clicked.connect(self.listarEfetivos)
        layout.addWidget(self.btnListarEfetivos)

        self.btnListarAulas = QPushButton("Listar Aulas Eventuais")
        self.btnListarAulas.clicked.connect(self.listarAulas)
        layout.addWidget(self.btnListarAulas)

        # Criando grupo para os botões de geração de gráficos e relatórios
        groupbox = QGroupBox("Relatórios e Gráficos")
        groupbox_layout = QVBoxLayout()

        self.btnGerarGraficoMensal = QPushButton("Gerar Gráfico Mensal")
        self.btnGerarGraficoMensal.clicked.connect(self.gerarGraficoMensal)
        groupbox_layout.addWidget(self.btnGerarGraficoMensal)

        self.btnGerarGraficoAnual = QPushButton("Gerar Gráfico Anual")
        self.btnGerarGraficoAnual.clicked.connect(self.gerarGraficoAnual)
        groupbox_layout.addWidget(self.btnGerarGraficoAnual)

        self.btnGerarRelatorioDiario = QPushButton("Gerar Relatório Diário")
        self.btnGerarRelatorioDiario.clicked.connect(self.gerarRelatorioDiario)
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

    def listarAulas(self):
        self.listWindow = ListarAulasEventuaisWindow()
        self.listWindow.show()

    def gerarGraficoMensal(self):
        self.graficoMensalWindow = GraficoWindow('mensal')
        self.graficoMensalWindow.show()

    def gerarGraficoAnual(self):
        self.graficoAnualWindow = GraficoWindow('anual')
        self.graficoAnualWindow.show()

    def gerarRelatorioDiario(self):
        self.relatorioDiarioWindow = RelatorioDiarioWindow()
        self.relatorioDiarioWindow.show()

class CadastroWindow(QWidget):
    def __init__(self, title, professor_class):
        super().__init__()
        self.setWindowTitle(title)
        self.professor_class = professor_class
        self.layout = QFormLayout()

        self.nome = QLineEdit()
        self.cpf = QLineEdit()
        self.conta = QLineEdit()
        self.agencia = QLineEdit()
        self.banco = QLineEdit()

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
        # Salvar no banco de dados
        novo_professor = self.professor_class(nome=nome, cpf=cpf, conta=conta, agencia=agencia, banco=banco)
        session.add(novo_professor)
        session.commit()
        self.close()

class CadastroAulasEventuaisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de Aulas Eventuais")
        self.layout = QFormLayout()

        self.professor_eventual = QComboBox()
        self.professor_efetivo = QComboBox()
        self.data_aula = QDateEdit(calendarPopup=True)
        self.horario_entrada = QDateTimeEdit(calendarPopup=True)
        self.horario_saida = QDateTimeEdit(calendarPopup=True)
        self.quantidade_aulas = QSpinBox()
        self.observacoes = QTextEdit()

        self.atualizarCombos()

        self.layout.addRow("Professor Eventual:", self.professor_eventual)
        self.layout.addRow("Professor Efetivo:", self.professor_efetivo)
        self.layout.addRow("Data da Aula:", self.data_aula)
        self.layout.addRow("Horário de Entrada:", self.horario_entrada)
        self.layout.addRow("Horário de Saída:", self.horario_saida)
        self.layout.addRow("Quantidade de Aulas:", self.quantidade_aulas)
        self.layout.addRow("Observações:", self.observacoes)

        self.btnSalvar = QPushButton("Salvar")
        self.btnSalvar.clicked.connect(self.salvar)
        self.layout.addRow("", self.btnSalvar)

        self.setLayout(self.layout)

    def atualizarCombos(self):
        professores_eventuais = session.query(ProfessorEventual).all()
        for professor in professores_eventuais:
            self.professor_eventual.addItem(professor.nome, userData=professor.id)
        
        professores_efetivos = session.query(ProfessorEfetivo).all()
        for professor in professores_efetivos:
            self.professor_efetivo.addItem(professor.nome, userData=professor.id)

    def salvar(self):
        professor_eventual_id = self.professor_eventual.currentData()
        professor_efetivo_id = self.professor_efetivo.currentData()
        data_aula = self.data_aula.date().toPyDate()
        horario_entrada = self.horario_entrada.dateTime().toPyDateTime()
        horario_saida = self.horario_saida.dateTime().toPyDateTime()
        quantidade_aulas = self.quantidade_aulas.value()
        observacoes = self.observacoes.toPlainText()

        nova_aula = AulaEventual(
            professor_eventual_id=professor_eventual_id,
            professor_efetivo_id=professor_efetivo_id,
            data_aula=data_aula,
            horario_entrada=horario_entrada,
            horario_saida=horario_saida,
            quantidade_aulas=quantidade_aulas,
            observacoes=observacoes,
 
        )
        session.add(nova_aula)
        session.commit()
        self.close()

class ListarProfessoresWindow(QWidget):
    def __init__(self, title, professor_class,):
        super().__init__()
        self.setWindowTitle(title)
        self.professor_class = professor_class

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.atualizarTabela()

    def atualizarTabela(self):
        professores = session.query(self.professor_class).all()
        self.table.setRowCount(len(professores))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nome", "CPF", "Conta", "Agência", "Banco"])

        for row, professor in enumerate(professores):
            self.table.setItem(row, 0, QTableWidgetItem(str(professor.id)))
            self.table.setItem(row, 1, QTableWidgetItem(professor.nome))
            self.table.setItem(row, 2, QTableWidgetItem(professor.cpf))
            self.table.setItem(row, 3, QTableWidgetItem(professor.conta))
            self.table.setItem(row, 4, QTableWidgetItem(professor.agencia))
            self.table.setItem(row, 5, QTableWidgetItem(professor.banco))

class ListarAulasEventuaisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listar Aulas Eventuais")

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.atualizarTabela()

    def atualizarTabela(self):
        aulas = session.query(AulaEventual).all()
        self.table.setRowCount(len(aulas))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Professor Eventual", "Professor Efetivo", 
            "Data da Aula", "Horário de Entrada", "Horário de Saída", 
            "Quantidade de Aulas", "Observações"
        ])

        for row, aula in enumerate(aulas):
            self.table.setItem(row, 0, QTableWidgetItem(str(aula.id)))
            professor_eventual = session.query(ProfessorEventual).get(aula.professor_eventual_id)
            self.table.setItem(row, 1, QTableWidgetItem(professor_eventual.nome if professor_eventual else ""))
            professor_efetivo = session.query(ProfessorEfetivo).get(aula.professor_efetivo_id)
            self.table.setItem(row, 2, QTableWidgetItem(professor_efetivo.nome if professor_efetivo else ""))
            self.table.setItem(row, 3, QTableWidgetItem(str(aula.data_aula)))
            self.table.setItem(row, 4, QTableWidgetItem(str(aula.horario_entrada)))
            self.table.setItem(row, 5, QTableWidgetItem(str(aula.horario_saida)))
            self.table.setItem(row, 6, QTableWidgetItem(str(aula.quantidade_aulas)))
            self.table.setItem(row, 7, QTableWidgetItem(aula.observacoes))

class GraficoWindow(QWidget):
    def __init__(self, tipo):
        super().__init__()
        self.setWindowTitle(f"Gerar Gráfico {tipo.capitalize()}")
        self.tipo = tipo
        self.layout = QVBoxLayout()

        self.dataInput = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.dataInput)

        self.btnGerar = QPushButton(f"Gerar Gráfico {tipo.capitalize()}")
        self.btnGerar.clicked.connect(self.gerarGrafico)
        self.layout.addWidget(self.btnGerar)

        self.setLayout(self.layout)

    def gerarGrafico(self):
        data = self.dataInput.date().toPyDate()
        if self.tipo == 'mensal':
            mes = data.month
            ano = data.year
            aulas = session.query(AulaEventual).filter(extract('year', AulaEventual.data_aula) == ano,
                                                       extract('month', AulaEventual.data_aula) == mes).all()
        elif self.tipo == 'anual':
            ano = data.year
            aulas = session.query(AulaEventual).filter(extract('year', AulaEventual.data_aula) == ano).all()

        total_aulas = len(aulas)
        aulas_eventuais = sum(1 for aula in aulas if aula.professor_eventual_id is not None)
        aulas_efetivos = total_aulas - aulas_eventuais

        percent_eventuais = (aulas_eventuais / total_aulas) * 100 if total_aulas > 0 else 0
        percent_efetivos = (aulas_efetivos / total_aulas) * 100 if total_aulas > 0 else 0

        labels = ['Aulas com Eventual', 'Aulas com Efetivo']
        sizes = [percent_eventuais, percent_efetivos]
        colors = ['#ff9999','#66b3ff']
        explode = (0.1, 0)

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')
        plt.title(f"Distribuição de Aulas ({self.tipo.capitalize()} {data.strftime('%Y-%m') if self.tipo == 'mensal' else data.strftime('%Y')})")
        plt.show()

class RelatorioDiarioWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerar Relatório Diário")
        self.layout = QVBoxLayout()

        self.dataInput = QDateEdit(calendarPopup=True)
        self.layout.addWidget(self.dataInput)

        self.btnGerar = QPushButton("Gerar Relatório Diário")
        self.btnGerar.clicked.connect(self.gerarRelatorio)
        self.layout.addWidget(self.btnGerar)

        self.setLayout(self.layout)

    def gerarRelatorio(self):
        data = self.dataInput.date().toPyDate()
        aulas = session.query(AulaEventual).filter(extract('year', AulaEventual.data_aula) == data.year,
                                                   extract('month', AulaEventual.data_aula) == data.month,
                                                   extract('day', AulaEventual.data_aula) == data.day).all()

        relatorio = QDialog(self)
        relatorio.setWindowTitle("Relatório Diário")
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setRowCount(len(aulas))
        table.setColumnCount(8)
        table.setHorizontalHeaderLabels([
            "ID", "Professor Eventual", "Professor Efetivo", 
            "Data da Aula", "Horário de Entrada", "Horário de Saída", 
            "Quantidade de Aulas", "Observações"
        ])

        for row, aula in enumerate(aulas):
            table.setItem(row, 0, QTableWidgetItem(str(aula.id)))
            professor_eventual = session.query(ProfessorEventual).get(aula.professor_eventual_id)
            table.setItem(row, 1, QTableWidgetItem(professor_eventual.nome if professor_eventual else ""))
            professor_efetivo = session.query(ProfessorEfetivo).get(aula.professor_efetivo_id)
            table.setItem(row, 2, QTableWidgetItem(professor_efetivo.nome if professor_efetivo else ""))
            table.setItem(row, 3, QTableWidgetItem(str(aula.data_aula)))
            table.setItem(row, 4, QTableWidgetItem(str(aula.horario_entrada)))
            table.setItem(row, 5, QTableWidgetItem(str(aula.horario_saida)))
            table.setItem(row, 6, QTableWidgetItem(str(aula.quantidade_aulas)))
            table.setItem(row, 7, QTableWidgetItem(aula.observacoes))

        layout.addWidget(table)
        relatorio.setLayout(layout)
        relatorio.exec_()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

### Adicionando a chamada das novas janelas no MainWindow
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Eventuais")
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

        # Botões de Listagem
        self.btnListarEventuais = QPushButton("Listar Professores Eventuais")
        self.btnListarEventuais.clicked.connect(self.listarEventuais)
        layout.addWidget(self.btnListarEventuais)

        self.btnListarEfetivos = QPushButton("Listar Professores Efetivos")
        self.btnListarEfetivos.clicked.connect(self.listarEfetivos)
        layout.addWidget(self.btnListarEfetivos)

        self.btnListarAulas = QPushButton("Listar Aulas Eventuais")
        self.btnListarAulas.clicked.connect(self.listarAulas)
        layout.addWidget(self.btnListarAulas)

        # Criando grupo para os botões de geração de gráficos e relatórios
        groupbox = QGroupBox("Relatórios e Gráficos")
        groupbox_layout = QVBoxLayout()

        self.btnGerarGraficoMensal = QPushButton("Gerar Gráfico Mensal")
        self.btnGerarGraficoMensal.clicked.connect(lambda: self.abrirGrafico('mensal'))
        groupbox_layout.addWidget(self.btnGerarGraficoMensal)

        self.btnGerarGraficoAnual = QPushButton("Gerar Gráfico Anual")
        self.btnGerarGraficoAnual.clicked.connect(lambda: self.abrirGrafico('anual'))
        groupbox_layout.addWidget(self.btnGerarGraficoAnual)

        self.btnGerarRelatorioDiario = QPushButton("Gerar Relatório Diário")
        self.btnGerarRelatorioDiario.clicked.connect(self.abrirRelatorioDiario)
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

    def listarAulas(self):
        self.listWindow = ListarAulasEventuaisWindow()
        self.listWindow.show()

    def abrirGrafico(self, tipo):
        self.graficoWindow = GraficoWindow(tipo)
        self.graficoWindow.show()

    def abrirRelatorioDiario(self):
        self.relatorioDiarioWindow = RelatorioDiarioWindow()
        self.relatorioDiarioWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

