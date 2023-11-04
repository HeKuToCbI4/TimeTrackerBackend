echo "Preparation of venv:"
echo "SKIPPED AS NOT IMPLEMENTED!"

echo "activate venv"
.\venv\Scripts\activate.ps1

echo "Update packages:"
echo "SKIP AS NOT IMPLEMENTED :)"


echo "Compile proto files"
.\compile_proto.ps1

echo "make migrations"
.\manage.py makemigrations

echo "migrate"
.\manage.py migrate

echo "loading data"
.\manage.py loaddata frame_consumer/categories.yaml