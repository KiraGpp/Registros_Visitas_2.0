import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash

web: gunicorn app:app

app = Flask(__name__)
app.secret_key = '1!Kiragp1234'

def ler_planilha_associados():
    caminho_associados = r"G:\Meu Drive\VP E WHY\CSV EXECUTAVEL\Carteira Associados\Python\Carteira Total\Associados_Totais.xlsx"
    df = pd.read_excel(caminho_associados)
    associados = df['Nome Fantasia ou Abreviacao'].sort_values().unique().tolist()
    gerentes = df['Gerente'].unique().tolist()
    return associados, gerentes


def adicionar_visita_arquivo_excel(nome_associado, nome_gerente, data_visita):
    caminho_visitas = r"G:\Meu Drive\VP E WHY\CSV EXECUTAVEL\Visitas\Registros de Visitas\Registros_Visitas.xlsx"
    try:
        df_visitas = pd.read_excel(caminho_visitas)
    except FileNotFoundError:  # Se o arquivo não existir, cria um novo DataFrame
        df_visitas = pd.DataFrame(columns=['nome_associado', 'nome_gerente', 'data_visita'])
    
    # Criando um novo DataFrame para a visita
    nova_visita = pd.DataFrame([[nome_associado, nome_gerente, data_visita]],
                               columns=['nome_associado', 'nome_gerente', 'data_visita'])
    
    # Usando pd.concat para adicionar a nova linha
    df_visitas = pd.concat([df_visitas, nova_visita], ignore_index=True)
    
    with pd.ExcelWriter(caminho_visitas, engine='openpyxl', mode='w') as writer:
        df_visitas.to_excel(writer, index=False)


@app.route('/')
def index():
    associados, gerentes = ler_planilha_associados()
    return render_template('index.html', associados=associados, gerentes=gerentes)


@app.route('/registrar-visita', methods=['POST'])
def registrar_visita():
    nome_associado = request.form['nomeAssociado']
    nome_gerente = request.form['nomeGerente']
    data_visita = request.form['dataVisita']
    adicionar_visita_arquivo_excel(nome_associado, nome_gerente, data_visita)
    flash('Visita registrada com sucesso!')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
