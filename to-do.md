# Błędy

- zmiana pozycji tasków i wyjście z widoku "task" sprawia, że current_project nadpisuje się wartością, która nie istnieje

# Rzeczy do zrobienia

- nadpisywanie menu_option, selected_task i project po uruchomieniu aplikacji na 0 -> w sumie w ogóle nie potrzebuje zapisywać state żadnego z elementów "na stałe" - po otworzeniu aplikacji ma być ustawione wszystko na bazowe ustawienia
- zapobiec sytuacji, gdy pliku nie ma lub jest wypełniony innymi danymi
- operacje na state, np. increase, decrease
- może wrzucić tasks osobno i by każde zadanie miało przypisane odgórnie konkretne ID projektu 
- poprawić centrowanie tekstu z poziomu input_dialog i confirmation_dialog
- zaimplementować automatyczne wykrywanie resize dla windows i ich odświeżanie
- dodać input jako dekorator?

## Dalsze

- bardzo prosta instalacja aplikacji na komputerze, by była dostępna jako komenda
- wyjście z aplikacji, jeśli okno terminala jest za małe
- ograniczenie szerokości inputa (ilość znaków, nazwy projektu, np. 20 znaków)
- ograniczenie liczby projektów do wysokości ekranu (?)

## Inspiracje
- https://snapcraft.io/taskbook
- https://github.com/xwmx/nb
- https://github.com/gammons/ultralist
- https://github.com/NayamAmarshe/please
- https://www.calcurse.org/
- https://github.com/kraanzu/dooit
- https://github.com/NerdyPepper/dijo