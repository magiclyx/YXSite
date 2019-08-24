export PYTHONUNBUFFERED=0
export DJANGO_SETTINGS_MODULE=YXSite.settings
export DEUB=on
export SECRET_KEY='-3%-jj8c$o-r0t)svgd)d(w#&-t@=f($8^#xw4r&fla$51*zui'
export ALLOWED_HOSTS=127.0.0.1,localhost

#python3 manage.py runserver 8000 >> run.log 2>&1

file_path=`date +%Y-%m-%d_%H%M%S`.log
python3 manage.py runserver 8000 2>&1 | tee -a logs/${file_path}


