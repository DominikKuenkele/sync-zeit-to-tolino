# sync-zeit-to-tolino
This service syncs the latest ZEIT e-paper to the Tolino cloud. It utilizes `selenium` to access the *Zeit* and *Tolino* websites. Currently, only *Thalia* is supported as a webstore.

This project is based on the following repositories:
- [zeit-on-tolino](https://github.com/fgebhart/zeit-on-tolino) by [fgebhart](https://github.com/fgebhart)
- [zeit-to-tolino](https://github.com/mlux86/zeit-to-tolino) by [mlux86](https://github.com/mlux86)

The reason for creating a new repository was mainly to have a small lightweight tool that runs in a docker container. For a more sophisticated tool that utilizes GitHub Actions, please refer to the [repository](https://github.com/fgebhart/zeit-on-tolino) by *fgebhart*.

## Usage
You can use `docker` or respectivley `docker-compose` to run the synchronisation. This will create a container with a cron job that syncs the e-paper every Wednesday at 18:15 after the release of the new issue.
### docker
Clone this repository and first export some evironment variables:

```bash
export ZEIT_USER=<zeit-user>
export ZEIT_PASSWORD=<zeit-password>
export THALIA_USER=<thalia-password>
export THALIA_PASSWORD=<thalia-password>
```
Then run the following commands:
```bash
docker build . -t sync-zeit-to-tolino
docker run -it sync-zeit-to-tolino
``` 

### docker-compose
Alternatively, you can use docker-compose. 
First, create a `.env` file based on `.env.example` and fill the variables. Then, create the following docker-compose file (you may replace the image by `build: .` to use this repo) and run `docker-compose up`.
```yml
version: "3.9"
services:
  sync-zeit-to-tolino:
    image: dominikkuenkele/sync-zeit-to-tolino:latest
    restart: always
    environment:
      - ZEIT_USER='${ZEIT_USER}'
      - ZEIT_PASSWORD='${ZEIT_PASSWORD}'
      - THALIA_USER='${THALIA_USER}'
      - THALIA_PASSWORD='${THALIA_PASSWORD}'
```

## Development
`firefox` and `geckodriver` need to be installed on your system. Then, you can clone this repository 
```bash
git clone https://github.com/DominikKuenkele/sync-zeit-to-tolino && cd sync-zeit-to-tolino
```
and install all requirements
```bash
pip install -r requirements.txt
```
export the environment variables (mentioned in *Usage*) and run the script:
```bash
python src/main.py
```