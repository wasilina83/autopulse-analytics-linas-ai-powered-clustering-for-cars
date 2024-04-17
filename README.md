# Anleitung für die Signlagenerator-Soft-/Hardware

1. **Prüfen der LAN-Verbindung mit dem Generator**

   Überprüfen Sie, ob eine Verbindung zum Generator über LAN besteht. Verwenden Sie die folgenden Bilder als Referenz:

   ![Bild 1](image.png)
   Abbilgung 1: Erfolgreiche LAN-Verbindung Quelle: Ausschnitt-Laptop 
   ![Bild 2](image-1.png)
   Abbilgung 2: LAN-Verbindung mit PC

2. **Browser aufrufen**

   Öffnen Sie einen Webbrowser und geben Sie die folgende Adresse ein:

   [pr-ffff40.local/scpi_manager/#](http://rp-ffff40.local/scpi_manager/#)

3. **Starten des SCPI-Servers**

   Starten Sie den SCPI-Server, indem Sie die Schaltfläche "RUN" auswählen. Notieren Sie sich die IP-Adresse des Red Pitaya-Boards (in diesem Fall 169.254.6.100) (s. Abbilgung 3).

   ![Bild 3](image-2.png)
   Abbilgung 3: Browseroberfläche SCPI
4. **Ändern der IP-Adresse des Red Pitaya-Boards im Python-Skript**


   Öffnen Sie das Skript `makeSig.py` im Terminal (Terminal öffnen über Menüefld -> Terminal) oder mit einem Editor (z. B. `nvim`) und ändern Sie die IP-Adresse entsprechend:

   ```nvim ~/repos/autopulse-analytics-linas-ai-powered-clustering-for-cars/Code/KIVYG/makeSig.py```
   Ändern Sie die IP-Adresse des Red Pitaya-Boards entsprechend.
   (Bei nvim: zur gewünsten Stelle navigiernen. i für Editieren drücken. Editieren und esc zum verlassen drücken. zum speichern und schlißen :wq eingeben und mit enter bestätigen.) 
![Bild 4](image-3.png)

## 5. Aktivieren der Python Virtual Environment

Aktivieren Sie die Python Virtual Environment mit dem folgenden Befehl:
```source ~/repos/autopulse-analytics-linas-ai-powered-clustering-for-cars/venv/bin/activate```

## 6. Wechseln zum Code-Verzeichnis

Navigieren Sie zum Verzeichnis `Code` mit dem folgenden Befehl:

```cd ~/repos/autopulse-analytics-linas-ai-powered-clustering-for-cars/Code```

## 7. Ausführen der Hauptdatei
Führen Sie die Datei `main.py` aus:
```python ~/repos/autopulse-analytics-linas-ai-powered-clustering-for-cars/KIVYG/main.py```