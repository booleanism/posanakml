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
  "umur": string | int,
  "jenis_kelamin": string | int
  "tinggi_badan": string | int,
}
```
### Respon body
```json
{
  "message": string
  "result": int
}
```
#### Fields
- result:
`-1` - error occurred
`>=0` - succeed (see message field)

- message
if `result` field `>=0`, it's mean succes
`0` = `tinggi` - childs taller than normal ones
`1` =  `normal` - normal childs 
`2` = `stunting` - supected stunting
`3` = `xstunting` - need further action
otherwise
`missing request body` - ensure you had passed json request body
`missing json field` - missing required fields or wrong data type
`could not predit` - something else
