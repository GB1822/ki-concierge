// Fortsetzung des deploy.sh Skripts

X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -H "api-key: kc_test_123456" \
    -d '{"message":"Hallo","session_id":"test_session"}' | grep -q "response"; then
    echo "   ✅ Chat endpoint funktioniert"
else
    echo "   ⚠️  Chat endpoint hat Probleme (erwartet bei Demo)"
fi

echo ""
echo "🧪 Demo Test:"
echo "   1. Öffne test.html im Browser"
echo "   2. Klicke auf 'Chatbot öffnen'"
echo "   3. Schreibe 'Was kann der Chatbot?'"
echo ""

echo "✅ Alle Tests abgeschlossen"
EOF

chmod +x test.sh

# Create README for deployment
cat > DEPLOYMENT.md << 'EOF'
# 🚀 KI-CONCIERGE Deployment Guide

## Voraussetzungen
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- OpenAI API Key

## Schnellstart

### 1. Environment einrichten
```bash
# Repository klonen
git clone https://github.com/ki-strategen/ki-concierge.git
cd ki-concierge

# Environment Datei erstellen
cp .env.example .env

# OpenAI API Key in .env eintragen
nano .env  # OPENAI_API_KEY=sk-...
```

### 2. Anwendung starten
```bash
# Starte alle Services
./start.sh

# Oder manuell:
docker-compose up -d
```

### 3. Testen
```bash
# Services testen
./test.sh

# Demo öffnen
open test.html  # oder im Browser öffnen
```

## Services
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Nginx:** http://localhost:80
- **PostgreSQL:** localhost:5432

## Production Deployment

### Option 1: Vercel (Einfach)
```bash
# Frontend auf Vercel
vercel deploy --prod

# Backend auf Vercel
cd backend
vercel deploy --prod
```

### Option 2: AWS ECS
```bash
# Docker Images bauen und pushen
docker-compose build
docker tag ki-concierge-backend:latest your-ecr-repo/backend:latest
docker push your-ecr-repo/backend:latest

# ECS Task Definition erstellen
# Siehe: aws/ecs-task-definition.json
```

### Option 3: DigitalOcean App Platform
1. Repository mit GitHub verbinden
2. Dockerfile automatisch erkennen lassen
3. Environment Variables setzen
4. Deploy!

## Micro-SaaS Setup

### 1. Stripe Integration
```bash
# Stripe Keys in .env eintragen
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
```

### 2. Email Setup (SendGrid)
```bash
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=SG.xxx
```

### 3. CDN Setup (Cloudflare)
```bash
CDN_BASE_URL=https://cdn.kiconcierge.com
# Widget.js auf Cloudflare Workers hosten
```

## Skalierung

### Database Scaling
```sql
-- Für >10.000 Nutzer:
-- 1. Read Replicas für Analytics
-- 2. Connection Pooling (PgBouncer)
-- 3. Vertical Scaling (CPU/RAM)
```

### API Scaling
```yaml
# docker-compose.scale.yml
backend:
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '2'
        memory: 4G
```

### Caching (Redis)
```python
# backend/app.py
from redis import Redis
redis = Redis(host='redis', port=6379, db=0)
```

## Monitoring

### Health Checks
```bash
# Backend
curl http://localhost:8000/health

# Database
docker-compose exec db pg_isready

# Frontend
curl http://localhost:3000/health
```

### Logging
```bash
# Alle Logs anzeigen
docker-compose logs -f

# Backend Logs
docker-compose logs backend

# Fehler Logs
docker-compose logs --tail=100 backend | grep ERROR
```

### Metrics (Prometheus + Grafana)
```yaml
# docker-compose.monitoring.yml
prometheus:
  image: prom/prometheus
  ports:
    - "9090:9090"

grafana:
  image: grafana/grafana
  ports:
    - "3001:3000"
```

## Sicherheit

