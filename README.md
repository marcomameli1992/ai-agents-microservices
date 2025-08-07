# AI Agents Microservices

Un sistema di microservizi per l'analisi intelligente dei contenuti web, composto da agenti AI specializzati e un'interfaccia frontend Flutter.

## 🏗️ Architettura del Sistema

Il progetto è strutturato come un'architettura a microservizi con i seguenti componenti:

### Servizi Backend
- **🌐 AI Web Search Agent** (porta 8001): Agente specializzato nella ricerca web
- **🔍 AI Content Analyzer Agent** (porta 8002): Agente per l'analisi e l'estrazione di contenuti
- **🚪 AI Agents Gateway** (porta 8000): Gateway principale che coordina gli agenti AI
- **💾 Data Storage Agent**: Gestione della persistenza dei dati

### Frontend
- **📱 Flutter Frontend** (porta 3000): Interfaccia utente web sviluppata in Flutter

## 📁 Struttura del Progetto

```
ai-agents-microservices/
├── docker-compose.yml                 # Configurazione Docker Compose principale
├── README.md                         # Questo file
├── config/
│   └── config.toml                   # Configurazioni globali
├── ai-agents-gateway/                # Gateway principale
│   ├── src/
│   ├── config/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── ai-web-search-agent/              # Agente di ricerca web
│   ├── src/
│   ├── config/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── ai-content-analyzer-agent/        # Agente di analisi contenuti
│   ├── src/
│   ├── config/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── data-storage-agent/               # Agente di storage dati
└── frontend/
    └── ai_agents_frontend/           # App Flutter
        ├── lib/
        ├── web/
        └── Dockerfile
```

## 🚀 Come Avviare il Sistema

### Prerequisiti
- Docker e Docker Compose installati
- Porte 3000, 8000, 8001, 8002 disponibili

### Avvio Completo
```bash
# Clona il repository
git clone <repository-url>
cd ai-agents-microservices

# Avvia tutti i servizi
docker-compose up --build
```

### Avvio Servizi Individuali
```bash
# Solo il gateway e gli agenti backend
docker-compose up --build ai-agents-gateway ai-web-search-agent ai-content-analyzer-agent

# Solo il frontend
docker-compose up --build frontend
```

## 🔧 Configurazione

### Variabili d'Ambiente
Ogni servizio ha il proprio file `.env.example`. Copia e modifica secondo le tue esigenze:

```bash
# Per ogni servizio
cp .env.example .env
# Modifica le configurazioni necessarie
```

### Configurazioni TOML
I servizi utilizzano file `config.toml` per le configurazioni specifiche. Consulta la documentazione di ogni servizio per i dettagli.

## 📚 Documentazione dei Servizi

### AI Agents Gateway
Il gateway principale che coordina tutti gli agenti AI. Per maggiori dettagli, consulta [ai-agents-gateway/README.md](ai-agents-gateway/README.md).

### AI Web Search Agent
Agente specializzato nella ricerca web intelligente. Documentazione completa in [ai-web-search-agent/README.md](ai-web-search-agent/README.md).

### AI Content Analyzer Agent
Agente per l'analisi e l'estrazione di contenuti. Vedi [ai-content-analyzer-agent/README.md](ai-content-analyzer-agent/README.md).

### Frontend Flutter
Interfaccia utente moderna sviluppata in Flutter. Guida in [frontend/ai_agents_frontend/README.md](frontend/ai_agents_frontend/README.md).

## 🔍 API Endpoints

### Gateway (porta 8000)
- `GET /health` - Controllo stato del gateway
- `POST /analyze` - Endpoint principale per l'analisi

### Agenti (porte 8001, 8002)
- `GET /health` - Controllo stato degli agenti
- Altri endpoint specifici per ogni agente

## 🧪 Testing

### Test Completi del Sistema
```bash
# Esegui tutti i test
docker-compose -f docker-compose.test.yml up --build
```

### Test per Servizio Singolo
```bash
# Esempio per il gateway
cd ai-agents-gateway
docker-compose up --build
```

## 🔧 Sviluppo

### Sviluppo Locale
1. Configura l'ambiente Python per ogni servizio backend
2. Installa Flutter per lo sviluppo frontend
3. Usa Docker per i test di integrazione

### Struttura dei Dati
Il sistema gestisce dati nel formato definito in [`analysis_results_page.dart`](frontend/ai_agents_frontend/lib/views/analysis_results_page.dart), includendo:
- Risultati di ricerca web
- Dati di analisi estratti
- Metadati dei contenuti

## 🌐 Network e Comunicazione

I servizi comunicano attraverso la rete Docker `ai-agents-network`. Il gateway orchestrated le chiamate agli agenti specializzati e restituisce i risultati aggregati al frontend.

## ⚡ Monitoraggio e Health Checks

Ogni servizio include health checks automatici:
- Intervallo: 30 secondi
- Timeout: 10 secondi  
- Retry: 3 tentativi

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT. Consulta il file [LICENSE](LICENSE) per i dettagli completi.

### Utilizzo Commerciale
La licenza MIT permette l'uso commerciale del codice. Se utilizzi questo progetto in prodotti commerciali, ti chiediamo gentilmente di:
- Mantenere l'attribuzione del copyright
- Considerare di contribuire con miglioramenti alla community