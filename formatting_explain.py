import json
import re
import requests


class formatting_explain:

    def __init__(self,
                 query='None',
                 body = '',
                 type_query = 'cat',
                 lvl = 7,
                 NAME_EXPLAIN_FILE='explain.json',
                 NAME_RESULT_FILE='ready_explain.txt'):
        self._NAME_EXPLAIN_FILE = NAME_EXPLAIN_FILE
        self._NAME_RESULT_FILE = NAME_RESULT_FILE
        self._query = query
        self._type = type_query
        self._lvl = lvl
        self._body = body

    def get_search_result(self):
        if self._type == 'cat':
            url = 'http://localhost:9200/products-prod-1/_search'
        elif self._type == 'ref AND':
            url = 'http://localhost:9200/products-references-prod-1/_search'
        elif self._type == 'prod':
            url = 'http://localhost:9200/products-prod-1/_search'

        result_search = requests.post(url=url, json=self._body)

        return json.loads(result_search.text)

    def _deserialization_json(self):
        try:
            with open(self._NAME_EXPLAIN_FILE, 'r') as read_file:
                data = json.load(read_file)
            return data
        except FileNotFoundError:
            print(f"{self._NAME_EXPLAIN_FILE} Not Found")

    def serialization(self, text, mode='a'):
        with open(self._NAME_RESULT_FILE, mode) as file:
            file.write(text)

    def formating(self):

        result_search = self.get_search_result()
        explain = result_search['hits']['hits'][0]['_explanation']['details']
        print(explain)

        self.serialization(f'''id Товара: {result_search['hits']['hits'][0]['_id']}\n''', 'w')
        self.serialization(f'''Query: {self._query}\n''')

        for lvl_0 in explain:
            self.serialization(
                f'''lvl_0: {str(float("{0:.1f}".format(lvl_0['value'])))} {lvl_0['description']}\n''')

            for lvl_1 in lvl_0['details']:
                self.serialization(
                    f'''\tlvl_1: {str(float("{0:.1f}".format(lvl_1['value'])))} {lvl_1['description']}\n''')

                for lvl_2 in lvl_1['details']:
                    lvl_2_text = '\t' + '\t' + 'lvl_2: ' + str(
                        float("{0:.1f}".format(lvl_2['value']))) + '  ' + re.sub(
                        f'''\[PerFieldSimilarity\], result of:''', '', lvl_2['description']) + '\n'
                    self.serialization(lvl_2_text)

                    for lvl_3 in lvl_2['details']:

                        lvl_3_text = '\t' + '\t' + '\t' + 'lvl_3: ' + str(
                            float("{0:.1f}".format(lvl_3['value']))) + ' ' + re.sub('from:', '',
                                                                                    lvl_3['description']) + '\n'
                        self.serialization(lvl_3_text)

                        for lvl_4 in lvl_3['details']:
                            lvl_4_text = '\t' + '\t'+'\t'+'\t' + 'lvl_4: ' + str(
                                float("{0:.1f}".format(lvl_4['value']))) + '  ' + re.sub(
                                f'''\[PerFieldSimilarity\], result of:''', '', lvl_4['description']) + '\n'
                            self.serialization(lvl_4_text)
                            for lvl_5 in lvl_4['details']:

                                lvl_5_text = '\t' + '\t' + '\t' + '\t' + '\t' + 'lvl_5: ' + str(
                                    float("{0:.1f}".format(lvl_5['value']))) + ' ' + re.sub('from:', '',
                                                                                            lvl_5['description']) + '\n'
                                if self._lvl > 4:
                                    self.serialization(lvl_5_text)

                                    for lvl_6 in lvl_5['details']:
                                        lvl_6_text = '\t' + '\t' + '\t' + '\t' + '\t'+'\t' + 'lvl_6: ' + str(
                                            float("{0:.1f}".format(lvl_6['value']))) + ' ' + re.sub('from:', '',
                                                                                                    lvl_6[
                                                                                                        'description']) + '\n'
                                        if self._lvl > 5:
                                            self.serialization(lvl_6_text)

                                            for lvl_7 in lvl_6['details']:
                                                lvl_7_text = '\t' + '\t' + '\t' + '\t' + '\t' + '\t'+'\t' + 'lvl_7: ' + str(
                                                    float("{0:.1f}".format(lvl_7['value']))) + ' ' + re.sub('from:', '',
                                                                                                            lvl_7[
                                                                                                                'description']) + '\n '
                                                if self._lvl > 6:
                                                    self.serialization(lvl_7_text)


if __name__ == '__main__':
    FEX = formatting_explain()
    FEX.formating()
