converter xml -> ram view (database objects)
converter ram -> xml file
---
work with databases sqlite, postgresql, mssql server
---
Схема загрузки:
xml -> ram -> sqlite
sqlite -> ram -> ddl инструкции -> postgres
ms sql -> ram -> sqlite -> ram -> ddl инструкции -> postgres  
