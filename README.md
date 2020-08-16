# berlin

This script can be used to search the Berlin Ämter for appointments. 

As is, there is no parameter option, you have to directly edit the file to change the service type, which you can find from the URL's linked on the service page: https://service.berlin.de/dienstleistungen/, along with the date range if you want to look beyond the default displayed 2 months. 

The locations are hardcoded at the top, but note not all Amt locations offer the same services. If you look for a service at an amt that doesn't offer it, the URL will fail. 

Package Dependencies: 
  - requests
  - bs4
