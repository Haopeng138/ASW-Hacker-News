# Instruccion para inicial Django

## Inciar el entorno virtual

source virtualenv/bin/activate

pip install --upgrade pip
## Installar todas las librererias

pip install -r requirements.txt

## Mirar las librererias

pip freeze

## Reiniciar la base de datos 

Eliminar manualmente el db.sqlite3 situado "hackersNews/db.sqlite3"
Eliminar todos los contenidos de la carpeta migrations excepto  __ ini__.py 

python manage.py makemigrations homepage 
python manage.py makemigrations accounts
python manage.py migrate 