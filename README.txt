Need in etc folder:
    - env.txt
    - email.txt
    - db.txt
    - secret_key.txt


If application changed:
sudo systemctl restart gunicorn

If gunicorn changed:
sudo systemctl daemon-reload
sudo systemctl restart gunicorn

If nginx changed:
sudo nginx -t && sudo systemctl restart nginx
