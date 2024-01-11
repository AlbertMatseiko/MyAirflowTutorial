from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

PATH_TO_OUTPUT = "/opt/airflow/output"
with DAG(
    "my_bash_echo_tutorial",
    default_args={
        "retries":21,
        "retry_delay": timedelta(minutes=5),
    },
    description="A simple tutorial DAG",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example"],
) as dag:

    t1 = BashOperator(
        task_id="create_hello.txt",
        bash_command=f"touch {PATH_TO_OUTPUT}/hello.txt",
    )

    t2 = BashOperator(
        task_id="fill_hello.txt",
        bash_command=f"echo 'hello Airflow' >> {PATH_TO_OUTPUT}/hello.txt",
    )

    # t3 = BashOperator(
    #     task_id="make_pwd",
    #     bash_command="ls -R | grep ':$' | sed -e 's/:$//' -e 's/[^-][^\/]*\//--/g' -e 's/^/   /' -e 's/-/|/'",
    # )

    t1 >> t2# >> t3