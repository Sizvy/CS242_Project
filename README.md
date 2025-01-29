### Scraping

 * We used scrapy.
 * Clone the repository, go to `stackoverflow_scraper/spiders/stackoverflow_spider.py` file and update the `error_tags`.
 * Go to `CS242_Project-master/stackoverflow_scraper` folder and run `scrapy crawl stackoverflow_spider --nolog`

### Json Data Splits

 * set_5 (Nabil)
     - `["error-reporting","error-log","rounding-error","ioerror","custom-errors","nserror","standard-error","onerror"] `
     - `['errorcontrolsystem', 'mysql-error-1349', 'setonerrorlistener', 'enotfound-error', 'mysql-error-1030', 'mysql-error-1040', 'mysql-error-1091', 'kotlin.notimplementederror', 'mysql-error-1415', 'application-onerror', 'error-response', 'illegalaccesserror', 'pg-column-does-not-exist-error', 'vs-error', 'error-kernel', 'aggregateerror', 'mysql-error-1416', 'mysql-error-1327', 'mysql-error-1007', 'mysql-error-1051', 'undefvarerror', 'network-error-logging', 'stale-if-error', 'mysql-error-1065', 'mysql-error-1138', 'mysql-error-1253', 'authentication-error', 'sitecore-error-manager', 'pbi.error']`
     - `['javascript', 'rust', 'c#']` (partial)
 * set_3 (Olid)
     - ` ["internal-server-error","modulenotfounderror","error-logging","http-error","nosuchmethoderror","build-error","index-error"] `
     - `['mysql-error-1292', 'internal-compiler-error', 'mysql-error-1067', 'errortemplate', 'extract-error-message', 'recursionerror', 'sslerrorhandler', 'flutter-renderflex-error', 'mysql-error-1025', 'startup-error', 'mysql-error-2013', 'mysql-error-1044', 'error-recovery', 'mysql-error-1068', 'mysql-error-1066', 'error-messages-for', 'better-errors-gem', 'jsondecodeerror', 'mat-error', 'strerror', 'mysql-error-1136', 'mysql-error-1267', 'mysql-error-1142', 'write-error', 'mysql-error-2006', 'abstractmethoderror', 'eoserror', 'ckerror', 'classformaterror', 'didfailwitherror', 'mysql-error-1364', 'mysql-error', 'nsxmlparsererrordomain']`
