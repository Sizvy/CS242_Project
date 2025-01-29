### Scraping

 * We used scrapy.
 * Clone the repository, go to `stackoverflow_scraper/spiders/stackoverflow_spider.py` file and update the `error_tags`.
 * Go to `CS242_Project-master/stackoverflow_scraper` folder and run `scrapy crawl stackoverflow_spider --nolog`

### Json Data Splits

 * set_5 (Nabil)
     - `["error-reporting","error-log","rounding-error","ioerror","custom-errors","nserror","standard-error","onerror"] `
     - `['errorcontrolsystem', 'mysql-error-1349', 'setonerrorlistener', 'enotfound-error', 'mysql-error-1030', 'mysql-error-1040', 'mysql-error-1091', 'kotlin.notimplementederror', 'mysql-error-1415', 'application-onerror', 'error-response', 'illegalaccesserror', 'pg-column-does-not-exist-error', 'vs-error', 'error-kernel', 'aggregateerror', 'mysql-error-1416', 'mysql-error-1327', 'mysql-error-1007', 'mysql-error-1051', 'undefvarerror', 'network-error-logging', 'stale-if-error', 'mysql-error-1065', 'mysql-error-1138', 'mysql-error-1253', 'authentication-error', 'sitecore-error-manager', 'pbi.error']`
     - `['javascript', 'rust', 'c#']` (partial)
