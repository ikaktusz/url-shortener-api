# url-shortener-api

Use the POST method to the /api/ endpoint.  
Here's an example:  
### Request:  
#### POST hostname/api/  
```json
{
    "original_url": "http://yourlongurl.com"  
}
```
### Responce:  
```json
{
    "short_url": "hostname/shorturl"  
}
```

You can use GET method to /api/ endpoint to see all links in database.  
DELETE method to /api/<short_path> to delete link from database.
