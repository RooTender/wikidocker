# Sprawozdanie z projektu ze Sztucznej Inteligencji

## WSTĘP

### Temat

Wikidocker, czyli szybki i nie tak naiwny klasyfikator Bayesa, jakby mogło się wydawać.



### Cel

Wikidocker ma za zadanie kwalifikować artykuł anglojęzyczny do najbardziej prawdopodobnej kategorii z 6 głównych, dostępnych w simple wikipedia. 



### Zastosowanie

Kategoria wyjściowa byłaby rekomendacją, która mogłaby znaleźć zastosowanie w kategoryzowaniu choćby nowych artykułów.



## PRZYGOTOWANIE

### Wykorzystana technologia

W projekcie użyty został naiwny klasyfikator Bayesowski wsparty techniką *stemmingu* (usuwanie końcówki wyrazu zostawiając tylko jego temat) do kwalifikacji wiadomości. 

//////można tu dać ewentualnie wzór i opis wzoru////////////////////

Do pobrania zbioru uczącego posłużyliśmy się biblioteką Beautiful Soup.

W celu uniknięcia każdorazowego pobierania danych i uczenia kwalifikatora użyliśmy serializacji słowników do pliku.

Do wygenerowania zbioru testowego użyliśmy funkcji biblioteki sklearn.



### Zbiór uczący

Zbiorem uczącym słowniki są wszystkie artykuły z 6 głównym kategorii "simple wikipedia" (https://simple.wikipedia.org/wiki/Main_Page).



### Zbiór testowy

Dane o poprawności niniejszego kwalifikatora opierały się na zbiorze testowym wygenerowanym ze zbioru uczącego.



## PROCES OBLICZENIOWY INICJALIZACJI KWALIFIKATORA

#### Pobranie artykułów.

Jest to najdłuższy proces ze wszystkich. W obecnej wersji ten proces może zająć nawet kilkadziesiąt minut. Nie jest on jednak brany pod uwagę, ponieważ można go zrobić tylko raz (lub też w sytuacji gdy chcemy zaktualizować bazę artykułów) i bazować na zserializowanym "dumpie". 
Przy pobieraniu, każdy artykuł przechodzi przez proces usuwania półsłówek, które źle wpływają na rezultaty. Dzięki temu, słowa kluczowe mają większą szansę w słownikach.



#### Generowanie zbioru uczącego i testowego.

Drugi proces pod względem prędkości. Jest również pomijalny w użytku "codziennym" ponieważ po wygenerowaniu zbiorów i nauczeniu słowników, proces jest wymagany tylko przy zaktualizowanym dumpie.



#### Uczenie słowników.

Najszybszy proces inicjalizacji całego kwalifikatora. Mimo, że najszybszy to również pomijalny dzięki serializacji słowników do plików.



## GŁÓWNY PROCES

- Pobiera słowniki z plików.
- Pobiera artykuł z konsoli.
- Parsuje dane, aby można je było wprowadzić w algorytm.
- Kwalifikuje artykuł, wypisując kategorię o największym prawdopodobieństwie.

Mając gotowe słowniki klas, mamy pewność, że sam proces kwalifikacji będzie bardzo szybki co jest kluczowe dla tego projektu.



## WYNIKI

#### Wyniki dla zbioru testowego.

###### Wynik poprawności nauczonego kwalifikatora odnosi się do proporcji 0.8 w generowaniu zbiorów testowych. Przy kwalifikowaniu artykułów użyta jest proporcja 0.999 tak aby zbiór treningowy był jak największy.

Poniższa grafika określa najlepszą poprawność decyzji, podjętej przez kwalifikator przy proporcji zbiorów 0.8.

![correctness](.\correctness.JPG)



#### Kilka poprawnie skwalifikowanych artykułów.

###### Przy proporcji zbiorów 0.999.

Applied sciences: 

https://www.dwell.com/article/alaska-the-final-architectural-frontier-78478d79 

https://encyclopedia2.thefreedictionary.com/modern+architecture   

People and social studies: 

https://www.sciencenewsforstudents.org/article/scientists-say-placebo 

https://www.psyarticles.com/health/student-mental-health-problems.htm   

Government and law :

https://theconversation.com/polands-judges-forced-into-retirement-purgatory-another-blow-to-justice-99478 

http://www.inquiriesjournal.com/articles/1806/the-effectiveness-of-the-international-criminal-court-challenges-and-pathways-for-prosecuting-human-rights-violations   

Natural sciences and maths: 

https://www.sciencenewsforstudents.org/article/the-pebbled-path-to-planet-formation 

https://www.sciencenewsforstudents.org/article/scientists-say-pollen   

Daily life, art and culture: 

https://www.britannica.com/art/Pop-art 

https://news.artnet.com/art-world/jean-shin-recipe-1974723   

Religions and beliefs:

https://www.christianitytoday.com/news/international/ 

https://www.history.com/topics/religion/islam



## INTERPRETACJA WYNIKÓW

#### Czy rezultat jest zadowalający?

Biorąc pod uwagę, że szansa wylosowania prawidłowej kategorii bez żadnej wiedzy, jest równa ~17%, wyniki sięgające nawet 50% (średnio 47%) są ogromną wartością dodaną, przy tak niskim czasie samej decyzji. Wynik jest na poziomie losowego prawdopodobieństwa wybrania jednej z dwóch klas, mimo że mamy 6!



