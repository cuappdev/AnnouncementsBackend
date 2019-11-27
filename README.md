# Endpoints
## /active/{app_name}/ • GET  
**Returns:**  
```json
{
	"success": true, 
    	"data": ["<Announcement>"]
}  
```
or  
```json
{
	"success": false,
 	"error": "<error_msg>"
 }  
```
*class* Announcement:

| **Name**        | **Type**                                       | **Description**                                                                                                                                                                                 |
| --------------- | ---------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id              | Int                                            | The ID number of the alert.                                                                                                                                                                     |
| body         | String                                         | The body of the announcement.                                                                                                                                                                       |
| ctaAction        | String                                         | The URL associated with this announcement's call to action.                                                           |
| ctaText          | String                                         | The text describing the behavior of the call to action (e.g. 'Download Now').                                                                            |
| expirationDate        | String                                         | The expiration date of the announcement.                                                                  |
| includedApps          | [String]                                         | The list of apps this announcement is valid for (e.g. ["eatery", "uplift"]).                                                                  |
| imageUrl        | String                                            | The URL of the image associated with the announcement.                                                                                                    |
| startDate      | String                                         | The start date of the announcement\. |
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



## /create/ • POST  
**Headers:** 
```json
{
	"Authorization": "Bearer <access_token>"
}
```
**Body:**  
```json
{
	"body":"Body",
	"cta_action": "Call to Action URL",
	"cta_text": "Call to Action Text",
	"expiration_date":"dd/mm/yyyy",
	"image_url": "Image URL",
	"included_apps": ["<app_name>","<app_name>","..."],
	"subject": "Subject",
	"start_date": "dd/mm/yyyy"
} 

```
**Returns:**
```json
{
	"success": true
} 
```
or  
```json
{
	"success": false,
 	"error": "<error_msg>"
 }  
```

## /update/{id}/ • POST     
**Headers:** 
```json
{
	"Authorization": "Bearer <access_token>"
}
```

**Body:**  
###### Note: the request body can have any combination of parameters as long as they are fields of the Announcement model.
```json
{
	"cta_text": "Call to Action Text",
	"expiration_date":"dd/mm/yyyy",
	"included_apps": ["<app_name>","<app_name>","..."],
	"subject": "Subject",
} 

```
**Returns:**
```json
{
	"success": true,
} 
```
or  
```json
{
	"success": false,
 	"error": "<error_msg>"
 }  
```

## /delete/{id}/ • DELETE  
**Headers:** 
```json
{
	"Authorization": "Bearer <access_token>"
}
```
**Returns:**
```json
{
	"success": true,
} 
```
or  
```json
{
	"success": false,
 	"error": "<error_msg>"
 }  
```