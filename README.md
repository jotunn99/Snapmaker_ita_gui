# Snapmaker U1/J1 - Italian GUI Mod 

Questa mod traduce **completamente in italiano** l'interfaccia grafica delle stampanti Snapmaker (Testata su firmware custom v1.4.0-paxx12-18 e v1.4.1-paxx12-19), mantenendo intatta la stabilità del sistema originale.

## ⚠️ Avvertenze e Disclaimer
* **Questa operazione modifica i file di sistema.** Lo script crea un backup in automatico, ma lo usi a tuo rischio e pericolo.
* L'autore della mod e Snapmaker non si assumono responsabilità per eventuali malfunzionamenti o brick della macchina.
* **NOTA BENE:** La mod sostituisce la lingua *Russa*. Dopo l'installazione, dovrai selezionare "Русский" nelle impostazioni della lingua per vedere l'Italiano.

## 🛠 Come Installare la Mod

1. Accendi la stampante e collegala al Wi-Fi.
2. Trova l'indirizzo IP della stampante (Impostazioni > Rete).
3. Apri il terminale del PC (o MobaXterm/PuTTY) e collegati via SSH:
   `ssh root@INDIRIZZO_IP_STAMPANTE`
   *(La password di default solitamente è `snapmaker`)*
4. Copia e incolla questo comando nel terminale della stampante e premi Invio:
   ```bash
   wget -qO- https://raw.githubusercontent.com/jotunn99/Snapmaker_ita_gui/refs/heads/main/install_ita.py | python3
Lo script farà tutto in automatico e riavvierà lo schermo in Italiano!

🔄 Disinstallazione / Aggiornamento
Se aggiorni il firmware ufficiale, la mod verrà cancellata. Per riaverla, lancia di nuovo il comando di installazione.
Per tornare alla lingua originale senza formattare, lancia via SSH:
cp /usr/bin/gui.bak /usr/bin/gui && killall gui
