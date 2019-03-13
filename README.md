
# To profile the program
python3 -m cProfile -o profile.log main.py

# To view a particular profile log
python3 print\_stats.py profile\_logs/0001.profile.log
