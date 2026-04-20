# Changelog

## Viikko 3

- Käyttäjä näkee tekemänsä treenit
- Lisätty WorkoutRepository-luokka, joka vastaa treenien tallennuksesta SQLite-tietokantaan
- Lisätty WorkoutService-luokka, joka vastaa sovelluslogiikan koodista
- Testattu, että WorkoutRepository-luokka palauttaa kaikki treenit oikein

## Viikko 4

- Käyttäjä voi lisätä treenin
- Käyttäjä voi muokata treenejä
- Testattu, että WorkoutRepository-luokka luo treenin oikein

## Viikko 5

- Käyttäjä voi lisätä omia lihasryhmiä ja liikkeitä
- Käyttäjä saa virheviestejä vääristä syötteistä
- Uudet luokat WorkoutRepository ja MuscleGroupRepository, jotka vastaavat liikkeiden ja lihasryhmien tietokantaoperaatioista
- Uudet luokat WorkoutService ja MuscleGroupService, jotka tarjoavat liikkeisiin ja lihasryhmiin liittyviä palveluita
- Testattu, että WorkoutService-luokka luo treenin oikein ja validoi sarjan oikein