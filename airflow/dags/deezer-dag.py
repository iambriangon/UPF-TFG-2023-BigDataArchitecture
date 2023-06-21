from datetime import timedelta
from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow import DAG

spark_master = 'spark://spark-master:7077'

python_path = '/opt/airflow/dags/ETL/deezer-scrapper.py'
spark_path = '/opt/airflow/dags/ETL/deezer-spark.py'

python_cmd = f'python3 {python_path}'
spark_cmd = f'spark-submit --master {spark_master} --name Spark_Deezer --verbose {spark_path}'

with DAG(
        dag_id='deezer_dag',
        description='This dag runs daily, extracts Deezer chart and uploads to HDFS and Hive',
        start_date=datetime(2023, 1, 1),
        schedule_interval=timedelta(days=1),
        catchup=False,
) as dag:
    start = EmptyOperator(task_id='start')

    etl = BashOperator(
        task_id='python_task',
        bash_command=python_cmd
    )

    spark = BashOperator(
        task_id='spark_task',
        bash_command=spark_cmd
    )

    end = EmptyOperator(task_id='end')

    start >> etl >> spark >> end
