USER = 'postgres'
PASSWORD = '123'
HOST = 'localhost'
PORT = '5433'
DATABASE_NAME = 'SPK_UAS'

DEV_SCALE = {
    'ram': {
        '32': 5, 
        '16': 4, 
        '12': 3, 
        '8': 2, 
        '4': 1,
    },
    'memori_internal': {
        '2': 5, 
        '1': 4, 
        '512': 3, 
        '256': 2, 
        '128': 1
    },
    'layar': {
        '17,3': 5,
        '15,6': 4,
        '14': 3,
        '13,3': 2,
        '13': 1,
        '11,6': 1,
    },
    'harga' : {
        '27600000 - 30000000': 1,
        '22200000 - 27600000': 2,
        '16800000 - 22200000': 3,
        '11400000 - 16800000': 4,
        '6000000 - 11400000': 5,
    },
    'baterai' : {
        '14000': 5,
        '12000': 4,
        '10000': 3,
        '9000': 2,
        '8000': 1,
        '7000': 1,
        '6000': 1,
    },
    'nilai' : {
    'Intel Core i9': 5,
    'Intel Core i7': 4,
    'AMD Ryzen 7': 3,
    'Intel Core i5': 2,
    'AMD Ryzen 5': 1,
    'AMD Ryzen 3': 1,
    'Apple M1': 1,
    'Intel Celeron': 1,
}

}

