## Information
 * [Django REST Framework guide (API KEY)](https://florimondmanca.github.io/djangorestframework-api-key/guide/#authorization-header)
 * [Django REST Framework Tutorial 1 - Serialization](https://www.django-rest-framework.org/tutorial/1-serialization/)


## Testing con curl
* Si la view tiene el decorador @permission_classes([HasAPIKey]) se debe enviar una API key en el header
* Para enviar la llave se debe usar el header: "Authorization: Api-Key <API-KEY>" donde <API-KEY> es una llave generada
* curl --header "Authorization: Api-Key <user.Key>" http://127.0.0.1:8000/api/.../