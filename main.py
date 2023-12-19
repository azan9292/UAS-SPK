import sys
from colorama import Fore, Style  # Assuming 'colorama' is used instead of 'colomodela'
from models import Base, Mobil
from engine import engine
from tabulate import tabulate
from sqlalchemy import select
from sqlalchemy.orm import Session
from settings import DEV_SCALE

session = Session(engine)


def create_table():
    Base.metadata.create_all(engine)
    print(f'{Fore.GREEN}[Success]: {Style.RESET_ALL}Database has been created!')


def review_data():
    query = select(Mobil)
    for mobil_instance in session.scalars(query):
        print(mobil_instance)


class BaseMethod:

    def __init__(self):
        self.raw_weight = {'Nama': 4, 'jenis': 3,
                           'merek': 3, 'model': 4, 'Komsumsi_bahan_bakar': 5}

    @property
    def weight(self):
        total_weight = sum(self.raw_weight.values())
        return {k: round(v/total_weight, 2) for k, v in self.raw_weight.items()}

    @property
    def data(self):
        query = select(Mobil.id, Mobil.nama_Mobil, Mobil.jenis, Mobil.Nama, Mobil.merek,
                       Mobil.model, Mobil.Komsumsi_bahan_bakar, Mobil.Komsumsi_bahan_bakar)
        result = session.execute(query).fetchall()
        return [{'id': mobil.id, 'nama_Mobil': mobil.nama_Mobil, 'jenis': mobil.jenis, 'Nama': mobil.Nama,
                 'merek': mobil.merek, 'model': mobil.model, 'Komsumsi_bahan_bakar': mobil.Komsumsi_bahan_bakar,
                 'Komsumsi_bahan_bakar': mobil.Komsumsi_bahan_bakar} for mobil in result]

    @property
    def normalized_data(self):
        jenis_values, Nama_values, merek_values, model_values, Komsumsi_bahan_bakar_values = [], [], [], [], []

        for data in self.data:
            # Jenis
            jenis_value = max(map(int, filter(str.isdigit, str(data['jenis']))), default=1)
            jenis_values.append(jenis_value)

            # Nama
            max_Nama_value = max(map(int, filter(str.split()[0].isdigit, str(data['Nama']))), default=1)
            Nama_values.append(max_Nama_value)

            # merek
            max_merek_value = max(map(float, filter(str.replace('.', '').isdigit, str(data['merek']))), default=1)
            merek_values.append(max_merek_value)

            # model
            max_model_value = max(map(int, filter(str.isdigit, str(data['model']))), default=1)
            model_values.append(max_model_value)

            # Komsumsi_bahan_bakar
            Komsumsi_bahan_bakar_value = DEV_SCALE.get('Komsumsi_bahan_bakar', {}).get(data.get('Komsumsi_bahan_bakar'), 1)
            Komsumsi_bahan_bakar_values.append(Komsumsi_bahan_bakar_value)

            # Komsumsi_bahan_bakar
            Komsumsi_bahan_bakar_cleaned = ''.join(char for char in str(data.get('Komsumsi_bahan_bakar', '')) if char.isdigit())
            Komsumsi_bahan_bakar_values.append(float(Komsumsi_bahan_bakar_cleaned) if Komsumsi_bahan_bakar_cleaned else 0)

        return [
            {
                'id': data['id'],
                'jenis': jenis_value / max(jenis_values),
                'Nama': max_Nama_value / max(Nama_values),
                'merek': max_merek_value / max(merek_values),
                'model': max_model_value / max(model_values),
                'Komsumsi_bahan_bakar': Komsumsi_bahan_bakar_value / max(Komsumsi_bahan_bakar_values),
                'Komsumsi_bahan_bakar': min(Komsumsi_bahan_bakar_values) / max(Komsumsi_bahan_bakar_values) if max(Komsumsi_bahan_bakar_values) != 0 else 0
            }
            for data, jenis_value, max_Nama_value, max_merek_value, max_model_value, Komsumsi_bahan_bakar_value, Komsumsi_bahan_bakar_value
            in zip(self.data, jenis_values, Nama_values, merek_values, model_values, Komsumsi_bahan_bakar_values, Komsumsi_bahan_bakar_values)
        ]


class WeightedProduct(BaseMethod):

    @property
    def calculate(self):
        normalized_data = self.normalized_data
        produk = [
            {
                'id': row['id'],
                'produk': row['jenis']**self.weight['jenis'] *
                row['Nama']**self.weight['Nama'] *
                row['merek']**self.weight['merek'] *
                row['model']**self.weight['model'] *
                row['Komsumsi_bahan_bakar']**self.weight['Komsumsi_bahan_bakar'] *
                row['Komsumsi_bahan_bakar']**self.weight['Komsumsi_bahan_bakar']
            }
            for row in normalized_data
        ]
        sorted_produk = sorted(produk, key=lambda x: x['produk'], reverse=True)
        sorted_data = [
            {
                'id': product['id'],
                'jenis': product['produk'] / self.weight['jenis'],
                'Nama': product['produk'] / self.weight['Nama'],
                'merek': product['produk'] / self.weight['merek'],
                'model': product['produk'] / self.weight['model'],
                'Komsumsi_bahan_bakar': product['produk'] / self.weight['Komsumsi_bahan_bakar'],
                'Komsumsi_bahan_bakar': product['produk'] / self.weight['Komsumsi_bahan_bakar'],
                'score': product['produk']  # Nilai skor akhir
            }
            for product in sorted_produk
        ]
        return sorted_data


class SimpleAdditiveWeighting(BaseMethod):

    @property
    def calculate(self):
        weight = self.weight
        result = {row['id']:
                  round(row['jenis'] * weight['jenis'] +
                        row['Nama'] * weight['Nama'] +
                        row['merek'] * weight['merek'] +
                        row['model'] * weight['model'] +
                        row['Komsumsi_bahan_bakar'] * weight['Komsumsi_bahan_bakar'] +
                        row['Komsumsi_bahan_bakar'] * weight['Komsumsi_bahan_bakar'], 2)
                  for row in self.normalized_data
                  }

        sorted_result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        return sorted_result


def run_saw():
    saw = SimpleAdditiveWeighting()
    result = saw.calculate
    print(tabulate(result.items(), headers=['Id', 'Score'], tablefmt='pretty'))


def run_wp():
    wp = WeightedProduct()
    result = wp.calculate
    headers = result[0].keys()
    rows = [
        {k: round(v, 4) if isinstance(v, float) else v for k, v in val.items()}
        for val in result
    ]
    print(tabulate(rows, headers="keys", tablefmt="grid"))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg = sys.argv[1]

        if arg == 'create_table':
            create_table()
        elif arg == 'saw':
            run_saw()
        elif arg == 'wp':
            run_wp()
        else:
            print('Command not found')
