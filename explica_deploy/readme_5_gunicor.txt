###############################################################################
# Replace
# mares_gunicorn to the name of the gunicorn file you want
# rogerio to your user name
# app_repo to the folder name of your project
# mares to the folder name where you find a file called wsgi.py
#
###############################################################################
# Criando o arquivo mares_gunicorn.socket
sudo nano /etc/systemd/system/mares_gunicorn.socket

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=gunicorn blog socket

[Socket]
ListenStream=/run/mares_gunicorn.socket

[Install]
WantedBy=sockets.target

###############################################################################
# Criando o arquivo mares_gunicorn.service
sudo nano /etc/systemd/system/mares_gunicorn.service

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=Gunicorn daemon (You can change if you want)
Requires=mares_gunicorn.socket
After=network.target

[Service]
User=rogerio
Group=www-data
Restart=on-failure
EnvironmentFile=/home/rogerio/app_repo/.env
WorkingDirectory=/home/rogerio/app_repo
# --error-logfile --enable-stdio-inheritance --log-level and --capture-output
# are all for debugging purposes.
ExecStart=/home/rogerio/app_repo/venv/bin/gunicorn \
          --error-logfile /home/rogerio/app_repo/gunicorn-error-log \
          --enable-stdio-inheritance \
          --log-level "debug" \
          --capture-output \
          --access-logfile - \
          --workers 6 \
          --bind unix:/run/mares_gunicorn.socket \
          mares.wsgi:application

[Install]
WantedBy=multi-user.target

############################################################################### leonine1983
sudo systemctl start mares_gunicorn.socket
sudo systemctl enable mares_gunicorn.socket

# Checando
sudo systemctl status mares_gunicorn.socket
curl --unix-socket /run/mares_gunicorn.socket localhost
sudo systemctl status mares_gunicorn

# Restarting
sudo systemctl restart mares_gunicorn.service
sudo systemctl restart mares_gunicorn.socket
sudo systemctl restart mares_gunicorn

# After changing something
sudo systemctl daemon-reload

# Debugging
sudo journalctl -u mares_gunicorn.service
sudo journalctl -u mares_gunicorn.socket