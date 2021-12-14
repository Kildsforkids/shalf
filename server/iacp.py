import requests
import json


class IACP:
    def __init__(self, data):
        self.data = data
        self.API_KEY = '6cf60d216c5b1b32ebfbbb5492c5a1b7'
        self.iacp_data = None
        self.iacp_result_file = None
    
    def _get_iacp_data(self):
        import_link = 'https://iacpaas.dvo.ru/api/fund/structure/export/user-item?path=/Сервис диагностики без интерфейса/Архив с одной ИБ&json-type=universal'

        response = requests.get(import_link, headers={"accept": "application/json", "X-API-KEY": self.API_KEY})
        result_json = json.loads(response._content.decode('utf-8'))
        result_json['data'] = json.loads(result_json['data'])

        self.iacp_data = result_json

        self._get_result_file_state()
        return response
    
    def _get_result_file_state(self):
        import_link = 'https://iacpaas.dvo.ru/api/fund/structure/export/user-item?path=/Сервис диагностики без интерфейса/Результат Диагн без интерфейса&json-type=universal'

        response = requests.get(import_link, headers={"accept": "application/json", "X-API-KEY": self.API_KEY})
        result_json = json.loads(response._content.decode('utf-8'))
        result_json['data'] = json.loads(result_json['data'])

        self.iacp_result_file = result_json
        return result_json['data']['successors'][1]

    def _set_result_file_state(self):
        resp_post = requests.post('https://iacpaas.dvo.ru/api/fund/structure/import', headers={"Content-Type": "application/json", "X-API-KEY": self.API_KEY, "accept": "application/json"}, data=json.dumps({
            'path': '/Сервис диагностики без интерфейса',
            'json': json.dumps(self.iacp_result_file['data']),
            'clearIfExists': True
        }))
        return json.loads(resp_post._content.decode('utf-8'))
    
    def _represent(self, value: int):
        '''
            @value: int(0) or int(1)
        '''
        return 'имеется' if value == 1 else 'отсутствует'
    
    def _fill_iacp_data(self):
        # self.iacp_data['data']['path'] = 'MedIACPaaS@mail.ru/Мой Фонд/Сервис диагностики без интерфейса/Архив с одной ИБ;'
        self.iacp_data['data']['$json_type'] = 'universal'
        idx, item = [(i, item) for i, item in enumerate(self.iacp_data['data']['successors']) if item['name'] == 'Automation'][0]
        
        complaints = self.iacp_data['data']['successors'][idx]['successors'][1]['successors']
        
        # боль в глазу
        complaints[0]['successors'][0]['successors'][0]['value'] = self._represent(self.data['боль в глазу'])
        
        # покраснение глаз
        complaints[1]['successors'][0]['successors'][0]['value'] = self._represent(self.data['покраснение глаза'])
        
        # Резь в глазу
        complaints[2]['successors'][0]['successors'][0]['value'] = self._represent(self.data['резь в глазу '])
        
        #Выделения из глаза
        complaints[3]['successors'][0]['successors'][0]['value'] = self._represent(self.data['выделение из глаз'])
        
        #Светобоязнь
        complaints[4]['successors'][0]['successors'][0]['value'] = self._represent(self.data['светобоязнь'])
        
        #Слезотечение
        complaints[5]['successors'][0]['successors'][0]['value'] = self._represent(self.data['слезотечение'])
        
        #Неприятные ощущения в глазу
        complaints[6]['successors'][0]['successors'][0]['value'] = self._represent(self.data['неприятные ощущения в глазу'])
        
        # Температура тела
        complaints[7]['successors'][0]['successors'][0]['value'] = self._represent(self.data['температура тела'])
        
        # Слабость
        complaints[8]['successors'][0]['successors'][0]['value'] = self._represent(self.data['слабость'])
        
        # Oщущение инородного тела в глазу
        complaints[9]['successors'][0]['successors'][0]['value'] = self._represent(self.data['ощущение инородного тела в глазу'])
        
        # Склеивание ресниц утром
        complaints[10]['successors'][0]['successors'][0]['value'] = self._represent(self.data['склеивание ресниц утром'])
        
        #TODO: если сломалась ИБ Automation
        # ib2_index, ib2_item = [(i, item) for i, item in enumerate(self.iacp_data['data']['successors']) if item['name'] == 'ИБ№2'][0]
        # ib2_item['name'] = 'Automation'
        # self.iacp_data['data']['successors'][idx] = ib2_item
    
    def _send_data(self):
        resp_post = requests.post('https://iacpaas.dvo.ru/api/fund/structure/import', headers={"Content-Type": "application/json", "X-API-KEY": self.API_KEY, "accept": "application/json"}, data=json.dumps({
            'path': '/Сервис диагностики без интерфейса',
            'json': json.dumps(self.iacp_data['data']),
            'clearIfExists': True
        }))
        self._set_result_file_state()
        return json.loads(resp_post._content.decode('utf-8'))
    
    def _run_solver(self):
        response = requests.get('https://iacpaas.dvo.ru/api/service/run/4640197744801057262', headers={"accept": "application/json", "X-API-KEY": self.API_KEY})
        assert response.status_code == 200
    
    def get_result(self):
        return self._get_result_file_state()
    
    def run(self):
        self._get_iacp_data()
        self._fill_iacp_data()
        self._send_data()
        self._run_solver()
        return self.get_result()