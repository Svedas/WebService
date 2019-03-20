# Reference for EPharma web service 

### Setting up

- git clone https://github.com/Svedas/WebService
- docker-compose up --build -d

### Usage

Responses have these forms:

**Form format**

```json
{
	"message": "Information",
	"data": []
}
```

**Client form**

```json
{
	"message": "OK",
	"data": [
	   {
		"name": "Vardenis Pavardenis",
		"address": "Vilnius, Didlaukio g. 14",
		"email": "test@mail.com",
		"id": "client24"
	   }
	]
}
```

**Order form**

```json
{
	"message": "OK",
	"data": [
	   {
		"item": "Apap",
		"price": "50.00",
		"amount": "10"
	   }
	]
	
}
```


## List of all clients

**Definition**

`GET /clients`

**Response**

- `200 OK` on success

```json
{
	"message": "OK",
	"data": [
	   {
		"name": "Vardenis Pavardenis",
		"address": "Vilnius, Didlaukio g. 14",
		"email": "test@mail.com",
		"id": "client24"
	   },
	   {
		"name": "Vardas Vardenis",
		"address": "Vilnius, Naugarduko g. 24",
		"email": "test@anothermail.com",
		"id": "client5"
	   }
	]
}
```


## Adding new client

**Definition**

`POST /clients`

**Arguments**

- `"name":string`  client name or full name
- `"address":string`  shipping address
- `"email":string`  contacting info

**Response**

- `201 Created` on success


## Deleting all clients

**Definition**

`DELETE /clients`

**Response**

- `204 No content` on success


## Getting client info

**Definition**

`GET /clients/<id>`

**Response**

- `200 OK` on success
- `404 Not Found` if client do not exists

```json
{
	"message": "OK",
	"data": [
	   {
		"name": "Vardenis Pavardenis",
		"address": "Vilnius, Didlaukio g. 14",
		"email": "test@mail.com",
		"id": "client24"
	   }
	]
}
```


## Deleting client

**Definition**

`DELETE /clients/<id>`

**Response**

- `204 No content` on success
- `404 Not Found` if client do not exists


## Updating client

**Definition**

`PUT /clients/<id>`

**Arguments**

- `"name":string`  client name or full name
- `"address":string`  shipping address
- `"email":string`  contacting info

**Response**

- `200 OK` on success


## List of client's orders

**Definition**

`GET /clients/<id>/orders`

**Response**

- `200 OK` on success

```json
{
	"message": "OK",
	"data": [
	   {
		"item": "AnyCommonMedication",
		"price": "12.00",
		"amount": "2"
	   },
	   {
		"item": "SomeGenericMedication",
		"price": "18.50",
		"amount": "3"
	   }
	]
}
```


## Adding new order for client

**Definition**

`POST /clients/<id>`

**Arguments**

- `"item":string`  item name
- `"price":string`  item price
- `"amount":string`  item amount

**Response**

- `201 Created` on success


## Deleting all client's orders

**Definition**

`DELETE /clients/<id>/orders`

**Response**

- `204 No content` on success
