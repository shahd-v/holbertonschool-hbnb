
# HBNB Project


## About 

## Table of content 
- [About](#about)
- [Description](#description)
- [Requirements](#requirements)
- [Environment](#environment)
- [Usage](#usage)
- [Diagram Structure](#diagram-structure)
- [API](#api)
- [Authors](#authors)

## Requierment

## Environment

## Usage 

## Diagram structure

### High level Package diagram

![Package Diagram](Package%20Diagram.drawio.png)

### Class diagram

![Class Diagram](Class%20Diagram.png)

### Sequence diagram

```mermaid
sequenceDiagram
participant User
participant API
participant BusinessLogic
participant Database

User->>API: API Call (e.g., Register User)
API->>BusinessLogic: Validate and Process Request
BusinessLogic->>Database: Save Data
Database-->>BusinessLogic: Confirm Save
BusinessLogic-->>API: Return Response
API-->>User: Return Success/Failure
```

## API ( Usage & Discription )

## Authors
- Mayasem Muneer
- Abdulwahab Almatrudi
- Shahad Fahad
