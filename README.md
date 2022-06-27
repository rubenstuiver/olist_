# Data analysis
- Document here the project: olist
- Description: Project Description
- Data Source: Kaggle Olist company data
- Type of analysis: Regression


# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for olist in gitlab.com/{group}.

- Create a new project on `gitlab.com/{group}/olist`
- Then populate it:

```bash
git remote add origin git@github.com:{group}/olist.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
olist-run
```

# Install

Go to `https://github.com/rubenstuiver/olist` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:rubenstuiver/olist.git
cd olist
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
olist-run
```
