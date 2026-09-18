#!/usr/bin/env python3
"""
Snapmaker U1/J1 - GUI Italian Patcher v1.1
Traduci l'interfaccia della tua stampante in Italiano in modo sicuro!
"""
import sys, os

print("==========================================")
print("  Snapmaker Italian GUI Patch - Mod v2.0  ")
print("==========================================\n")

SRC  = '/usr/bin/gui'
BAK  = '/usr/bin/gui.bak'
DST  = '/tmp/gui_patched'

# Margine di tolleranza sul numero di CARATTERI (non byte) che la stringa
# italiana può avere in più rispetto a quella russa originale, prima di
# essere scartata per rischio di sconfinamento grafico sui widget vicini.
# 1.0  = nessuna tolleranza (stesso numero di caratteri, massima sicurezza)
# 1.15 = fino al 15% di caratteri in più (buon compromesso, default)
# 1.30 = più permissivo, più rischio di overlap su testi/bottoni vicini
LUNGHEZZA_TOLLERANZA = 1.15

# IL TUO DIZIONARIO COMPLETO
TRANSLATIONS = {

    'Об устройстве': 'Informazioni',
    'О программе': 'Info',
    'О принтере': 'Info',
    'Информация': 'Info',
    'About': 'Info',

    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 1. Проверьте, не отключен ли датчик калибровки. Для получения помощи обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 1 anomalo. Controlla se è scollegato. Contatta il supporto per assistenza.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 2. Проверьте, не отключен ли датчик калибровки. Для получения помощи обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 2 anomalo. Controlla se è scollegato. Contatta il supporto per assistenza.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 3. Проверьте, не отключен ли датчик калибровки. Для получения помощи обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 3 anomalo. Controlla se è scollegato. Contatta il supporto per assistenza.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 4. Проверьте, не отключен ли датчик калибровки. Для получения помощи обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 4 anomalo. Controlla se è scollegato. Contatta il supporto per assistenza.' + ' ' * 20,

    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 1. Данные датчика вышли за допустимый диапазон. Обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 1 anomalo. Dati fuori range. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 2. Данные датчика вышли за допустимый диапазон. Обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 2 anomalo. Dati fuori range. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 3. Данные датчика вышли за допустимый диапазон. Обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 3 anomalo. Dati fuori range. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки_Аномалия датчика калибровки печатающей головки 4. Данные датчика вышли за допустимый диапазон. Обратитесь в техническую поддержку.': 'Errore calibrazione_Sensore testina 4 anomalo. Dati fuori range. Contattare il supporto tecnico.' + ' ' * 20,

    'Системная аномалия_Загрузка файла в облачное хранилище не удалась. Проверьте подключение к сети и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia sistema_Upload file cloud fallito. Verificare rete. Se persiste, contattare supporto.' + ' ' * 20,

    # --- INTERFACCIA, AVVISI E MENU ---
    'Сообщить о проблеме с ИИ-мониторингом': 'Segnala problema AI',
    'Температура в камере слишком высокая. Это может привести к засорению экструдера. Продолжить печать?': 'Temp. camera troppo alta. Rischio intasamento estrusore. Continuare?' + ' ' * 20,
    'Динамическая калибровка потока\n· При включении этой функции принтер\n  автоматически откалибрует компенсацию\n  потока перед печатью.\n· Рекомендуется после каждой замены филамента.\n': 'Calibrazione dinamica flusso\n· Se attiva, la stampante\n  calibra in automatico la\n  compensazione flusso.\n· Consigliata a ogni cambio.\n' + ' ' * 20,
    'После подключения верхнего кожуха рекомендуется повторно выполнить калибровку компенсации вибрации для обеспечения качества печати.': 'Dopo aver collegato la copertura, ricalibrare la compensazione vibrazione per garantire la qualità.' + ' ' * 20,
    'Выполнить калибровку сейчас': 'Calibra ora',
    'Снижение скорости вентилятора может повлиять на эффективность фильтрации. Продолжить?': 'Ridurre la ventola riduce il filtraggio. Continuare?' + ' ' * 20,
    'Верхний кожух отсоединен. Для обеспечения качества печати подключите его перед продолжением работы.': 'Copertura scollegata. Collegarla per continuare a stampare.' + ' ' * 20,
    'Текущий режим': 'Mod. attuale',
    'внешняя циркуляция': 'circolazione esterna',
    'внутренняя циркуляция': 'circolazione interna',
    'ожидание': 'in attesa',
    'Автоматическая загрузка\n· Вставьте филамент в подающий механизм до тех пор, пока индикаторы не подтвердят правильную установку. Система подаст филамент в заданное положение. Автоматическая загрузка завершится при запуске печати.\n\nРаспознавание филамента\n· Фирменные филаменты определяются автоматически, для сторонних филаментов требуется ручной ввод. Автоматическая загрузка фирменных филаментов — вставьте в подающий механизм до подтверждения индикаторами.\n\nСторонние филаменты\n· укажите тип и цвет вручную, затем вставьте в подающий механизм до подтверждения индикаторами.\n': 'Caricamento automatico\n· Inserisci il filamento finché i LED confermano. Il sistema lo posizionerà.\n\nRiconoscimento filamento\n· I filamenti ufficiali sono automatici, i terzi manuali. Ufficiali: inserisci fino a conferma LED.\n\nFilamenti terzi\n· Imposta tipo/colore e inserisci fino a conferma LED.\n' + ' ' * 20,
    'Если экструзия не происходит, вставьте нить обратно в печатающую головку и выберите «Повторить экструзию». Следите за появлением экструзии.': 'Se non c\'è estrusione, reinserisci il filamento e premi Riprova estrusione. Verifica l\'uscita.' + ' ' * 20,
    'Пропустить предварительную загрузку филамента >': 'Salta pre-caricamento >',
    '• Автоматическое распознавание после предварительной загрузки.': '• Riconoscimento automatico a seguito del pre-caricamento.',
    '• После предварительной загрузки требуется ручная настройка профиля.': '• Dopo il pre-carico è richiesta configurazione manuale.' + ' ' * 20,
    'Следуйте инструкциям на экране, нажмите «Далее», а затем аккуратно потяните нить, пока экструдер втягивает.': 'Segui lo schermo, premi Avanti e tira delicatamente il filo.' + ' ' * 20,
    'Экспорт на USB': 'Esporta su USB',
    'Экспорт журналов на USB-накопитель': 'Esporta log su USB',
    'Откройте Snapmaker Orca и введите этот код доступа': 'Apri Snapmaker Orca e inserisci questo codice accesso',
    'Сервер обнаружения...': 'Rilevamento server...',
    'При окончании филамента принтер может автоматически переключиться на филамент того же бренда и типа, но другого цвета, чтобы продолжить печать. Цвет изделия может измениться.': 'Se esaurito, passa a filamento di stessa marca e tipo ma colore diverso. Il colore pezzo cambierà.' + ' ' * 20,
    'Восстановление после потери шага': 'Recupero perdita passi',
    'Печать будет автоматически приостановлена, если будет обнаружена «спагетти-паутина».': 'Stampa in pausa automatica se rileva "spaghetti".' + ' ' * 20,
    'Никаких отклонений обнаружено не было;\nобнаружение ИИ было подтверждено как ложная тревога.\n': 'Nessuna anomalia;\nil rilevamento AI è un falso allarme.\n' + ' ' * 20,
    'Загрузить журналы ИИ-мониторинга и отправить отзыв\nВыберите неполадки, наблюдавшиеся во время печати. Это поможет повысить точность ИИ-распознавания.\nКонфиденциальность: загружаются только снимки с обнаруженными проблемами, пользовательские данные не собираются.\n': 'Invia log AI e feedback\nScegli i problemi visti per migliorare l\'AI.\nPrivacy: verranno inviate solo le foto dei problemi, nessun dato personale.\n' + ' ' * 20,
    'Спагетти': 'Spaghetti',
    'Посторонний предмет': 'Oggetto estraneo',
    'Загрузка выполнена': 'Carico completato',
    'Ошибка загрузки': 'Carico fallito',
    'Заменить фильтр': 'Cambiare filtro',
    'Извлеките старый фильтр и установите новый, как показано на рисунке.': 'Estrarre il vecchio filtro e installare il nuovo come in figura.',
    'Замена фильтра не завершена. Выйти все равно?': 'Sostituzione filtro incompleta. Vuoi uscire?',
    'Нажимайте кнопки ниже, чтобы отрегулировать положение механизма смены печатающих головок до тех пор, пока установочный штифт не окажется по центру гнезда печатающей головки. После выравнивания нажмите «Далее».': 'Usa i tasti per centrare il perno di allineamento nel vano testina. Poi premi Avanti.' + ' ' * 20,
    'Нажмите «Готово», чтобы сохранить новые координаты печатающей головки.': 'Premi Fatto per salvare le coordinate testina.' + ' ' * 20,
    'Определение положения пластины PEI...\nОсталось примерно 10 минут\n': 'Rilevamento lastra PEI...\nCirca 10 min rimanenti\n' + ' ' * 20,
    '«Калибровка ручного выравнивания» сейчас\nзапустится, это займет около 10 минут\n': 'La "Calibrazione Manuale" sta\nper iniziare (circa 10 min)\n' + ' ' * 20,
    'Обнаружено, что PEI-пластина не снята. Снимите PEI-пластину и нажмите «Далее», чтобы продолжить калибровку.': 'Lastra PEI rilevata. Rimuovila e premi Avanti per continuare.' + ' ' * 20,
    'PEI-пластина не обнаружена. Установите PEI-пластину на нагреваемый стол и нажмите «Далее».': 'Lastra PEI assente. Installala sul piano e premi Avanti.' + ' ' * 20,
    'PEI-пластина не обнаружена. Установите PEI-пластину и нажмите «Далее», чтобы продолжить выравнивание.': 'Lastra PEI assente. Installala e premi Avanti per livellare.' + ' ' * 20,
    'Возможно, на печатном столе обнаружен посторонний предмет_Пожалуйста, проверьте и удалите все посторонние предметы. Если посторонних предметов не обнаружено, нажмите «Продолжить», чтобы возобновить печать.': 'Possibile oggetto estraneo sul piano_Verifica e rimuovi eventuali oggetti. Se assenti, premi "Continua" per riprendere la stampa.' + ' ' * 20,
    'Обнаружен возможный дефект спагетти_Пожалуйста, осмотрите модель. Если обнаруженные дефекты допустимы или дефекты не найдены, нажмите «Продолжить» для возобновления печати.': 'Possibile difetto spaghetti_Ispeziona il modello. Se accettabile o assente, premi "Continua" per riprendere la stampa.' + ' ' * 20,
    'На печатной платформе обнаружены возможные остатки._Пожалуйста, проверьте и удалите все остатки клея. Если ничего не обнаружено, нажмите «Продолжить», чтобы возобновить печать.': 'Possibili residui sul piano._Verifica e rimuovi residui di colla. Se assenti, premi "Continua" per riprendere la stampa.' + ' ' * 20,
    
    # --- TERMINI DI SERVIZIO (TOS) ---
    '• Специальные разрешения при активации\n  • Включение этой опции предоставляет вам права на\n    изменение файлов конфигурации принтера. Мы\n    настоятельно не рекомендуем изменять эти настройки,\n    если вы полностью не понимаете функции параметров\n    конфигурации принтера. Произвольные изменения\n    могут привести к сбоям в работе функций устройства,\n    таких как защита от перегрева, калибровка XYZ,\n    выравнивание нагреваемого стола и автоматическая\n    подача филамента.\n  • Расширенный режим позволяет свободно добавлять,\n    удалять или изменять файлы конфигурации устройства,\n    что может привести к потенциальным проблемам,\n    включая, помимо прочего: дефекты заданий печати,\n    непоправимый ущерб принтеру, необратимый вред,\n    а также проблемы с безопасностью и\n    конфиденциальностью данных.\n• Влияние на права и интересы послепродажного\n    обслуживания\n  • Компания Snapmaker не имеет возможности установить\n    или проверить результаты, вытекающие из активации\n    расширенного режима. Включая этот режим, вы\n    признаете и принимаете все связанные с этим риски\n    или последствия и берете на себя полную\n    ответственность за них. В максимальной степени,\n    допустимой действующим законодательством, мы не\n    несем ответственности за любые убытки или риски,\n    возникающие в результате использования или\n    невозможности использования продукта, а также не\n    обязуемся предоставлять техническую поддержку\n    по вопросам или аномалиям, возникающим во время\n    использования продукта, включая, помимо прочего,\n    сбои в работе системы, невозможность выполнения\n    команд или потерю файлов.\n  • Включение расширенного режима может повлиять на\n    действие официальной гарантии. Пожалуйста,\n    внимательно обдумайте, стоит ли включать\n    расширенный режим.\n': '• Permessi speciali all\'attivazione\n  • Questa opzione concede i permessi per\n    modificare i file di configurazione.\n    Sconsigliamo vivamente di modificarli\n    se non si comprendono le funzioni.\n    Modifiche arbitrarie possono causare\n    malfunzionamenti a funzioni vitali come\n    protezione termica, calibrazione XYZ,\n    livellamento piano e alimentazione.\n  • La Modalità avanzata permette di\n    aggiungere, rimuovere o modificare file,\n    causando potenziali problemi tra cui:\n    difetti di stampa, danni irreversibili,\n    e problemi di sicurezza/privacy.\n• Impatto sulla garanzia\n  • Snapmaker non può verificare i risultati\n    della Modalità avanzata. Attivandola,\n    accetti tutti i rischi e le responsabilità.\n    Nella misura massima consentita dalla\n    legge, non siamo responsabili per danni\n    derivanti dall\'uso e non forniremo\n    supporto per anomalie conseguenti,\n    inclusi guasti, comandi persi o file corrotti.\n  • L\'attivazione può invalidare la garanzia.\n    Valuta attentamente se procedere.\n' + ' ' * 20,
    
    '• Предупреждение о получении root-доступа\n  • Получение root-доступа — операция с высоким\n    риском. Хотя само по себе включение root-доступа не\n    аннулирует гарантию на продукт, любой ущерб,\n    причиненный изменениями системы, требующими\n    root-доступа, может привести к аннулированию\n    гарантии. Пожалуйста, действуйте с осторожностью.\n  • После получения root-доступа пользователи получат\n    более высокие права доступа к системе, позволяющие\n    им прошивать сторонние микропрограммы, изменять\n    конфигурации системы или настраивать системные\n    ресурсы. Поскольку сторонние микропрограммы,\n    плагины или модифицированные системы не были\n    полностью проверены официальной командой, они\n    могут привести к сбоям в работе устройства,\n    функциональным отказам, повреждению системы\n    или проблемам с безопасностью. Официальная\n    команда не несет ответственности за любой ущерб,\n    сбои или опасности (включая, помимо прочего,\n    аномальный перегрев, задымление, возгорание и\n    т. д.), вызванные получением root-доступа и\n    последующими связанными с этим модификациями.\n• Риск повреждения устройства\n  • Root-доступ позволяет получать доступ к критически\n    важным системным ресурсам и изменять их, а также\n    может поставить под угрозу целостность исходной\n    системы.\n  • Если системные файлы, логика работы или критически\n    важные конфигурации изменены некорректно,\n    устройство может столкнуться с такими проблемами,\n    как невозможность загрузки, невозможность печати,\n    неисправность, потеря управления или невозможность\n    восстановления.\n• Риски безопасности\n  • Получение прав root ослабляет границы защиты\n    системы устройства, увеличивая риски безопасности.\n  • Например, при незаконном доступе к локальной сети\n    пользователя, устройство с правами root может быть\n    легче взломано, контролировано или использовано\n    злоумышленниками, что приводит к непредсказуемым\n    последствиям.\n  • Кроме того, злоумышленники могут использовать\n    скомпрометированное устройство для дальнейших атак\n    на облачные сервисы или для взлома или кражи\n    информации с устройства.\n• Риски обновления и восстановления\n  • После получения прав root устройство может быть не\n    в состоянии корректно использовать официальные\n    обновления OTA, удаленную диагностику или некоторые\n    облачные возможности, а также могут возникать сбои\n    обновления, конфликты версий и проблемы\n    совместимости.\n  • Поскольку программное обеспечение сторонних\n    производителей и связанные с ним системные\n    модификации не подлежат официальной проверке и\n    контролю, официальная команда не гарантирует,\n    что пользователи смогут успешно восстановить свою\n    систему или снова получить доступ к официальной\n    поддержке после прошивки программного обеспечения\n    сторонних производителей.\n': '• Avviso permessi di Root\n  • L\'accesso root è ad alto rischio.\n    Sebbene non invalidi direttamente la\n    garanzia, eventuali danni causati\n    da modifiche root lo faranno. Procedi\n    con estrema cautela.\n  • Il Root concede privilegi di sistema\n    elevati per flashare firmware terzi o\n    modificare risorse di sistema. Poiché\n    i firmware terzi non sono testati dal\n    team ufficiale, possono causare crash,\n    danni o rischi di sicurezza. Il team\n    ufficiale declina ogni responsabilità\n    per danni o pericoli (inclusi incendi,\n    fumo, ecc.) derivanti dal root.\n• Rischio danni al dispositivo\n  • Il Root può compromettere l\'integrità\n    del sistema originale.\n  • Modifiche errate a file critici possono\n    causare blocchi di avvio, impossibilità\n    di stampare o guasti irreparabili.\n• Rischi di sicurezza\n  • Il Root indebolisce le difese, aumentando\n    l\'esposizione agli hacker in rete locale,\n    con conseguenze imprevedibili e furto dati.\n• Rischi aggiornamenti e ripristino\n  • Con il root, il dispositivo potrebbe\n    non ricevere più aggiornamenti OTA\n    o supporto cloud, causando conflitti.\n  • Non garantiamo il ripristino o il\n    ritorno al supporto ufficiale dopo\n    aver flashato software di terze parti.\n' + ' ' * 20,

    # --- ERRORI E ANOMALIE GENERALI ---
    'Системная аномалия_См. подробности об аномалии. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Vedi dettagli anomalia. Contattare il supporto tecnico.' + ' ' * 20,
    'Системная аномалия_Обратитесь в службу технической поддержки.': 'Anomalia sistema_Contattare il supporto tecnico.' + ' ' * 20,
    'Системная аномалия_Принтер остановлен. См. подробности об ошибке. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Stampante ferma. Vedi dettagli errore e contatta il supporto tecnico.' + ' ' * 20,
    'Не удалось запустить систему_Аномалия при загрузке конфигурации. Обратитесь в службу технической поддержки или восстановите заводские настройки.': 'Errore avvio sistema_Anomalia carico configurazione. Contattare supporto o ripristinare dati di fabbrica.' + ' ' * 20,
    'Не удалось запустить систему_Аномалия загрузки протокола связи. Обратитесь в службу технической поддержки или обновите микропрограмму.': 'Errore avvio sistema_Anomalia carico protocollo. Contattare supporto o aggiornare firmware.' + ' ' * 20,
    'Не удалось запустить систему_Сбой подключения к главному микроконтроллеру. Обратитесь в техническую поддержку.': 'Errore avvio sistema_Connessione a MCU principale fallita. Contattare il supporto.' + ' ' * 20,
    'Не удалось запустить систему_Сбой подключения микроконтроллера материнской платы. Обратитесь в техническую поддержку.': 'Errore avvio sistema_Connessione a MCU scheda madre fallita. Contattare il supporto.' + ' ' * 20,
    'Не удалось запустить систему_Некорректное подключение микроконтроллера. Обратитесь в техническую поддержку.': 'Errore avvio sistema_Connessione MCU errata. Contattare il supporto tecnico.' + ' ' * 20,
    'Системная аномалия_Соединение с главным микроконтроллером прервано. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Connessione a MCU principale interrotta. Contattare il supporto.' + ' ' * 20,
    'Системная аномалия_Соединение с микроконтроллером материнской платы прервано. Обратитесь в техническую поддержку.': 'Anomalia sistema_Connessione a MCU scheda madre interrotta. Contattare il supporto.' + ' ' * 20,
    'Аномалия датчика_Аномалия в памяти акселерометра. Попробуйте выключить и снова включить устройство, чтобы возобновить работу. Если проблема повторится, обратитесь в службу технической поддержки.': 'Anomalia sensore_Anomalia memoria accelerometro. Riavviare il dispositivo. Se persiste, contattare il supporto.' + ' ' * 20,
    'Аномалия датчика_Акселерометр не смог получить действительный идентификатор устройства. Попробуйте выключить и снова включить устройство. Если проблема повторится, обратитесь в службу технической поддержки.': 'Anomalia sensore_ID accelerometro non valido. Riavviare il dispositivo. Se persiste, contattare il supporto.' + ' ' * 20,
    'Аномалия драйвера двигателя_Аномалия в драйвере двигателя. См. подробности аномалии. Обратитесь в службу технической поддержки.': 'Err. driver motore_Anomalia nel driver motore. Vedi dettagli. Contattare il supporto tecnico.' + ' ' * 20,
    'Температурная аномалия_Нагревательный модуль не смог нормально нагреться. Система отключилась в целях безопасности. Экспортируйте журналы принтера и обратитесь в службу технической поддержки.': 'Anomalia temperatura_Riscaldatore guasto. Sistema spento per sicurezza. Esporta i log e contatta il supporto.' + ' ' * 20,
    'Системная аномалия_Время ожидания ответа от главного микроконтроллера истекло. Система завершила работу в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Timeout risposta MCU principale. Sistema spento per sicurezza. Contattare il supporto.' + ' ' * 20,
    'Системная аномалия_Время ожидания ответа от микроконтроллера материнской платы истекло. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Timeout risposta MCU scheda madre. Sistema spento per sicurezza. Contattare il supporto.' + ' ' * 20,
    'Системная аномалия_Микроконтроллер материнской платы обнаружил сигнал отключения питания. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_Rilevata caduta alimentazione scheda madre. Sistema spento per sicurezza. Contattare il supporto.' + ' ' * 20,
    'Аномальная температура нагрева печатного стола_Возможна неисправность датчика температуры. Обратитесь в службу технической поддержки.': 'Anomalia temp. piano_Possibile guasto sensore temperatura. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномальная температура в печатной камере_Проверьте правильность подключения кабеля датчика температуры или обратитесь в службу технической поддержки.': 'Anomalia temp. camera_Controllare cavo sensore temperatura o contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Сначала обнулите оси X и Y, затем обнулите ось Z.': 'Errore homing_Azzerare prima X e Y, poi azzerare Z.' + ' ' * 20,
    'Аномалия движения по оси_КранДом Сначала переместите ось X.': 'Errore movim. asse_Muovere prima l\'asse X.' + ' ' * 20,
    'Аномалия движения по оси_КранДомСначала переместите ось Y.': 'Errore movim. asse_Muovere prima l\'asse Y.' + ' ' * 20,
    'Аномалия движения по оси_КранДом Сначала переместите ось Z.': 'Errore movim. asse_Muovere prima l\'asse Z.' + ' ' * 20,
    'Аномалия движения по оси_Перемещение по оси X превысило допустимый предел хода.': 'Errore movim. asse_Limite di movimento asse X superato.' + ' ' * 20,
    'Аномалия движения по оси_Перемещение по оси Y превысило допустимый предел.': 'Errore movim. asse_Limite di movimento asse Y superato.' + ' ' * 20,
    'Аномалия движения по оси_Перемещение по оси Z превысило допустимый предел хода.': 'Errore movim. asse_Limite di movimento asse Z superato.' + ' ' * 20,
    'Аномалия движения по оси_Аномалия перемещения по оси X. Повторите попытку. Если аномалия повторяется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Anomalia movimento asse X. Riprovare. Se persiste, contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия движения по оси_Аномалия перемещения по оси Y. Повторите попытку. Если аномалия повторяется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Anomalia movimento asse Y. Riprovare. Se persiste, contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия движения по оси_Аномалия перемещения по оси Z. Повторите попытку. Если аномалия повторяется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Anomalia movimento asse Z. Riprovare. Se persiste, contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия движения по оси_Проверьте, нет ли явного сопротивления при перемещении по оси X, затем повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Verificare attriti o resistenza asse X e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия движения по оси_Проверьте, нет ли явного сопротивления при перемещении по оси Y, затем повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Verificare attriti o resistenza asse Y e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия движения по оси_Проверьте, нет ли явного сопротивления при перемещении по оси Z, затем повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Verificare attriti o resistenza asse Z e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия движения по оси_Проверьте, не возникает ли явное сопротивление при перемещении осей, затем повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Verificare attriti o resistenza agli assi e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия движения по оси_Проверьте, правильно ли натянуты зубчатые ремни, плавно ли перемещаются оси X и Y и нет ли препятствий в положениях возврата в исходное положение по осям X и Y. Повторите попытку после устранения неполадок. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore movim. asse_Verificare tensione cinghie, movimento X/Y e ostacoli all\'homing. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Системная аномалия_Система находится в режиме защиты от выключения, не удается выполнить калибровку. Перезагрузите принтер и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia sistema_Sistema in protezione spegnimento, impossibile calibrare. Riavvia e riprova. Se persiste, contatta il supporto.' + ' ' * 20,
    'Системная аномалия_Система находится в режиме защиты от выключения, выравнивание невозможно. Перезагрузите принтер и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia sistema_Sistema in protezione spegnimento, impossibile livellare. Riavvia e riprova. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия датчика_Не удалось активировать. Повторите попытку. Если ошибка повторяется, обратитесь в службу технической поддержки.': 'Anomalia sensore_Attivazione fallita. Riprovare. Se persiste, contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Перед выполнением этой операции сначала установите координаты осей X и Y в исходное положение.': 'Errore homing_Azzerare prima le coordinate degli assi X e Y per continuare.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Проверьте, правильно ли натянуты зубчатые ремни, плавно ли перемещаются оси X и Y и нет ли препятствий в положениях возврата в исходное положение по осям X и Y. Повторите попытку после устранения неполадок. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore homing_Verificare tensione cinghie, movimento fluido X/Y e ostacoli all\'homing. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Повторите попытку. Если проблема не исчезнет, обратитесь в службу технической поддержки.': 'Errore homing_Riprovare. Se il problema persiste, contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки_Перед работой модуля калибровки необходимо выполнить возврат печатающей головки в исходное положение. Выполните возврат и повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Err. calibrazione_Eseguire l\'homing della testina prima di usare il modulo. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Неверные параметры калибровки. Обратитесь в службу технической поддержки.': 'Errore calibrazione_Parametri non validi. Contattare il supporto tecnico per assistenza.',
    'Аномалия калибровки_Сбой калибровки. Проверьте правильность позиционирования печатающей головки, выполните ручной возврат в исходное положение и повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Err. calibrazione_Errore. Verificare posizione testina, fare homing manuale e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Неверная команда операции. Проверьте соответствие печатающих головок номерам позиций, убедитесь в совпадении номеров и повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Err. calibrazione_Comando non valido. Verificare corrispondenza testine/posizioni e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Модель модуля калибровки текущей печатающей головки не соответствует требуемой. Обратитесь в техническую поддержку.': 'Err. calibrazione_Modello modulo calibrazione non corrispondente. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки_Аномалия команды зондирования. Используются оси, отличные от X, Y, Z. Применяйте корректные команды.': 'Err. calibrazione_Anomalia probing. In uso assi diversi da X, Y, Z. Usare comandi corretti.' + ' ' * 20,
    'Аномалия калибровки_Проверьте ось X на наличие препятствий и остатков материала в сопле печатающей головки. Очистите сопло и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Err. calibrazione_Verificare ostacoli su asse X e pulire ugello. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Проверьте ось Y на наличие препятствий и остатков материала в сопле печатающей головки. Очистите сопло и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Err. calibrazione_Verificare ostacoli su asse Y e pulire ugello. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Проверьте ось Z на наличие препятствий и убедитесь в отсутствии остатков материала в сопле печатающей головки. Очистите сопло и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Err. calibrazione_Verificare ostacoli su asse Z e pulire ugello. Riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Аномалия калибровки_Калибровка недоступна из-за системной ошибки. Обратитесь в службу технической поддержки.': 'Err. calibrazione_Calibrazione non disponibile per errore di sistema. Contattare il supporto.' + ' ' * 20,
    'Аномалия обнаружения печатного стола_Обнаружено снятие PEI-пластины. Установите PEI-пластину и повторите печать.': 'Errore ril. piano_Rilevata rimozione lastra PEI. Installare lastra PEI e ripetere la stampa.' + ' ' * 20,
    'Аномалия обнаружения печатного стола_PEI-пластина не снята. Снимите и повторите калибровку.': 'Errore ril. piano_Lastra PEI non rimossa. Rimuoverla e ripetere la calibrazione.' + ' ' * 20,
    'Системная аномалия_Не удалось получить список файлов.': 'Anomalia sistema_Impossibile ottenere lista file.',
    'Системная аномалия_Принтер печатает, но не может обрабатывать файлы нарезки. Повторите попытку, когда принтер находится в режиме ожидания.': 'Anomalia sistema_Stampante in funzione, impossibile elaborare G-code. Riprovare in standby.' + ' ' * 20,
    'Системная аномалия_Команды M28, M29, M30 не поддерживаются. Пожалуйста, удалите их.': 'Anomalia sistema_Comandi M28, M29, M30 non supportati. Rimuoverli dal file.' + ' ' * 20,
    'Системная аномалия_Анализ команд G-кода из файла нарезки. Сброс файла нарезки не допускается.': 'Anomalia sistema_Analisi G-code in corso. Annullamento non consentito.' + ' ' * 20,
    'Системная аномалия_Не удается открыть файл нарезки.': 'Anomalia sistema_Impossibile aprire file slicing.',
    'Системная аномалия_Удаление данных о выключении питания во время печати запрещено.': 'Anomalia sistema_Cancellazione dati spegnimento vietata durante la stampa.',
    'Системная аномалия_Ошибка чтения USB-флеш-накопителя. Убедитесь, что флеш-накопитель правильно подключен, и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia sistema_Errore lettura USB. Verificare connessione e riprovare. Se persiste, contatta il supporto.' + ' ' * 20,
    'Не удалось запустить систему_Не удается установить связь с модулем адаптера печатающей головки.': 'Errore avvio sistema_Impossibile comunicare con modulo adattatore testina.' + ' ' * 20,
    'Системная аномалия_Связь с модулем адаптера печатающей головки была прервана.': 'Anomalia sistema_Comunicazione modulo adattatore testina interrotta.' + ' ' * 20,

    # --- ERRORI TESTINE 1, 2, 3, 4 ---
    'Не удалось запустить систему_Сбой подключения микроконтроллера к печатающей головке 1. Выключите принтер, проверьте кабель печатающей головки, затем перезапустите принтер. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore avvio sistema_Connessione MCU testina 1 fallita. Spegni, controlla cavo e riavvia. Se persiste, contatta supporto.' + ' ' * 20,
    'Не удалось запустить систему_Сбой подключения MCU к печатающей головке 2. Выключите принтер, проверьте кабель печатающей головки, затем перезапустите принтер. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore avvio sistema_Connessione MCU testina 2 fallita. Spegni, controlla cavo e riavvia. Se persiste, contatta supporto.' + ' ' * 20,
    'Не удалось запустить систему_Сбой подключения MCU к печатающей головке 3. Выключите принтер, проверьте кабель печатающей головки, затем перезапустите принтер. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore avvio sistema_Connessione MCU testina 3 fallita. Spegni, controlla cavo e riavvia. Se persiste, contatta supporto.' + ' ' * 20,
    'Не удалось запустить систему_Сбой подключения MCU к печатающей головке 4. Выключите принтер, проверьте кабель печатающей головки, затем перезапустите принтер. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Errore avvio sistema_Connessione MCU testina 4 fallita. Spegni, controlla cavo e riavvia. Se persiste, contatta supporto.' + ' ' * 20,

    'Системная аномалия_Соединение с микроконтроллером печатающей головки 1 прервано. Выключите принтер, проверьте кабель печатающей головки 1, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Connessione MCU testina 1 interrotta. Spegni, controlla cavo testina 1 e riavvia.' + ' ' * 20,
    'Системная аномалия_Соединение с микроконтроллером Toolhead 2 прервано. Выключите принтер, проверьте кабель Toolhead 2, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Connessione MCU testina 2 interrotta. Spegni, controlla cavo testina 2 e riavvia.' + ' ' * 20,
    'Системная аномалия_Соединение с микроконтроллером Toolhead 3 прервано. Выключите принтер, проверьте кабель Toolhead 3, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Connessione MCU testina 3 interrotta. Spegni, controlla cavo testina 3 e riavvia.' + ' ' * 20,
    'Системная аномалия_Соединение с микроконтроллером головки инструмента 4 прервано. Выключите принтер, проверьте кабель головки инструмента 4, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Connessione MCU testina 4 interrotta. Spegni, controlla cavo testina 4 e riavvia.' + ' ' * 20,

    'Системная аномалия_Время ожидания управления микроконтроллером печатающей головки 1 истекло. Система отключилась в целях безопасности. Выключите принтер, проверьте кабель печатающей головки 1, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Timeout MCU testina 1. Sistema spento per sicurezza. Spegni, controlla cavo testina 1 e riavvia.' + ' ' * 20,
    'Системная аномалия_Время ожидания управления микроконтроллером Toolhead 2 истекло. Система отключилась в целях безопасности. Выключите принтер, проверьте кабель Toolhead 2, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Timeout MCU testina 2. Sistema spento per sicurezza. Spegni, controlla cavo testina 2 e riavvia.' + ' ' * 20,
    'Системная аномалия_Время ожидания управления микроконтроллером Toolhead 3 истекло. Система отключилась в целях безопасности. Выключите принтер, проверьте кабель Toolhead 3, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Timeout MCU testina 3. Sistema spento per sicurezza. Spegni, controlla cavo testina 3 e riavvia.' + ' ' * 20,
    'Системная аномалия_Время ожидания управления микроконтроллером Toolhead 4 истекло. Система отключилась в целях безопасности. Выключите принтер, проверьте кабель Toolhead 4, затем перезапустите его для возобновления работы.': 'Anomalia sistema_Timeout MCU testina 4. Sistema spento per sicurezza. Spegni, controlla cavo testina 4 e riavvia.' + ' ' * 20,

    'Системная аномалия_Микроконтроллер инструментальной головки 1 обнаружил сигнал отключения питания. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_MCU testina 1 rileva caduta di tensione. Spegnimento di sicurezza. Contattare supporto.' + ' ' * 20,
    'Системная аномалия_Микроконтроллер инструментальной головки 2 обнаружил сигнал отключения питания. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_MCU testina 2 rileva caduta di tensione. Spegnimento di sicurezza. Contattare supporto.' + ' ' * 20,
    'Системная аномалия_Микроконтроллер инструментальной головки 3 обнаружил сигнал отключения питания. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_MCU testina 3 rileva caduta di tensione. Spegnimento di sicurezza. Contattare supporto.' + ' ' * 20,
    'Системная аномалия_Микроконтроллер инструментальной головки 4 обнаружил сигнал отключения питания. Система выключилась в целях безопасности. Обратитесь в службу технической поддержки.': 'Anomalia sistema_MCU testina 4 rileva caduta di tensione. Spegnimento di sicurezza. Contattare supporto.' + ' ' * 20,

    'Аномалия филамента_Обнаружено окончание подачи филамента в печатающей головке 1. Попробуйте перезагрузить филамент, затем нажмите кнопку воспроизведения, чтобы возобновить печать.': 'Errore filamento_Esaurimento filamento in testina 1. Ricarica e premi play per riprendere stampa.' + ' ' * 20,
    'Аномалия филамента_Обнаружено окончание подачи филамента в печатающей головке 2. Попробуйте перезагрузить филамент, затем нажмите кнопку воспроизведения, чтобы возобновить печать.': 'Errore filamento_Esaurimento filamento in testina 2. Ricarica e premi play per riprendere stampa.' + ' ' * 20,
    'Аномалия филамента_В печатающей головке 3 обнаружено окончание подачи филамента. Попробуйте перезагрузить филамент, затем нажмите кнопку воспроизведения, чтобы возобновить печать.': 'Errore filamento_Esaurimento filamento in testina 3. Ricarica e premi play per riprendere stampa.' + ' ' * 20,
    'Аномалия филамента_Обнаружено окончание подачи филамента в печатающей головке 4. Попробуйте перезагрузить филамент, затем нажмите кнопку воспроизведения, чтобы возобновить печать.': 'Errore filamento_Esaurimento filamento in testina 4. Ricarica e premi play per riprendere stampa.' + ' ' * 20,

    'Аномалия температуры сопла_Температура сопла печатающей головки 1 недостаточна. Температура экструзии сопла должна быть выше 170°C.': 'Errore temp. ugello_Temp. testina 1 insufficiente. Deve superare i 170°C per l\'estrusione.' + ' ' * 20,
    'Аномалия температуры сопла_Температура сопла печатающей головки 2 недостаточна. Температура экструзии сопла должна быть выше 170°C.': 'Errore temp. ugello_Temp. testina 2 insufficiente. Deve superare i 170°C per l\'estrusione.' + ' ' * 20,
    'Аномалия температуры сопла_Температура сопла печатающей головки 3 недостаточна. Температура экструзии сопла должна быть выше 170°C.': 'Errore temp. ugello_Temp. testina 3 insufficiente. Deve superare i 170°C per l\'estrusione.' + ' ' * 20,
    'Аномалия температуры сопла_Температура сопла печатающей головки 4 недостаточна. Температура экструзии сопла должна быть выше 170°C.': 'Errore temp. ugello_Temp. testina 4 insufficiente. Deve superare i 170°C per l\'estrusione.' + ' ' * 20,

    'Аномалия температуры сопла_Выключите принтер, затем проверьте подключение терморезистора на печатающей головке 1.': 'Errore temp. ugello_Spegni la stampante e verifica connessione termistore testina 1.' + ' ' * 20,
    'Аномалия температуры сопла_Выключите принтер, затем проверьте подключение терморезистора на печатающей головке 2.': 'Errore temp. ugello_Spegni la stampante e verifica connessione termistore testina 2.' + ' ' * 20,
    'Аномалия температуры сопла_Выключите принтер, затем проверьте подключение терморезистора на печатающей головке 3.': 'Errore temp. ugello_Spegni la stampante e verifica connessione termistore testina 3.' + ' ' * 20,
    'Аномалия температуры сопла_Выключите принтер, затем проверьте подключение терморезистора на печатающей головке 4.': 'Errore temp. ugello_Spegni la stampante e verifica connessione termistore testina 4.' + ' ' * 20,

    'Длина экструзии превышена_Расстояние экструзии для печатающей головки 1 слишком велико. Возможно, в файле G-кода содержатся некорректные данные. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Estrusione eccessiva_Distanza estrusione testina 1 troppo alta. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Длина экструзии превышена_Расстояние экструзии для печатающей головки 2 слишком велико. Возможно, в файле G-кода содержатся некорректные данные. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Estrusione eccessiva_Distanza estrusione testina 2 troppo alta. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Длина экструзии превышена_Расстояние экструзии для печатающей головки 3 слишком велико. Возможно, в файле G-кода содержатся некорректные данные. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Estrusione eccessiva_Distanza estrusione testina 3 troppo alta. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Длина экструзии превышена_Расстояние экструзии для печатающей головки 4 слишком велико. Возможно, в файле G-кода содержатся некорректные данные. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Estrusione eccessiva_Distanza estrusione testina 4 troppo alta. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,

    'Поток экструзии превышен_Объем экструзии печатающей головки 1 превысил максимально допустимый. Возможно, в файле G-кода указаны некорректные параметры. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Flusso eccessivo_Volume estrusione testina 1 oltre limite. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Поток экструзии превышен_Объем экструзии печатающей головки 2 превысил максимально допустимый. Возможно, в файле G-кода указаны некорректные параметры. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Flusso eccessivo_Volume estrusione testina 2 oltre limite. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Поток экструзии превышен_Объем экструзии печатающей головки 3 превысил максимально допустимый. Возможно, в файле G-кода содержатся некорректные настройки. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Flusso eccessivo_Volume estrusione testina 3 oltre limite. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,
    'Поток экструзии превышен_Объем экструзии печатающей головки 4 превысил максимально допустимый. Возможно, в файле G-кода содержатся некорректные настройки. Для предотвращения этой проблемы рекомендуется использовать файлы G-кода, экспортированные программой Snapmaker Orca.': 'Flusso eccessivo_Volume estrusione testina 4 oltre limite. G-code errato. Usa Snapmaker Orca.' + ' ' * 20,

    'Аномалия температуры сопла_В файле G-кода может быть указана печатающая головка, не распознаваемая принтером. Для предотвращения этой проблемы рекомендуется использовать для печати файлы G-кода, экспортированные с помощью Snapmaker Orca.': 'Errore temp. ugello_Testina G-code sconosciuta al sistema. Usa sempre Snapmaker Orca per evitare errori.' + ' ' * 20,

    # --- ERRORI CAMBIO TESTINA SINGOLA E MULTIPLA ---
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 1. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 1 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 2. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 2 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 3. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 3 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка при замене печатной головки_Не удалось выполнить смену печатающей головки 4. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Cambio testina 4 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Аномалия замены печатной головки_Проверьте, правильно ли установлена текущая печатающая головка, и убедитесь, что все неактивные головки на станции надежно закреплены. Переустановите смещенные головки и нажмите, чтобы возобновить задание.': 'Errore cambio testina_Verifica che testina attuale e inattive siano installate saldamente. Reinstalla e riprendi.' + ' ' * 20,

    # --- ERRORI PARCHEGGIO E AGGANCIO ---
    'Сбой парковки печатной головки_Ошибка парковки печатающей головки 1. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore parcheggio_Parcheggio testina 1 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Сбой парковки печатной головки_Ошибка парковки печатающей головки 2. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore parcheggio_Parcheggio testina 2 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Сбой парковки печатной головки_Ошибка парковки печатающей головки 3. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore parcheggio_Parcheggio testina 3 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Сбой парковки печатной головки_Ошибка парковки печатающей головки 4. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore parcheggio_Parcheggio testina 4 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Повторите попытку. Если проблема не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Riprova. Se persiste, contatta il supporto tecnico.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 2, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1 e 2 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 3, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1, 2 e 3 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 2 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1, 2 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 1, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 1, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте, не провисли и не перекосились ли печатающие головки 2, 3 и 4, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla testine 2, 3 e 4 per disallineamenti. Regola e riprova.' + ' ' * 20,

    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 1. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 1 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 2. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 2 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 3. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 3 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,
    'Ошибка захвата печатной головки_Ошибка захвата печатающей головки 4. Проверьте поочередно все печатающие головки на предмет провисания или перекоса, отрегулируйте вручную и повторите попытку. Если аномалия не устранена, обратитесь в техническую поддержку.': 'Errore aggancio_Aggancio testina 4 fallito. Controlla TUTTE le testine per disallineamenti. Regola e riprova.' + ' ' * 20,

    # --- SENSORI E CARICAMENTO ---
    'Температура сопла выходит за пределы допустимого диапазона._Установленная температура сопла для печатающей головки 1 выходит за допустимые пределы. Сбросьте до корректных параметров.': 'Temp. ugello fuori range consentito._Temp. target per la testina 1 fuori limiti. Reimposta parametri.' + ' ' * 20,
    'Температура сопла выходит за пределы допустимого диапазона._Установленная температура сопла для печатающей головки 2 выходит за допустимые пределы. Сбросьте до корректных параметров.': 'Temp. ugello fuori range consentito._Temp. target per la testina 2 fuori limiti. Reimposta parametri.' + ' ' * 20,
    'Температура сопла выходит за пределы допустимого диапазона._Установленная температура сопла для печатающей головки 3 выходит за допустимые пределы. Сбросьте до корректных параметров.': 'Temp. ugello fuori range consentito._Temp. target per la testina 3 fuori limiti. Reimposta parametri.' + ' ' * 20,
    'Температура сопла выходит за пределы допустимого диапазона._Установленная температура сопла для печатающей головки 4 выходит за допустимые пределы. Сбросьте до корректных параметров.': 'Temp. ugello fuori range consentito._Temp. target per la testina 4 fuori limiti. Reimposta parametri.' + ' ' * 20,

    'Аномалия калибровки потока_Аномалия калибровки потока печатающей головки 1. Обратитесь в техническую поддержку.': 'Errore cal. flusso_Anomalia calibrazione flusso testina 1. Contatta il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки потока_Аномалия калибровки потока печатающей головки 2. Обратитесь в техническую поддержку.': 'Errore cal. flusso_Anomalia calibrazione flusso testina 2. Contatta il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки потока_Аномалия калибровки потока печатающей головки 3. Обратитесь в техническую поддержку.': 'Errore cal. flusso_Anomalia calibrazione flusso testina 3. Contatta il supporto tecnico.' + ' ' * 20,
    'Аномалия калибровки потока_Аномалия калибровки потока печатающей головки 4. Обратитесь в техническую поддержку.': 'Errore cal. flusso_Anomalia calibrazione flusso testina 4. Contatta il supporto tecnico.' + ' ' * 20,

    'Аномалия филамента_Аномалия подачи филамента печатающей головки 1. Обратитесь в техническую поддержку.': 'Errore filamento_Errore alimentazione testina 1. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия филамента_Аномалия подачи филамента печатающей головки 2. Обратитесь в техническую поддержку.': 'Errore filamento_Errore alimentazione testina 2. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия филамента_Аномалия подачи филамента печатающей головки 3. Обратитесь в техническую поддержку.': 'Errore filamento_Errore alimentazione testina 3. Contattare il supporto tecnico.' + ' ' * 20,
    'Аномалия филамента_Аномалия подачи филамента печатающей головки 4. Обратитесь в техническую поддержку.': 'Errore filamento_Errore alimentazione testina 4. Contattare il supporto tecnico.' + ' ' * 20,

    'Аномалия филамента_Аномалия загрузки филамента в подающй механизм 1. Проверьте наличие запутывания филамента или ослабленных соединений разъемов. Если печать уже ведется, нажмите кнопку воспроизведения, чтобы возобновить печать после устранения неполадок.': 'Errore filamento_Errore carico alimentatore 1. Controlla se aggrovigliato. Risolvi e premi per riprendere.' + ' ' * 20,
    'Аномалия филамента_Аномалия загрузки филамента в подающий механизм 2. Проверьте наличие запутывания филамента или ослабленных соединений разъемов. Если печать уже ведется, нажмите кнопку воспроизведения, чтобы возобновить печать после устранения неполадок.': 'Errore filamento_Errore carico alimentatore 2. Controlla se aggrovigliato. Risolvi e premi per riprendere.' + ' ' * 20,
    'Аномалия филамента_Аномалия загрузки филамента в устройство подачи филамента 3. Проверьте наличие запутывания филамента или ослабленных соединений разъемов. Если печать уже ведется, нажмите кнопку воспроизведения, чтобы возобновить печать после устранения неполадок.': 'Errore filamento_Errore carico alimentatore 3. Controlla se aggrovigliato. Risolvi e premi per riprendere.' + ' ' * 20,
    'Аномалия филамента_Аномалия загрузки филамента в подающий механизм 4. Проверьте наличие запутывания филамента или ослабленных соединений разъемов. Если печать уже ведется, нажмите кнопку воспроизведения, чтобы возобновить печать после устранения неполадок.': 'Errore filamento_Errore carico alimentatore 4. Controlla se aggrovigliato. Risolvi e premi per riprendere.' + ' ' * 20,

    'Филамент не загружен_Подающий механизм филамента печатающей головки 1 не обнаружил поступление нити. Вставьте филамент.': 'Filamento assente_L\'alimentatore 1 non rileva il filamento. Inserisci il filamento.' + ' ' * 20,
    'Филамент не загружен_Подающий механизм филамента печатающей головки 2 не обнаружил поступление нити. Вставьте филамент.': 'Filamento assente_L\'alimentatore 2 non rileva il filamento. Inserisci il filamento.' + ' ' * 20,
    'Филамент не загружен_Подающий механизм филамента печатающей головки 3 не обнаружил поступление нити. Вставьте филамент.': 'Filamento assente_L\'alimentatore 3 non rileva il filamento. Inserisci il filamento.' + ' ' * 20,
    'Филамент не загружен_Подающий механизм филамента печатающей головки 4 не обнаружил поступление нити. Вставьте филамент.': 'Filamento assente_L\'alimentatore 4 non rileva il filamento. Inserisci il filamento.' + ' ' * 20,

    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 1 истекло. Проверьте, не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы запустить задание печати.': 'Errore filamento_Timeout carico testina 1. Verifica che il tubo sia libero e riprova.' + ' ' * 20,
    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 2 истекло. Проверьте, не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout carico testina 2. Verifica che il tubo sia libero e riprova.' + ' ' * 20,
    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку  3 истекло. Проверьте, не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout carico testina 3. Verifica che il tubo sia libero e riprova.' + ' ' * 20,
    'Аномалия филамента_Время загрузки филамента в печатающую головку 4 истекло. Проверьте, не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout carico testina 4. Verifica che il tubo sia libero e riprova.' + ' ' * 20,

    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 1 истекло. Проверьте, не отсоединилась ли трубка с филаментом и не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout testina 1. Controlla che il tubo sia ben collegato e libero, poi riprova.' + ' ' * 20,
    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 2 истекло. Проверьте, не отсоединилась ли трубка с филаментом и не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout testina 2. Controlla che il tubo sia ben collegato e libero, poi riprova.' + ' ' * 20,
    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 3 истекло. Проверьте, не отсоединилась ли трубка с филаментом и не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout testina 3. Controlla che il tubo sia ben collegato e libero, poi riprova.' + ' ' * 20,
    'Аномалия филамента_Время ожидания загрузки филамента в печатающую головку 4 истекло. Проверьте, не отсоединилась ли трубка с филаментом и не заблокирован ли путь загрузки, убедитесь, что он свободен, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Errore filamento_Timeout testina 4. Controlla che il tubo sia ben collegato e libero, poi riprova.' + ' ' * 20,

    'Аномалия филамента_В печатающей головке 1 остались остатки филамента. Сначала извлеките филамент из головки, затем повторите попытку.': 'Errore filamento_Rimasti residui in testina 1. Estrai il filamento e riprova.' + ' ' * 20,
    'Аномалия филамента_В печатающей головке 2 остались остатки филамента. Сначала извлеките филамент из головки, затем повторите попытку.': 'Errore filamento_Rimasti residui in testina 2. Estrai il filamento e riprova.' + ' ' * 20,
    'Аномалия филамента_В печатающей головке 3 остались остатки филамента. Сначала извлеките филамент из головки, затем повторите попытку.': 'Errore filamento_Rimasti residui in testina 3. Estrai il filamento e riprova.' + ' ' * 20,
    'Аномалия филамента_В печатающей головке 4 остались остатки филамента. Сначала извлеките филамент из головки, затем повторите попытку.': 'Errore filamento_Rimasti residui in testina 4. Estrai il filamento e riprova.' + ' ' * 20,

    'Аномалия филамента_Информация о филаменте для печатающей головки 1 не задана. Перейдите на страницу с информацией о филаменте для редактирования, затем нажмите, чтобы возобновить печать.': 'Errore filamento_Info filamento 1 assenti. Modifica il profilo filamento e riprendi la stampa.' + ' ' * 20,
    'Аномалия филамента_Информация о филаменте для печатающей головки 2 не задана. Перейдите на страницу настроек филамента, чтобы отредактировать её, затем нажмите, чтобы возобновить печать.': 'Errore filamento_Info filamento 2 assenti. Modifica il profilo filamento e riprendi la stampa.' + ' ' * 20,
    'Аномалия филамента_Информация о филаменте для печатающей головки 3 не задана. Перейдите на страницу настроек филамента для редактирования, затем нажмите, чтобы возобновить печать.': 'Errore filamento_Info filamento 3 assenti. Modifica il profilo filamento e riprendi la stampa.' + ' ' * 20,
    'Аномалия филамента_Информация о филаменте для печатающей головки 4 не задана. Перейдите на страницу настроек филамента, чтобы отредактировать её, затем нажмите, чтобы возобновить печать.': 'Errore filamento_Info filamento 4 assenti. Modifica il profilo filamento e riprendi la stampa.' + ' ' * 20,

    # --- PRE-CARICO FILAMENTO ---
    'Аномалия предварительной загрузки филамента_Аномалия подающего механизма 1. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore pre-carico_Anomalia alimentatore 1. Clicca il codice per i dettagli. Contatta il supporto.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия подающего механизма 2. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore pre-carico_Anomalia alimentatore 2. Clicca il codice per i dettagli. Contatta il supporto.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия подающего механизма 3. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore pre-carico_Anomalia alimentatore 3. Clicca il codice per i dettagli. Contatta il supporto.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия подающего механизма 4. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore pre-carico_Anomalia alimentatore 4. Clicca il codice per i dettagli. Contatta il supporto.' + ' ' * 20,

    'Аномалия предварительной загрузки филамента_Аномалия скорости двигателя подающего механизма 1. Проверьте и убедитесь, что кабель подающего механизма подключен правильно. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore pre-carico_Anomalia motore alimentatore 1. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости двигателя подающего механизма 2. Проверьте и убедитесь, что кабель подающего механизма подключен правильно. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore pre-carico_Anomalia motore alimentatore 2. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости двигателя подающего механизма 3. Проверьте и убедитесь, что кабель подающего механизма подключен правильно. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore pre-carico_Anomalia motore alimentatore 3. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости двигателя подающего механизма 4. Проверьте и убедитесь, что кабель подающего механизма подключен правильно. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore pre-carico_Anomalia motore alimentatore 4. Controlla la connessione del cavo.' + ' ' * 20,

    'Аномалия предварительной загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 1. Возможно, филамент запутался или заблокирован путь подачи. Перезагрузите филамент после устранения проблемы.': 'Errore pre-carico_Anomalia encoder alimentatore 1. Filamento bloccato o aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 2. Возможно, филамент запутался или заблокирован путь подачи. Перезагрузите филамент после устранения проблемы.': 'Errore pre-carico_Anomalia encoder alimentatore 2. Filamento bloccato o aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 3. Возможно, филамент запутался или заблокирован путь подачи. Перезагрузите филамент после устранения проблемы.': 'Errore pre-carico_Anomalia encoder alimentatore 3. Filamento bloccato o aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 4. Возможно, филамент запутался или заблокирован путь подачи. Перезагрузите филамент после устранения проблемы.': 'Errore pre-carico_Anomalia encoder alimentatore 4. Filamento bloccato o aggrovigliato.' + ' ' * 20,

    'Аномалия предварительной загрузки филамента_В подающем механизме 1 нить не обнаружена. Вставьте нить.': 'Errore pre-carico_Nessun filamento nell\'alimentatore 1. Inseriscilo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_В подающем механизме 2 нить не обнаружена. Вставьте нить.': 'Errore pre-carico_Nessun filamento nell\'alimentatore 2. Inseriscilo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_В подающем механизме 3 нить не обнаружена. Вставьте нить.': 'Errore pre-carico_Nessun filamento nell\'alimentatore 3. Inseriscilo.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_В подающем механизме 4 нить не обнаружена. Вставьте нить.': 'Errore pre-carico_Nessun filamento nell\'alimentatore 4. Inseriscilo.' + ' ' * 20,

    'Аномалия предварительной загрузки филамента_Ошибка подачи филамента (таймаут подачи 1). Возможно, филамент запутался или путь подачи заблокирован. После устранения проблемы перезагрузите филамент.': 'Errore pre-carico_Timeout alimentazione 1. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Ошибка подачи филамента (таймаут подачи 2). Возможно, филамент запутался или путь подачи заблокирован. После устранения проблемы перезагрузите филамент.': 'Errore pre-carico_Timeout alimentazione 2. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Ошибка подачи филамента (таймаут подачи 3). Возможно, филамент запутался или путь подачи заблокирован. После устранения проблемы перезагрузите филамент.': 'Errore pre-carico_Timeout alimentazione 3. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Ошибка подачи филамента (таймаут подачи 4). Возможно, филамент запутался или путь подачи заблокирован. После устранения проблемы перезагрузите филамент.': 'Errore pre-carico_Timeout alimentazione 4. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,

    'Аномалия предварительной загрузки филамента_Остатки нити в печатающей головке 1. Удалите остатки нити из головки, затем загрузите ее обратно.': 'Errore pre-carico_Residui in testina 1. Rimuovili e ricarica.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Остатки нити в печатающей головке 2. Удалите остатки нити из головки, затем загрузите ее обратно.': 'Errore pre-carico_Residui in testina 2. Rimuovili e ricarica.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Остатки нити в печатающей головке 3. Удалите остатки нити из головки, затем загрузите ее обратно.': 'Errore pre-carico_Residui in testina 3. Rimuovili e ricarica.' + ' ' * 20,
    'Аномалия предварительной загрузки филамента_Остатки нити в печатающей головке 4. Удалите остатки нити из головки, затем загрузите ее обратно.': 'Errore pre-carico_Residui in testina 4. Rimuovili e ricarica.' + ' ' * 20,

    # --- ERRORI DI CARICAMENTO E SCARICAMENTO ---
    'Аномалия загрузки филамента_Аномалия в механизме подачи 1. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться в службу технической поддержки за помощью.': 'Errore carico fil._Anomalia alimentatore 1. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия в механизме подачи 2. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться в службу технической поддержки за помощью.': 'Errore carico fil._Anomalia alimentatore 2. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия в механизме подачи 3. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться в службу технической поддержки за помощью.': 'Errore carico fil._Anomalia alimentatore 3. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия в механизме подачи 4. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться в службу технической поддержки за помощью.': 'Errore carico fil._Anomalia alimentatore 4. Clicca il codice errore per i dettagli.' + ' ' * 20,

    'Аномалия загрузки филамента_Аномалия скорости двигателя механизма подачи 1. Проверьте и убедитесь в правильности подключения кабеля подающего устройства. Если ошибка сохраняется, обратитесь в службу технической поддержки.': 'Errore carico fil._Anomalia motore alimentatore 1. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости двигателя механизма подачи 2. Проверьте и убедитесь в правильности подключения кабеля подающего устройства. Если ошибка сохраняется, обратитесь в службу технической поддержки.': 'Errore carico fil._Anomalia motore alimentatore 2. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости двигателя механизма подачи 3. Проверьте и убедитесь в правильности подключения кабеля подающего устройства. Если ошибка сохраняется, обратитесь в службу технической поддержки.': 'Errore carico fil._Anomalia motore alimentatore 3. Controlla la connessione del cavo.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости двигателя механизма подачи 4. Проверьте и убедитесь в правильности подключения кабеля подающего устройства. Если ошибка сохраняется, обратитесь в службу технической поддержки.': 'Errore carico fil._Anomalia motore alimentatore 4. Controlla la connessione del cavo.' + ' ' * 20,

    'Аномалия загрузки филамента_Аномалия скорости вращения энкодерного колеса механизма подачи 1. Возможно, нить запуталась или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите нить заново после устранения проблемы.': 'Errore carico fil._Anomalia encoder alimentatore 1. Filamento bloccato. Risolvi e riprendi.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости вращения энкодерного колеса механизма подачи 2. Возможно, нить запуталась или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите нить заново после устранения проблемы.': 'Errore carico fil._Anomalia encoder alimentatore 2. Filamento bloccato. Risolvi e riprendi.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 3. Возможно, нить запуталась или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите нить заново после устранения проблемы.': 'Errore carico fil._Anomalia encoder alimentatore 3. Filamento bloccato. Risolvi e riprendi.' + ' ' * 20,
    'Аномалия загрузки филамента_Аномалия скорости вращения энкодерного колеса подающего механизма 4. Возможно, нить запуталась или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите нить заново после устранения проблемы.': 'Errore carico fil._Anomalia encoder alimentatore 4. Filamento bloccato. Risolvi e riprendi.' + ' ' * 20,

    'Аномалия загрузки филамента_В подающем механизме 1 нить не обнаружена. Вставьте нить.': 'Errore carico fil._Nessun filamento nell\'alimentatore 1. Inseriscilo.' + ' ' * 20,
    'Аномалия загрузки филамента_В подающем механизме 2 нить не обнаружена. Вставьте нить.': 'Errore carico fil._Nessun filamento nell\'alimentatore 2. Inseriscilo.' + ' ' * 20,
    'Аномалия загрузки филамента_В подающем механизме 3 нить не обнаружена. Вставьте нить.': 'Errore carico fil._Nessun filamento nell\'alimentatore 3. Inseriscilo.' + ' ' * 20,
    'Аномалия загрузки филамента_В подающем механизме 4 нить не обнаружена. Вставьте нить.': 'Errore carico fil._Nessun filamento nell\'alimentatore 4. Inseriscilo.' + ' ' * 20,

    'Аномалия загрузки филамента_Превышено время ожидания подачи филамента через подающий механизм 1. Возможно, филамент запутался или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите филамент заново после устранения проблемы.': 'Errore carico fil._Timeout alimentatore 1. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия загрузки филамента_Превышено время ожидания подачи филамента через подающий механизм 2. Возможно, филамент запутался или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите филамент заново после устранения проблемы.': 'Errore carico fil._Timeout alimentatore 2. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия загрузки филамента_Превышено время ожидания подачи филамента через подающий механизм 3. Возможно, филамент запутался или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите филамент заново после устранения проблемы.': 'Errore carico fil._Timeout alimentatore 3. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,
    'Аномалия загрузки филамента_Превышено время ожидания подачи филамента через подающий механизм 4. Возможно, филамент запутался или путь подачи заблокирован. Нажмите, чтобы возобновить подачу, или загрузите филамент заново после устранения проблемы.': 'Errore carico fil._Timeout alimentatore 4. Tubo ostruito o filamento aggrovigliato.' + ' ' * 20,

    'Аномалия загрузки филамента_Происходит переполнение подающего механизма 1. Проверьте, не отсоединилась ли трубка с нитью от этого подающего механизма. После повторного соединения постучите по трубке, чтобы возобновить подачу, или загрузите нить заново.': 'Errore carico fil._Sovraccarico alimentatore 1. Controlla il tubo e riprova.' + ' ' * 20,
    'Аномалия загрузки филамента_Происходит переполнение подающего механизма 2. Проверьте, не отсоединилась ли трубка с нитью от этого подающего механизма. После повторного соединения постучите по трубке, чтобы возобновить подачу, или загрузите нить заново.': 'Errore carico fil._Sovraccarico alimentatore 2. Controlla il tubo e riprova.' + ' ' * 20,
    'Аномалия загрузки филамента_Происходит переполнение подающего механизма 3. Проверьте, не отсоединилась ли трубка с нитью от этого подающего механизма. После повторного соединения постучите по трубке, чтобы возобновить подачу, или загрузите нить заново.': 'Errore carico fil._Sovraccarico alimentatore 3. Controlla il tubo e riprova.' + ' ' * 20,
    'Аномалия загрузки филамента_Происходит переполнение подающего механизма 4. Проверьте, не отсоединилась ли трубка с нитью от этого подающего механизма. После повторного соединения постучите по трубке, чтобы возобновить подачу, или загрузите нить заново.': 'Errore carico fil._Sovraccarico alimentatore 4. Controlla il tubo e riprova.' + ' ' * 20,

    'Аномалия экструзии_Аномалия подающего механизма 1. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore estrusione_Anomalia alimentatore 1. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия экструзии_Аномалия подающего механизма 2. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore estrusione_Anomalia alimentatore 2. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия экструзии_Аномалия подающего механизма 3. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore estrusione_Anomalia alimentatore 3. Clicca il codice errore per i dettagli.' + ' ' * 20,
    'Аномалия экструзии_Аномалия подающего механизма 4. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore estrusione_Anomalia alimentatore 4. Clicca il codice errore per i dettagli.' + ' ' * 20,

    'Аномалия экструзии_Сбой подачи в подающем механизме 2. Возможно, филамент запутался, застрял в экструзионных шестернях или засорилось сопло. Устраните проблему и повторите попытку.': 'Errore estrusione_Fallimento alimentatore 2. Filamento ostruito o aggrovigliato.' + ' ' * 20,
    'Аномалия экструзии_Сбой подачи в подающем механизме 3. Возможно, филамент запутался, застрял в экструзионных шестернях или засорилось сопло. Устраните проблему и повторите попытку.': 'Errore estrusione_Fallimento alimentatore 3. Filamento ostruito o aggrovigliato.' + ' ' * 20,
    'Аномалия экструзии_Сбой подачи в подающем механизме 4. Возможно, филамент запутался, застрял в экструзионных шестернях или засорилось сопло. Устраните проблему и повторите попытку.': 'Errore estrusione_Fallimento alimentatore 4. Filamento ostruito o aggrovigliato.' + ' ' * 20,

    'Аномалия выгрузки филамента_Аномалия выгрузки в подающем механизме 1. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore scarico_Anomalia scarico alimentatore 1. Clicca il codice errore.' + ' ' * 20,
    'Аномалия выгрузки филамента_Аномалия выгрузки в подающем механизме 2. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore scarico_Anomalia scarico alimentatore 2. Clicca il codice errore.' + ' ' * 20,
    'Аномалия выгрузки филамента_Аномалия выгрузки в подающем механизме 3. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore scarico_Anomalia scarico alimentatore 3. Clicca il codice errore.' + ' ' * 20,
    'Аномалия выгрузки филамента_Аномалия выгрузки в подающем механизме 4. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore scarico_Anomalia scarico alimentatore 4. Clicca il codice errore.' + ' ' * 20,

    'Аномалия ручной загрузки_Аномалия ручной загрузки в подающем механизме 1. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore carico manuale_Anomalia manuale alimentatore 1. Clicca il codice errore.' + ' ' * 20,
    'Аномалия ручной загрузки_Аномалия ручной загрузки в подающем механизме 2. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore carico manuale_Anomalia manuale alimentatore 2. Clicca il codice errore.' + ' ' * 20,
    'Аномалия ручной загрузки_Аномалия ручной загрузки в подающем механизме 3. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore carico manuale_Anomalia manuale alimentatore 3. Clicca il codice errore.' + ' ' * 20,
    'Аномалия ручной загрузки_Аномалия ручной загрузки в подающем механизме 4. Нажмите на код ошибки для получения подробной информации. Рекомендуется обратиться за помощью в техническую поддержку.': 'Errore carico manuale_Anomalia manuale alimentatore 4. Clicca il codice errore.' + ' ' * 20,

    # --- ERRORI TESTINE SCOLLEGATE E CONTATTI POGOPIN ---
    'Аномалия замены печатной головки_Печатающая головка 2 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Testina 2 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Печатающая головка 3 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Testina 3 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Печатающая головка 4 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Testina 4 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,

    'Аномалия замены печатной головки_Аномалия установки печатающей головки 1. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Installazione anomala testina 1. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия установки печатающей головки 2. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Installazione anomala testina 2. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия установки печатающей головки 3. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Installazione anomala testina 3. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия установки печатающей головки 4. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Installazione anomala testina 4. Reinstallala e riprendi.' + ' ' * 20,

    'Аномалия замены печатной головки_Не удалось выполнить возврат печатающей головки 1. Возможно, в зоне парковки или рабочей области находятся посторонние предметы. Удалите препятствия и нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Ritorno testina 1 fallito. Ostacoli in area di parcheggio.' + ' ' * 20,
    'Аномалия замены печатной головки_Не удалось выполнить возврат печатающей головки 2. Возможно, в зоне парковки или рабочей области находятся посторонние предметы. Удалите препятствия и нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Ritorno testina 2 fallito. Ostacoli in area di parcheggio.' + ' ' * 20,
    'Аномалия замены печатной головки_Не удалось выполнить возврат печатающей головки 3. Возможно, в зоне парковки или рабочей области находятся посторонние предметы. Удалите препятствия и нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Ritorno testina 3 fallito. Ostacoli in area di parcheggio.' + ' ' * 20,
    'Аномалия замены печатной головки_Не удалось выполнить возврат печатающей головки 4. Возможно, в зоне парковки или рабочей области находятся посторонние предметы. Удалите препятствия и нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Ritorno testina 4 fallito. Ostacoli in area di parcheggio.' + ' ' * 20,

    'Аномалия замены печатной головки_Аномалия подпружиненных контактов (Pogopin) печатающей головки 1. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Contatti pogo pin testina 1 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия подпружиненных контактов (Pogopin) печатающей головки 2. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Contatti pogo pin testina 2 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия подпружиненных контактов (Pogopin) печатающей головки 3. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Contatti pogo pin testina 3 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия замены печатной головки_Аномалия подпружиненных контактов (Pogopin) печатающей головки 4. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore cambio testina_Contatti pogo pin testina 4 sporchi. Puliscili e riprendi.' + ' ' * 20,

    'Аномалия возврата в исходное положение_Печатающая головка 1 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Testina 1 scollegata. Reinstallala manualmente e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Печатающая головка 2 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Testina 2 scollegata. Reinstallala manualmente e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Печатающая головка 3 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Testina 3 scollegata. Reinstallala manualmente e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Печатающая головка 4 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Testina 4 scollegata. Reinstallala manualmente e premi riprendi.' + ' ' * 20,

    'Аномалия возврата в исходное положение_Аномалия установки печатающей головки 1. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Installazione testina 1 anomala. Reinstallala e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Аномалия установки печатающей головки 2. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Installazione testina 2 anomala. Reinstallala e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Аномалия установки печатающей головки 3. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Installazione testina 3 anomala. Reinstallala e premi riprendi.' + ' ' * 20,
    'Аномалия возврата в исходное положение_Аномалия установки печатающей головки 4. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore homing_Installazione testina 4 anomala. Reinstallala e premi riprendi.' + ' ' * 20,

    'Аномалия обнаружения_Печатающая головка 1 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Testina 1 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Печатающая головка 2 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Testina 2 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Печатающая головка 3 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Testina 3 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Печатающая головка 4 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Testina 4 scollegata. Reinstallala manualmente e riprendi.' + ' ' * 20,

    'Аномалия обнаружения_Аномалия подпружиненных контактов (Pogopin) печатающей головки 1. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Contatti pogo pin testina 1 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия подпружиненных контактов (Pogopin) печатающей головки 2. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Contatti pogo pin testina 2 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия подпружиненных контактов (Pogopin) печатающей головки 3. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Contatti pogo pin testina 3 sporchi. Puliscili e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия подпружиненных контактов (Pogopin) печатающей головки 4. Очистите контакты как на самой головке, так и на механизме смены с помощью безворсовой салфетки. Затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Contatti pogo pin testina 4 sporchi. Puliscili e riprendi.' + ' ' * 20,

    'Аномалия обнаружения_Аномалия установки печатающей головки 1. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Installazione testina 1 anomala. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия установки печатающей головки 2. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Installazione testina 2 anomala. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия установки печатающей головки 3. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Installazione testina 3 anomala. Reinstallala e riprendi.' + ' ' * 20,
    'Аномалия обнаружения_Аномалия установки печатающей головки 4. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Errore rilevamento_Installazione testina 4 anomala. Reinstallala e riprendi.' + ' ' * 20,
    
    'Аномалия печати': 'Anomalia stampa',
    
    # Variante combinata con Titolo (Testine 1, 2, 3 e 4)
    'Аномалия печати_Проверьте, не сломан ли филамент внутри трубки для печатающей головки 1, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Anomalia di stampa_Verificare se il filamento nel tubo testina 1 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Аномалия печати_Проверьте, не сломан ли филамент внутри трубки для печатающей головки 2, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Anomalia di stampa_Verificare se il filamento nel tubo testina 2 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Аномалия печати_Проверьте, не сломан ли филамент внутри трубки для печатающей головки 3, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Anomalia di stampa_Verificare se il filamento nel tubo testina 3 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Аномалия печати_Проверьте, не сломан ли филамент внутри трубки для печатающей головки 4, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Anomalia di stampa_Verificare se il filamento nel tubo testina 4 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,

    # Variante corpo separato dal Titolo (Testine 1, 2, 3 e 4)
    'Проверьте, не сломан ли филамент внутри трубки для печатающей головки 1, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Verificare se il filamento nel tubo testina 1 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Проверьте, не сломан ли филамент внутри трубки для печатающей головки 2, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Verificare se il filamento nel tubo testina 2 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Проверьте, не сломан ли филамент внутри трубки для печатающей головки 3, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Verificare se il filamento nel tubo testina 3 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Проверьте, не сломан ли филамент внутри трубки для печатающей головки 4, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Verificare se il filamento nel tubo testina 4 è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    
    # Variante dinamica di sicurezza (se usano la variabile %d)
    'Аномалия печати_Проверьте, не сломан ли филамент внутри трубки для печатающей головки %d, не запутался ли он на катушке и не засорилась ли сама головка. После устранения неисправностей нажмите, чтобы возобновить печать. Если проблема не устранена, обратитесь в техническую поддержку.': 'Anomalia di stampa_Verificare se il filamento nel tubo testina %d è rotto, aggrovigliato o se la testina è ostruita. Risolto, premere per riprendere. Se persiste, contattare il supporto.' + ' ' * 20,
    'Автоматическая дозаправка': 'Cambio automatico filamento',
    'Разрешить автоматическое продолжение печати филаментом другого цвета.': 'Consenti stampa continua con colore diverso.',
    'При окончании филамента принтер может автоматически переключиться на филамент того же бренда и типа, но другого цвета, чтобы продолжить печать.': 'Se esaurito, passa a un filamento della stessa marca e tipo, ma di colore diverso.',
    'Автоматическое сопоставление нитей': 'Abbinamento automatico filamenti',
    'Система автоматически подбирает наиболее подходящий филамент на основе материала и цвета.': 'Il sistema seleziona il filamento più adatto per materiale e colore.',
    'Выключите светодиод после печати.': 'Spegni i LED a fine stampa.',
    'Низкий': 'Basso',
    'Середина': 'Medio',
    'Высокий': 'Alto',
    'Must home Z axis first:': "Azzerare prima l'asse Z:",
    'ru-RU': 'it-IT',
    'Русский': 'Italiano',
    'Отмена': 'Annulla',
    'Подтвердить': 'Conferma',
    'Понятно': 'Capito',
    'Завершено': 'Completato',
    'Успешно': 'Successo',
    'Неудачно': 'Fallito',
    'Готово': 'Fatto',
    'Позже': 'Dopo',
    'Открыть': 'Apri',
    'Закрыть': 'Chiudi',
    'Продолжить': 'Continua',
    'Исправить сейчас': 'Correggi ora',
    'Отправить': 'Invia',
    'Осталось': 'Rimanente',
    'Общий': 'Totale',
    'Начать': 'Inizia',
    'Далее': 'Avanti',
    'Удалить': 'Elimina',
    'Домой': 'Home',
    'Домой...': 'Home...',
    'Пропустить': 'Salta',
    'Локально': 'Locale',
    'Экспорт': 'Esporta',
    'Взять': 'Prendi',
    'Сохранить': 'Salva',
    'Сохранено': 'Salvato',
    'Возобновить': 'Riprendi',
    'Повторить попытку': 'Riprova',
    'Согласиться': 'Accetto',
    'Выйти': 'Esci',
    'Обнаружить': 'Rileva',
    'Сканировать': 'Scansiona',
    'Очистить': 'Pulisci',
    'Редактировать сейчас': 'Modifica ora',
    'Настройте позже': 'Configura dopo',
    'Подключить сеть': 'Connetti rete',
    'Подключиться сейчас': 'Connetti ora',
    'Давайте создадим что-нибудь чудесное.': 'Creiamo qualcosa di meraviglioso.',
    'Вы уверены, что хотите остановить печать?': 'Vuoi davvero fermare la stampa?',
    'Восстановление печати, Питание принтера было отключено во время печати. Хотите возобновить печать?': 'Mancanza di corrente rilevata durante la stampa. Riprendere?',
    'Печать': 'Stampa',
    'Печать модели': 'Stampa modello',
    'Выбор файла': 'Scegli file',
    'Настройка цветов': 'Imposta colori',
    'Начало печати': 'Inizio stampa',
    'Перепечатка': 'Ristampa',
    'Печать отменена': 'Stampa annullata',
    'Запрещено во время печати': 'Vietato durante la stampa',
    'Загрузка файла для печати...': 'Caricamento file di stampa...',
    'Распаковка файлов...': 'Estrazione file...',
    'Настройки печати': 'Impostaz. stampa',
    'Возобновление печати...': 'Ripresa stampa...',
    'Расширенные параметры': 'Parametri avanzati',
    'Скорость печати': 'Velocità stampa',
    'Пропуск деталей': 'Salta oggetti',
    'Удалить выбранные файлы?': 'Eliminare i file scelti?',
    'Экспортировать выбранные файлы?': 'Esportare i file selezionati?',
    'Пожалуйста, выберите файл для удаления.': 'Seleziona un file da eliminare.',
    'Местный экспорт': 'Esporta locale',
    'Локальное удаление': 'Elimina locale',
    'Ваш принтер готов. Давайте распечатаем вашу первую модель!': 'Stampante pronta. Stampiamo il primo modello!',
    'Для повторной печати будут использоваться та же самая печатающая головка и тот же филамент.': 'Verranno usate la stessa testina e lo stesso filamento.',
    'Вы уверены, что хотите пропустить этот объект?': 'Vuoi davvero saltare questo oggetto?',
    'Съемка таймлапс': 'Timelapse',
    'Недостаточно места для запуска съемки таймлапс. Пожалуйста, освободите место и попробуйте снова.': 'Spazio esaurito per timelapse. Libera spazio e riprova.',
    'Видеоролики с тайм-лапс отсутствуют.': 'Nessun video time-lapse.',
    'Экспорт тайм-лапс съемки': 'Esporta time-lapse',
    'Удалить тайм-лапс съемку': 'Elimina time-lapse',
    'Динамическая калибровка потока': 'Calibrazione dinamica flusso',
    'Калибровка экструзионного потока': 'Calibrazione flusso estrusione',
    'Выберите печатную головку': 'Seleziona testina',
    'Скорость вентилятора': "Velocità ventola",
    'Ошибка запуска Klipper': 'Errore avvio Klipper',
    'Обнаружение стола\u2026': 'Rilevamento piano...',
    'Файлы Gcode отсутствуют': 'Nessun file Gcode trovato',
    'Нераспознанный тип G-кода': 'Tipo G-code non riconosciuto',
    'Нераспознанный тип G-кода. Продолжение печати может привести к сбою или повреждению принтера. Вы хотите продолжить?': 'G-code non riconosciuto. Continuare potrebbe causare errori o danni. Continuare?',
    'Сканирование файла Gcode...': 'Scansione file Gcode...',
    'Текущая температура печатающей головки установлена \u200b\u200bна 0 градусов Цельсия. Продолжение печати может привести к сбою. Продолжить?': 'Temp. testina a 0 gradi C. Continuare potrebbe causare errori. Continuare?',
    'Возврат по осям X и Y в исходное положение\u2026': 'Homing assi X e Y...',
    'Хотите удалить все файлы Gcode и файлы таймлапса?': 'Eliminare tutti i file Gcode e timelapse?',
    'Сначала вставьте USB-флешку.': 'Inserire prima la chiavetta USB.',
    'Печатающие головки': 'Testine di stampa',
    'Печатающая головка': 'Testina di stampa',
    'Печатающая головка 1': 'Testina 1',
    'Печатающая головка 2': 'Testina 2',
    'Печатающая головка 3': 'Testina 3',
    'Печатающая головка 4': 'Testina 4',
    'Сопло': 'Ugello',
    'сопло': 'ugello',
    'Экструдер': 'Estrusore',
    'РЕТРАКТ': 'RITRAI',
    'ЭКСТРУЗИЯ': 'ESTRUDI',
    'Загрузка...': 'Caricamento…',
    'Прикрепить печатающую головку': 'Aggancia testina',
    'Отсоедините печатающую головку': 'Sgancia testina',
    'Информация о печатающей головке': 'Info testina',
    'Диаметр сопла': 'Diam. ugello',
    'Диаметр сопла: Печатающая головка 1': 'Diametro ugello: Testina 1',
    'Диаметр сопла: Печатающая головка 2': 'Diametro ugello: Testina 2',
    'Диаметр сопла: Печатающая головка 3': 'Diametro ugello: Testina 3',
    'Диаметр сопла: Печатающая головка 4': 'Diametro ugello: Testina 4',
    'Примерное оставшееся время': 'Tempo rimanente stimato',
    'Температура сопла': 'Temperatura ugello',
    'Выберите печатающую головку(и) для калибровки.': 'Seleziona testina/e per la calibrazione.',
    'Выберите как минимум одну печатающую головку для калибровки.': 'Seleziona almeno una testina per la calibrazione.',
    'Пожалуйста, выберите печатающую головку, из которой вы хотите удалить материал после печати.': 'Seleziona la testina da cui rimuovere il materiale a fine stampa.',
    'Пожалуйста, выберите хотя бы одну печатающую головку для возврата материала.': 'Seleziona almeno una testina per la retrazione.',
    'Установка печатающей головки': 'Installazione testina',
    'Отсоединение печатающей головки': 'Smontaggio testina',
    'Калибровка печатающей головки': 'Calibrazione testina',
    'Ошибка установки и возврата печатающей головки': 'Errore installazione e ritorno testina',
    'Исключение при возврате в исходное положение': 'Eccezione ritorno posizione',
    'Проверка крепления и отсоединения печатающей головки...': 'Verifica montaggio e smontaggio testina...',
    'Контроль': 'Controllo',
    'Движение': 'Movimento',
    'Температура': 'Temperatura',
    'Температура нагреваемой платформы': 'Temperatura piano riscaldato',
    'Светодиодная лента': 'Striscia LED',
    'Очиститель': 'Pulitore',
    'Скорость вращения основного вентилятора охлаждения': 'Velocità ventola di raffreddamento principale',
    'Скорость вращения вентилятора системы охлаждения': 'Velocità ventola di raffreddamento ausiliaria',
    'Скорость вентилятора очистителя': "Velocità ventola purificatore",
    'Скорость внешнего вентилятора': "Velocità ventola esterna",
    'Скорость внутреннего вентилятора': "Velocità ventola interna",
    'Верхняя крышка': 'Coperchio sup.',
    'Обнаружена новая верхняя крышка': 'Nuovo coperchio superiore rilevato',
    'Страница управления верхней крышкой доступна на панели управления': 'Pagina controllo coperchio disponibile nel pannello',
    'Нажмите чтобы перейти на страницу управления верхней крышкой': 'Tocca per aprire il controllo coperchio',
    'Нагрев сопла': 'Risc. ugello',
    'нагрев': 'riscald.',
    'Нагрев': 'Riscald.',
    'Макс. температура платформы': 'Temp. max piano',
    'Макс. температура сопла': 'Temp. max ugello',
    'Мин. температура сопла': 'Temp. min ugello',
    'Аномалия движения по оси': 'Anomalia movimento asse',
    'КранДом Сначала переместите ось Z.': "Tocca prima Home, poi muovi l'asse Z.",
    'Нажмите на пустое поле, чтобы закрыть.': 'Tocca area vuota per chiudere.',
    'Снижение скорости вентилятора может повлиять на качество печати, продолжить?': "Ridurre velocità ventola può influire sulla qualità. Continuare?",
    'В данный момент включен режим внутренней циркуляции, внешний вентилятор не может быть включен': 'Circolazione interna attiva, ventola esterna non disponibile',
    'В данный момент включен режим внешней циркуляции, внутренний вентилятор не может быть включен': 'Circolazione esterna attiva, ventola interna non disponibile',
    'Настройка филамента': 'Config. filamento',
    'Автоматическая перезагрузка филамента...': 'Ricarica automatica filamento...',
    'Проверка печатных головок...': 'Controllo testine...',
    'Автоматическая загрузка филамента...': 'Caricamento automatico filamento...',
    'Предварительная экструзия...': 'Pre-estrusione...',
    'Автоматическая выгрузка филамента...': 'Scaricamento automatico filamento...',
    'Автоматический выход филамента': 'Espulsione automatica filamento',
    'Регулировка температуры камеры...': 'Regolazione temperatura camera...',
    'Филамент не распознан. Измените настройки, чтобы продолжить печать.': 'Filamento non riconosciuto. Modifica impostazioni per continuare.',
    'Здесь отображается предустановленный тип филамента для данной модели.': 'Tipo filamento preimpostato per questo modello.',
    'Здесь отображается фактически загруженная в соответствующую печатающую головку нить.': 'Filamento attualmente caricato nella testina.',
    'Принтер автоматически сопоставит предустановленный филамент с загруженным филаментом того же типа и наиболее   близкого цвета. Вы также можете настроить соответствие цветов вручную.': 'Abbinamento automatico per tipo e colore. La configurazione manuale è disponibile.',
    'Выберите филамент того же типа, что и предустановленный, для сопоставления.': 'Scegli filamento dello stesso tipo per abbinamento.',
    'Диаметр сопла не соответствует настройкам файла слайсера. Пожалуйста, убедитесь, что установленный диаметр сопла соответствует параметрам слайсера и проверьте, не изменялась ли информация о сопле.': 'Diametro ugello non corrisponde allo slicer. Verificare le impostazioni ugello.',
    'Производитель': 'Produttore',
    'Филамент': 'Filamento',
    'Тип': 'Tipo',
    'Цвет': 'Colore',
    'Руководство по загрузке филамента': 'Guida caricamento filamento',
    'Просмотреть руководство по загрузке филамента >': 'Guida caricamento filamento >',
    'Переключиться на ручную загрузку >': 'Passa a caricamento manuale >',
    'Выгрузка': 'Scarico',
    'Загрузка': 'Carico',
    'Официальные филаменты': 'Filamenti ufficiali',
    'Филаменты сторонних производителей': 'Filamenti di terze parti',
    'Особенный': 'Speciale',
    'Ручная загрузка': 'Carico manuale',
    'Автоматическая загрузка не удалась?': 'Caricamento automatico fallito?',
    'Ручная подача 1. Нажмите кнопку бокового подающего механизма, чтобы вручную подать нить в подающее отверстие   печатающей головки. 2. Вытяните направляющую трубку материала над печатающей головкой и вручную вставьте нить в головку.': 'Carico manuale: 1. Premi il pulsante laterale per inserire il filamento. 2. Estrai il tubo guida e inserisci manualmente.',
    'Нить загружена, но тип не распознан. Устраните проблему сейчас, чтобы обеспечить правильную печать.': 'Filamento caricato ma tipo sconosciuto. Risolvi per garantire stampa corretta.',
    'Пожалуйста, выберите печатающую головку для выгрузки': 'Seleziona testina per scaricamento',
    'Пожалуйста, выберите печатающую головку для ручной загрузки': 'Seleziona testina per caricamento manuale',
    'Пожалуйста, выберите печатающую головку для автоматической загрузки.': 'Seleziona testina per carico automatico.',
    'выгрузка филамента...': 'scarico filamento...',
    'Все печатающие головки разгружены. Извлеките филамент вручную.': 'Tutte le testine scaricate. Rimuovere filamento manualmente.',
    'Вы уверены, что хотите выйти из режима выгрузки филамента?': "Uscire dalla modalità di scaricamento filamento?",
    'Хотите выйти из процесса ручной загрузки?': 'Uscire dal caricamento manuale?',
    'Вручную подавайте нить через подающее устройство до тех пор, пока она полностью не войдет в зацепление с приводными шестернями в печатающей головке.': "Inserire manualmente il filamento nell'alimentatore finché si innesta negli ingranaggi.",
    'Убедитесь что нить правильно зафиксирована в приводных шестернях инструментальной головки': 'Verificare che il filamento sia bloccato negli ingranaggi.',
    'Проверьте успешность экструзии из печатающей головки': "Verificare l'estrusione dalla testina",
    'экструзия': 'estrusione',
    'Экструзия из': 'Estrusione da',
    'Экструдированный': 'Estruso',
    'Повторить экструзию': 'Ripeti estrusione',
    'загрузка филамента...': 'caricamento filamento...',
    'Ручная загрузка выполнена успешно': 'Caricamento manuale completato',
    'Ручная загрузка не удалась': 'Caricamento manuale fallito',
    'Автоматическая загрузка прошла успешно': 'Caricamento automatico riuscito',
    'Автоматическая загрузка не удалась': 'Caricamento automatico fallito',
    'Уборка': 'Pulizia',
    'Очистка от старого филамента': 'Pulizia vecchio filamento',
    'Выгрузка прервана...': 'Scarico interrotto...',
    'Прерывание ручной загрузки...': 'Interruzione carico manuale...',
    'Ошибка при выгрузке филамента!': 'Errore scaricamento filamento!',
    'Предварительная загрузка филамента': 'Pre-caricamento filamento',
    'Установите катушку, как показано, и попробуйте выполнить подачу. Вставьте филамент в подающий механизм до тех пор, пока индикаторы не подтвердят правильную установку. Система подаст филамент в заданное положение. Автоматическая загрузка завершится при запуске печати.': "Installare la bobina come mostrato. Inserire filamento finché gli indicatori confermano. Il sistema porterà in posizione. Il carico termina all'avvio stampa.",
    'Вставьте филамент в соответствующее подающее отверстие, чтобы завершить процедуру предварительной загрузки.': 'Inserire il filamento nel foro di alimentazione per completare il pre-caricamento.',
    'Режим загрузки': 'Modalità carico',
    'Режим выгрузки': 'Modalità scarico',
    'Нет филамента': 'Manca filamento',
    'Загружено': 'Caricato',
    'Требуется ручное вмешательство': 'Intervento manuale richiesto',
    'Во время процесса выгрузки вытяните нить наружу.': 'Durante lo scarico, estrarre il filamento.',
    'Для выгрузки гибких филаментов требуется ручное вмешательство.': 'I materiali flessibili richiedono scaricamento manuale.',
    'Выберите печатающую головку требующую ручной загрузки': 'Seleziona la testina che richiede caricamento manuale',
    'Подача филамента': 'Alimenta filamento',
    'Прерывание автоматической загрузки...': 'Interruzione caricamento automatico...',
    'Хотите выйти из режима автоматической загрузки филамента?': 'Uscire dalla modalità di caricamento automatico?',
    'Подробная информация о филаменте': 'Dettagli filamento',
    'Устройство подачи филамента не работает.': 'Alimentatore filamento non funziona.',
    'Обнаружен неизвестный филамент. Перед загрузкой отредактируйте профиль материала.': 'Filamento sconosciuto. Modifica profilo materiale prima del carico.',
    'Пожалуйста, выберите тип филамента': 'Seleziona tipo filamento',
    'Гибкие расходные материалы не поддерживают автоматическое втягивание.': 'I materiali flessibili non supportano retrazione automatica.',
    'Автоматическая загрузка': 'Caricamento automatico',
    'Если эта функция отключена, автоматическая загрузка будет отключена для соответствующей печатающей головки.': 'Se disabilitato, il caricamento automatico sarà disattivato per la testina corrispondente.',
    'Распознавание филамента': 'Riconoscimento filamento',
    'Редактирование профиля филамента': 'Modifica profilo filamento',
    'загрузка филамента': 'carico filamento',
    'Когда текущий филамент заканчивается, принтер автоматически переключается на другую печатающую головку с тем же материалом и цветом, чтобы продолжить печать.': "Quando il filamento finisce, la stampante passa automaticamente a un'altra testina con stesso materiale e colore.",
    'Калибровка устройства': 'Calibrazione dispositivo',
    'Калибровка завершена': 'Calibrazione completata',
    'Калибровка не удалась': 'Calibrazione fallita',
    'Хотите выйти из процесса калибровки?': 'Uscire dalla calibrazione?',
    'Прервать выравнивание': 'Interrompi livellamento',
    'Калибровка смещения нескольких печатающих головок': 'Calibrazione offset testine',
    'Советы по калибровке смещения экструдеров': 'Suggerimenti calibrazione offset estrusori',
    'Компенсация вибрации': 'Comp. vibrazione',
    'Советы по калибровке виброгасителей': 'Suggerimenti calibrazione ammortizzatori',
    'Прогресс выравнивания': 'Avanzamento livellamento',
    'Советы по калибровке нагревательной платформы': 'Suggerimenti calibrazione piano riscaldato',
    'Предварительный нагрев нагревательного стола...': 'Pre-riscaldamento piano...',
    'Предварительное зондирование нагревательного стола...': 'Pre-probing piano riscaldato...',
    'Сейчас начнётся компенсация вибрации.\nЭто займёт около 5 минут.\n': "La compensazione vibrazione sta per iniziare.\nRichiederà circa 5 minuti.\n",
    'Очистка сопла...': 'Pulizia ugello...',
    'Очистка сопла': 'Pulizia ugello',
    'Очистка сопла 1': 'Pulizia ugello 1',
    'Очистка сопла 2': 'Pulizia ugello 2',
    'Очистка сопла 3': 'Pulizia ugello 3',
    'Очистка сопла 4': 'Pulizia ugello 4',
    'Очистите сопло прилагаемой проволочной щеткой и поддерживайте чистоту в месте стыковки.': 'Pulire ugello con spazzolino metallico e mantenere pulito il punto di aggancio.',
    'Калибровка сопла 1': 'Calibr. ugello 1',
    'Калибровка сопла 2': 'Calibr. ugello 2',
    'Калибровка сопла 3': 'Calibr. ugello 3',
    'Калибровка сопла 4': 'Calibr. ugello 4',
    'Калибровка системы подавления вибрации на начальном этапе...': 'Calibrazione sistema anti-vibrazione iniziale...',
    'Калибровка компенсации вибрации...': 'Calibr. compensaz. vibrazione...',
    'Вибрация принтера во время этого процесса является нормальным явлением.': 'Le vibrazioni durante questo processo sono normali.',
    'Тест захвата/установки': 'Test aggancio/install.',
    'Прервать калибровку': 'Interrompi calibr.',
    'Охлаждение сопла': 'Raffredda ugello',
    'Следуйте приведенной ниже инструкции, чтобы установить печатающую головку на место и проверить ее положение.': 'Seguire le istruzioni per reinstallare la testina e verificarne la posizione.',
    'Неисправность': 'Guasto',
    'Ручное выравнивание': 'Livellamento manuale',
    'Далее, следуя инструкциям, отрегулируйте вручную четыре регулировочных колеса, как показано на рисунке.': 'Seguire le istruzioni e regolare manualmente le quattro ruote come mostrato.',
    'Обратитесь к иллюстрации ниже и вручную поверните четыре регулировочных колеса до тех пор, пока их поверхность не   окажется на одном уровне с концами винтов.': 'Ruotare le quattro ruote fino a che la superficie sia al livello delle viti.',
    'Расчет референсной высоты': 'Calcolo altezza rif.',
    'Зондирование': 'Probing',
    'Регулировка колес выравнивания': 'Regolazione ruote livellamento',
    'Повторная проверка контрольных точек...': 'Verifica punti di controllo...',
    'Ручное выравнивание выполнено успешно': 'Livellamento manuale completato',
    'Калибровка возврата в исходное положение': 'Calibrazione ritorno in posizione',
    'Вы уверены, что можете выйти из процесса калибровки возврата в исходное положение?': 'Uscire dalla calibrazione ritorno in posizione?',
    'Прерывание калибровки возврата в исходное положение...': 'Interruzione calibrazione ritorno...',
    'Пожалуйста, выполняйте калибровку только под руководством официальной технической поддержки. Неправильная регулировка может привести к сбоям при возврате в исходное положение или смене инструмента.': 'Eseguire la calibrazione solo con supporto ufficiale. Regolazioni errate causano problemi al ritorno in posizione.',
    'Натяните ремень ГРМ': 'Tendere la cinghia',
    'Ослабьте (но не выкручивайте) два показанных винта, повернув их против часовой стрелки примерно на два оборота.': 'Allentare (senza rimuovere) le due viti di circa due giri in senso antiorario.',
    'Переместите механизм смены печатающих головок вручную по указанной траектории примерно два цикла.': 'Spostare manualmente il meccanismo di cambio testine per circa due cicli.',
    'Затяните два винта в указанных местах.': 'Stringere le due viti indicate.',
    'Расчетное время': 'Tempo stimato',
    'Пожалуйста, натяните ремень ГРМ и попробуйте снова.': 'Tendere la cinghia e riprovare.',
    'Настройка': 'Impostaz.',
    'Калибровка не удалась. Пожалуйста, скорректируйте координаты и повторите попытку.': 'Calibrazione fallita. Correggere le coordinate e riprovare.',
    'Следуйте инструкциям, чтобы совместить установочный штифт    1    с гнездом печатающей головки.   2': 'Seguire le istruzioni per allineare il perno 1 con il vano testina. 2',
    'Выполняется калибровка возврата в исходное положение\u2026': 'Calibrazione ritorno in posizione in corso...',
    'Выполняется калибровка координат печатающей головки\u2026': 'Calibrazione coordinate testina in corso...',
    'Нажимайте кнопки ниже, чтобы отрегулировать положение механизма смены печатающих головок до тех пор, пока установочный штифт не окажется по центру гнезда печатающей головки. После выравнивания нажмите «Avanti': "Usare i pulsanti per regolare il meccanismo finché il perno si centra nel vano testina. Dopo l'allineamento premere Avanti",
    'Корректировку координат следует проводить под руководством специалистов технической поддержки. Произвольные   корректировки могут привести к сбоям в установке/снятии печатающей головки.': 'La correzione coordinate va eseguita con supporto tecnico. Correzioni arbitrarie causano malfunzionamenti.',
    'Нажмите «Fatto': 'Premere Fatto',
    'Регулировка координат при креплении /отсоединении печатающей головки': 'Regolazione coordinate montaggio/smontaggio testina',
    'Выберите печатающую головку, требующую корректировки координат.': 'Seleziona la testina che richiede correzione coordinate.',
    'Настройка координат крепления/отсоединения печатающей головки': 'Impostazione coordinate montaggio/smontaggio testina',
    'Совет: Для точной настройки можно использовать внешний источник света.': 'Suggerimento: usare luce esterna per una regolazione precisa.',
    'Установите печатающую головку обратно на станцию вручную. Затем повторите попытку настройки координат для   установки/снятия.': 'Reinstallare manualmente la testina. Poi ripetere la regolazione coordinate.',
    'Убедитесь, что все печатающие головки надежно закреплены в своих стыковочных станциях.': 'Verificare che tutte le testine siano fissate nelle stazioni.',
    'После завершения установки красная метка на ползунке больше не должна быть видна.': "Dopo l'installazione il segno rosso sul cursore non deve essere visibile.",
    'Вы уверены, что вышли из режима корректировки координат присоединения/отсоединения печатающей головки?': "Uscire dalla modalità di correzione coordinate?",
    'Подтвердить выход? Калибровочные координаты не будут сохранены.': 'Confermare uscita? Le coordinate di calibrazione non saranno salvate.',
    '«Калибровка ручного выравнивания» сейчас\nзапустится, это займет около 10 минут': 'La "Calibrazione Livellamento Manuale" sta per iniziare,\nrichiederà circa 10 minuti.',
    'Снимите PEI-пластину перед калибровкой.': 'Rimuovere la lastra PEI prima.',
    'Перед калибровкой поместите пластину PEI на место.': 'Posizionare la lastra PEI prima della calibrazione.',
    'Выполняется проверка установки PEI-пластины\u2026': 'Verifica installazione lastra PEI...',
    'Определение положения пластины PEI...': 'Rilevamento posizione lastra PEI...',
    'Выравнивание нагреваемой платформы': 'Livellamento piano riscaldato',
    'Калибровка смещения нескольких печатающих головок завершена. Установите PEI-пластину обратно на нагреваемый стол.': 'Calibrazione offset testine completata. Rimettere la lastra PEI sul piano riscaldato.',
    'Обнаружено, что PEI-пластина не снята. Снимите PEI-пластину и нажмите «Avanti': 'Lastra PEI non rimossa. Rimuoverla e premere Avanti',
    'PEI-пластина не обнаружена. Установите PEI-пластину на нагреваемый стол и нажмите «Avanti': 'Lastra PEI non trovata. Installarla sul piano riscaldato e premere Avanti',
    'PEI-пластина не обнаружена. Установите PEI-пластину и нажмите «Avanti': 'Lastra PEI non trovata. Installarla e premere Avanti',
    'Поверните регулировочные колесики, и зеленый ползунок внизу переместится соответствующим образом. Подождите не менее двух   секунд после того, как зеленый ползунок достигнет центрального положения, прежде чем нажимать «Далее».': 'Ruotare le ruote di regolazione, il cursore verde si sposterà. Attendere almeno 2 sec. dopo che il cursore ha raggiunto il centro prima di premere Avanti.' + ' ' * 40,
    'Нанесите литиевую смазку': 'Applicare grasso al litio',
    'Нанесите литиевую смазку на 3 стальных шарика на каждой головке': "Applicare grasso al litio sulle 3 sfere d'acciaio di ogni testina",
    'Очистка подпружиненных контактов': 'Pulizia contatti pogo',
    'Очистите контактные штыри на всех печатающих головках и устройстве смены головок с помощью прилагаемой салфетки': 'Pulire i perni di contatto su tutte le testine con il panno in dotazione',
    'Проведение планового технического обслуживания может повлиять на качество печати и срок службы стальных шариков. Подтвердите завершение?': "La manutenzione può influire sulla qualità di stampa. Confermare completamento?",
    'Техническое обслуживание завершено.': 'Manutenzione completata.',
    'Рекомендуется смазка': 'Lubrificaz. consigliata',
    'Смазка завершена': 'Lubrificazione OK',
    'Инструкция по замене фильтрующего элемента 1. Откройте крышку фильтра. 2. Извлеките старый фильтр. 3. Установите   новый фильтр. 4. После замены вернитесь на предыдущую страницу и вручную нажмите кнопку «Заменено», чтобы пересчитать время работы фильтра.': 'Sostituzione filtro: 1. Aprire coperchio. 2. Estrarre vecchio filtro. 3. Installare nuovo filtro. 4. Tornare e premere Sostituito per resettare il timer.',
    'Настройки': 'Impostaz.',
    'Сеть': 'Rete',
    'Язык': 'Lingua',
    'Условия предоставления услуг': 'Termini di servizio',
    'Обслуживание': 'Manutenzione',
    'Тайм-аут экрана': 'Timeout schermo',
    'Статистика использования': 'Statistiche utilizzo',
    'Расширенный режим': "Modalità avanzata",
    'Расширенный режим включен': "Modalità avanzata attivata",
    'Отключить расширенный режим': "Disattiva modalità avanzata",
    'Права root': 'Diritti root',
    'Права root включены': 'Root attivato',
    'Права root отключены': 'Root disattivato',
    'Сброс к заводским настройкам': 'Ripristino di fabbrica',
    'Подтвердить сброс к заводским настройкам?': 'Confermare ripristino impostazioni di fabbrica?',
    'Восстановление заводских настроек...': 'Ripristino in corso...',
    'Очистить все данные': 'Cancella tutti i dati',
    'Пароль Wi-Fi': 'Password Wi-Fi',
    'Введите SSID сети': 'Inserisci SSID rete',
    'MAC-адрес': 'MAC address',
    'Wi-Fi отключен': 'Wi-Fi disattivo',
    'Wi-Fi подключен': 'Wi-Fi connesso',
    'Wi-Fi не подключен': 'Wi-Fi non connesso',
    'Перейдите на страницу настроек Wi-Fi': 'Vai alle impostazioni Wi-Fi',
    'Неверный пароль, пожалуйста, попробуйте еще раз.': 'Password errata, riprovare.',
    'Соединение не удалось, пожалуйста, попробуйте еще раз.': 'Connessione fallita, riprovare.',
    'Сеть управления': 'Rete di controllo',
    'Вы уверены, что хотите удалить эту сеть?': 'Eliminare questa rete?',
    'Подключение к скрытой сети': 'Connessione a rete nascosta',
    'Выберите тип шифрования': 'Scegli crittografia',
    'Сохраненные сети': 'Reti salvate',
    'Включить максимальную совместимость': "Abilita compatibilità massima",
    'Режим локальной сети': "Modalità rete locale",
    'Локальная сеть': 'Rete locale',
    'Режим локальной сети включен.': "Modalità rete locale attivata.",
    'В режиме локальной сети (LAN) работа служб учетной записи будет прервана.': "In modalità LAN i servizi account saranno interrotti.",
    'Перейти на страницу локальной сети': 'Vai a rete locale',
    'Не удалось установить режим локальной сети.': "Impossibile attivare modalità rete locale.",
    'Не удалось получить информацию о соединении.': 'Impossibile ottenere info connessione.',
    'Не удалось получить код доступа к локальной сети': 'Impossibile ottenere codice rete locale',
    'Код доступа': 'Codice acc.',
    'код доступа': 'codice acc.',
    'Отключить': 'Disconnetti',
    'Отключено': 'Disconnesso',
    'Вы отключаете устройство от клиента в локальной сети? Вы уверены, что отключаете именно его?': 'Disconnettere il dispositivo da un client LAN. Sei sicuro?',
    'Нажатие кнопки отключает это устройство от клиентов локальной сети.': 'Questo disconnette il dispositivo dai client LAN.',
    'К устройству не подключен ни один клиент локальной сети': 'Nessun client LAN connesso al dispositivo',
    'Учетная запись': 'Account',
    'Выбор региона': 'Scegli regione',
    'Материковый Китай': 'Cina continentale',
    'Глобальный': 'Globale',
    'Войти в аккаунт': 'Accedi ad account',
    'Подтвердить выход?': 'Confermare uscita?',
    'Имя пользователя': 'Nome utente',
    'Войдите в систему, чтобы включить удаленное управление принтером.': 'Accedere per abilitare il controllo remoto.',
    'Для входа в систему отсканируйте QR-код с помощью приложения Snapmaker.': "Scansiona il QR-code con l'app Snapmaker per accedere.",
    'Перед входом в учетную запись подключитесь к Wi-Fi.': 'Connettiti al Wi-Fi prima di accedere.',
    'Вход с рабочего стола': 'Accesso da desktop',
    'Вход с мобильного устройства': 'Accesso da mobile',
    'ПИН-код': 'PIN',
    'Обновление через': 'Aggiornamento tra',
    'секунд': 'secondi',
    'Нет подключения к интернету. Не удается войти.': 'Nessuna connessione. Impossibile accedere.',
    'Не удалось привязать пользователя': 'Impossibile collegare utente',
    'Получение ПИН-кода...': 'Recupero PIN...',
    'Не удалось получить PIN-код, пожалуйста, проверьте сеть': 'Impossibile ottenere PIN, verificare la rete',
    'Откройте Snapmaker Orca и введите этот codice LAN': 'Aprire Snapmaker Orca e inserire il codice LAN',
    'Проверка сети...': 'Verifica rete...',
    'Проверка устройства...': 'Verifica dispositivo...',
    'Подключение к серверу...': 'Connessione al server...',
    'Отключение от сервера...': 'Disconness. server...',
    'Пожалуйста, подтвердите местоположение устройства и попробуйте снова.': 'Confermare la posizione del dispositivo e riprovare.',
    'Выход из учетной записи не удался.': 'Disconnessione account fallita.',
    'запросить соединение...': 'richiesta connessione...',
    'запрос на подключение не удался': 'richiesta connessione fallita',
    'Использование устройств в разных регионах ограничено; их можно привязать или подключить только в пределах обозначенного региона продаж.': "L'uso in regioni diverse è limitato; il collegamento è possibile solo nella regione di vendita designata.",
    'Текущее устройство находится в недоступном регионе, и сгенерировать QR-код для входа в систему невозможно.': 'Dispositivo in regione non disponibile, impossibile generare QR-code di accesso.',
    'Данное устройство недоступно в регионе, и сгенерировать PIN-код невозможно.': 'Dispositivo non disponibile in questa regione, impossibile generare PIN.',
    'Версия прошивки': 'Versione firmware',
    'Проверяем наличие обновлений...': 'Verifica aggiornamenti...',
    'Уже последняя версия': "Già all'ultima versione",
    'Локальное обновление': 'Aggiornamento locale',
    'Файл обновления не обнаружен': 'File aggiornamento non trovato',
    'Скачать сейчас': 'Scarica ora',
    'Обновите сейчас': 'Aggiorna ora',
    'Проверьте сеть и повторите попытку': 'Controlla la rete e riprova',
    'Нет подключения к интернету. Невозможно обновить онлайн.': 'Nessuna connessione. Aggiornamento online non possibile.',
    'Подтвердите обновление файла': 'Conferma aggiornamento file',
    'Обнаружена новая версия': 'Nuova versione rilevata',
    'Найдена версия': 'Versione trovata',
    'Во время обновления система может перезагрузиться. Не выключайте питание!': "Durante l'aggiornamento il sistema potrebbe riavviarsi. Non spegnere!",
    'Скачать сейчас?': 'Scaricare ora?',
    'Новая версия готова': 'Nuova versione pronta',
    'Обновление займет около 5 minuti': 'Aggiornamento: circa 5 minuti',
    'Обновление займет около 5 минут. Устройство автоматически перезагрузится. Убедитесь, что питание   подключено. Обновить сейчас?': "Aggiornamento in 5 min. Il sistema si riavvierà. Alimentazione collegata? Aggiornare ora?",
    'Обновление прошивки не удалось. Пожалуйста, перезагрузите устройство.': 'Aggiornamento firmware fallito. Riavviare il dispositivo.',
    'Обновление прошивки не удалось. Пожалуйста, проверьте, действителен ли файл прошивки.': "Aggiornamento firmware fallito. Verificare validità del file.",
    '. Устройство автоматически перезагрузится. Убедитесь, что питание   подключено. Обновить сейчас?': ". Il dispositivo si riavvierà. Alimentazione collegata? Aggiornare ora?",
    'Название устройства': 'Nome dispositivo',
    'Модель устройства': 'Modello dispositivo',
    'Серийный номер': 'Numero seriale',
    'Емкость хранилища': "Capacità storage",
    'Системный журнал': 'Log di sistema',
    'Сертификаты': 'Certificati',
    'Обнаружен модуль CAN': 'Modulo CAN rilevato',
    'Модуль CAN не обнаружен': 'Modulo CAN non rilevato',
    'Экспорт фотографий мониторинга ИИ': 'Esporta foto monitoraggio AI',
    'Помогает устранять неполадки в мониторинге ИИ и другие проблемы.': 'Aiuta a risolvere problemi nel monitoraggio AI.',
    'Экспорт журналов в локальное хранилище': 'Esporta log in archivio locale',
    'Журналы экспорта': 'Esporta log',
    'Экспорт... Пожалуйста, подождите.': 'Esportazione... Attendere.',
    'Успешный экспорт': 'Export riuscito',
    'Экспорт не удался. Повторите попытку.': 'Esportazione fallita. Riprovare.',
    'Удаление... Пожалуйста, подождите.': 'Eliminazione... Attendere.',
    'Мониторинг с помощью ИИ': 'Monitoraggio AI',
    'Настройки чувствительности обнаружения': "Sensibilità rilevamento",
    'Обнаружение посторонних предметов': 'Rilevamento oggetti estranei',
    'Принтер автоматически приостановит работу, если во время подготовки будет обнаружен посторонний предмет.': "La stampante si fermerà se viene rilevato un oggetto estraneo.",
    'Идет печать. Нужно ли отключать мониторинг с помощью ИИ?': 'Stampa in corso. Disattivare monitoraggio AI?',
    'Мониторинг с помощью ИИ включен. Выключение светодиода может снизить точность обнаружения. Выключить его все равно?': 'Monitoraggio AI attivo. Spegnere il LED riduce l\'accuratezza. Spegnere comunque?',
    'Ложная тревога обратной связи': 'Segnala falso allarme',
    'Обнаружение печати в воздухе': 'Rilevamento spaghetti',
    'Обнаружение "спагетти"': 'Rilevamento "spaghetti"',
    'Печать автоматически приостанавливается при обнаружении запутывания филамента или засорения сопла.': 'La stampa si metterà in pausa in caso di groviglio o ugello ostruito.',
    'Чувствительность обнаружения печати в воздухе': "Sensibilità rilevamento spaghetti",
    'Обнаружение наматывания': 'Rileva ingarbugl.',
    'Никаких отклонений обнаружено не было;\nобнаружение ИИ было подтверждено как ложная тревога.': 'Nessuna anomalia rilevata;\nmonitoraggio AI confermato come falso allarme.',
    'минут': 'minuti',
    'Никогда': 'Mai',
    'Общее время печати': 'Ore di stampa totali',
    'Количество смен печатающих головок': 'Conteggio cambi testina',
    'Время работы очистителя воздуха': 'Ore filtro aria',
    'Предложите изменения': 'Suggerisci modifiche',
    'Время работы фильтра': 'Vita filtro HEPA',
    'Фильтр работает слишком долго, рекомендуется его заменить.': 'Filtro esausto, si consiglia la sostituzione.',
    'Измененный': 'Modificato',
    'Выполнить смену': 'Esegui cambio',
    'Помощник устройства': 'Assist. dispositivo',
    'Новых сообщений нет. Все системы работают в норме.': 'Nessun avviso. Tutti i sistemi operativi.',
    'Код': 'Cod.',
    'Напомни мне позже': 'Ricordamelo dopo',
    'Устранение неполадок сейчас': 'Risolvi ora',
    'Код ошибки': 'Cod. errore',
    'Посмотреть решение': 'Vedi soluzione',
    '[Ошибка]': '[Errore]',
    '[Предупреждение]': '[Avviso]',
    '[Уведомление]': '[Notifica]',
    'Свяжитесь support@snapmaker.com.': 'Contatta support@snapmaker.com.',
    'Свяжитесь support@snapmaker.com, если проблема сохраняется.': 'Contatta support@snapmaker.com se il problema persiste.',
    'Отсканируйте этот QR-код, чтобы получить руководство по устранению неполадок.': 'Scansiona il QR-code per la guida alla risoluzione dei problemi.',
    'Тестирование устройства': 'Test diagnostici',
    'Камера': 'Camera',
    'Очиститель не обнаружен': 'Purificatore non rilevato',
    'Проверка очистителя...': 'Verifica purificatore...',
    'Ошибка очистителя': 'Errore purificatore',
    'Очиститель обычный': 'Purificatore normale',
    'Камера подключена': 'Telecamera connessa',
    'Камера отключена': 'Camera disconn.',
    'Плохо': 'Scarso',
    'Хорошо': 'Bene',
    'Отлично': 'Ottimo',
    'Условия': 'Termini',
    'Для продолжения ознакомьтесь со следующими Условиями и примите их.\n\nУсловия использования\nПолитика конфиденциальности\n': "Per continuare accettare i seguenti Termini.\n\nTermini d'uso\nPrivacy Policy\n",
    'Отсканируйте, чтобы просмотреть полные условия': 'Scansiona per EULA completa',
    'Принтер выполнит следующие калибровки:': "La stampante eseguirà le calibrazioni:",
    'Далее процедура загрузки филамента будет завершена примерно через 5 минут': "Il caricamento filamento si completerà in circa 5 minuti",
    'Не удалось запустить систему_Печатающая головка не обнаружена. Обратитесь в службу технической поддержки.': 'Errore avvio sistema_Testina non rilevata. Contattare il supporto.',
    'Аномалия датчика_Конфигурация датчика АЦП превысила допустимый предел. Система отключена в целях безопасности. Экспортируйте журналы принтера и обратитесь в службу технической поддержки.': 'Anomalia sensore_Configurazione ADC fuori limite. Sistema spento per sicurezza. Esportare log e contattare supporto.',
    'Аномалия температуры сопла_Выключите принтер и проверьте подключение керамического нагревателя или терморезистора печатающей головки 1.': 'Anomalia temp. ugello_Spegnere e verificare riscaldatore/termistore testina 1.',
    'Аномалия температуры сопла_Выключите принтер и проверьте подключение керамического нагревателя или терморезистора печатающей головки 2.': 'Anomalia temp. ugello_Spegnere e verificare riscaldatore/termistore testina 2.',
    'Аномалия температуры сопла_Выключите принтер и проверьте подключение керамического нагревателя или терморезистора печатающей головки 3.': 'Anomalia temp. ugello_Spegnere e verificare riscaldatore/termistore testina 3.',
    'Аномалия температуры сопла_Выключите принтер и проверьте подключение керамического нагревателя или терморезистора печатающей головки 4.': 'Anomalia temp. ugello_Spegnere e verificare riscaldatore/termistore testina 4.',
    'Техническое обслуживание печатной головки_Количество смен печатающих головок достигло значения, требуемого для технического обслуживания. Очистите подпружиненные контакты с обеих сторон и нанесите смазку на стальные шарики и штифты печатающей головки.': 'Manutenzione testina_Cambi raggiunti. Pulire contatti pogo e lubrificare sfere e perni testina.',
    'Блокировка экструзии_Заблокирована экструзия филамента на приводном колесе печатающей головки 1. Проверьте и очистите, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Blocco estrusione_Bloccata ruota testina 1. Verificare e pulire. Se in stampa, premere play per riprendere.',
    'Блокировка экструзии_Заблокирована экструзия филамента на приводном колесе печатающей головки 2. Проверьте и очистите, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Blocco estrusione_Bloccata ruota testina 2. Verificare e pulire. Se in stampa, premere play per riprendere.',
    'Блокировка экструзии_Заблокирована экструзия филамента на приводном колесе печатающей головки 3. Проверьте и очистите, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Blocco estrusione_Bloccata ruota testina 3. Verificare e pulire. Se in stampa, premere play per riprendere.',
    'Блокировка экструзии_Заблокирована экструзия филамента на приводном колесе печатающей головки 4. Проверьте и очистите, затем повторите попытку. Если принтер печатает, нажмите кнопку воспроизведения, чтобы возобновить задание печати.': 'Blocco estrusione_Bloccata ruota testina 4. Verificare e pulire. Se in stampa, premere play per riprendere.',
    'Аномальная температура нагрева печатного стола_Аномалия нагрева печатного стола. Обратитесь в службу технической поддержки.': 'Anomalia riscaldamento piano_Anomalia rilevata. Contattare il supporto.',
    'Аномалия возврата в исходное положение_Текущая печатающая головка недоступна, невозможно выполнить калибровку. Перезапустите принтер и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia homing_Testina non disponibile. Riavviare e riprovare. Se persiste, contattare supporto.',
    'Аномалия обнаружения печатного стола_Обнаружена аномалия в работе нагревательного стола. Обратитесь в службу технической поддержки.': 'Anomalia piano riscaldato_Anomalia rilevata. Contattare il supporto.',
    'Системная аномалия_Печать не возобновилась после отключения электроэнергии.': 'Anomalia sistema_Stampa non ripresa dopo interruzione alimentazione.',
    'Аномалия возврата в исходное положение_Датчик возврата в исходное положение не сработал. Проверьте сопло на наличие остатков нити и очистите его перед повторной попыткой. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia homing_Sensore homing non attivato. Controllare e pulire ugello. Se persiste, contattare supporto.',
    'Системная аномалия_Загрузка файла в облачное хранилище не удалась. Проверьте подключение к сети и повторите попытку. Если проблема сохраняется, обратитесь в службу технической поддержки.': 'Anomalia sistema_Upload file cloud fallito. Verificare rete. Se persiste, contattare supporto.' + ' ' * 20,
    'Аномалия экструзии_Сбой подачи в подающем механизме 1. Возможно, филамент запутался, застрял в экструзионных шестернях или засорилось сопло. Устраните проблему и повторите попытку.': 'Anomalia estrusione_Errore alimentatore 1. Filamento aggrovigliato, bloccato o ugello intasato. Risolvere e riprovare.',
    'Аномалия замены печатной головки_Печатающая головка 1 отсоединена. Установите её обратно вручную, затем нажмите для возобновления задания. Если ошибка не устранена, обратитесь в техническую поддержку.': 'Anomalia cambio testina_Testina 1 scollegata. Reinstallare e premere per riprendere. Se persiste, contattare supporto.',
    'Нераспознанные команды G-кода_Файл для печати содержит команды G-кода, не поддерживаемые данным устройством. Печать прекращена.': 'Comandi G-code non supportati_Il file contiene comandi non supportati. Stampa interrotta.',
    'Сбой калибровки возврата в исходное положение_Пожалуйста, натяните ремень ГРМ и попробуйте снова. Если проблема не исчезнет, выполните калибровку для возврата в исходное положение.': 'Errore cal. homing_Tendere la cinghia e riprovare. Se persiste, eseguire calibrazione homing.',
    'Обнаружена неравномерность нагрева стола_Отклонение плоскостности нагреваемого стола слишком велико. Выполните ручное выравнивание стола.': "Piano irregolare_Planarità fuori tolleranza. Eseguire livellamento manuale.",
    'Сбой калибровки возврата в исходное положение_Ошибка диагонального зондирования.': 'Errore cal. homing_Errore probing diagonale.',
    'Сбой калибровки возврата в исходное положение_Не удалось проверить точку зондирования.': 'Errore cal. homing_Impossibile verificare punto di probing.',
    'Сбой калибровки возврата в исходное положение_Достигнуто максимальное количество попыток.': 'Errore cal. homing_Raggiunto numero massimo tentativi.',
    'Мало места в хранилище_Недостаток памяти на устройстве может повлиять на функциональность печати. Удалите некоторые файлы G-кода или таймлапса, чтобы освободить место.': "Spazio insufficiente_Lo spazio ridotto può influire sulla stampa. Eliminare file Gcode o timelapse.",
    'Аномалия обнаружения_Установите любую одну печатающую головку и повторите попытку.': 'Anomalia rilevamento_Installare almeno una testina e riprovare.',
    'Аномалия обнаружения печатного тола_PEI-пластина установлена неправильно. Установите PEI-пластину корректно и повторите попытку.': 'Anomalia rilevamento piano_Lastra PEI installata in modo errato. Reinstallare correttamente.',
    'Возможно, на печатном столе обнаружен посторонний предмет_Пожалуйста, проверьте и удалите все посторонние предметы. Если посторонних предметов не обнаружено, нажмите «Continua': 'Oggetto estraneo rilevato sul piano_Verificare e rimuovere. Se non trovato, premere Continua',
    'Обнаружен возможный дефект спагетти_Пожалуйста, осмотрите модello. Если обнаруженные дефекты допустимы или дефекты не найдены, нажмите «Continua': 'Possibile difetto spaghetti_Ispezionare il modello. Se accettabile, premere Continua',
    'На печатной платформе обнаружены возможные остатки._Пожалуйста, проверьте и удалите все остатки клея. Если ничего не обнаружено, нажмите «Continua': 'Possibili residui sul piano_Verificare e rimuovere residui di colla. Se assenti, premere Continua',
    '• Специальные разрешения при активации\n  • Включение этой опции предоставляет вам права на\n    изменение файлов конфигурации принтера. Мы\n    настоятельно не рекомендуем изменять эти настройки,\n    если вы полностью не понимаете функции параметров\n    конфигурации принтера. Произвольные изменения\n    могут привести к сбоям в работе функций устройства,\n    таких как защита от перегрева, калибровка XYZ,\n    выравнивание нагреваемого стола и автоматическая\n    подача филамента.\n  • Modalità sviluppatore\n   позволяет свободно добавлять,\n    удалять или изменять файлы конфигурации устройства,\n    что может привести к потенциальным проблемам,\n    включая, помимо прочего: дефекты заданий печати,\n    непоправимый ущерб принтеру, необратимый вред,\n    а также проблемы с безопасностью и\n    конфиденциальностью данных.\n• Влияние на права и интересы послепродажного\n    обслуживания\n  • Компания Snapmaker не имеет возможности установить\n    или проверить результаты, вытекающие из активации\n    расширенного режима. Включая этот режим, вы\n    признаете и принимаете все связанные с этим риски\n    или последствия и берете на себя полную\n    ответственность за них. В максимальной степени,\n    допустимой действующим законодательством, мы не\n    несем ответственности за любые убытки или риски,\n    возникающие в результате использования или\n    невозможности использования продукта, а также не\n    обязуемся предоставлять техническую поддержку\n    по вопросам или аномалиям, возникающим во время\n    использования продукта, включая, помимо прочего,\n    сбои в работе системы, невозможность выполнения\n    команд или потерю файлов.': "• Permessi speciali all'attivazione\n  • Questa opzione concede i diritti di modifica dei file di configurazione. Si sconsiglia vivamente di modificare queste impostazioni senza conoscerle. Modifiche arbitrarie possono causare guasti come protezione da surriscaldamento, calibrazione XYZ, livellamento piano e alimentazione filamento.\n  • La modalita' avanzata consente di modificare liberamente i file di configurazione, il che puo' causare difetti di stampa, danni irreparabili, problemi di sicurezza e privacy.\n• Impatto sulla garanzia post-vendita\n  • Snapmaker non puo' stabilire o verificare i risultati derivanti dall'attivazione della modalita' avanzata. Attivando questa modalita', si riconoscono e si accettano tutti i rischi. Nella misura massima consentita dalla legge, non siamo responsabili per perdite o rischi derivanti dall'uso del prodotto."
}

