# traefik-acme-cleanup
Clean domains that does not exist anymore from traefik acme json file

## Usage
Just run the script like this:
```sh
python traefik-acme-cleanup.py PATH
```

`PATH` must be the path to the configured acme storage in the traefik configuration: `certificatesResolvers.YOUR-RESOLVER.acme.storage`.