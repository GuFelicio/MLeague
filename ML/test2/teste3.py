from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from tqdm import tqdm
from pyspark.sql.functions import col

# Inicializando a sessão Spark com mais memória e ajuste de paralelismo
spark = SparkSession.builder \
    .appName("LoL_ML_Training") \
    .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "8g") \
    .config("spark.sql.shuffle.partitions", "200") \
    .config("spark.executor.instances", "4") \
    .config("spark.executor.cores", "4") \
    .getOrCreate()

# Carregar os dados
data_path = r"D:\NBHelp\noobHelp\venv\data\CSV\match_details_transformed(2).csv"
data = spark.read.csv(data_path, header=True, inferSchema=True)

# Converter gameResult para numérico
data = data.withColumn("gameResult", col("gameResult").cast("double"))

# Transformar colunas em features
feature_columns = [col for col in data.columns if col != 'gameResult']
assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
data = assembler.transform(data)

# Dividir os dados em treino e teste
train_data, test_data = data.randomSplit([0.8, 0.2])

# Definir o classificador RandomForest
rf = RandomForestClassifier(labelCol="gameResult", featuresCol="features", numTrees=100)

# Grid de parâmetros
paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [100, 200]) \
    .addGrid(rf.maxDepth, [5, 10]) \
    .build()

# Avaliador
evaluator = MulticlassClassificationEvaluator(labelCol="gameResult", metricName="accuracy")

# Validação cruzada
crossval = CrossValidator(estimator=rf,
                          estimatorParamMaps=paramGrid,
                          evaluator=evaluator,
                          numFolds=3)

# Treinamento do modelo com barra de progresso
for _ in tqdm(crossval.fit(train_data), desc="Treinando modelo RandomForest com Spark ML"):
    pass

# Avaliação no conjunto de teste
predictions = crossval.bestModel.transform(test_data)
accuracy = evaluator.evaluate(predictions)
print(f"Acurácia: {accuracy:.2f}")

# Salvar o modelo treinado
crossval.bestModel.write().overwrite().save(r"D:\NBHelp\noobHelp\venv\data\ML\best_stacking_model(4).pkl")
