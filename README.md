L'application est déployée grâce à render.com, à l'adresse https://simplove.onrender.com/accueil
Les médias et photos sont host sur Supabase storage.

Pour tester l'application en local, voici les commandes :

Installation poetry :
$ pip install poetry

Commencer par installer les dépendances.
$ poetry shell
$ poetry install

Ensuite, effectuer les migrations :
$ poetry run python manage.py makemigrations

Commit les migrations :
$ poetry run python manage.py migrate

Upload les datas des fixtures (c'est un json avec des examples bateau de profiles : charlie66 et jack 112):
$ poetry run python manage.py loaddata fixtures/data_simplove.json

Puis run le server:
$ poetry run python manage.py runserver


Possibilité de faire un Makefile directement pour ne pas taper les commandes à la main.
Voici le contenu du Makefile : 

install:
    poetry install

run:
	poetry run python manage.py runserver

migrate:*
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

seed:
	poetry run python manage.py loaddata fixtures/data_simplove.json