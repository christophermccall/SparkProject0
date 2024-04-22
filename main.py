from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from make_requests import get_top_vids



def spark_df(vids):
    spark = SparkSession.builder.appName("Trending").getOrCreate()
    df = spark.createDataFrame(vids)
    df.limit(10).show()



trending_vids = get_top_vids()
spark_df(trending_vids)
