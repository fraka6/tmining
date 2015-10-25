# download anaconda, install and setup
wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda-2.3.0-Linux-x86_64.sh
chmod 755 Anaconda-2.3.0-Linux-x86_64.sh
./
alias python=/home/$USER/anaconda/bin/python
alias ipython=/home/$USER/anaconda/bin/ipython
alias pip=/home/$USER/anaconda/bin/pip
# install mlboost
 hg clone ssh://hg@bitbucket.org/fraka6/mlboost