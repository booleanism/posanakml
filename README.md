# PosAnak ML Integration
## Docker
### Build
```bash
docker build -t posanakml .
```
### Run
```bash
docker run -d -p 8000:8000 posanakml
```

## RESTful API
### Endpoint
```
POST / HTTP/1.1
```
### Request body:
```json
{
  "umur": "string | int",
  "jenis_kelamin": "string | int",
  "tinggi_badan": "string | int"
}
```
### Respon body
```json
{
  "message": "string",
  "result": "int"
}
```
#### Fields
- result:<br>
`-1` - error occurred<br>
`>=0` - succeed (see message field)

- message<br>
if `result` field `>=0`, it's mean success<br>
`0` = `tinggi` - childs taller than normal ones<br>
`1` =  `normal` - normal childs<br>
`2` = `stunting` - supected stunting<br>
`3` = `xstunting` - need further action<br>
otherwise:<br>
`missing request body` - ensure you had passed json request body<br>
`missing json field` - missing required fields or wrong data type<br>
`could not predit` - something else<br>

