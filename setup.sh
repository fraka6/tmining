alias python=/home/$USER/anaconda/bin/python
alias pip=/home/$USER/anaconda/bin/pip
alias ipython=/home/$USER/anaconda/bin/ipython
pwd=`pwd`
export PYTHONPATH=$PYTHONPATH:$pwd/mlboost
export PYTHONPATH=$PYTHONPATH:$pwd/pytrade
export PYTHONPATH=$PYTHONPATH:$pwd
#pip install -r requirements.txt
#conda install --file conda-requirements.txt