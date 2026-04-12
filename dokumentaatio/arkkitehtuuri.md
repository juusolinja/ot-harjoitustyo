## Luokkakaavio

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