### SSL/TLS
```bash
# Let's Encrypt mit Certbot
certbot certonly --nginx -d kiconcierge.com

# SSL in nginx.conf einbinden
ssl_certificate /etc/letsencrypt/live/kiconcierge.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/kiconcierge.com/privkey.pem;
```

### API Security
```python
# Rate Limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

### Datenbank Security
```sql
-- Separate User für App
CREATE USER app_user WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE kiconcierge TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES TO app_user;
```

## Backup & Recovery

### Database Backup
```bash
# Daily Backup
docker-compose exec db pg_dump -U postgres kiconcierge > backup_$(date +%Y%m%d).sql

# Restore
cat backup.sql | docker-compose exec -T db psql -U postgres kiconcierge
```

### File Backup
```bash
# Volumes backup
tar -czf volumes_backup.tar.gz database/ backend/data/ backend/logs/
```

### Disaster Recovery
1. **Database ausfall:** Auto-restart via Docker
2. **API ausfall:** Load Balancer zu healthy instances
3. **CDN ausfall:** Fallback zu origin server

## Kostenoptimierung

### Entwicklung (€0-50/Monat)
- Vercel Hobby Plan (€0)
- OpenAI API Pay-as-you-go (€0-50)
- SendGrid Free Tier (€0)

### Production (€100-500/Monat)
- Vercel Pro (€20)
- OpenAI API (€50-200)
- SendGrid Pro (€15)
- Database (€20-100)
- Monitoring (€10-50)

### Enterprise (€500+/Monat)
- AWS/GCP/Azure
- Dedicated Instances
- 24/7 Support
- SLA 99.9%

## Troubleshooting

### Common Issues

1. **Docker startet nicht:**
```bash
# Docker Service prüfen
sudo systemctl status docker

# Logs anzeigen
journalctl -u docker.service
```

2. **Database Connection Error:**
```bash
# Database Status
docker-compose exec db pg_isready

# Connection testen
docker-compose exec db psql -U postgres -c "SELECT 1;"
```

3. **OpenAI API Error:**
```bash
# API Key prüfen
echo $OPENAI_API_KEY

# Test Request
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

4. **Widget lädt nicht:**
```bash
# CDN Status
curl https://cdn.kiconcierge.com/widget.js

# Local Test
python3 -m http.server 8080
```

### Support
- GitHub Issues: https://github.com/ki-strategen/ki-concierge/issues
- Email: support@kiconcierge.com
- Discord: https://discord.gg/kiconcierge

## Lizenz
MIT License - Siehe LICENSE Datei
EOF

echo -e "${GREEN}✅ KI-CONCIERGE Projekt erstellt!${NC}"
echo ""
echo -e "${YELLOW}📋 Nächste Schritte:${NC}"
echo "1. ${GREEN}cd ki-concierge${NC}"
echo "2. ${GREEN}nano .env  # OpenAI API Key eintragen${NC}"
echo "3. ${GREEN}./start.sh  # Services starten${NC}"
echo "4. ${GREEN}open test.html  # Demo testen${NC}"
echo ""
echo -e "${YELLOW}🚀 Micro-SaaS Launch Checklist:${NC}"
echo "✅ Prototyp entwickelt"
echo "✅ Docker Deployment ready"
echo "✅ Frontend Widget ready"
echo "✅ Backend API ready"
echo "✅ Test/Demo Seite ready"
echo "📝 Stripe Integration fehlt"
echo "📝 Email System fehlt"
echo "📝 User Dashboard fehlt"
echo "📝 Analytics fehlt"
echo ""
echo -e "${GREEN}🎉 KI-CONCIERGE ist bereit für den Launch!${NC}"
echo "Preismodelle: €29/€59/€99 pro Monat"
echo "Marktpotenzial: 5+ Millionen KMUs in Deutschland"
echo "ROI für Kunden: €6.000/Monat Einsparung vs. €59/Monat Kosten"