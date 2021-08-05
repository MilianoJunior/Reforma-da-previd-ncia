import chardet
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

with open('../dados/Efetivo_ativo.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
ativo = pd.read_csv('../dados/Efetivo_ativo.csv', encoding=result['encoding'],sep=';',index_col=False)
ativo['ValorBruto'] = ativo['ValorBruto'].str.replace(',', '.').astype(float)

with open('../dados/Efetivo_inativo.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
inativo = pd.read_csv('../dados/Efetivo_inativo.csv',encoding=result['encoding'],sep=';',index_col=False)
inativo['ValorBruto'] = inativo['ValorBruto'].str.replace(',', '.').astype(float)

with open('../dados/efetivo_comissionado_ativo.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
comissionado_ativo = pd.read_csv('../dados/efetivo_comissionado_ativo.csv',encoding=result['encoding'],sep=';',index_col=False)
comissionado_ativo['ValorBruto'] = comissionado_ativo ['ValorBruto'].str.replace(',', '.').astype(float)

with open('../dados/Pensionista_especial.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
pensionista_especial = pd.read_csv('../dados/Pensionista_especial.csv',encoding=result['encoding'],sep=';',index_col=False)
pensionista_especial['ValorBruto'] = pensionista_especial['ValorBruto'].str.replace(',', '.').astype(float)

with open('../dados/Pensionista_iprev.csv', 'rb') as f:
    result = chardet.detect(f.read())  # or readline if the file is large
pensionista_iprev = pd.read_csv('../dados/Pensionista_iprev.csv',encoding=result['encoding'],sep=';',index_col=False)
pensionista_iprev['ValorBruto'] = pensionista_iprev['ValorBruto'].str.replace(',', '.').astype(float)

tabela = pensionista_iprev.isnull().sum()

from unidecode import unidecode
# cargos ativos civil 691, ativos militares 52


def duplicidade(dados):
    y = 0
    for nome in dados['Cargo']:
        dados.loc[y,'Cargo'] = unidecode(nome)
        
        y+= 1
    print('termino')
    return dados

ativo = duplicidade(ativo)
inativo = duplicidade(inativo)
comissionado_ativo = duplicidade(comissionado_ativo)
# pensionista_especial = duplicidade(pensionista_especial)
pensionista_iprev = duplicidade(pensionista_iprev)

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
''' Verificação de todos os cargos duplicidade'''
cargos_inativos = inativo['Cargo'].value_counts()
cargos_pensionista = pensionista_especial['OrgaoOrigem'].value_counts()
cargos_pensionista_iprev = pensionista_iprev['Cargo'].value_counts()

#------------------------------------------

cargos_ativos_c = ativo_civil['Cargo'].value_counts()

cargos_comissionado_c = comissionado_ativo_civil['Cargo'].value_counts()

cargos_inativos_c = inativo_civil['Cargo'].value_counts()

cargos_ativos_m = ativo_militar['Cargo'].value_counts()

cargos_inativos_m = inativo_militar['Cargo'].value_counts()

cargos_comissionado_m = comissionado_ativo_militar['Cargo'].value_counts()


def comparar(a,b):
    for s in a.index:
        for d in b.index:
            if s != d:
                print(s)

comparar(cargos_inativos,cargos_inativos)

#232



cargos_despesas = pd.DataFrame(cargos_inativos.index,columns=['tipo'])
cargos_despesas['quantidade'] = cargos_inativos.values

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
cargos_despesas.loc[232,'quantidade'] = len(pensionista_especial['ValorBruto'])
#---------------------------------------------------
cargos_despesas.loc[233,'tipo'] = 'PENSIONISTA DO IPREV'
cargos_despesas.loc[233,'despesas'] = sum(pensionista_iprev['ValorBruto'])
cargos_despesas.loc[233,'quantidade'] = len(pensionista_iprev['ValorBruto'])

#----------------------------------------------------


# Arrecadação

# 1 Arrecadação civil cargos ativados


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

filtro = cargos_arrecadacao['tipo'].value_counts()
arrecadar_filtro= pd.DataFrame(filtro.index,columns=['tipo'])
y = 0
for fil in filtro.index:
    soma = 0
    for i in range(len(cargos_arrecadacao)):
        if fil == cargos_arrecadacao['tipo'].values[i]:
            soma = soma + cargos_arrecadacao['arrecadacao'].values[i]
    arrecadar_filtro.loc[y,'arrecadacao'] = soma
    y+= 1
    


cargos_total= pd.DataFrame(columns=['tipo','arrecadacao','despesas'])
count = 0
y = 0
for nome in arrecadar_filtro.tipo:
    
    nome_txt = "'"+nome+"'"
    texto = f'tipo == {nome_txt}'
    despesa = cargos_despesas.query(texto)
    if len(despesa) > 0:
        print(despesa['despesas'])
        cargos_total.loc[y,'tipo'] = nome
        cargos_total.loc[y,'arrecadacao'] = float(arrecadar_filtro['arrecadacao'][count])
        cargos_total.loc[y,'despesas'] = float(despesa['despesas'].values)
        cargos_total.loc[y,'diferenca'] = float(arrecadar_filtro['arrecadacao'][count]) - float(despesa['despesas'].values)
        count += 1
        y += 1

    
cargos_total_b= pd.DataFrame(columns=['Cargos','arrecadação','Despesas'])
y = 0
s = 0
for ca in range(len(arrecadar_filtro)):
    ficha = True
    s = 0
    for cd in range(len(cargos_despesas)):
        if arrecadar_filtro['tipo'][ca] ==  cargos_despesas['tipo'][cd]:
            ficha = False
            s+= 1
            cargos_total_b.loc[y,'Cargos'] =arrecadar_filtro['tipo'][ca]
            cargos_total_b.loc[y,'Arrecadação'] = float(arrecadar_filtro['arrecadacao'][ca])
            cargos_total_b.loc[y,'Despesas'] = float(cargos_despesas['despesas'][cd])
            cargos_total_b.loc[y,'Diferença'] = float(arrecadar_filtro['arrecadacao'][ca] - cargos_despesas['despesas'][cd])
            cargos_total_b.loc[y,'Quantidade'] = float(cargos_despesas['quantidade'][cd])
            cargos_total_b.loc[y,'Aposentadoria Media'] = float(cargos_despesas['despesas'][cd])/float(cargos_despesas['quantidade'][cd])
            y += 1
        if s>1:
            print(s,'Cargo reptido: ',arrecadar_filtro['tipo'][ca])
    if ficha:
        print(ca,'Não tem cargo nos inativos: ',arrecadar_filtro['tipo'][ca])
    #     cargos_total.loc[y,'tipo'] = cargos_arrecadacao['tipo'][ca]
    #     cargos_total.loc[y,'arrecadacao'] = float(cargos_arrecadacao['arrecadacao'][ca])
    #     cargos_total.loc[y,'despesas'] = 0
    #     cargos_total.loc[y,'diferenca'] = float(cargos_arrecadacao['arrecadacao'][ca])
    #     y += 1
        
# inativo_civil = (inativo[inativo.OrgaoOrigem != 'POLICIA MILITAR']) 
# cargos_p = cargos_arrecadacao['tipo']
import plotly.graph_objects as go
import plotly.express as px

cargos_total_b = cargos_total_b.sort_values(by=['Diferença'])
grafico=[]
# for rs in range(0,20):
# grafico.append(go.Bar(name='SF Zoo', x=cargos_total_b['tipo'][0:20].values, y=[20, 14, 23]))
periodo = 10
fig = go.Figure(data=[
    go.Bar(name='Arrecadação', x=cargos_total_b['Cargos'][0:periodo].values, y=cargos_total_b['Arrecadação'][0:periodo].values),
    go.Bar(name='Despesas', 
           x=cargos_total_b['Cargos'][0:periodo].values, 
           y=cargos_total_b['Despesas'][0:periodo].values,
           marker_color='crimson'),
    go.Bar(name='Défice', 
           x=cargos_total_b['Cargos'][0:periodo].values, 
           y=cargos_total_b['Diferença'][0:periodo].values,marker_color='red')
])

# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6)
                  
fig.update_layout(
    title_text='OS 10 MAIORES CARGOS DEFICITÁRIOS',
    yaxis=dict(
        title='R$(milhões)',
        titlefont_size=13,
        tickfont_size=12,
    ),
    legend=dict(
        x=0.7,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    font=dict(
        size=10,
        color="RebeccaPurple"
    ),
)
fig.write_html("menores.html")

cargos_total_b = cargos_total_b.sort_values(by=['Diferença'],ascending=False)

periodo = 10
fig = go.Figure(data=[
    go.Bar(name='Arrecadação', x=cargos_total_b['Cargos'][0:periodo].values, y=cargos_total_b['Arrecadação'][0:periodo].values),
    go.Bar(name='Despesas', 
           x=cargos_total_b['Cargos'][0:periodo].values, 
           y=cargos_total_b['Despesas'][0:periodo].values,
           marker_color='crimson'),
    go.Bar(name='Superávite', 
           x=cargos_total_b['Cargos'][0:periodo].values, 
           y=cargos_total_b['Diferença'][0:periodo].values,marker_color='cyan')
])

# fig.update_traces(texttemplate='%{text:.2s}', textposition='outside',marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',marker_line_width=1.5, opacity=0.6)
                  
fig.update_layout(
    title_text='OS 10 MAIORES CARGOS SUPERAVITÁRIOS',
    yaxis=dict(
        title='R$(milhões)',
        titlefont_size=13,
        tickfont_size=12,
    ),
    legend=dict(
        x=0.7,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    font=dict(
        size=10,
        color="RebeccaPurple"
    ),

)
fig.write_html("maiores.html")


html= cargos_total_b.to_html()
arq = open("tabela.html","w")
arq.write(html)



print(' ')
print('Criando tabela em markdown')
name_colunas = '|'
rows='|'
dados_colunas =''
dados_linhas= '|'
for colunas in cargos_total_b:
    name_colunas += f'{colunas}|'
    rows+='--------|'
print(name_colunas)
for dados in cargos_total_b.values:
    dados_linhas= '|'
    for s in dados:
        # print(s,type(s))
        s = str(round(float(s),3)) if isinstance(s,float) else s
        # print(s)
        dados_linhas += f'{s}|'
    dados_colunas += dados_linhas
    print(dados_linhas)
        
# print(name_colunas)
# print(rows)
# print(dados_colunas)









































