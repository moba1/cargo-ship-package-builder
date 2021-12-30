def main():
    with open("/etc/ld.so.conf", 'w+') as ld_so_conf:
        ld_so_conf.truncate(0)
        lines = [
            "# Begin /etc/ld.so.conf",
            "/usr/local/lib",
            "/opt/lib",
        ]
        for line in lines:
            print(line, file=ld_so_conf)


if __name__ == '__main__':
    main()
