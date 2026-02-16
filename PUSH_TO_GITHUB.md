# 🚀 KI-CONCIERGE auf GitHub pushen

## Schritt 1: GitHub Repository erstellen

1. **Gehe zu:** https://github.com/new
2. **Fülle aus:**
   - Owner: `ki-strategen` (oder dein Account)
   - Repository name: `ki-concierge`
   - Description: `Micro-SaaS Chatbot for Websites - Automatic Crawling & PDF Processing`
   - Public ✅ (wichtig für GitHub Pages)
   - Initialize with README: ❌ NEIN (wir haben schon eine)
   - Add .gitignore: Python
   - License: MIT
3. **Klicke "Create repository"**

## Schritt 2: Lokalen Code pushen

**Öffne Terminal und führe diese Befehle aus:**

```bash
# 1. In das Verzeichnis wechseln
cd /Users/gb2206/.openclaw/workspace/ki-concierge

# 2. GitHub Repository als Remote hinzufügen
# ERSTELLE DAS REPOSITORY ÜBER DIE WEBSEITE, DANN:
git remote add origin https://github.com/ki-strategen/ki-concierge.git

# 3. Code pushen
git branch -M main
git push -u origin main
```

## Schritt 3: GitHub Pages aktivieren

1. **Gehe zu:** https://github.com/ki-strategen/ki-concierge/settings/pages
2. **Einstellungen:**
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
3. **Klicke "Save"**

**Warte 1-2 Minuten** bis die Seite deployed ist.

## Schritt 4: Demo URLs

**Nach erfolgreichem Deployment:**

- **Chatbot Demo:** https://ki-strategen.github.io/ki-concierge/test.html
- **ROI-Rechner:** https://ki-strategen.github.io/ki-concierge/roi-calculator.html
- **Hauptseite:** https://ki-strategen.github.io/ki-concierge/

## Schritt 5: Custom Domain (optional)

Falls du eine eigene Domain verwenden möchtest:

1. **Domain kaufen** (z.B. `kiconcierge.com` bei one.com)
2. **DNS Einstellungen:**
   ```
   CNAME demo → ki-strategen.github.io
   ```
3. **In GitHub Pages:**
   - Settings → Pages → Custom domain
   - Domain eintragen: `demo.kiconcierge.com`
   - Enforce HTTPS aktivieren

## 📁 Dateien im Repository

```
ki-concierge/
├── test.html              # Live Chatbot Demo
├── roi-calculator.html    # ROI-Rechner (Lead-Magnet)
├── frontend/widget.js     # Embeddable Chatbot Widget
├── backend/app.py         # Python Backend API
├── README.md              # Dokumentation
├── deploy.sh              # Deployment Script
└── PUSH_TO_GITHUB.md      # Diese Anleitung
```

## 🎯 Sofort nutzbar

**Nach dem Push kannst du sofort:**

1. **Demo teilen:** https://ki-strategen.github.io/ki-concierge/test.html
2. **ROI-Rechner verlinken:** https://ki-strategen.github.io/ki-concierge/roi-calculator.html
3. **In LinkedIn Posts** die Links teilen
4. **In Email-Signature** einbauen
5. **Auf ki-strategen.eu** verlinken

## 🔧 Troubleshooting

**Falls `git push` fehlschlägt:**
```bash
# Repository existiert schon? Lösche und neu erstellen
git remote remove origin
# Dann neu hinzufügen mit korrekter URL
```

**Falls GitHub Pages nicht lädt:**
- Warte 2-3 Minuten
- Prüfe ob `test.html` im root Verzeichnis ist
- Browser Cache leeren (Ctrl+F5)

## 📞 Support

Bei Problemen:
1. **GitHub Issues:** https://github.com/ki-strategen/ki-concierge/issues
2. **Email:** info@ki-strategen.eu
3. **Telegram:** @Q2206

---

**🚀 Viel Erfolg! Dein Micro-SaaS ist bereit für den Launch!**