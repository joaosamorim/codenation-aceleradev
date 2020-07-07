#!/usr/bin/env python
# coding: utf-8

# # Desafio 4
# 
# Neste desafio, vamos praticar um pouco sobre testes de hipóteses. Utilizaremos o _data set_ [2016 Olympics in Rio de Janeiro](https://www.kaggle.com/rio2016/olympic-games/), que contém dados sobre os atletas das Olimpíadas de 2016 no Rio de Janeiro.
# 
# Esse _data set_ conta com informações gerais sobre 11538 atletas como nome, nacionalidade, altura, peso e esporte praticado. Estaremos especialmente interessados nas variáveis numéricas altura (`height`) e peso (`weight`). As análises feitas aqui são parte de uma Análise Exploratória de Dados (EDA).
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[135]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as sct
import seaborn as sns
import statsmodels.api as sm


# In[136]:


#%matplotlib inline

from IPython.core.pylabtools import figsize

figsize(12, 8)

sns.set()


# In[137]:


athletes = pd.read_csv("athletes.csv")


# In[138]:


def get_sample(df, col_name, n=100, seed=42):
    """Get a sample from a column of a dataframe.
    
    It drops any numpy.nan entries before sampling. The sampling
    is performed without replacement.
    
    Example of numpydoc for those who haven't seen yet.
    
    Parameters
    ----------
    df : pandas.DataFrame
        Source dataframe.
    col_name : str
        Name of the column to be sampled.
    n : int
        Sample size. Default is 100.
    seed : int
        Random seed. Default is 42.
    
    Returns
    -------
    pandas.Series
        Sample of size n from dataframe's column.
    """
    np.random.seed(seed)
    
    random_idx = np.random.choice(df[col_name].dropna().index, size=n, replace=False)
    
    return df.loc[random_idx, col_name]


# ## Inicia sua análise a partir daqui

# In[139]:


athletes.head()


# In[140]:


athletes.describe()


# ## Questão 1
# 
# Considerando uma amostra de tamanho 3000 da coluna `height` obtida com a função `get_sample()`, execute o teste de normalidade de Shapiro-Wilk com a função `scipy.stats.shapiro()`. Podemos afirmar que as alturas são normalmente distribuídas com base nesse teste (ao nível de significância de 5%)? Responda com um boolean (`True` ou `False`).

# In[141]:


def q1():
    height_sample = get_sample(athletes, 'height', 3000)
    
    if (sct.shapiro(height_sample)[1] > 0.05):
        return True
    else:
        return False


# __Para refletir__:
# 
# 1. Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# 
#     **Resposta**: Sim, visualmente a amostra realmente segue uma distribuição normal.
#     
#     
# 2. Plote o qq-plot para essa variável e a analise.
# 
#     **Resposta**: Apresentada no código abaixo.
#     
#     
# 3. Existe algum nível de significância razoável que nos dê outro resultado no teste? (Não faça isso na prática. Isso é chamado _p-value hacking_, e não é legal).
# 
#     **Resposta**: Sim, algum nível de significância (alfa) maior do que 15% resultaria em uma distribuição não normal.

# In[142]:


# Showing the normal distribution

height_sample = get_sample(athletes, 'height', 3000)

plt.hist(x=height_sample, bins=25);


# In[143]:


# Comparing the sample 'height_sample' with the normal distribution

sm.qqplot(height_sample, fit=True, line="45");


# ## Questão 2
# 
# Repita o mesmo procedimento acima, mas agora utilizando o teste de normalidade de Jarque-Bera através da função `scipy.stats.jarque_bera()`. Agora podemos afirmar que as alturas são normalmente distribuídas (ao nível de significância de 5%)? Responda com um boolean (`True` ou `False`).

# In[144]:


def q2():
    height_sample = get_sample(athletes, 'height', 3000)
    
    if (sct.jarque_bera(height_sample)[1] > 0.05):
        return True
    else:
        return False


# __Para refletir__:
# 
# 1. Esse resultado faz sentido?
# 
#     **Resposta**: Sim!

# ## Questão 3
# 
# Considerando agora uma amostra de tamanho 3000 da coluna `weight` obtida com a função `get_sample()`. Faça o teste de normalidade de D'Agostino-Pearson utilizando a função `scipy.stats.normaltest()`. Podemos afirmar que os pesos vêm de uma distribuição normal ao nível de significância de 5%? Responda com um boolean (`True` ou `False`).

# In[145]:


def q3():
    weight_sample = get_sample(athletes, 'weight', 3000)
    
    if (sct.normaltest(weight_sample)[1] > 0.05):
        return True
    else:
        return False


# __Para refletir__:
# 
# * Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# * Um _box plot_ também poderia ajudar a entender a resposta.

# In[146]:


# Showing the normal distribution

weight_sample = get_sample(athletes, 'weight', 3000)

plt.hist(x=weight_sample, bins=25);


# In[147]:


# Plotting a boxplot from the sample to showing how to disperse it is.

fig, ax = plt.subplots()
bp = ax.boxplot(weight_sample)

ax.set_ylabel('weight')
plt.setp(bp['whiskers'], color='k', linestyle='-')
plt.setp(bp['fliers'], markersize=3.0);


# ## Questão 4
# 
# Realize uma transformação logarítmica em na amostra de `weight` da questão 3 e repita o mesmo procedimento. Podemos afirmar a normalidade da variável transformada ao nível de significância de 5%? Responda com um boolean (`True` ou `False`).

