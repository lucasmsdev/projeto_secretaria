import matplotlib.pyplot as plt
import pandas as pd

# Função para gerar gráfico mensal
def gerar_grafico_mensal(mes):
    query = session.query(AulaEventual).filter(
        func.strftime('%Y-%m', AulaEventual.entrada) == mes
    ).all()

    data = {
        'Tipo': [],
        'Quantidade': []
    }

    for aula in query:
        if aula.eventual_id:
            data['Tipo'].append('Eventual')
       
