Projekt Twitter-Kafka-Cassandra
===============================

## 1. Uruchamianie

   Aby zbudować i postawić obraz należy wykonać polecenie `docker-compose --build`. Jeżeli nie jest wymagana przebudowa kontenera (Dockerfile nie zmienił się), można używać polecenia `docker-compose up`.

   Następnie można uruchomić program main.py wykonując `docker-compose exec kafka python3 /external/main.py`. W aktualnej postaci powinno to spowodować dostarczenie wiadomości do topiku my_third_topic. Źródło main.py znajduje się w bieżącym katalogu i, podczas pracy, jest zamontowane do wewnątrz kontenera. Zmiany w pliku main.py znajdują odzwierciedlenie w pliku /external/main.py w kontenerze. 

   Aby usunąć kontenery należy wykonać `docker-compose down`.

## 2. Opis zawartości

   - docker-compose.yml

     Nasz docker-compose. Powoduje zbudowanie kontenera na podstawie instrukcji zawartych w Dockerfile, mapuje odpowiednie porty, montuje bieżący katalog do /external wewnątrz kontenera.

   - Dockerfile

     Definicja tworzonego kontenera. Podstawą jest landoop/fast-data-dev:2.6. To najnowsza wersja, która jednocześnie nie jest `latest`.

   - requirements.txt

     Tu znajdują się wszystkie zależności Pythona. Zostaną one zainstalowane w kontenerze po jego przebudowaniu `docker-compose down && docker-compose up --build`.

   - variables.env

     Plik odpowiadający za tworzenie topików w kontenerze. 