###############################################################################
# Replace
# quiz_gunicorn to the name of the gunicorn file you want
# rogerio to your user name
# app_repo to the folder name of your project
# mares to the folder name where you find a file called wsgi.py
#
###############################################################################
# Criando o arquivo quiz_gunicorn.socket
sudo nano /etc/systemd/system/quiz_gunicorn.socket

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=gunicorn blog socket

[Socket]
ListenStream=/run/quiz_gunicorn.socket

[Install]
WantedBy=sockets.target

###############################################################################
# Criando o arquivo quiz_gunicorn.service
sudo nano /etc/systemd/system/quiz_gunicorn.service

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=Gunicorn daemon (You can change if you want)
Requires=quiz_gunicorn.socket
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
          --bind unix:/run/quiz_gunicorn.socket \
          mares.wsgi:application

[Install]
WantedBy=multi-user.target

###############################################################################
# Ativando
sudo systemctl start quiz_gunicorn.socket
sudo systemctl enable quiz_gunicorn.socket

# Checando
sudo systemctl status quiz_gunicorn.socket
curl --unix-socket /run/quiz_gunicorn.socket localhost
sudo systemctl status quiz_gunicorn

# Restarting
sudo systemctl restart quiz_gunicorn.service
sudo systemctl restart quiz_gunicorn.socket
sudo systemctl restart quiz_gunicorn

# After changing something (Depois que mudar alguma coisa de fazer esse codigo abaixo)
sudo systemctl daemon-reload

# Debugging
sudo journalctl -u quiz_gunicorn.service
sudo journalctl -u quiz_gunicorn.socket