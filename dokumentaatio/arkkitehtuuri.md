# Arkkitehtuurikuvaus

## Rakenne
Ohjelma noudattaa kolmitasoista kerrosarkkitehtuuria. Käyttöliittymästä, sovelluslogiikasta ja tietojen pysyväistallennuksesta vastaavat koodit on eroteltu omiin pakkauksiinsa ***ui***, ***services*** ja ***repositories***. Sovelluksen käyttämät tietokohteet on myös määritelty omassa pakkauksessaan ***entities***. Liian monen turhan tietokantaoperaation välttämiseksi on myös käyttöliittymän tarvitsemat kevyemmät tietokohteet määritelty pakkauksessa ***dto***.

## Sovelluslogiikka
Sovelluksen loogisen tietomallin muodostavat luokat Workout, SetEntry, Movement ja MuscleGroup. Luokkien yhteydet voidaan havainnollistaa luokkakaaviolla:

```mermaid
classDiagram
    class Workout {
       
    }
    class SetEntry {

    }
    class Movement {
       
    }
    class MuscleGroup {
        
    }
    
    Workout "1" -- "*"  SetEntry
    SetEntry "1" -- "1" Movement
    Movement "*" -- "1" MuscleGroup
```
Sovelluksen toiminnallisuuksista vastaa ***services*** pakkauksen luokat ***MovementService***, ***WorkoutService***, ***MuscleGroupService*** ja ***AnalysisService***. Näillä luokilla on yhdet oliot, jota käyttöliittymä käyttää. Pysyvän tiedon käsiin ***services*** pakkauksen luokat pääsevät ***repositories*** pakkauksen luokkien ***WorkoutRepository***, ***MovementRepository*** ja ***MuscleGroupRepository*** kautta. ***WorkoutRepository***, ***MovementRepository*** ja ***MuscleGroupRepository*** luokkien oliot injektoidaan konstruktorin kautta ***services*** pakkauksen luokille.

## Toiminnallisuuksia

### Liikkeen luominen sekvensiikaaviona

```mermaid
sequenceDiagram
  actor User
  participant UI
  participant MovementService
  participant MovementRepository
  participant Movement
  User ->> UI: selects muscle group and enters movement name
  User ->> UI: clicks "Add" button
  UI ->> MovementService: create(name, muscle_group)
  MovementService ->> Movement: Movement(name, muscle_group)
  MovementService ->> MovementRepository: create(movement)
  MovementRepository -->> MovementService: movement
  MovementService -->> UI: movement
  UI -> UI: refresh()
  UI -> UI: _on_add_movement()
```