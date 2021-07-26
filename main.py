import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

ativo = pd.read_csv('dados/Efetivo_ativo.csv',sep=';',index_col=False)
ativo['ValorBruto'] = ativo['ValorBruto'].str.replace(',', '.').astype(float)


inativo = pd.read_csv('dados/Efetivo_inativo.csv',sep=';',index_col=False)
inativo['ValorBruto'] = inativo['ValorBruto'].str.replace(',', '.').astype(float)

comissionado_ativo = pd.read_csv('dados/efetivo_comissionado_ativo.csv',sep=';',index_col=False)
comissionado_ativo['ValorBruto'] = comissionado_ativo ['ValorBruto'].str.replace(',', '.').astype(float)

pensionista_especial = pd.read_csv('dados/Pensionista_especial.csv',sep=';',index_col=False)
pensionista_especial['ValorBruto'] = pensionista_especial['ValorBruto'].str.replace(',', '.').astype(float)


pensionista_iprev = pd.read_csv('dados/Pensionista_iprev.csv',sep=';',index_col=False)
pensionista_iprev['ValorBruto'] = pensionista_iprev['ValorBruto'].str.replace(',', '.').astype(float)


# Calculos de arrecadação

# Separar dados entre cível e militar dos ativos

ativo_militar = ativo.query(" OrgaoOrigem == 'POLICIA MILITAR' or OrgaoOrigem == 'CORPO DE BOMBEIROS MILITAR' ")

