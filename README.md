# Ohjelmistotekniikka harjoitustyö

Olen **tekemässä** *treeni kirjanpito-ohjelmaa*

[Linkki uusimpaan releaseen](https://github.com/juusolinja/ot-harjoitustyo/releases/tag/viikko6)

## Dokumentaatio
- [Käyttöohje](dokumentaatio/kayttoohje.md)
- [Vaatimusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Changelog](dokumentaatio/changelog.md)
- [Arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [Testausdokumentti](dokumentaatio/testaus.md)

## Sovelluksen asennus ja käynnistys

1. Asenna sovelluksen riippuvuudet komennolla:
```bash
poetry install
```

2. Suorita sovelluksen alustustoimenpiteet komennolla:
```bash
poetry run invoke build
````

3. Sovelluksen voi nyt käynnistää komennolla:
```bash
poetry run invoke start
```

## Testaus
Testit voidaan suorittaa komennolla:
```bash
poetry run invoke test
```

## Testikattavuus
Testikattavuusraportin voi generoida komennolla:
```bash
poetry run invoke coverage-report
````

Testikattavuusraportin voi myös generoida ja avata suoraan komennolla:
```bash
poetry run invoke open-coverage-report
```

## Pylint
Pylint-tarkistuksen voi suortittaa komennolla:
```bash
poetry run invoke lint
```
