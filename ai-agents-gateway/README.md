# ai-agents-gateway

Questo progetto è un gateway per interagire con agenti AI, specificamente progettato per utilizzare due agenti: `ai-web-search-agent` e `ai-content-analyzer-agent`. Il gateway restituisce informazioni all'utente in formato JSON.

## Struttura del Progetto

- **src/**: Contiene il codice sorgente dell'applicazione.
  - **main.py**: Punto di ingresso dell'applicazione, avvia il server e gestisce le richieste.
  - **gateway_service.py**: Logica del servizio gateway, interazione con gli agenti AI.
  - **models/**: Contiene gli schemi dei dati.
    - **schemas.py**: Definizione degli schemi dei dati.
  - **utils/**: Funzioni utili e configurazioni.
    - **logging_config.py**: Configurazione del logging.

- **config/**: Contiene i file di configurazione.
  - **config.toml**: Configurazione dell'applicazione in formato TOML.

- **tests/**: Contiene i test per l'applicazione.
  - **test_main.py**: Test per il file `main.py`.
  - **test_gateway_service.py**: Test per il file `gateway_service.py`.

- **requirements.txt**: Elenco delle dipendenze necessarie per il progetto.

- **Dockerfile**: Definizione dell'immagine Docker per l'applicazione.

- **docker-compose.yml**: Configurazione per eseguire i test del gateway.

- **.env.example**: Esempio di variabili d'ambiente necessarie per l'applicazione.

## Come Eseguire il Progetto

1. Clona il repository.
2. Naviga nella cartella del progetto.
3. Costruisci l'immagine Docker:
   ```
   docker-compose build
   ```
4. Esegui i test:
   ```
   docker-compose up
   ```

## Contribuire

Se desideri contribuire a questo progetto, sentiti libero di aprire una pull request o segnalare problemi.