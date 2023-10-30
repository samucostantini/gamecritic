# gamecritic

## Introduction
GameCritics is a web application designed to expand user knowledge in the field of video games and keep them updated on new releases. <br>
The project aims to create a web application to discover, browse, publicate, analyze, review... video games.

## Techonologies and Feature overview
### Programming Language: 
Python.

### Framework: 
Django.

### Front-end Technologies:
HTML. <br>
CSS. <br>
JavaScript. <br>

### Modules and Libraries:
chart.js: Used for generating analysis charts. <br>
django-countries: Employed for handling countries during registration.<br>
djsngo-forms: used to manage user registration.<br>

### Template Optimizations:
2 context_processors have been implemented for console and categories to avoid repetitive field definitions across different HTML pages.<br>
context_processor_console.<br>
context_processor_category.<br>

### Image Processing:
Images are processed using the Pillow library.<br>

### Database Engine:
SQLite has been used as the database engine for this project.<br>

## Download
clone the project on a local directory on your computer.<br>
open the terminal and go to project-directory.<br>
run this command: "pipenv shell"<br>
run "pip install -r requirements.txt" to download all the dependencies necessary to the project.<br>
move to webapp directory and check if the file manage.py is there.<br>
run : "python manage.py runserver" <br>
on the terminal there should be https:..... copy and paste on your browser.<br>
if something went wrong please verify if your pipenv is updated and verify you have installed all the requirements specified in requirements.txt<br>

