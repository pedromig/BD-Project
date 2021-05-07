## Query Examples (To be better formatted in the future)
* User login Query
```bash
curl -X PUT http://localhost:8080/dbproj/user -H "Content-Type: application/json" -d '{"username": "Marega", "password": "Maregod"}'
```

* Expected Response
```json
{
"token": "Here goes a big string that is in fact a token"
}
```

* User Registry Query
```bash
curl -X POST http://localhost:8080/dbproj/user -H "Content-Type: application/json" -d '{"username": "HereGoesaName", "password": "HereGoesAPassword", "email":"HereGoesAnEmail"}'
```

* Expected Response
```json
{
"token": "Here goes a big string that is in fact a token"
}
```

