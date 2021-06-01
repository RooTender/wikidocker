# WikiDocker - sprawozdanie

Autorzy: Jan Kornacki, Hubert Lewandowski, Grzegorz Pozorski



## Wstęp

**Wikidocker**, czyli szybki i nie tak naiwny klasyfikator Bayesa, jakby mogło się wydawać. Program ma kwalifikuje artykuł anglojęzyczny do najbardziej prawdopodobnej kategorii z 6 głównych, dostępnych na [Simple Wikipedia](https://simple.wikipedia.org/wiki/Main_Page).

Kategoria wyjściowa byłaby rekomendacją, która mogłaby znaleźć zastosowanie w kategoryzowaniu choćby nowych artykułów. Przykładowo taki program mógłby mieć zastosowanie do automatyzacji tworzenia nawigacji na stronach internetowych z olbrzymimi bazami danych.



## Przygotowanie

### Wykorzystana technologia

W projekcie użyty został naiwny klasyfikator Bayesowski wsparty techniką *stemmingu* (usuwanie końcówki wyrazu zostawiając tylko jego temat) do kwalifikacji wiadomości.

Wzór, którego użyliśmy, wygląda następująco:
$$
P(X_i|y) = {{N_{X_i|y} + \alpha} \over {N_y + \alpha \cdot |V|}}
$$

Opis symboli:

|      Symbol       |                             Opis                             |
| :---------------: | :----------------------------------------------------------: |
|  $$ P(X_i|y) $$   | Prawdopodobieństwo warunkowe słowa $$ X_i $$ należącego do klasy $$ y $$ |
| $$ {N_{X_i|y}} $$ | Liczba wystąpień słowa $$ X_i $$ we wszystkich fragmentach należących do klasy $$ y $$ |
|     $$ N_y $$     | Liczba słów we wszystkich fragmentach należących do klasy $$ y $$ |
|     $$ |V| $$     |               Całkowita liczba słów w słowniku               |
|   $$ \alpha $$    |    Parametr służący uniknięciu prawdopodobieństw zerowych    |



#### Biblioteki

Do wyciągnięcia artykułów dla zbioru uczącego posłużyliśmy się bibliotekami:

- [requests](https://pypi.org/project/requests/) - obsługuje żądania, które były kierowane do strony Wikipedii
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - w celu wyciągnięcia konkretnych danych
- [sklearn](https://scikit-learn.org/stable/) - do wygenerowania zbioru testowego

> W celu uniknięcia każdorazowego pobierania danych i uczenia kwalifikatora użyliśmy serializacji słowników do pliku.



### Zbiór uczący

Zbiorem uczącym słowniki są **wszystkie** artykuły z 6 głównych kategorii na stronie [Simple Wikipedia](https://simple.wikipedia.org/wiki/Main_Page). 

![wiki_categories](.\wiki_categories.png)



### Zbiór testowy

Dane o poprawności niniejszego kwalifikatora opierały się na zbiorze testowym wygenerowanym ze zbioru uczącego.



## Proces obliczeniowy kwalifikatora

### Pobranie artykułów

Jest to **najdłuższy** proces ze wszystkich. W obecnej wersji ten proces może zająć nawet kilkadziesiąt minut!

Nie jest on jednak brany pod uwagę, ponieważ można go zrobić <u>tylko raz</u> (lub też w sytuacji gdy chcemy zaktualizować bazę artykułów) i bazować na zserializowanym "dumpie".

Przy pobieraniu, każdy artykuł przechodzi przez proces usuwania półsłówek (np przysłówków, przymiotników, określniki, itp), które źle wpływają na rezultaty. Dzięki temu, słowa kluczowe mają większą szansę w słownikach.

Dane o wyrazach są wyciągnięte z *wybranych* artykułów dotyczących kategorii "[Angielskie Lematy](https://en.wiktionary.org/wiki/Category:English_lemmas)".



### Generowanie zbioru uczącego i testowego

Drugi proces pod względem prędkości. Jest również pomijalny w użytku "codziennym" ponieważ po wygenerowaniu zbiorów i nauczeniu słowników, proces jest wymagany tylko przy zaktualizowanym dumpie.



### Uczenie słowników

Najszybszy proces inicjalizacji całego kwalifikatora. Mimo, że najszybszy to również pomijalny dzięki serializacji słowników do plików.



### Podsumowując

Program kolejno:

1. Generuje słowniki z plików
2. Pobiera paragrafy z artykułu podanego na wejściu
3. Przetwarza dane, w celu uzyskania formy akceptowalnej przez algorytm
4. Kwalifikuje artykuł do kategorii, dla której określono największe prawdopodobieństwo

> Mając gotowe słowniki klas proces kwalifikacji będzie bardzo szybki, co jest kluczowe dla tego projektu.



## Wyniki

### Wyniki dla zbioru testowego

Wynik poprawności nauczonego kwalifikatora odnosi się do proporcji 0.8 w generowaniu zbiorów testowych. Przy kwalifikowaniu artykułów użyta jest proporcja 0.999 tak aby zbiór treningowy był jak największy.

Poniższe dane określa najlepszą poprawność decyzji, podjętej przez kwalifikator przy proporcji zbiorów 0.8.

```python
### CORRECTNESS ###
50,373% of articles was qualified correctly.
```



### Przykłady artykułów testowych

Applied sciences: 

- [Alaska: The Final (Architectural) Frontier](https://www.dwell.com/article/alaska-the-final-architectural-frontier-78478d79)

- [Modern Architecture](https://encyclopedia2.thefreedictionary.com/modern+architecture)

    

People and social studies: 

- [Scientists Say: Placebo](https://www.sciencenewsforstudents.org/article/scientists-say-placebo)

- [Common Mental Health Problems Students May Face This Year](https://www.psyarticles.com/health/student-mental-health-problems.htm)

    

Government and law :

- [Poland’s judges forced into retirement purgatory – another blow to justice](https://theconversation.com/polands-judges-forced-into-retirement-purgatory-another-blow-to-justice-99478)

- [The Effectiveness of the International Criminal Court: Challenges and Pathways for Prosecuting Human Rights Violations](http://www.inquiriesjournal.com/articles/1806/the-effectiveness-of-the-international-criminal-court-challenges-and-pathways-for-prosecuting-human-rights-violations)

    

Natural sciences and maths: 

- [The pebbled path to planets](https://www.sciencenewsforstudents.org/article/the-pebbled-path-to-planet-formation)

- [Scientists Say: Pollen](https://www.sciencenewsforstudents.org/article/scientists-say-pollen)

    

Daily life, art and culture: 

- [Pop art](https://www.britannica.com/art/Pop-art)

- [In the Kitchen: Artist Jean Shin Shares the Korean Dumpling Recipe That Embodies the Same No-Waste Philosophy as Her Art](https://news.artnet.com/art-world/jean-shin-recipe-1974723)

    

Religions and beliefs:

- [Buddhism: Basic Beliefs](https://www.uri.org/kids/world-religions/buddhist-beliefs)

- [Islam](https://www.history.com/topics/religion/islam)



### Czy rezultat jest zadowalający?

Biorąc pod uwagę, że szansa wylosowania prawidłowej kategorii bez żadnej wiedzy, jest równa ~17%, wyniki sięgające nawet 50% (średnio 47%) są ogromną wartością dodaną, przy tak niskim czasie samej decyzji.

Wynik jest na poziomie losowego prawdopodobieństwa wybrania jednej z dwóch klas, mimo że mamy 6!
