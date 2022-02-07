import urllib.request

import toml


def main():
    url = 'https://quantalon.gd2.qingstor.com/trading-calendar/meta.toml'
    response = urllib.request.urlopen(url)
    content = response.read().decode('utf-8')
    meta = toml.loads(content)
    print(meta)



if __name__ == '__main__':
    main()
