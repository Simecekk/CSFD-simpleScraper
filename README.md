# Simple ČSFD scraper app
Applikace byla vytvořena za účelem osobního vzdělání

## Použití
1) ``python manage.py get_data_from_csfd`` získá data z ČSFD (top 300 filmů + herci) a uloží do DB
2) *http://\<server-name>/* zde leží homepage, přes kterou lze nad filmy a herci vyhledávat
3) každý film a autor mají vlastní detail page na *http://\<server-name>/actor/\<int:pk>/* nebo *http://\<server-name>/movie/\<int:pk>/*