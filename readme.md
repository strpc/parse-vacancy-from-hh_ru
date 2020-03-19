# parse-vacancy-from-hh_ru
Async parsing vacancy with hh.ru and writing result to a csv file.
![How it works](https://github.com/strpc/parse-vacancy-from-hh_ru/raw/develop/image/screen.gif)

## Discription
A async parser that collects job data from the hh.ru site into a csv file. The final table contains data with the name of the vacancy, description, salary, company name(1945 vacansy in 8.38 sec). 

## Install
```sh
git clone https://github.com/strpc/parse-vacancy-from-hh_ru.git
cd parse-vacancy-from-hh_ru
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 parse.py {name title} or python3 parse.py
```