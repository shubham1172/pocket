# Pocket
Container in Python :smile_cat:

## Requirements

- Linux operating system (tested on Debian and Arch)
- Python3.6+

## Using pocket

- Clone the repository
```bash
$ git clone https://github.com/shubham1172/pocket
```

- Install the requirements
```bash
$ python3 -m pip install -r requirements.txt
```

- Create your first configuration file
```bash
$ touch pocket.yaml
$ cat <<EOF >> pocket.yaml
name: my-container
image: ubuntu:14.04
copy:
 - src: /etc/resolv.conf # for enabling DNS
   dest: etc/resolv.conf
run:
 - /bin/bash
limit:
 mem: 100
 cpu: 10
EOF
```

- Start your first container
```bash
$ python3 -m pocket.cli.main create pocket.yaml
```

- List all containers
```bash
$ python3 -m pocket.cli.main ls
```

- Run a command in a container
```bash
$ python3 -m pocket.cli.main run <container-id> <command>
```

- Delete a container
```bash
$ python3 -m pocket.cli.main rm <container-id>
```

- Delete all containers
```bash
$ python3 -m pocket.cli.main rm -a
```