/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
export PATH="$PATH:/opt/homebrew/bin"
brew install colima
brew install docker docker-compose
ln -sfn /opt/homebrew/opt/docker-compose/bin/docker-compose ~/.docker/cli-plugins/docker-compose
colima start --memory 8
mkdir -p ./dags ./logs ./plugins ./config ./output ./airflow_data
echo -e "AIRFLOW_UID=$(id -u)" > .env
docker compose up airflow-init
docker compose up --build