# In[148]:


def q4():
    weight_sample = get_sample(athletes, 'weight', 3000)
    
    weight_log_sample = np.log(weight_sample)
    
    if (sct.normaltest(weight_sample)[1] > 0.05):
        return True
    else:
        return False


# __Para refletir__:
# 
# 1. Plote o histograma dessa variável (com, por exemplo, `bins=25`). A forma do gráfico e o resultado do teste são condizentes? Por que?
# 
#     **Resposta**: Sim, apesar de visualmente a aparência ser de uma distribuição normal, as caudas da curva são muito acentuadas, e como o nível de significância é bem preciso (baixo), isso impossibilita a distribuição de ser normal.
# 
# 2. Você esperava um resultado diferente agora?
# 
#     **Resposta**: Em uma primeira análise sim, entretanto, ao analisar o q-q plot fica mais evidente que a amostra não segue uma distribuição normal em todo o seu espectro.

# In[149]:


# Showing the normal distribution

weight_sample = get_sample(athletes, 'weight', 3000)
    
weight_log_sample = np.log(weight_sample)

plt.hist(x=weight_log_sample, bins=25);


# In[150]:


# Comparing the sample 'weight_log_sample' with the normal distribution

sm.qqplot(weight_log_sample, fit=True, line="45");


# > __Para as questão 5 6 e 7 a seguir considere todos testes efetuados ao nível de significância de 5%__.

# ## Questão 5
# 
# Obtenha todos atletas brasileiros, norte-americanos e canadenses em `DataFrame`s chamados `bra`, `usa` e `can`,respectivamente. Realize um teste de hipóteses para comparação das médias das alturas (`height`) para amostras independentes e variâncias diferentes com a função `scipy.stats.ttest_ind()` entre `bra` e `usa`. Podemos afirmar que as médias são estatisticamente iguais? Responda com um boolean (`True` ou `False`).

# In[151]:


def q5():
    bra = athletes[athletes['nationality'] == 'BRA']
    usa = athletes[athletes['nationality'] == 'USA']

    if (sct.ttest_ind(bra['height'], usa['height'], equal_var=False, nan_policy='omit')[1] > 0.05):
        return True
    else:
        return False


# ## Questão 6
# 
# Repita o procedimento da questão 5, mas agora entre as alturas de `bra` e `can`. Podemos afimar agora que as médias são estatisticamente iguais? Reponda com um boolean (`True` ou `False`).

# In[152]:


def q6():
    bra = athletes[athletes['nationality'] == 'BRA']
    can = athletes[athletes['nationality'] == 'CAN']

    if (sct.ttest_ind(bra['height'], can['height'], equal_var=False, nan_policy='omit')[1] > 0.05):
        return True
    else:
        return False


# ## Questão 7
# 
# Repita o procedimento da questão 6, mas agora entre as alturas de `usa` e `can`. Qual o valor do p-valor retornado? Responda como um único escalar arredondado para oito casas decimais.

# In[153]:


def q7():
    usa = athletes[athletes['nationality'] == 'USA']
    can = athletes[athletes['nationality'] == 'CAN']

    pvalue = sct.ttest_ind(usa['height'], can['height'], equal_var=False, nan_policy='omit')[1]
    
    return float(round(pvalue, 8))


# __Para refletir__:
# 
# 1. O resultado faz sentido?
# 
#     **Respostas**: A partir da plotagem abaixo, fica evidente que a média nas questões 5 e 7 realmente não são condizentes para um nível de significância de 5%, enquanto para a questão 6, possivelmente os valores são considerados iguais.

# In[154]:


athletes_nan = athletes.dropna()

usa = athletes_nan[athletes_nan['nationality'] == 'USA']
can = athletes_nan[athletes_nan['nationality'] == 'CAN']
bra = athletes_nan[athletes_nan['nationality'] == 'BRA']

figsize(15, 6)

fig, axs = plt.subplots(1, 3)

axs[0].set_title('Question 5')
axs[0].set_ylabel('Height')
axs[0].hist(usa['height'], bins=25, alpha=0.5, color='r', label='USA')
axs[0].hist(bra['height'], bins=25, alpha=0.5, color='b', label='BRA')
axs[0].axvline(usa['height'].mean(), color='r', linestyle='dashed', linewidth=1)
axs[0].axvline(bra['height'].mean(), color='b', linestyle='dashed', linewidth=1)
axs[0].legend(loc='upper right')

axs[1].set_title('Question 6')
axs[1].set_ylabel('Height')
axs[1].hist(can['height'], bins=25, alpha=0.5, color='r', label='CAN')
axs[1].hist(bra['height'], bins=25, alpha=0.5, color='b', label='BRA')
axs[1].axvline(can['height'].mean(), color='r', linestyle='dashed', linewidth=1)
axs[1].axvline(bra['height'].mean(), color='b', linestyle='dashed', linewidth=1)
axs[1].legend(loc='upper right')

axs[2].set_title('Question 7')
axs[2].set_ylabel('Height')
axs[2].hist(usa['height'], bins=25, alpha=0.5, color='r', label='USA')
axs[2].hist(can['height'], bins=25, alpha=0.5, color='b', label='CAN')
axs[2].axvline(usa['height'].mean(), color='r', linestyle='dashed', linewidth=1)
axs[2].axvline(can['height'].mean(), color='b', linestyle='dashed', linewidth=1)
axs[2].legend(loc='upper right');

