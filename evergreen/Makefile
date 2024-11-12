all: sorting blackening flaking type_checking

sorting: 
	poetry run isort .

blackening:
	poetry run black .

flaking: 
	poetry run flake8 

type_checking:
	poetry run mypy .