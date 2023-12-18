# WzParser ![License](https://img.shields.io/github/license/everdeep/WzParser)

This is just a simple parser I made based on the MapleLib library used in [HaRepacker](https://github.com/lastbattle/Harepacker-resurrected/tree/master), along with some inspirition from an existinig barely implemented python [wz](https://pypi.org/project/wz/) package.

This project is still on-going and was mainly just made to help me understand the WZ file format and also rewrite the data into my own format for easier access.

It is still incomplete, but will eventually turn it into a proper  python package for general use in other projects.

#### Features
- [ ] Read wz files (only tested with v83)
    - Only tested with UI.wz for now.
- [ ] Export IMG data to custom format
- [x] treelib integration for structure debugging

#### Treelib fix
Please manually update the treelib package to fix the issue with tree printing. ([Reference](https://stackoverflow.com/questions/46345677/treelib-prints-garbage-instead-of-pseudographics-in-python3))

Inside the `treelib` folder, open `tree.py` and change line `932` from:
```python
print(self._reader.encode('utf-8'))
```
to:
```python
print(self._reader)
```

#### Usage

1. Navigate to the `src` folder and update the relevant paths in `main.py` such as changing the wz path.

2. Setup the virtual environment and install the required packages.
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
``` 

3. Run the script.
```bash
python main.py
```
