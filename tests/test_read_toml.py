import toml


def main():
    with open('meta.toml') as f:
        content = f.read()

    print(f'type: {type(content)}')
    print(content)

    meta = toml.loads(content)

    print(meta)

    print(f"{meta['futures']=}")


if __name__ == '__main__':
    main()
