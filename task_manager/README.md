Google Tasks API with django sample
===================================

django で Google Tasks API を使ったサンプルアプリ

See https://cloud.google.com/appengine/articles/python/getting_started_with_tasks_api

## Usage

create `client_secrets.json` under the root directory.

```json
{
	"web": {
		"client_id": "[YOUR_CLIENT_ID_HERE]",
		"client_secret": "[YOUR_CLIENT_SECRET_HERE]",
		"redirect_uris": [],
		"auth_uri": "https://accounts.google.com/o/oauth2/auth",
		"token_uri": "https://accounts.google.com/o/oauth2/token"
	}
}
```
