import glob 

def main():
    path = glob.glob('facturas/**/*.pdf')
    for file in path:
        print(file)


if __name__ == "__main__":
    main()