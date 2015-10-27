alias python=/home/$USER/anaconda/bin/python
alias pip=/home/$USER/anaconda/bin/pip
alias ipython=/home/$USER/anaconda/bin/ipython
pwd=`pwd`
export PYTHONPATH=$PYTHONPATH:$pwd/mlboost
export PYTHONPATH=$PYTHONPATH:$pwd/pytrade
export PYTHONPATH=$PYTHONPATH:$pwd
# requirements
#pip install -r requirements.txt
#conda install --file conda-requirements.txt
# other libs
#hg clone https://bitbucket.org/fraka6/mlboost
#git clone https://github.com/fraka6/pytrade.git
