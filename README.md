# Canny-Edge-Detection---Best-Hackathon
## Zadanie kwalifikacyjne na BEST career Hackathon
Narzędzie wykrywające krawędzie za pomocą własnej interpretacji algorytmu Canny

## Użyte biblioteki
- Numpy do podstawowych operacji algebraicznych oraz fast fourier transform.
- TKinter do szybkiego skonstruowania podstawowego UI 
- Pillow do obsługi wczytywania zdjęć w wielu formatach
- Numba do przyspieszenia niektórych operacji

## Środowisko/Interpreter
Do uruchomienia projektu potrzebne jest środowisko Conda

## Użycie programu
Po zainstalowaniu potrzebnych modułów(np. za pomocą pip install) i uruchomieniu
skryptu zawartego w main.py otwarte zostaje proste w obsłudze GUI składające się z 
5 głównych elementów
![przykład użycia programu]("https://i.ibb.co/fNf6TTz/edge.png")

### Load
Pozwala załadować dowolne zdjęcie

### Save
Pozwala zapisać wynik wykrywania krawędzi do pliku

### Refresh
Pozwala ponownie obliczyć krawędzie dla nowych ustawień 

### Suwak Threshold
Ustawia minimalny próg wykrywania krawędzi

### Pole wyświetlanego obrazu
Wyświetla podgląd wyniku algorytmu
	
