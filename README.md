## Endpoints
#### GET • /active/{app_name}/   
*returns*:  
{"success": true, data: [Announcement]}  
*class* Announcement:

| **Name**        | **Type**                                       | **Description**                                                                                                                                                                                 |
| --------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id              | Int                                            | The ID number of the alert.                                                                                                                                                                     |
| body         | String                                         | The body of the announcement.                                                                                                                                                                       |
| cta_action        | String                                         | The 'action' associated with the announcement. (e.g. URL)                                                            |
| cta_text          | String                                         | The text describing the behavior of the cta_action (e.g. 'Download Now').                                                                            |
| expiration_date        | String                                         | The expiration date of the announcement (formatted mm/dd/yyyy).                                                                  |
| included_apps          | [String]                                         | The list of apps this announcement is valid for (e.g. ["eatery", "uplift"]).                                                                  |
| image_url        | String                                            | The URL of the image associated with the announcement.                                                                                                    |
| start_date      | String                                         | The start date of the announcement (formatted mm/dd/yyyy). |
| subject          | String                                          | The subject of the announcement.                                                                                                                                                                                                                                       |
----------
*example response:*
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "body": "BodyTest",
            "ctaAction": "https://www.cornellappdev.com",
            "ctaText": "CTATest",
            "expirationDate": "2022-04-10",
            "includedApps": [
                "eatery"
            ],
            "imageUrl": "https://pbs.twimg.com/profile_images/898067434107682816/TyrkP8wz_400x400.jpg",
            "startDate": "2019-04-11",
            "subject": "SubjectTest"
        }
    ]
}
```



#### POST • /create/   
*Headers*: 
```json
{
	"Authorization": "Bearer <access_token>"
}
```
*Body*:  
```json
{
	"body":"Body",
	"cta_action": "Call to Action URL",
	"cta_text": "Call to Action Text",
	"expiration_date":"dd/mm/yyyy",
	"image_url": "Image URL",
	"included_apps": ["<app_name>","<app_name>"],
	"subject": "Subject",
	"start_date": "dd/mm/yyyy"
} 

```
*returns*:
```json
{
	"success":true,
} 
```

#### POST • /update/{id}/   
*Headers*: 
```json
{
	"Authorization": "Bearer <access_token>"
}
```

*Body*:  
###### Note: the request body can have any number of valid parameters.
```json
{
	"cta_text": "Call to Action Text",
	"expiration_date":"dd/mm/yyyy",
	"included_apps": ["<app_name>","<app_name>"],
	"subject": "Subject",
} 

```
*returns*:
```json
{
	"success":true,
} 
```

#### DELETE • /delete/{id}/   
*Headers*: 
```json
{
	"Authorization": "Bearer <access_token>"
}
```
*returns*:
```json
{
	"success":true,
} 
```


