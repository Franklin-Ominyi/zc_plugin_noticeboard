import requests, json
from urllib.parse import urlencode
from django.conf import settings


CENTRIFUGO_TOKEN = "58c2400b-831d-411d-8fe8-31b6e337738b"

class Dbnoticeboard:

    """Class based DB to Read and write to zc_core using the read and write endpoints"""

    def __init__(self):
        BASE_URL = "https://api.zuri.chat"
        self.read_endpoint = (
            BASE_URL + "/data/read/613fc3ea6173056af01b4b3e/{collec_name}/{org_id}?{query}"
        )
        self.write_endpoint = BASE_URL + "/data/write"
        self.delete_endpoint = BASE_URL + "/data/delete"
        self.centrifugo_url = "https://realtime.zuri.chat/api"
        self.upload_api = BASE_URL+"/upload/file/613fc3ea6173056af01b4b3e"
        self.upload_multiple_api = BASE_URL+"/upload/files/613fc3ea6173056af01b4b3e"
        self.delete_file_api = BASE_URL+"/delete/file/613fc3ea6173056af01b4b3e"

    def post_to_centrifugo(self, channel_name:str, data:dict):
        
        '''
        This function is used to post data to centrifugo
        '''

        headers = {'Content-type': 'application/json', 'Authorization': f'apikey {CENTRIFUGO_TOKEN}'}
        command = {
            "method": "publish",    
            "params": {
                "channel": channel_name, 
                "data": data
                }
            }
        response = requests.post(self.centrifugo_url, headers=headers, json=command).json()
        print("="*50)
        print(response)
        print("="*50)
        return response

    def read(self, collection_name, org_id, filter={}):
        """Gets json data from the Db"""

        query = urlencode(filter)

        url = self.read_endpoint.format(
            collec_name=collection_name,
            org_id=org_id,
            query=query
        )

        try:
            res = requests.get(url=url).json()
            print("Working.................!")
            print(res)
            return res

        except Exception as e:
            print("OOps: There is a problem with the Request", e)
        

    def save(self, collection_name, org_id, notice_data):
        """This method stores noticeboard related data as json to the Db.
        It does this using the collection name and the serialized json
        """
        di = {
            "plugin_id": settings.PLUGIN_ID,
            "organization_id": org_id,
            "collection_name": collection_name,
            "bulk_write": False,
            "payload": notice_data,
        }
        
        data=json.dumps(di).encode('utf-8')
        print(data)
        try:
            r = requests.post(self.write_endpoint,data)
            print(r.text)
            r.raise_for_status()
        except Exception as e:
            print("OOps: There is a problem with the Request", e)


    def update(self, collection_name, org_id, notice_data, object_id):
        """This method updates noticeboard related data as json to the Db.
        It does this using the collection name and the serialized json
        """
        di = {
            "plugin_id": settings.PLUGIN_ID,
            "organization_id": org_id,
            "collection_name": collection_name,
            "bulk_write": False,
            "object_id": object_id,
            "payload": notice_data,
        }
        
        try:
            res = requests.put(self.write_endpoint, json=di)
            response = res.json()
            print(response)
            return response
        except Exception as e:
            print("OOps: There is a problem with the Request", e)


    def delete(self, org_id, collection_name, object_id):
        data = {
            "plugin_id": settings.PLUGIN_ID,
            "organization_id": org_id,
            "collection_name": collection_name,
            "bulk_delete": False,
            "object_id": object_id,
            "filter":{}
        }

        try:
            res = requests.post(self.delete_endpoint, json.dumps(data))
            response = res.json()
            print(response)
            return response
        except Exception as e:
            print("OOps: There is a problem with the Request", e)

    def upload(self, file, token):                   #takes in files oh, 1 file
            url = self.upload_multiple_api
            files = {"file":file}
            try:
                response = requests.post(url=url, files=files, headers={
                    'Authorization': f'{token}'
                    })
            except Exception as e:
                print("OOps: There is a problem with the Request", e)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": response.status_code, "message": response.reason}
    
    def multiple_uplaod(self, files, token):
        url = self.upload_multiple_api
        try:
            response = requests.post(url=url, files=files, headers={
                'Authorization': f'{token}'
                })
        except Exception as e:
            print("OOps: There is a problem with the Request", e)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status": response.status_code, "message": response.reason}

    def delete_file(self, file_url):
        url = self.delete_file_api
        body = dict(
            file_url=file_url
        )

        try:
            response = requests.post(url=url, json=body)
        except Exception as e:
            print("OOps: There is a problem with the Request", e)
        if response.status_code == 200:
            return response.json()
        else:
            return {"status_code": response.status_code, "message": response.reason}

db = Dbnoticeboard()
