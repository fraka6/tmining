# install dependencies
pip install --upgrade cython falcon
pip install --upgrade gevent gunicorn
pip install --upgrade httpie
# run server
gunicorn app:api &
# request data
http GET localhost:8000/bucket
