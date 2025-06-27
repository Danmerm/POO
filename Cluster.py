import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 1. Criar dados fictícios
np.random.seed(42)
n_samples = 1000

idade = np.random.randint(18, 70, n_samples)
renda = np.random.randint(20000, 100000, n_samples)
freq_compras = np.random.randint(1, 20, n_samples)
valor_medio_compra = 50 + 0.001 * renda + np.random.normal(0, 10, n_samples)

# Criar DataFrame
df = pd.DataFrame({
    'idade': idade,
    'renda': renda,
    'freq_compras': freq_compras,
    'valor_medio_compra': valor_medio_compra
})

# 2. Realizar clustering
kmeans = KMeans(n_clusters=3, random_state=42)
df['cluster'] = kmeans.fit_predict(df[['idade', 'renda', 'freq_compras']])

# 3. Visualizar clusters
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df['idade'], df['renda'], c=df['cluster'], cmap='viridis')
plt.colorbar(scatter)
plt.xlabel('Idade')
plt.ylabel('Renda')
plt.title('Clusters de Clientes')
plt.show()

# 4. Treinar modelos preditivos para cada cluster
models = {}
for cluster in df['cluster'].unique():
    cluster_data = df[df['cluster'] == cluster]
    X = cluster_data[['idade', 'renda', 'freq_compras']]
    y = cluster_data['valor_medio_compra']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    models[cluster] = model
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"MSE para cluster {cluster}: {mse:.2f}")

# 5. Fazer previsões para novos dados
novo_cliente = np.array([[35, 60000, 10]])  # idade, renda, freq_compras
cluster_novo_cliente = kmeans.predict(novo_cliente)[0]
previsao = models[cluster_novo_cliente].predict(novo_cliente)[0]

print(f"\nNovo cliente pertence ao cluster: {cluster_novo_cliente}")
print(f"Previsão de valor médio de compra: ${previsao:.2f}")


# import numpy as np
# import pandas as pd
# from sklearn.cluster import KMeans
# from sklearn.linear_model import LinearRegression
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error
# import matplotlib.pyplot as plt

# # 1. Criar dados fictícios
# np.random.seed(42)
# n_samples = 1000

# idade = np.random.randint(18, 70, n_samples)
# tempo_site = np.random.randint(1, 60, n_samples)
# compras_anteriores = np.random.randint(0, 20, n_samples)

# # Criar valor_compra com alguma relação não-linear com as outras variáveis
# valor_compra = (idade * 0.5 + tempo_site * 2 + compras_anteriores * 10 + 
#                 np.random.normal(0, 100, n_samples))

# data = pd.DataFrame({
#     'idade': idade,
#     'tempo_site': tempo_site,
#     'compras_anteriores': compras_anteriores,
#     'valor_compra': valor_compra
# })

# # 2. Dividir em conjunto de treino e teste
# X = data[['idade', 'tempo_site', 'compras_anteriores']]
# y = data['valor_compra']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # 3. Aplicar clustering nos dados de treino
# kmeans = KMeans(n_clusters=3, random_state=42)
# cluster_labels = kmeans.fit_predict(X_train)

# # 4. Treinar um modelo para cada cluster
# models = {}
# for cluster in range(3):
#     cluster_data = X_train[cluster_labels == cluster]
#     cluster_target = y_train[cluster_labels == cluster]
#     model = LinearRegression()
#     model.fit(cluster_data, cluster_target)
#     models[cluster] = model

# # 5. Função para prever usando o modelo de clustering
# def predict_with_clustering(X):
#     cluster = kmeans.predict(X)
#     predictions = np.zeros(len(X))
#     for i in range(len(X)):
#         predictions[i] = models[cluster[i]].predict(X.iloc[i].values.reshape(1, -1))
#     return predictions

# # 6. Fazer previsões e calcular o erro
# y_pred_cluster = predict_with_clustering(X_test)
# mse_cluster = mean_squared_error(y_test, y_pred_cluster)

# # Comparar com um modelo simples sem clustering
# simple_model = LinearRegression()
# simple_model.fit(X_train, y_train)
# y_pred_simple = simple_model.predict(X_test)
# mse_simple = mean_squared_error(y_test, y_pred_simple)

# print(f"MSE com clustering: {mse_cluster}")
# print(f"MSE sem clustering: {mse_simple}")

# # 7. Visualizar os resultados
# plt.figure(figsize=(12, 6))
# plt.scatter(y_test, y_pred_cluster, alpha=0.5)
# plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
# plt.xlabel("Valor real")
# plt.ylabel("Valor previsto")
# plt.title("Previsões usando Clustering Preditivo")
# plt.show()