ativo_civil = (ativo[ativo.OrgaoOrigem != 'POLICIA MILITAR']) 
ativo_civil = (ativo_civil[ativo_civil .OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR']) 
# ativo_civil = ativo.query(" OrgaoOrigem != 'POLICIA MILITAR' or OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR' ")

# Separar dados entre cível e militar dos inativos

inativo_militar = inativo.query(" OrgaoOrigem == 'POLICIA MILITAR' or OrgaoOrigem == 'CORPO DE BOMBEIROS MILITAR' ")

inativo_civil = (inativo[inativo.OrgaoOrigem != 'POLICIA MILITAR']) 
inativo_civil = (inativo_civil[inativo_civil .OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR'])

# Separar dados entre cível e militar dos comissionados

comissionado_ativo_militar = comissionado_ativo.query(" OrgaoOrigem == 'POLICIA MILITAR' or OrgaoOrigem == 'CORPO DE BOMBEIROS MILITAR' ")

comissionado_ativo_civil = (comissionado_ativo[comissionado_ativo.OrgaoOrigem != 'POLICIA MILITAR']) 
comissionado_ativo_civil = (comissionado_ativo_civil[comissionado_ativo_civil .OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR'])
# Separar dados entre cível e militar dos pensionistas especiais 

pensionista_especial_militar = pensionista_especial.query(" OrgaoOrigem == 'POLICIA MILITAR' or OrgaoOrigem == 'CORPO DE BOMBEIROS MILITAR' ")

pensionista_especial_civil = pensionista_especial.query(" OrgaoOrigem != 'POLICIA MILITAR' or OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR' ")

# Separar dados entre cível e militar dos pensionista iprev 

pensionista_iprev_militar = pensionista_iprev.query(" OrgaoOrigem == 'POLICIA MILITAR' or OrgaoOrigem == 'CORPO DE BOMBEIROS MILITAR' ")

pensionista_iprev_civil = pensionista_iprev.query(" OrgaoOrigem != 'POLICIA MILITAR' or OrgaoOrigem != 'CORPO DE BOMBEIROS MILITAR' ")


'''Separar os valores acima do teto do INSS Inativos Civil'''
teto_inss = 6433.57

def soma_arrecadacao_civil_ativo(dados,aliquota):
    valor_contribuicao=0
    soma = 0
    for valor in dados['ValorBruto']:
        valor_contribuicao = (valor)*aliquota + (valor*0.28)
        soma = soma + valor_contribuicao
        print('salario:',valor,' patronal: ',(valor*0.28),' aliquota: ',(valor)*aliquota,' total: ',valor_contribuicao,' acumulado: ',soma)
    return soma

def soma_arrecadacao_civil_inativo(dados,aliquota,teto_inss):
    valor_contribuicao=0
    soma = 0
    for valor in dados['ValorBruto']:
        if valor > teto_inss:
            valor_contribuicao = (valor - teto_inss)*aliquota
            soma = soma + valor_contribuicao
    return soma

def soma_arrecadacao_militar(dados,aliquota):
    valor_contribuicao=0
    soma = 0
    for valor in dados['ValorBruto']:
        valor_contribuicao = valor*aliquota
        soma = soma + valor_contribuicao
    return soma
        
# ativo
# Servidores ativos: 14% sobre o salário de contribuição.
ativo_contribuicao_civil = soma_arrecadacao_civil_ativo(ativo_civil,0.14)
ativo_contribuicao_militar= soma_arrecadacao_militar(ativo_militar,0.105)

#inativo
inativo_contribuicao_civil = soma_arrecadacao_civil_inativo(inativo_civil,0.14,teto_inss)

inativo_contribuicao_militar= soma_arrecadacao_militar(inativo_militar,0.105)

#comissionado
comissionado_ativo_contribuicao_civil = soma_arrecadacao_civil_ativo(comissionado_ativo_civil,0.14)

comissionado_ativo_contribuicao_militar= soma_arrecadacao_militar(comissionado_ativo_militar,0.105)

#pensionista especial

pensionista_especial_contribuicao = soma_arrecadacao_civil_inativo(pensionista_especial_civil,0.14,teto_inss)

#pensionista iprev

pensionista_iprev_contribuicao = soma_arrecadacao_civil_inativo(pensionista_iprev_civil,0.14,teto_inss)

civil = ativo_contribuicao_civil + comissionado_ativo_contribuicao_civil
militar = comissionado_ativo_contribuicao_militar + ativo_contribuicao_militar
# soma total de arrecadação:
lista = [civil,
         inativo_contribuicao_civil,
         militar,
         inativo_contribuicao_militar,
         pensionista_especial_contribuicao,
         pensionista_iprev_contribuicao]

arrecadacao = pd.DataFrame(columns=['valor'],index=('ativo civil','inativo civil',
                                          'ativo militar',
                                          'inativo militar',
                                          'pensionista especial',
                                          'pensionista iprev'))


div =1
arrecadacao.loc['ativo civil','valor'] = ((lista[0] + (lista[0] * 2)))/div
arrecadacao.loc['inativo civil','valor'] = (lista[1])/div
arrecadacao.loc['ativo militar','valor'] = (lista[2])/div
arrecadacao.loc['inativo militar','valor'] = lista[3]/div
arrecadacao.loc['pensionista especial','valor'] = (lista[4])/div
arrecadacao.loc['pensionista iprev','valor'] = (lista[5])/div
# arrecadacao = arrecadacao.T
arrecadacao['vinculo'] = arrecadacao.index
arrecadacao = arrecadacao.reset_index(drop=True)


coluna = np.array(['ativo civil', 'inativo civil', 'ativo militar', 'inativo militar',
       'pensionista especial', 'pensionista iprev'])
# ativo = arrecadacao.valor.values[0]
# inativo = arrecadacao.valor.values[1]
x = np.arange(6)  # the label locations
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
s=0
rect=[]

for lab in coluna:
    ax.bar(coluna[s],arrecadacao.valor.values[s],label=lab)
    s+=1
        
ax.set_ylabel('Valores em Milhões')
ax.set_title('Arrecadação por Vínculos')
ax.set_xticklabels(('1', '2', '3', '4', '5','6'))
ax.legend()
fig.tight_layout()
plt.show()

# Gastos com inativos civis
gastos_civis = sum(inativo_civil['ValorBruto'])
gastos_militares = sum(inativo_militar['ValorBruto'])

gastos_pensionista_civil =sum(pensionista_especial_civil['ValorBruto'])

gastos_pensionista_iprev = sum(pensionista_iprev_civil['ValorBruto'])

gastos = pd.DataFrame(columns=['valor'],index=('inativo civil','inativo militar',
                                          'pensionista',
                                          'pensionista iprev'))

gastos.loc['inativo civil','valor'] = gastos_civis /div
gastos.loc['inativo militar','valor'] = gastos_militares/div
gastos.loc['pensionista','valor'] = gastos_pensionista_civil/div
gastos.loc['pensionista iprev','valor'] = gastos_pensionista_iprev/div

coluna = np.array(['inativo civil','inativo militar',
                                          'pensionista',
                                          'pensionista iprev'])
# ativo = arrecadacao.valor.values[0]
# inativo = arrecadacao.valor.values[1]
x = np.arange(6)  # the label locations
width = 0.35  # the width of the bars
fig, ax = plt.subplots()
s=0
rect=[]

for lab in coluna:
    ax.bar(coluna[s],gastos.valor.values[s],label=lab)
    s+=1
        
ax.set_ylabel('Valores em Milhões')
ax.set_title('Despesa por Vínculos')
ax.set_xticklabels(('1', '2', '3', '4'))
ax.legend()
fig.tight_layout()
plt.show()
# arrecadação por cargo
total_arrecadacao = sum(arrecadacao.valor)
print(total_arrecadacao)
total_despesa = sum(gastos.valor)

fig, ax = plt.subplots()


ax.bar('arrecadação',total_arrecadacao,label='arrecadação')
ax.bar('despesas',total_despesa,label='despesas')

        
ax.set_ylabel('Valores em Milhões')
ax.set_title('Arrecadação X Despesas')
ax.set_xticklabels(('1', '2'))
ax.legend()
fig.tight_layout()
plt.show()

# Despesas por cargo

cargos_inativos = inativo['Cargo'].value_counts()
cargos_pensionista = pensionista_especial['OrgaoOrigem'].value_counts()
cargos_pensionista_iprev = pensionista_iprev['Cargo'].value_counts()

cargos_despesas = pd.DataFrame(cargos_inativos.index,columns=['tipo'])

y = 0
for nome in cargos_despesas.tipo:
    nome_txt = "'"+nome+"'"
    texto = f' Cargo == {nome_txt}'
    # print(texto)
    todos = inativo.query(texto)
    # print('cargo: ', nome, 'total: ',len(todos))
    soma = sum(todos['ValorBruto'])
    cargos_despesas.loc[y,'despesas'] = soma
    y += 1


cargos_despesas.loc[232,'tipo'] = 'PENSOES ESPECIAIS'
cargos_despesas.loc[232,'despesas'] = sum(pensionista_especial['ValorBruto'])
#---------------------------------------------------
cargos_despesas.loc[233,'tipo'] = 'PENSIONISTA DO IPREV'
cargos_despesas.loc[233,'despesas'] = sum(pensionista_iprev['ValorBruto'])
#----------------------------------------------------

    
# Arrecadação

# 1 Arrecadação civil cargos ativados
cargos_ativos_c = ativo_civil['Cargo'].value_counts()

cargos_ativos_civil = pd.DataFrame(cargos_ativos_c.index,columns=['tipo'])

y=0
for nome in cargos_ativos_civil.tipo:
    # Arrecadacao ativo por cargo
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    # print(texto)
    todos_b = ativo_civil.query(texto)
    # Servidores ativos: 14% sobre o salário de contribuição.
    soma = soma_arrecadacao_civil_ativo(todos_b,0.14)
    cargos_ativos_civil.loc[y,'arrecadacao'] = soma
    y += 1

# 2 Arrecadação Cargos Comissionados civil ativados

cargos_comissionado_c = comissionado_ativo_civil['Cargo'].value_counts()

cargos_comissionado_civil = pd.DataFrame(cargos_comissionado_c.index,columns=['tipo'])

y = 0
for nome in cargos_comissionado_civil.tipo:
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    print(texto)
    todos = comissionado_ativo_civil.query(texto)
    soma = soma_arrecadacao_civil_ativo(todos,0.14)
    cargos_comissionado_civil.loc[y,'arrecadacao'] = soma
    y += 1


# 3 Arrecadação civil cargos inativos
cargos_inativos_c = inativo_civil['Cargo'].value_counts()

cargos_inativos_civil = pd.DataFrame(cargos_inativos_c.index,columns=['tipo'])

y = 0
for nome in cargos_inativos_civil.tipo:
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    # print(texto)
    todos = inativo_civil.query(texto)
    soma = soma_arrecadacao_civil_inativo(todos,0.14,teto_inss)
    cargos_inativos_civil.loc[y,'arrecadacao'] = soma
    y += 1

# 4 Arrecadação pensionista especial cargos inativos
soma = 0
cargos_pensionista = pd.DataFrame(['PENSOES ESPECIAIS'],columns=['tipo'])
soma = soma_arrecadacao_civil_inativo(pensionista_especial,0.14,teto_inss)
cargos_pensionista.loc[0,'arrecadacao'] = soma

# 5 Arrecadação pensionista iprev
soma = 0
cargos_pensionista_iprev = pd.DataFrame(['PENSIONISTA DO IPREV'],columns=['tipo'])
soma = soma_arrecadacao_civil_inativo(pensionista_iprev,0.14,teto_inss)
cargos_pensionista_iprev.loc[0,'arrecadacao'] = soma

# 6 Arrecadação militares ativo

cargos_ativos_m = ativo_militar['Cargo'].value_counts()

cargos_ativos_militar = pd.DataFrame(cargos_ativos_m.index,columns=['tipo'])

y=0
for nome in cargos_ativos_militar.tipo:
    # Arrecadacao ativo por cargo
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    # print(texto)
    todos_b = ativo_militar.query(texto)
    # Servidores ativos: 14% sobre o salário de contribuição.
    soma = soma_arrecadacao_militar(todos_b,0.105)
    cargos_ativos_militar.loc[y,'arrecadacao'] = soma
    y += 1

# 7 Arrecadação  Militares inativos 

cargos_inativos_m = inativo_militar['Cargo'].value_counts()

cargos_inativos_militar = pd.DataFrame(cargos_inativos_m.index,columns=['tipo'])

y=0
for nome in cargos_inativos_militar.tipo:
    # Arrecadacao ativo por cargo
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    # print(texto)
    todos_b = inativo_militar.query(texto)
    # Servidores ativos: 14% sobre o salário de contribuição.
    soma = soma_arrecadacao_militar(todos_b,0.105)
    cargos_inativos_militar.loc[y,'arrecadacao'] = soma
    y += 1

# 8 Arrecadação  Militares comissionados

cargos_comissionado_m = comissionado_ativo_militar['Cargo'].value_counts()

cargos_comissionado_militar = pd.DataFrame(cargos_comissionado_m.index,columns=['tipo'])

y=0
for nome in cargos_comissionado_militar.tipo:
    # Arrecadacao ativo por cargo
    soma = 0
    nome_txt = "'"+nome+"'"
    texto = f'Cargo == {nome_txt}'
    # print(texto)
    todos_b = comissionado_ativo_militar.query(texto)
    # Servidores ativos: 14% sobre o salário de contribuição.
    soma = soma_arrecadacao_militar(todos_b,0.105)
    cargos_comissionado_militar.loc[y,'arrecadacao'] = soma
    y += 1


print('Todos os dados dos cargos')
print('total despesas: ',sum(cargos_despesas['despesas']))
print('Total de arrecadação')
arrecadacao_t = sum(cargos_ativos_civil['arrecadacao']) + sum(cargos_comissionado_civil['arrecadacao'])+sum(cargos_inativos_civil['arrecadacao'])+sum(cargos_pensionista['arrecadacao'])+sum(cargos_pensionista_iprev['arrecadacao'])+sum(cargos_ativos_militar['arrecadacao'])+sum(cargos_inativos_militar['arrecadacao'])+sum(cargos_comissionado_militar['arrecadacao'])

cargos_arrecadacao = pd.concat([cargos_ativos_civil, cargos_comissionado_civil,
                                cargos_inativos_civil,cargos_pensionista,
                                cargos_pensionista_iprev,cargos_ativos_militar,
                                cargos_inativos_militar,cargos_comissionado_militar])

cargos_arrecadacao = cargos_arrecadacao.reset_index(drop=True)

cargos_total= pd.DataFrame(columns=['tipo','arrecadacao','despesas'])
count = 0
y = 0
for nome in cargos_arrecadacao.tipo:
    count += 1
    nome_txt = "'"+nome+"'"
    texto = f'tipo == {nome_txt}'
    despesa = cargos_despesas.query(texto)
    if len(despesa):
        print(despesa['despesas'])
        cargos_total.loc[y,'tipo'] = nome
        cargos_total.loc[y,'arrecadacao'] = float(cargos_arrecadacao['arrecadacao'][count])
        cargos_total.loc[y,'despesas'] = float(despesa['despesas'].values)
        cargos_total.loc[y,'diferenca'] = float(cargos_arrecadacao['arrecadacao'][count]) - float(despesa['despesas'].values)
        y += 1

    
y = 0
for ca in range(len(cargos_arrecadacao)):
    ficha = True
    for cd in range(len(cargos_despesas)):
        if cargos_arrecadacao['tipo'][ca] ==  cargos_despesas['tipo'][cd]:
            ficha = False
            cargos_total.loc[y,'tipo'] = cargos_arrecadacao['tipo'][ca]
            cargos_total.loc[y,'arrecadacao'] = float(cargos_arrecadacao['arrecadacao'][ca])
            cargos_total.loc[y,'despesas'] = float(cargos_despesas['despesas'][cd])
            cargos_total.loc[y,'diferenca'] = float(cargos_arrecadacao['arrecadacao'][ca] - cargos_despesas['despesas'][cd])
            y += 1
    # if ficha:
    #     cargos_total.loc[y,'tipo'] = cargos_arrecadacao['tipo'][ca]
    #     cargos_total.loc[y,'arrecadacao'] = float(cargos_arrecadacao['arrecadacao'][ca])
    #     cargos_total.loc[y,'despesas'] = 0
    #     cargos_total.loc[y,'diferenca'] = float(cargos_arrecadacao['arrecadacao'][ca])
    #     y += 1
        
inativo_civil = (inativo[inativo.OrgaoOrigem != 'POLICIA MILITAR']) 
cargos_p = cargos_arrecadacao['tipo']
import plotly.graph_objects as go
animals=['giraffes', 'orangutans', 'monkeys']

fig = go.Figure(data=[
    go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
    go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
])
# Change the bar mode
fig.update_layout(barmode='group')
fig.show()


'''
inativo = 

comissionado_ativo = 

pensionista_especial = 

pensionista_iprev = 




print('-------------------------------------------------------------')
print('Valor total gasto com ativos: ', sum(ativo['ValorBruto']))

print('Valor total gasto com inativos: ', sum(inativo['ValorBruto']))


cargos_ativo_qtd = ativo['Cargo'].value_counts()

cargos_ativo_qtd = cargos_ativo_qtd.to_frame(name='Quantidade')
cargos_ativo_qtd['Cargos'] = cargos_ativo_qtd.index
cargos_ativo_qtd = cargos_ativo_qtd.reset_index(drop = True)
posicao = [x for x in range(1,len(cargos_ativo_qtd)+1)]
cargos_ativo_qtd['RANKING'] = posicao
cargos_ativo_qtd = cargos_ativo_qtd[['RANKING','Cargos','Quantidade']]

cargos_inativo_qtd = inativo['Cargo'].value_counts()

cargos_inativo_qtd = cargos_inativo_qtd.to_frame(name='Quantidade')
cargos_inativo_qtd['Cargos'] = cargos_inativo_qtd.index
cargos_inativo_qtd = cargos_inativo_qtd.reset_index(drop = True)
posicao = [x for x in range(1,len(cargos_inativo_qtd)+1)]
cargos_inativo_qtd['RANKING'] = posicao
cargos_inativo_qtd = cargos_inativo_qtd[['RANKING','Cargos','Quantidade']]


# Numero de Órgãos ativos

Orgaos_ativo_qtd = ativo['OrgaoOrigem'].value_counts()
Orgaos_ativo_qtd = Orgaos_ativo_qtd.to_frame(name='Quantidade')
Orgaos_ativo_qtd['Orgaos'] = Orgaos_ativo_qtd.index
Orgaos_ativo_qtd = Orgaos_ativo_qtd.reset_index(drop = True)
posicao = [x for x in range(1,len(Orgaos_ativo_qtd)+1)]
Orgaos_ativo_qtd['RANKING'] = posicao
Orgaos_ativo_qtd = Orgaos_ativo_qtd[['RANKING','Orgaos','Quantidade']]

# Numero de Órgãos inativos

Orgaos_inativo_qtd = inativo['OrgaoOrigem'].value_counts()
Orgaos_inativo_qtd = Orgaos_inativo_qtd.to_frame(name='Quantidade')
Orgaos_inativo_qtd['Orgaos'] = Orgaos_inativo_qtd.index
Orgaos_inativo_qtd = Orgaos_inativo_qtd.reset_index(drop = True)
posicao = [x for x in range(1,len(Orgaos_inativo_qtd)+1)]
Orgaos_inativo_qtd['RANKING'] = posicao
Orgaos_inativo_qtd = Orgaos_inativo_qtd[['RANKING','Orgaos','Quantidade']]


# Fazer a soma por grupos
ativo_valor = ativo[['OrgaoOrigem','ValorBruto']]

salario_orgao_ativo = ativo_valor.groupby(['OrgaoOrigem']).sum()
# salario_orgao_ativo = Orgaos_inativo_qtd.to_frame(name='Quantidade')
salario_orgao_ativo['Orgaos'] = salario_orgao_ativo.index
salario_orgao_ativo = salario_orgao_ativo.sort_values(['ValorBruto'])
salario_orgao_ativo= salario_orgao_ativo.reset_index(drop = True)

inativo_valor = inativo[['OrgaoOrigem','ValorBruto']]

salario_orgao_inativo = inativo_valor.groupby(['OrgaoOrigem']).sum()
# salario_orgao_ativo = Orgaos_inativo_qtd.to_frame(name='Quantidade')
salario_orgao_inativo['Orgaos'] = salario_orgao_inativo.index
salario_orgao_inativo = salario_orgao_inativo.sort_values(['ValorBruto'])
salario_orgao_inativo= salario_orgao_inativo.reset_index(drop = True)


# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# import plotly.express as px
# import pandas as pd

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



# fig = px.bar(ativo, x="OrgaoOrigem", y="ValorBruto", color="Cargo")

# fig_orgaos = px.bar(Orgaos_ativo_qtd , x="Quantidade", y="Orgaos")

# app.layout = html.Div(children=[
#     html.H1(children='Divisão por Orgão'),

#     html.Div(children='''
#         Agrupamento por Orgão de Origem.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     ),
#     html.Div(children='''
#         Agrupamento por Orgão de Origem.
#     '''),

#     dcc.Graph(
#         id='example-graph2',
#         figure=fig_orgaos
#     )
# ])

# if __name__ == '__main__':
#     app.run_server(debug=True)

