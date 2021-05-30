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

Poniższa grafika obrazuje objętość każdej z 6 klas w zbiorze uczącym.

![training](D:\PG\4 SEMESTR\Sztuczna Inteligencja\wikidocker\report\training.JPG)



Poniższa grafika obrazuje objętość każdej z 6 klas w zbiorze testowym.

![test](D:\PG\4 SEMESTR\Sztuczna Inteligencja\wikidocker\report\test.JPG)



Poniższa grafika określa poprawność decyzji, podejmowanych przez kwalifikator.

![correctness](D:\PG\4 SEMESTR\Sztuczna Inteligencja\wikidocker\report\correctness.JPG)



#### Kilka próbnych wyników dla różnych artykułów.

//////[link do artykułu, krótko o jego specyfice (czy jest bardzo ukierunkowany czy nie), wynik algorytmu] x **n**, gdzie **n** to liczba próbek (artykułów) które chcemy pokazać///////



## INTERPRETACJA WYNIKÓW

#### Czy rezultat jest zadowalający?

Biorąc pod uwagę, że szansa wylosowania prawidłowej kategorii bez żadnej wiedzy, jest równa ~17%, wyniki sięgające nawet 41% są ogromną wartością dodaną, przy tak niskim czasie samej decyzji. 



#### Jak poprawić wynik?

**Usunięcie "półsłówek".**

Jedną z możliwości jest usunięcie nieważnych słów takich jak "and", "or" itp. Tego typu słowa mają tendencję do występowania częściej w pewnych kategoriach, przez co zawyżają obliczenia, a nic merytorycznego nie wnoszą. Dzięki ich usunięciu, większą rolę będą grały słowa kluczowe dla danej kategorii.



