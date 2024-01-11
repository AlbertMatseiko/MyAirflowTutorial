from airflow.models.dag import DAG
from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
import os

PATH_TO_OCR = "/opt/airflow/airflow_data"
def get_command_line(PATH_TO_OCR):
    try:
        list_of_names = sorted([n for n in os.listdir(f"{PATH_TO_OCR}/pics/") if n.endswith('png')])
        command_string = ""
        for i, name in enumerate(list_of_names):
            command_string += f"tesseract {PATH_TO_OCR}/pics/{name} {PATH_TO_OCR}/ocr/exp{i+1} -l rus+equ+eng &&"
        return command_string[:-3] 
    except:
        pass

with DAG(
    "my_ocr_dag_tutorial",
    default_args={
        "retries":21,
        "retry_delay": timedelta(minutes=5),
    },
    description="Convert pdf to txt file.",
    schedule=timedelta(days=1),
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["example","ocr"],
) as dag:

    t1 = BashOperator(
        task_id="make_dirs_structure",
        bash_command=f"mkdir -p {PATH_TO_OCR} {PATH_TO_OCR}/ocr {PATH_TO_OCR}/pics",
    )

    t2 = BashOperator(
        task_id="download_book",
        bash_command=f"rm -f {PATH_TO_OCR}/*.pdf*\
                       && wget --no-check-certificate https://mathus.ru/math/geometric-progression.pdf -P {PATH_TO_OCR}/",
    )

    t3 = BashOperator(
        task_id="transform_to_pngs",
        bash_command=f"rm -f {PATH_TO_OCR}/ocr/*.txt*\
                       && gs -dNOPAUSE -dBATCH -sDEVICE=png16m -r300 -sOutputFile='{PATH_TO_OCR}/pics/Pic%d.png' {PATH_TO_OCR}/geometric-progression.pdf",
    )

    t4 = BashOperator(
        task_id="do_ocr",
        bash_command=get_command_line(PATH_TO_OCR),
    )

    t5 = BashOperator(
        task_id="concat",
        bash_command=f"cat {PATH_TO_OCR}/ocr/* > {PATH_TO_OCR}/result.txt",
    )

    t1 >> t2 >> t3 >> t4 >> t5