def patch_binary(src, dst, translations):
    if not os.path.exists(src):
        print(f"[-] Errore: File {src} non trovato!")
        sys.exit(1)

    if not os.path.exists(BAK):
        print(f"[*] Creazione backup in {BAK}...")
        os.system(f"cp {src} {BAK}")
    else:
        print(f"[*] Backup già presente: ripristino il binario ORIGINALE (russo) da {BAK} prima di ripatchare...")
        # cp diretto fallirebbe con "Text file busy" perché il processo gui
        # è in esecuzione e mappa quell'inode: bisogna prima "liberare" il
        # nome file (rm) e poi ricrearlo (cp), esattamente come si fa più
        # sotto per installare il binario patchato.
        os.system(f"rm -f {src}")
        os.system(f"cp {BAK} {src}")

    with open(src, 'rb') as f:
        data = bytearray(f.read())

    # Controllo di sicurezza: se il binario che stiamo per patchare non
    # contiene più nemmeno una stringa russa banale, vuol dire che il
    # ripristino dal backup non è andato a buon fine (es. "Text file busy"
    # silenzioso) e stiamo per rileggere un binario già patchato in italiano.
    # In quel caso meglio fermarsi con un errore chiaro invece di produrre
    # silenziosamente "0 tradotte".
    sonda = 'Отмена'.encode('utf-8')
    if sonda not in data:
        print(f"[-] ERRORE: nessuna stringa russa di controllo trovata in {src}.")
        print(f"    Il binario sembra già patchato (il ripristino da {BAK} potrebbe essere fallito).")
        print(f"    Verifica manualmente con: cmp {src} {BAK}")
        sys.exit(1)

    items = sorted(translations.items(), key=lambda x: len(x[0].encode('utf-8')), reverse=True)

    ok = skip = notfound = 0
    skipped_report = []
    print("[*] Iniezione traduzioni in corso...")

    for ru_str, it_str in items:
        ru_b = ru_str.encode('utf-8')
        it_b = it_str.encode('utf-8')

        # Confronto sui CARATTERI (glifi renderizzati), non sui byte.
        # Il cirillico in UTF-8 usa 2 byte/carattere, l'italiano 1 byte/carattere:
        # a parità di byte disponibili l'italiano avrebbe quasi il doppio dei
        # caratteri, sconfinando visivamente sui widget vicini (bottoni,
        # slider, ecc.). Per questo il limite va posto sul numero di
        # caratteri della stringa russa originale.
        # Per le parole/frasi molto corte una tolleranza puramente
        # percentuale è troppo rigida (il 15% di 3 caratteri è <1), quindi
        # garantiamo comunque un margine minimo fisso di 2 caratteri.
        budget = max(len(ru_str) + 2, int(len(ru_str) * LUNGHEZZA_TOLLERANZA))
        if len(it_str) > budget:
            skip += 1
            eccesso = len(it_str) - len(ru_str)
            skipped_report.append((ru_str, it_str, eccesso))
            continue

        # Il padding per riempire il buffer resta comunque in BYTE, perché
        # stiamo scrivendo direttamente nel buffer a lunghezza fissa del binario.
        padded_it = it_b + b'\x00' * (len(ru_b) - len(it_b))
        
        count = idx = 0
        while True:
            pos = data.find(ru_b, idx)
            if pos == -1: break
            data[pos:pos+len(ru_b)] = padded_it
            idx = pos + len(padded_it)
            count += 1
            
        if count > 0: ok += 1
        else: notfound += 1

    orig_debug = b'/oem/.debug'
    fake_debug = b'/oem/.dummy'
    idx = 0
    while True:
        pos = data.find(orig_debug, idx)
        if pos == -1: break
        data[pos:pos+len(orig_debug)] = fake_debug
        idx = pos + len(fake_debug)

    with open(dst, 'wb') as f:
        f.write(data)

    print(f"\n[*] Riepilogo: {ok} tradotte, {notfound} non trovate nel binario, {skip} scartate per eccesso caratteri.")

    if skipped_report:
        print("\n[!] Voci scartate perché la traduzione italiana ha più CARATTERI dell'originale russo:")
        print("    (queste stringhe restano in russo nella GUI finché non le accorci)\n")
        # Ordino dalle più critiche (eccesso maggiore) alle meno critiche
        for ru_str, it_str, eccesso in sorted(skipped_report, key=lambda x: -x[2]):
            ru_preview = (ru_str[:50] + '…') if len(ru_str) > 50 else ru_str
            it_preview = (it_str[:50] + '…') if len(it_str) > 50 else it_str
            print(f"    +{eccesso:3d} car. | RU[{len(ru_str)}]: {ru_preview!r}")
            print(f"              IT[{len(it_str)}]: {it_preview!r}")

if __name__ == '__main__':
    patch_binary(SRC, DST, TRANSLATIONS)
    print("\n[*] Installazione di sistema in corso...")
    os.system("touch /oem/.debug") 
    os.system("killall gui 2>/dev/null")
    os.system(f"rm -f {SRC}")
    os.system(f"cp {DST} {SRC}")
    os.system(f"chmod +x {SRC}")
    os.system("killall gui 2>/dev/null")
    print("\n[V] FATTO! L'interfaccia si sta riavviando in Italiano.")
