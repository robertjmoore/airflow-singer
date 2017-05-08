"""
Code that goes along with the Airflow located at:
http://airflow.readthedocs.org/en/latest/tutorial.html
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'robertjmoore',
    'depends_on_past': True,
    'start_date': datetime(2016, 7, 13),
    'email': ['robertj@robertjmoore.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

scriptpath = '~/Dropbox/airflow-singer/scripts/'
base_path = '/tmp/singer-sync/'

dag = DAG(
    'salesforce-singer-sync', default_args=default_args, schedule_interval=timedelta(1))

t_download = BashOperator(
    task_id='download_today',
    bash_command='python3 ' + scriptpath + 'downloadtoday.py "{{ execution_date }}"',
    retries=3,
    dag=dag)

t_extract = BashOperator(
    task_id='extract_downloads',
    bash_command='python3 ' + scriptpath + 'extractdownloads.py "{{ execution_date }}"',
    retries=3,
    dag=dag)

t_singerconfig = BashOperator(
    task_id='singer_config',
    bash_command='python3 ' + scriptpath + 'generatesingerconfig.py "{{ execution_date }}"',
    retries=3,
    dag=dag)

t_singerpush = BashOperator(
    task_id='singer_push',
    bash_command='tap-csv -c ' + base_path + "{{ execution_date.strftime('%Y-%m-%d') }}" + '/' + 'csv-config.json | target-stitch -c ~/Stitch/configs/stitch_mbi_config.json',
    retries=3,
    dag=dag)

t_cleanup = BashOperator(
    task_id='cleanup',
    bash_command='python3 ' + scriptpath + 'cleanup.py "{{ execution_date }}"',
    retries=3,
    dag=dag)

t_cleanup.set_upstream(t_singerpush)
t_singerpush.set_upstream(t_singerconfig)
t_singerconfig.set_upstream(t_extract)
t_extract.set_upstream(t_download)